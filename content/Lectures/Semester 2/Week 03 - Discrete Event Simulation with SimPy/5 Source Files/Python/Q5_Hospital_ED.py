"""
Question 5: Hospital Emergency Department (Integrated Challenge)
Simulation combining M/M/c with preemptive resources for patient prioritization.
"""

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Global data collection
urgent_wait_times = []
standard_wait_times = []
standard_interruptions = []

def urgent_patient(env, name, doctors, treatment_rate):
    """Urgent patient - high priority, interrupts standard patients."""
    arrival_time = env.now
    
    # Request doctor with highest priority (priority=0)
    with doctors.request(priority=0) as request:
        yield request
        
        # Record wait time
        wait_time = env.now - arrival_time
        urgent_wait_times.append(wait_time)
        
        # Treatment time (exponential)
        treatment_time = random.expovariate(treatment_rate)
        yield env.timeout(treatment_time)

def standard_patient(env, name, doctors, treatment_rate):
    """Standard patient - lower priority, can be interrupted."""
    arrival_time = env.now
    interruption_count = 0
    remaining_treatment = random.expovariate(treatment_rate)
    
    # Request doctor with normal priority (priority=1)
    with doctors.request(priority=1) as request:
        yield request
        
        # Record wait time (time to first see doctor)
        wait_time = env.now - arrival_time
        standard_wait_times.append(wait_time)
        
        # Keep trying to complete treatment
        while remaining_treatment > 0:
            try:
                # Try to complete remaining treatment
                start_time = env.now
                yield env.timeout(remaining_treatment)
                
                # Success! Treatment completed
                remaining_treatment = 0
                
            except simpy.Interrupt:
                # Interrupted by urgent patient
                treatment_done = env.now - start_time
                remaining_treatment -= treatment_done
                interruption_count += 1
        
        # Record interruptions for this patient
        standard_interruptions.append(interruption_count)

def urgent_patient_generator(env, doctors, arrival_rate, treatment_rate):
    """Generate urgent patients."""
    patient_number = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        patient_number += 1
        env.process(urgent_patient(env, f"Urgent {patient_number}", doctors, treatment_rate))

def standard_patient_generator(env, doctors, arrival_rate, treatment_rate):
    """Generate standard patients."""
    patient_number = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        patient_number += 1
        env.process(standard_patient(env, f"Standard {patient_number}", doctors, treatment_rate))

def run_simulation(num_doctors, urgent_arrival_rate, standard_arrival_rate,
                   urgent_treatment_mean, standard_treatment_mean, sim_time, random_seed=42):
    """Run simulation with specified configuration."""
    
    # Reset global data
    global urgent_wait_times, standard_wait_times, standard_interruptions
    urgent_wait_times = []
    standard_wait_times = []
    standard_interruptions = []
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    doctors = simpy.PreemptiveResource(env, capacity=num_doctors)
    
    # Treatment rates
    urgent_treatment_rate = 1 / urgent_treatment_mean
    standard_treatment_rate = 1 / standard_treatment_mean
    
    # Start generators
    env.process(urgent_patient_generator(env, doctors, urgent_arrival_rate, urgent_treatment_rate))
    env.process(standard_patient_generator(env, doctors, standard_arrival_rate, standard_treatment_rate))
    
    # Run
    env.run(until=sim_time)
    
    # Calculate statistics
    total_urgent = len(urgent_wait_times)
    total_standard = len(standard_wait_times)
    
    # Urgent patient metrics
    avg_urgent_wait = np.mean(urgent_wait_times) if urgent_wait_times else 0
    urgent_under_10min = sum(1 for w in urgent_wait_times if w < 10)
    pct_urgent_under_10min = 100 * urgent_under_10min / total_urgent if total_urgent > 0 else 0
    
    # Standard patient metrics
    avg_standard_wait = np.mean(standard_wait_times) if standard_wait_times else 0
    standard_under_30min = sum(1 for w in standard_wait_times if w < 30)
    pct_standard_under_30min = 100 * standard_under_30min / total_standard if total_standard > 0 else 0
    avg_std_interruptions = np.mean(standard_interruptions) if standard_interruptions else 0
    
    # Calculate utilization (approximate)
    total_arrival_rate = urgent_arrival_rate + standard_arrival_rate
    avg_treatment_time = (urgent_arrival_rate * urgent_treatment_mean + 
                          standard_arrival_rate * standard_treatment_mean) / total_arrival_rate
    utilization = (total_arrival_rate * avg_treatment_time) / (num_doctors * 60)  # per hour basis
    
    return {
        'num_doctors': num_doctors,
        'total_urgent': total_urgent,
        'total_standard': total_standard,
        'avg_urgent_wait': avg_urgent_wait,
        'pct_urgent_under_10min': pct_urgent_under_10min,
        'meets_urgent_target': pct_urgent_under_10min >= 90,
        'avg_standard_wait': avg_standard_wait,
        'pct_standard_under_30min': pct_standard_under_30min,
        'meets_standard_target': pct_standard_under_30min >= 80,
        'avg_standard_interruptions': avg_std_interruptions,
        'utilization': utilization,
        'meets_both_targets': pct_urgent_under_10min >= 90 and pct_standard_under_30min >= 80
    }

