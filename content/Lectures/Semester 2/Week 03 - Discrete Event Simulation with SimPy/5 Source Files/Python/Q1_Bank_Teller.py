"""
Question 1: Bank Teller Analysis (M/M/1 Queue)
Simulation of a bank with a single teller serving customers.
"""

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Global data collection
wait_times = []
service_times = []
system_times = []

def customer(env, name, teller, service_rate):
    """Customer arrives, waits for teller, gets served, and leaves."""
    arrival_time = env.now
    
    with teller.request() as request:
        yield request
        
        # Record wait time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        # Service time (exponential)
        service_time = random.expovariate(service_rate)
        service_times.append(service_time)
        
        yield env.timeout(service_time)
        
        # Record total system time
        system_time = env.now - arrival_time
        system_times.append(system_time)

def customer_generator(env, teller, arrival_rate, service_rate):
    """Generate customers arriving at the bank."""
    customer_number = 0
    while True:
        # Wait for next customer
        yield env.timeout(random.expovariate(arrival_rate))
        
        customer_number += 1
        env.process(customer(env, f"Customer {customer_number}", teller, service_rate))

def run_simulation(arrival_rate, service_rate, sim_time, random_seed=42):
    """Run a single simulation and return statistics."""
    
    # Reset global data
    global wait_times, service_times, system_times
    wait_times = []
    service_times = []
    system_times = []
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    teller = simpy.Resource(env, capacity=1)
    
    # Start generator
    env.process(customer_generator(env, teller, arrival_rate, service_rate))
    
    # Run simulation
    env.run(until=sim_time)
    
    # Calculate statistics
    total_customers = len(wait_times)
    avg_wait = np.mean(wait_times) if wait_times else 0
    avg_system_time = np.mean(system_times) if system_times else 0
    max_wait = max(wait_times) if wait_times else 0
    pct_waited = 100 * sum(1 for w in wait_times if w > 0) / total_customers if total_customers > 0 else 0
    
    # Calculate utilization
    utilization = arrival_rate / service_rate
    
    # Theoretical values (M/M/1 formulas)
    if utilization < 1:
        theoretical_wait_queue = utilization / (service_rate * (1 - utilization))
        theoretical_time_system = 1 / (service_rate - arrival_rate)
    else:
        theoretical_wait_queue = float('inf')
        theoretical_time_system = float('inf')
    
    return {
        'arrival_rate': arrival_rate,
        'utilization': utilization,
        'total_customers': total_customers,
        'avg_wait': avg_wait,
        'avg_system_time': avg_system_time,
        'max_wait': max_wait,
        'pct_waited': pct_waited,
        'theoretical_wait': theoretical_wait_queue,
        'theoretical_system': theoretical_time_system,
        'wait_times_data': wait_times.copy()
    }

# Simulation parameters
SIM_TIME = 480  # 8 hours in minutes
SERVICE_TIME_MEAN = 3  # minutes
SERVICE_RATE = 1 / SERVICE_TIME_MEAN  # customers per minute

# Three scenarios with different arrival rates
scenarios = [
    {'name': 'Scenario 1', 'arrival_rate': 15/60},  # 15 customers/hour = 0.25/min
    {'name': 'Scenario 2', 'arrival_rate': 18/60},  # 18 customers/hour = 0.30/min
    {'name': 'Scenario 3', 'arrival_rate': 20/60},  # 20 customers/hour = 0.333/min
]

print("="*80)
print("BANK TELLER ANALYSIS (M/M/1 QUEUE)")
print("="*80)
print(f"Service time: {SERVICE_TIME_MEAN} minutes average")
print(f"Simulation time: {SIM_TIME} minutes (8 hours)")
print()

