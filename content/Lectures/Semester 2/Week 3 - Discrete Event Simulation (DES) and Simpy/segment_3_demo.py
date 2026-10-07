import simpy
import random
import matplotlib.pyplot as plt

# Data collection
job_completion_times = []
job_interruptions = []
total_interruptions = 0

def machine_breakdown_process(env, machine, mtbf, mttr):
    """
    Randomly breaks the machine down.
    
    Args:
        mtbf: Mean Time Between Failures (hours)
        mttr: Mean Time To Repair (hours)
    """
    global total_interruptions
    
    while True:
        # Work for some time before breaking
        uptime = random.expovariate(1.0 / mtbf)
        yield env.timeout(uptime)
        
        print(f"{env.now:.2f}: ⚠️  MACHINE BREAKDOWN!")
        total_interruptions += 1
        
        # Request machine with highest priority to "seize" it for repairs
        with machine.request(priority=-1, preempt=True) as req:
            yield req
            
            # Repair the machine
            repair_time = random.expovariate(1.0 / mttr)
            yield env.timeout(repair_time)
            
            print(f"{env.now:.2f}: ✓  Machine repaired (took {repair_time:.2f} hours)")

def job(env, name, machine, processing_time):
    """
    A job that uses the machine and can be interrupted.
    
    Args:
        processing_time: Total time needed to complete the job
    """
    print(f"{env.now:.2f}: {name} arrives (needs {processing_time:.2f} hours)")
    
    arrival_time = env.now
    interruption_count = 0
    remaining_time = processing_time
    
    # Request machine with normal priority
    with machine.request(priority=1) as req:
        yield req
        
        # Keep trying to complete the job
        while remaining_time > 0:
            print(f"{env.now:.2f}: {name} working (needs {remaining_time:.2f} more hours)")
            
            try:
                # Try to complete remaining work
                start_time = env.now
                yield env.timeout(remaining_time)
                
                # Success! Job completed
                completion_time = env.now - arrival_time
                job_completion_times.append(completion_time)
                job_interruptions.append(interruption_count)
                
                print(f"{env.now:.2f}: {name} COMPLETED (total time: {completion_time:.2f} hours, interruptions: {interruption_count})")
                remaining_time = 0
                
            except simpy.Interrupt as interrupt:
                # Machine broke down!
                work_done = env.now - start_time
                remaining_time -= work_done
                interruption_count += 1
                
                print(f"{env.now:.2f}: {name} INTERRUPTED (completed {work_done:.2f} hours, {remaining_time:.2f} hours remaining)")

def job_generator(env, machine, arrival_rate, processing_time_mean):
    """Generate jobs arriving at the machine."""
    
    job_number = 0
    while True:
        # Wait for next job
        yield env.timeout(random.expovariate(arrival_rate))
        
        job_number += 1
        processing_time = random.expovariate(1.0 / processing_time_mean)
        env.process(job(env, f"Job {job_number}", machine, processing_time))

def preventive_maintenance_process(env, machine, maintenance_interval, maintenance_time):
    """Perform scheduled maintenance."""
    
    while True:
        # Wait for maintenance interval
        yield env.timeout(maintenance_interval)
        
        print(f"{env.now:.2f}: Scheduled maintenance starting")
        
        # Request machine for maintenance
        with machine.request(priority=0) as req:  # Higher priority than jobs
            yield req
            yield env.timeout(maintenance_time)
            print(f"{env.now:.2f}: Maintenance complete")


def run_simulation(mtbf, mttr, sim_time=200, arrival_rate=0.1, processing_time=5.0, random_seed=42):
    """Run simulation with specified breakdown parameters."""
    
    # Reset globals
    global job_completion_times, job_interruptions, total_interruptions
    job_completion_times = []
    job_interruptions = []
    total_interruptions = 0
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    machine = simpy.PreemptiveResource(env, capacity=1)
    
    # Start processes
    env.process(machine_breakdown_process(env, machine, mtbf, mttr))
    env.process(job_generator(env, machine, arrival_rate, processing_time))
    env.process(preventive_maintenance_process(env, machine, maintenance_interval=200, maintenance_time=2))
    
    # Run
    print("="*70)
    print(f"Simulation: MTBF={mtbf}h, MTTR={mttr}h")
    print("="*70)
    env.run(until=sim_time)
    
    # Return statistics
    return {
        'mtbf': mtbf,
        'mttr': mttr,
        'jobs_completed': len(job_completion_times),
        'avg_completion_time': sum(job_completion_times) / len(job_completion_times) if job_completion_times else 0,
        'max_completion_time': max(job_completion_times) if job_completion_times else 0,
        'avg_interruptions': sum(job_interruptions) / len(job_interruptions) if job_interruptions else 0,
        'total_breakdowns': total_interruptions
    }

SIM_TIME = 500
# Run baseline: No breakdowns (MTBF = very high)
print("\n" + "="*70)
print("BASELINE: No Breakdowns")
print("="*70)
baseline = run_simulation(mtbf=10000, mttr=1, sim_time=SIM_TIME)

print(f"\nJobs completed: {baseline['jobs_completed']}")
print(f"Average completion time: {baseline['avg_completion_time']:.2f} hours")
print(f"Maximum completion time: {baseline['max_completion_time']:.2f} hours")

# Run with moderate breakdowns
print("\n" + "="*70)
print("SCENARIO 1: Moderate Reliability (MTBF=50h)")
print("="*70)
scenario1 = run_simulation(mtbf=50, mttr=5, sim_time=SIM_TIME)

print(f"\nJobs completed: {scenario1['jobs_completed']}")
print(f"Average completion time: {scenario1['avg_completion_time']:.2f} hours")
print(f"Maximum completion time: {scenario1['max_completion_time']:.2f} hours")
print(f"Average interruptions per job: {scenario1['avg_interruptions']:.2f}")
print(f"Total breakdowns: {scenario1['total_breakdowns']}")

# Run with frequent breakdowns
print("\n" + "="*70)
print("SCENARIO 2: Poor Reliability (MTBF=20h)")
print("="*70)
scenario2 = run_simulation(mtbf=20, mttr=5, sim_time=SIM_TIME)

print(f"\nJobs completed: {scenario2['jobs_completed']}")
print(f"Average completion time: {scenario2['avg_completion_time']:.2f} hours")
print(f"Maximum completion time: {scenario2['max_completion_time']:.2f} hours")
print(f"Average interruptions per job: {scenario2['avg_interruptions']:.2f}")
print(f"Total breakdowns: {scenario2['total_breakdowns']}")