def calculate_cost(stats, doctor_cost_per_hour, sim_hours, 
                   urgent_dissatisfaction_per_min, standard_dissatisfaction_per_min):
    """Calculate total operational cost."""
    
    # Doctor costs
    doctor_costs = stats['num_doctors'] * doctor_cost_per_hour * sim_hours
    
    # Patient dissatisfaction costs
    urgent_dissatisfaction = stats['total_urgent'] * stats['avg_urgent_wait'] * urgent_dissatisfaction_per_min
    standard_dissatisfaction = stats['total_standard'] * stats['avg_standard_wait'] * standard_dissatisfaction_per_min
    
    total_cost = doctor_costs + urgent_dissatisfaction + standard_dissatisfaction
    
    return {
        'doctor_costs': doctor_costs,
        'urgent_dissatisfaction': urgent_dissatisfaction,
        'standard_dissatisfaction': standard_dissatisfaction,
        'total_cost': total_cost
    }

# Simulation parameters
SIM_TIME = 720  # 12 hours in minutes
SIM_HOURS = 12

# Patient arrival rates (per hour, convert to per minute)
URGENT_ARRIVAL_RATE = 1 / 60  # 1 per hour
STANDARD_ARRIVAL_RATE = 3 / 60  # 3 per hour

# Treatment times (minutes)
URGENT_TREATMENT_MEAN = 30
STANDARD_TREATMENT_MEAN = 20

# Cost parameters
DOCTOR_COST_PER_HOUR = 40
URGENT_DISSATISFACTION_PER_MIN = 5
STANDARD_DISSATISFACTION_PER_MIN = 1

# Doctor configurations to test
doctor_configs = [2, 3, 4, 5]

print("="*90)
print("HOSPITAL EMERGENCY DEPARTMENT SIMULATION")
print("="*90)
print(f"Simulation time: {SIM_TIME} minutes ({SIM_HOURS} hours)")
print(f"\nPatient Arrivals:")
print(f"  Urgent: {URGENT_ARRIVAL_RATE*60:.1f} patients/hour")
print(f"  Standard: {STANDARD_ARRIVAL_RATE*60:.1f} patients/hour")
print(f"\nTreatment Times:")
print(f"  Urgent: {URGENT_TREATMENT_MEAN} minutes average")
print(f"  Standard: {STANDARD_TREATMENT_MEAN} minutes average")
print(f"\nService Level Targets:")
print(f"  Urgent: 90% wait < 10 minutes")
print(f"  Standard: 80% wait < 30 minutes")
print(f"\nCosts:")
print(f"  Doctor: £{DOCTOR_COST_PER_HOUR}/hour")
print(f"  Urgent dissatisfaction: £{URGENT_DISSATISFACTION_PER_MIN}/minute")
print(f"  Standard dissatisfaction: £{STANDARD_DISSATISFACTION_PER_MIN}/minute")
print()

results = []