results = []
for scenario in scenarios:
    print(f"\n{scenario['name']}: Arrival rate = {scenario['arrival_rate']*60:.1f} customers/hour")
    print("-"*80)
    
    stats = run_simulation(scenario['arrival_rate'], SERVICE_RATE, SIM_TIME)
    results.append(stats)
    
    print(f"Utilization (ρ): {stats['utilization']:.3f}")
    print(f"\nSimulation Results:")
    print(f"  Total customers served: {stats['total_customers']}")
    print(f"  Average wait time: {stats['avg_wait']:.2f} minutes")
    print(f"  Average time in system: {stats['avg_system_time']:.2f} minutes")
    print(f"  Maximum wait time: {stats['max_wait']:.2f} minutes")
    print(f"  Customers who waited: {stats['pct_waited']:.1f}%")
    
    print(f"\nTheoretical Results (M/M/1 formulas):")
    if stats['theoretical_wait'] != float('inf'):
        print(f"  Average wait time: {stats['theoretical_wait']:.2f} minutes")
        print(f"  Average time in system: {stats['theoretical_system']:.2f} minutes")
    else:
        print(f"  System is UNSTABLE (ρ ≥ 1)")
    
    print(f"\nDifference (Simulation - Theoretical):")
    if stats['theoretical_wait'] != float('inf'):
        wait_diff = stats['avg_wait'] - stats['theoretical_wait']
        system_diff = stats['avg_system_time'] - stats['theoretical_system']
        print(f"  Wait time difference: {wait_diff:+.2f} minutes")
        print(f"  System time difference: {system_diff:+.2f} minutes")

# Summary comparison
print("\n" + "="*80)
print("SUMMARY COMPARISON")
print("="*80)
print(f"{'Scenario':<12} {'ρ':<8} {'Avg Wait':<12} {'Theoretical':<12} {'Max Wait':<12} {'% Waited':<10}")
print("-"*80)
for i, stats in enumerate(results):
    theo = f"{stats['theoretical_wait']:.2f}" if stats['theoretical_wait'] != float('inf') else "UNSTABLE"
    print(f"{scenarios[i]['name']:<12} {stats['utilization']:<8.3f} {stats['avg_wait']:<12.2f} "
          f"{theo:<12} {stats['max_wait']:<12.2f} {stats['pct_waited']:<10.1f}")

print("\n" + "="*80)
print("ANALYSIS")
print("="*80)
print("\nAcceptable service levels:")
for i, stats in enumerate(results):
    if stats['utilization'] < 0.85 and stats['avg_wait'] < 5:
        print(f"  {scenarios[i]['name']}: ACCEPTABLE (low utilization, short waits)")
    elif stats['utilization'] < 0.95 and stats['avg_wait'] < 10:
        print(f"  {scenarios[i]['name']}: MODERATE (medium utilization, acceptable waits)")
    else:
        print(f"  {scenarios[i]['name']}: POOR (high utilization, long waits)")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Wait time distributions
colors = ['blue', 'orange', 'red']
for i, stats in enumerate(results):
    axes[0, 0].hist(stats['wait_times_data'], bins=20, alpha=0.5, 
                    label=scenarios[i]['name'], color=colors[i], edgecolor='black')
axes[0, 0].set_xlabel('Wait Time (minutes)')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Distribution of Wait Times')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Average wait time comparison
scenario_names = [s['name'] for s in scenarios]
avg_waits = [r['avg_wait'] for r in results]
theoretical_waits = [r['theoretical_wait'] if r['theoretical_wait'] != float('inf') else 0 
                     for r in results]

x = np.arange(len(scenario_names))
width = 0.35
axes[0, 1].bar(x - width/2, avg_waits, width, label='Simulation', color='steelblue')
axes[0, 1].bar(x + width/2, theoretical_waits, width, label='Theoretical', color='coral')
axes[0, 1].set_xlabel('Scenario')
axes[0, 1].set_ylabel('Average Wait Time (minutes)')
axes[0, 1].set_title('Simulation vs Theoretical Wait Times')
axes[0, 1].set_xticks(x)
axes[0, 1].set_xticklabels(scenario_names)
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Plot 3: Utilization
utilizations = [r['utilization'] for r in results]
axes[1, 0].bar(scenario_names, utilizations, color=['green', 'yellow', 'red'], alpha=0.7)
axes[1, 0].axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='Critical (ρ=1)')
axes[1, 0].set_xlabel('Scenario')
axes[1, 0].set_ylabel('Utilization (ρ)')
axes[1, 0].set_title('System Utilization')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Plot 4: Maximum wait times
max_waits = [r['max_wait'] for r in results]
axes[1, 1].bar(scenario_names, max_waits, color='darkred', alpha=0.7)
axes[1, 1].set_xlabel('Scenario')
axes[1, 1].set_ylabel('Maximum Wait Time (minutes)')
axes[1, 1].set_title('Maximum Wait Time Observed')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('Q1_Bank_Teller_Results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'Q1_Bank_Teller_Results.png'")
plt.show()
