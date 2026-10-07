"""
Question 4: Manufacturing Machine Reliability Analysis (Machine Breakdowns)
Simulation of a CNC machine with random breakdowns.
"""

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Global data collection
part_completion_times = []
part_interruptions = []
part_delays = []
total_breakdowns = 0

def machine_breakdown_process(env, machine, mtbf, mttr):
    """
    Randomly breaks the machine down.
    
    Args:
        mtbf: Mean Time Between Failures (minutes)
        mttr: Mean Time To Repair (minutes)
    """
    global total_breakdowns
    
    while True:
        # Work for some time before breaking
        uptime = random.expovariate(1.0 / mtbf)
        yield env.timeout(uptime)
        
        total_breakdowns += 1
        
        # Request machine with highest priority to interrupt jobs
        with machine.request(priority=-1, preempt=True) as req:
            yield req
            
            # Repair the machine
            repair_time = random.expovariate(1.0 / mttr)
            yield env.timeout(repair_time)

def part(env, name, machine, processing_time, expected_time):
    """
    A part that uses the machine and can be interrupted.
    
    Args:
        processing_time: Total time needed to complete the part
        expected_time: Expected processing time (for delay calculation)
    """
    arrival_time = env.now
    interruption_count = 0
    remaining_time = processing_time
    
    # Request machine with normal priority
    with machine.request(priority=1) as req:
        yield req
        
        # Keep trying to complete the part
        while remaining_time > 0:
            try:
                # Try to complete remaining work
                start_time = env.now
                yield env.timeout(remaining_time)
                
                # Success! Part completed
                completion_time = env.now - arrival_time
                part_completion_times.append(completion_time)
                part_interruptions.append(interruption_count)
                
                # Calculate delay (time beyond expected processing time)
                delay = max(0, completion_time - expected_time)
                part_delays.append(delay)
                
                remaining_time = 0
                
            except simpy.Interrupt:
                # Machine broke down!
                work_done = env.now - start_time
                remaining_time -= work_done
                interruption_count += 1

def part_generator(env, machine, arrival_rate, processing_time_mean, expected_time):
    """Generate parts arriving at the machine."""
    part_number = 0
    while True:
        # Wait for next part
        yield env.timeout(random.expovariate(arrival_rate))
        
        part_number += 1
        processing_time = random.expovariate(1.0 / processing_time_mean)
        env.process(part(env, f"Part {part_number}", machine, processing_time, expected_time))

def run_simulation(mtbf, mttr, sim_time=960, arrival_rate=1/15, processing_time=10, random_seed=42):
    """Run simulation with specified breakdown parameters."""
    
    # Reset globals
    global part_completion_times, part_interruptions, part_delays, total_breakdowns
    part_completion_times = []
    part_interruptions = []
    part_delays = []
    total_breakdowns = 0
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    machine = simpy.PreemptiveResource(env, capacity=1)
    
    # Start processes
    env.process(machine_breakdown_process(env, machine, mtbf, mttr))
    env.process(part_generator(env, machine, arrival_rate, processing_time, processing_time))
    
    # Run
    env.run(until=sim_time)
    
    # Calculate availability
    availability = mtbf / (mtbf + mttr)
    
    # Return statistics
    return {
        'mtbf': mtbf,
        'mttr': mttr,
        'availability': availability,
        'parts_completed': len(part_completion_times),
        'avg_completion_time': np.mean(part_completion_times) if part_completion_times else 0,
        'max_completion_time': max(part_completion_times) if part_completion_times else 0,
        'avg_interruptions': np.mean(part_interruptions) if part_interruptions else 0,
        'total_breakdowns': total_breakdowns,
        'avg_delay': np.mean(part_delays) if part_delays else 0
    }

def calculate_profit(stats, part_profit=500, repair_cost=300, delay_penalty_per_hour=50):
    """Calculate total profit for the simulation period."""
    
    # Revenue from completed parts
    revenue = stats['parts_completed'] * part_profit
    
    # Repair costs
    repair_costs = stats['total_breakdowns'] * repair_cost
    
    # Delay costs (convert delay from minutes to hours)
    avg_delay_hours = stats['avg_delay'] / 60
    delay_costs = stats['parts_completed'] * avg_delay_hours * delay_penalty_per_hour
    
    # Total profit
    profit = revenue - repair_costs - delay_costs
    
    return {
        'revenue': revenue,
        'repair_costs': repair_costs,
        'delay_costs': delay_costs,
        'profit': profit
    }