for num_doctors in doctor_configs:
    print(f"\n{'='*90}")
    print(f"Configuration: {num_doctors} Doctors")
    print(f"{'='*90}")
    
    stats = run_simulation(num_doctors, URGENT_ARRIVAL_RATE, STANDARD_ARRIVAL_RATE,
                           URGENT_TREATMENT_MEAN, STANDARD_TREATMENT_MEAN, SIM_TIME)
    
    costs = calculate_cost(stats, DOCTOR_COST_PER_HOUR, SIM_HOURS,
                           URGENT_DISSATISFACTION_PER_MIN, STANDARD_DISSATISFACTION_PER_MIN)
    
    # Combine stats and costs
    stats.update(costs)
    results.append(stats)
    
    print(f"\nUrgent Patient Metrics:")
    print(f"  Total treated: {stats['total_urgent']}")
    print(f"  Average wait: {stats['avg_urgent_wait']:.2f} minutes")
    print(f"  % waiting < 10 min: {stats['pct_urgent_under_10min']:.1f}% ", end='')
    print("✓ MEETS TARGET" if stats['meets_urgent_target'] else "✗ BELOW TARGET")
    
    print(f"\nStandard Patient Metrics:")
    print(f"  Total treated: {stats['total_standard']}")
    print(f"  Average wait: {stats['avg_standard_wait']:.2f} minutes")
    print(f"  % waiting < 30 min: {stats['pct_standard_under_30min']:.1f}% ", end='')
    print("✓ MEETS TARGET" if stats['meets_standard_target'] else "✗ BELOW TARGET")
    print(f"  Average interruptions: {stats['avg_standard_interruptions']:.2f}")
    
    print(f"\nSystem Metrics:")
    print(f"  Doctor utilization: {stats['utilization']:.1%}")
    print(f"  Both targets met: ", end='')
    print("✓ YES" if stats['meets_both_targets'] else "✗ NO")
    
    print(f"\nCost Analysis:")
    print(f"  Doctor costs: £{stats['doctor_costs']:.2f}")
    print(f"  Urgent dissatisfaction: £{stats['urgent_dissatisfaction']:.2f}")
    print(f"  Standard dissatisfaction: £{stats['standard_dissatisfaction']:.2f}")
    print(f"  TOTAL COST: £{stats['total_cost']:.2f}")

# Find optimal configuration
meeting_targets = [r for r in results if r['meets_both_targets']]
if meeting_targets:
    optimal = min(meeting_targets, key=lambda x: x['total_cost'])
    optimal_found = True
else:
    # If no config meets both targets, choose best compromise
    optimal = min(results, key=lambda x: x['total_cost'])
    optimal_found = False

# Summary
print("\n" + "="*90)
print("SUMMARY COMPARISON")
print("="*90)
print(f"{'Doctors':<10} {'Urgent %':<12} {'Std %':<12} {'Targets':<10} {'Util':<10} {'Total Cost':<15}")
print("-"*90)
for stats in results:
    targets = "✓ Both" if stats['meets_both_targets'] else "✗ Miss"
    print(f"{stats['num_doctors']:<10} {stats['pct_urgent_under_10min']:<12.1f} "
          f"{stats['pct_standard_under_30min']:<12.1f} {targets:<10} "
          f"{stats['utilization']:<10.1%} £{stats['total_cost']:<14.2f}")

# Recommendation
print("\n" + "="*90)
print("RECOMMENDATION")
print("="*90)
if optimal_found:
    print(f"\nOptimal configuration: {optimal['num_doctors']} doctors")
    print(f"Minimum cost while meeting targets: £{optimal['total_cost']:.2f}")
    print(f"\nThis configuration:")
    print(f"  • Meets urgent patient target: {optimal['pct_urgent_under_10min']:.1f}% wait < 10 min (target: 90%)")
    print(f"  • Meets standard patient target: {optimal['pct_standard_under_30min']:.1f}% wait < 30 min (target: 80%)")
    print(f"  • Doctor utilization: {optimal['utilization']:.1%}")
    print(f"  • Standard patients experience {optimal['avg_standard_interruptions']:.2f} interruptions on average")
    print(f"\nImpact of interruptions:")
    if optimal['avg_standard_interruptions'] > 1:
        print(f"  Standard patients are frequently interrupted (avg {optimal['avg_standard_interruptions']:.2f} times)")
        print(f"  This may impact patient experience despite meeting wait time targets")
    else:
        print(f"  Interruptions are minimal, indicating good capacity buffer")