# Simulation parameters
SIM_TIME = 960  # 16 hours (2 shifts) in minutes
ARRIVAL_RATE = 1 / 15  # 1 part every 15 minutes
PROCESSING_TIME = 10  # minutes (expected)

# Reliability scenarios
scenarios = [
    {'name': 'A', 'mtbf': 100*60, 'mttr': 2*60, 'description': 'New machine'},
    {'name': 'B', 'mtbf': 50*60, 'mttr': 2*60, 'description': 'Good condition'},
    {'name': 'C', 'mtbf': 30*60, 'mttr': 3*60, 'description': 'Average condition'},
    {'name': 'D', 'mtbf': 20*60, 'mttr': 4*60, 'description': 'Poor condition'},
    {'name': 'E', 'mtbf': 15*60, 'mttr': 5*60, 'description': 'Very poor condition'},
]

print("="*90)
print("CNC MACHINE RELIABILITY ANALYSIS")
print("="*90)
print(f"Parts arrive: 1 every 15 minutes")
print(f"Processing time: {PROCESSING_TIME} minutes average")
print(f"Simulation time: {SIM_TIME} minutes (16 hours = 2 shifts)")
print(f"Part profit: £500")
print(f"Repair cost: £300 per breakdown")
print(f"Delay penalty: £50 per hour")
print()

results = []

for scenario in scenarios:
    print(f"\n{'='*90}")
    print(f"Scenario {scenario['name']}: {scenario['description']}")
    print(f"MTBF = {scenario['mtbf']/60:.0f} hours, MTTR = {scenario['mttr']/60:.0f} hours")
    print(f"{'='*90}")
    
    stats = run_simulation(scenario['mtbf'], scenario['mttr'], SIM_TIME, ARRIVAL_RATE, PROCESSING_TIME)
    financial = calculate_profit(stats)
    
    # Combine stats and financial data
    stats.update(financial)
    stats['scenario_name'] = scenario['name']
    stats['description'] = scenario['description']
    results.append(stats)
    
    print(f"\nReliability Metrics:")
    print(f"  MTBF: {stats['mtbf']/60:.1f} hours")
    print(f"  MTTR: {stats['mttr']/60:.1f} hours")
    print(f"  Availability: {stats['availability']:.1%}")
    print(f"  Total breakdowns: {stats['total_breakdowns']}")
    
    print(f"\nProduction Metrics:")
    print(f"  Parts completed: {stats['parts_completed']}")
    print(f"  Average completion time: {stats['avg_completion_time']:.2f} minutes")
    print(f"  Maximum completion time: {stats['max_completion_time']:.2f} minutes")
    print(f"  Average interruptions per part: {stats['avg_interruptions']:.2f}")
    print(f"  Average delay per part: {stats['avg_delay']:.2f} minutes")
    
    print(f"\nFinancial Analysis:")
    print(f"  Revenue: £{stats['revenue']:,.2f}")
    print(f"  Repair costs: £{stats['repair_costs']:,.2f}")
    print(f"  Delay costs: £{stats['delay_costs']:,.2f}")
    print(f"  PROFIT: £{stats['profit']:,.2f}")

# Summary comparison
print("\n" + "="*90)
print("SUMMARY COMPARISON")
print("="*90)
print(f"{'Scenario':<12} {'Avail%':<10} {'Parts':<10} {'Breakdowns':<12} {'Avg Int':<10} {'Profit (£)':<15}")
print("-"*90)
for stats in results:
    print(f"{stats['scenario_name'] + ': ' + stats['description']:<12} "
          f"{stats['availability']*100:<10.1f} {stats['parts_completed']:<10} "
          f"{stats['total_breakdowns']:<12} {stats['avg_interruptions']:<10.2f} "
          f"{stats['profit']:<15,.0f}")

# Analysis and recommendation
print("\n" + "="*90)
print("ANALYSIS AND RECOMMENDATIONS")
print("="*90)

# Find best and worst scenarios
best = max(results, key=lambda x: x['profit'])
worst = min(results, key=lambda x: x['profit'])