else:
    print(f"\nWARNING: No configuration meets both service level targets!")
    print(f"Best compromise: {optimal['num_doctors']} doctors")
    print(f"  • Urgent: {optimal['pct_urgent_under_10min']:.1f}% (target: 90%)")
    print(f"  • Standard: {optimal['pct_standard_under_30min']:.1f}% (target: 80%)")
    print(f"\nRecommendation: Consider increasing doctors beyond {max(doctor_configs)} or revising targets")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Extract data for plotting
doctors = [r['num_doctors'] for r in results]
urgent_service = [r['pct_urgent_under_10min'] for r in results]
standard_service = [r['pct_standard_under_30min'] for r in results]
total_costs = [r['total_cost'] for r in results]
doctor_costs = [r['doctor_costs'] for r in results]
dissatisfaction_costs = [r['urgent_dissatisfaction'] + r['standard_dissatisfaction'] for r in results]
avg_interruptions = [r['avg_standard_interruptions'] for r in results]

# Plot 1: Service level achievement
axes[0, 0].plot(doctors, urgent_service, marker='o', linewidth=2, markersize=8, 
                label='Urgent (< 10 min)', color='red')
axes[0, 0].plot(doctors, standard_service, marker='s', linewidth=2, markersize=8,
                label='Standard (< 30 min)', color='blue')
axes[0, 0].axhline(y=90, color='red', linestyle='--', linewidth=1, alpha=0.5)
axes[0, 0].axhline(y=80, color='blue', linestyle='--', linewidth=1, alpha=0.5)
axes[0, 0].set_xlabel('Number of Doctors')
axes[0, 0].set_ylabel('% Meeting Target')
axes[0, 0].set_title('Service Level Achievement')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_ylim([0, 105])

# Plot 2: Total cost breakdown (stacked bar)
width = 0.6
axes[0, 1].bar(doctors, doctor_costs, width, label='Doctor Costs', color='steelblue', alpha=0.8)
axes[0, 1].bar(doctors, dissatisfaction_costs, width, bottom=doctor_costs, 
               label='Dissatisfaction Costs', color='coral', alpha=0.8)
if optimal_found:
    optimal_idx = doctors.index(optimal['num_doctors'])
    axes[0, 1].bar(doctors[optimal_idx], results[optimal_idx]['total_cost'], width,
                   edgecolor='gold', linewidth=4, fill=False, label='Optimal')
axes[0, 1].set_xlabel('Number of Doctors')
axes[0, 1].set_ylabel('Cost (£)')
axes[0, 1].set_title('Cost Breakdown')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Plot 3: Wait times comparison
avg_urgent_waits = [r['avg_urgent_wait'] for r in results]
avg_standard_waits = [r['avg_standard_wait'] for r in results]

x = np.arange(len(doctors))
width = 0.35
axes[1, 0].bar(x - width/2, avg_urgent_waits, width, label='Urgent', color='red', alpha=0.7)
axes[1, 0].bar(x + width/2, avg_standard_waits, width, label='Standard', color='blue', alpha=0.7)
axes[1, 0].set_xlabel('Number of Doctors')
axes[1, 0].set_ylabel('Average Wait Time (minutes)')
axes[1, 0].set_title('Average Wait Times by Patient Type')
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(doctors)
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Plot 4: Interruptions
axes[1, 1].plot(doctors, avg_interruptions, marker='^', linewidth=2, markersize=10, color='orange')
axes[1, 1].set_xlabel('Number of Doctors')
axes[1, 1].set_ylabel('Average Interruptions per Standard Patient')
axes[1, 1].set_title('Impact of Preemption on Standard Patients')
axes[1, 1].grid(True, alpha=0.3)

# Add annotation
axes[1, 1].text(0.5, 0.95, 'Lower is better\n(fewer disruptions)', 
                transform=axes[1, 1].transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('Q5_Hospital_ED_Results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'Q5_Hospital_ED_Results.png'")
plt.show()