print(f"\nBest scenario: {best['scenario_name']} ({best['description']})")
print(f"  - Profit: £{best['profit']:,.2f}")
print(f"  - Availability: {best['availability']:.1%}")
print(f"  - Parts completed: {best['parts_completed']}")

print(f"\nWorst scenario: {worst['scenario_name']} ({worst['description']})")
print(f"  - Profit: £{worst['profit']:,.2f}")
print(f"  - Availability: {worst['availability']:.1%}")
print(f"  - Parts completed: {worst['parts_completed']}")

# Determine acceptable reliability threshold
print("\nReliability Threshold Analysis:")
acceptable_threshold = best['profit'] * 0.75  # 75% of best profit
for stats in results:
    status = "ACCEPTABLE" if stats['profit'] >= acceptable_threshold else "UNACCEPTABLE"
    print(f"  Scenario {stats['scenario_name']}: {status} (Profit: £{stats['profit']:,.0f}, "
          f"{stats['profit']/best['profit']:.0%} of optimal)")

# Recommendation
unacceptable = [s for s in results if s['profit'] < acceptable_threshold]
if unacceptable:
    threshold_scenario = unacceptable[0]
    print(f"\n>>> RECOMMENDATION:")
    print(f"    Machine becomes unacceptable at Scenario {threshold_scenario['scenario_name']} "
          f"(MTBF = {threshold_scenario['mtbf']/60:.0f}h, Availability = {threshold_scenario['availability']:.1%})")
    print(f"    At this point, profit drops to £{threshold_scenario['profit']:,.0f} "
          f"({threshold_scenario['profit']/best['profit']:.0%} of optimal)")
    print(f"    Machine should be refurbished or replaced before reaching this condition.")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Extract data for plotting
mtbf_hours = [s['mtbf']/60 for s in results]
scenario_names = [s['scenario_name'] for s in results]
parts_completed = [s['parts_completed'] for s in results]
profits = [s['profit'] for s in results]
avg_interruptions = [s['avg_interruptions'] for s in results]
availabilities = [s['availability']*100 for s in results]

# Plot 1: Parts completed vs MTBF
axes[0, 0].plot(mtbf_hours, parts_completed, marker='o', linewidth=2, markersize=10, color='steelblue')
axes[0, 0].set_xlabel('MTBF (hours)')
axes[0, 0].set_ylabel('Parts Completed')
axes[0, 0].set_title('Production Throughput vs Reliability')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].invert_xaxis()

# Plot 2: Profit vs MTBF
axes[0, 1].plot(mtbf_hours, profits, marker='s', linewidth=2, markersize=10, color='green')
axes[0, 1].axhline(y=acceptable_threshold, color='red', linestyle='--', 
                   linewidth=2, label='Acceptable threshold (75%)')
axes[0, 1].set_xlabel('MTBF (hours)')
axes[0, 1].set_ylabel('Profit (£)')
axes[0, 1].set_title('Profit vs Machine Reliability')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].invert_xaxis()

# Plot 3: Average interruptions vs MTBF
axes[1, 0].plot(mtbf_hours, avg_interruptions, marker='^', linewidth=2, markersize=10, color='orange')
axes[1, 0].set_xlabel('MTBF (hours)')
axes[1, 0].set_ylabel('Average Interruptions per Part')
axes[1, 0].set_title('Production Disruption vs Reliability')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].invert_xaxis()

# Plot 4: Availability
axes[1, 1].bar(scenario_names, availabilities, color=['green', 'lightgreen', 'yellow', 'orange', 'red'], 
               alpha=0.7, edgecolor='black', linewidth=2)
axes[1, 1].set_xlabel('Scenario')
axes[1, 1].set_ylabel('Availability (%)')
axes[1, 1].set_title('Machine Availability by Scenario')
axes[1, 1].grid(True, alpha=0.3, axis='y')
axes[1, 1].axhline(y=90, color='blue', linestyle='--', linewidth=2, label='90% target')
axes[1, 1].legend()

# Add values on bars
for i, v in enumerate(availabilities):
    axes[1, 1].text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
plt.savefig('Q4_CNC_Machine_Results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'Q4_CNC_Machine_Results.png'")
plt.show()
