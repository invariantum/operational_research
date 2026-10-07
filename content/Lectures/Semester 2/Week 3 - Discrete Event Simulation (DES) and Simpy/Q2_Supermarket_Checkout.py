"""
Question 2: Supermarket Checkout Optimization (M/M/c Queue)
Simulation to find the optimal number of checkout lanes.
"""

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Global data collection
wait_times = []
system_times = []
queue_lengths = []

def customer(env, name, checkouts, service_rate):
    """Customer arrives, waits for checkout, gets served, and leaves."""
    arrival_time = env.now
    
    # Record queue length at arrival
    queue_lengths.append(len(checkouts.queue))
    
    with checkouts.request() as request:
        yield request
        
        # Record wait time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        # Service time (exponential)
        service_time = random.expovariate(service_rate)
        yield env.timeout(service_time)
        
        # Record total system time
        system_time = env.now - arrival_time
        system_times.append(system_time)

def customer_generator(env, checkouts, arrival_rate, service_rate):
    """Generate customers arriving at the supermarket."""
    customer_number = 0
    while True:
        # Wait for next customer
        yield env.timeout(random.expovariate(arrival_rate))
        
        customer_number += 1
        env.process(customer(env, f"Customer {customer_number}", checkouts, service_rate))

def run_simulation(num_checkouts, arrival_rate, service_rate, sim_time, random_seed=42):
    """Run a single simulation and return statistics."""
    
    # Reset global data
    global wait_times, system_times, queue_lengths
    wait_times = []
    system_times = []
    queue_lengths = []
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    checkouts = simpy.Resource(env, capacity=num_checkouts)
    
    # Start generator
    env.process(customer_generator(env, checkouts, arrival_rate, service_rate))
    
    # Run simulation
    env.run(until=sim_time)
    
    # Calculate statistics
    total_customers = len(wait_times)
    avg_wait = np.mean(wait_times) if wait_times else 0
    avg_system_time = np.mean(system_times) if system_times else 0
    avg_queue_length = np.mean(queue_lengths) if queue_lengths else 0
    max_queue_length = max(queue_lengths) if queue_lengths else 0
    pct_waited = 100 * sum(1 for w in wait_times if w > 0) / total_customers if total_customers > 0 else 0
    
    # Calculate utilization
    utilization = arrival_rate / (num_checkouts * service_rate)
    
    return {
        'num_checkouts': num_checkouts,
        'utilization': utilization,
        'total_customers': total_customers,
        'avg_wait': avg_wait,
        'avg_system_time': avg_system_time,
        'avg_queue_length': avg_queue_length,
        'max_queue_length': max_queue_length,
        'pct_waited': pct_waited
    }

def calculate_cost(stats, staff_cost_per_hour, wait_cost_per_minute, sim_hours):
    """Calculate total cost for the simulation period."""
    
    # Staff cost
    staff_cost = stats['num_checkouts'] * staff_cost_per_hour * sim_hours
    
    # Wait cost (total wait time across all customers)
    total_wait_time = stats['total_customers'] * stats['avg_wait']
    wait_cost = total_wait_time * wait_cost_per_minute
    
    # Total cost
    total_cost = staff_cost + wait_cost
    
    return {
        'staff_cost': staff_cost,
        'wait_cost': wait_cost,
        'total_cost': total_cost
    }

# Simulation parameters
SIM_TIME = 240  # 4 hours in minutes
ARRIVAL_RATE = 48 / 60  # 48 customers/hour = 0.8 customers/minute
SERVICE_TIME_MEAN = 4  # minutes
SERVICE_RATE = 1 / SERVICE_TIME_MEAN  # customers per minute per checkout

# Cost parameters
STAFF_COST_PER_HOUR = 12  # £12 per hour per checkout
WAIT_COST_PER_MINUTE = 0.20  # £0.20 per minute of wait
SIM_HOURS = SIM_TIME / 60  # 4 hours

print("="*80)
print("SUPERMARKET CHECKOUT OPTIMIZATION (M/M/c QUEUE)")
print("="*80)
print(f"Arrival rate: {ARRIVAL_RATE*60:.1f} customers/hour")
print(f"Service time: {SERVICE_TIME_MEAN} minutes average per customer")
print(f"Simulation time: {SIM_TIME} minutes ({SIM_HOURS} hours)")
print(f"Staff cost: £{STAFF_COST_PER_HOUR}/hour per checkout")
print(f"Wait cost: £{WAIT_COST_PER_MINUTE}/minute per customer")
print()

results = []
checkout_configs = [2, 3, 4, 5, 6]

for num_checkouts in checkout_configs:
    print(f"\n{'='*80}")
    print(f"Configuration: {num_checkouts} Checkout Lanes")
    print(f"{'='*80}")
    
    stats = run_simulation(num_checkouts, ARRIVAL_RATE, SERVICE_RATE, SIM_TIME)
    costs = calculate_cost(stats, STAFF_COST_PER_HOUR, WAIT_COST_PER_MINUTE, SIM_HOURS)
    
    # Combine statistics and costs
    stats.update(costs)
    results.append(stats)
    
    print(f"\nPerformance Metrics:")
    print(f"  System utilization (ρ): {stats['utilization']:.3f}")
    print(f"  Total customers served: {stats['total_customers']}")
    print(f"  Average wait time: {stats['avg_wait']:.2f} minutes")
    print(f"  Average queue length: {stats['avg_queue_length']:.2f} customers")
    print(f"  Maximum queue length: {stats['max_queue_length']} customers")
    print(f"  Customers who waited: {stats['pct_waited']:.1f}%")
    
    print(f"\nCost Analysis:")
    print(f"  Staff cost: £{stats['staff_cost']:.2f}")
    print(f"  Wait cost: £{stats['wait_cost']:.2f}")
    print(f"  TOTAL COST: £{stats['total_cost']:.2f}")

# Find optimal configuration
optimal = min(results, key=lambda x: x['total_cost'])

print("\n" + "="*80)
print("SUMMARY COMPARISON")
print("="*80)
print(f"{'Lanes':<8} {'ρ':<8} {'Avg Wait':<12} {'Queue Len':<12} {'Staff £':<12} {'Wait £':<12} {'Total £':<12}")
print("-"*80)
for stats in results:
    print(f"{stats['num_checkouts']:<8} {stats['utilization']:<8.3f} {stats['avg_wait']:<12.2f} "
          f"{stats['avg_queue_length']:<12.2f} {stats['staff_cost']:<12.2f} "
          f"{stats['wait_cost']:<12.2f} {stats['total_cost']:<12.2f}")

print("\n" + "="*80)
print("RECOMMENDATION")
print("="*80)
print(f"\nOptimal number of checkout lanes: {optimal['num_checkouts']}")
print(f"Minimum total cost: £{optimal['total_cost']:.2f}")
print(f"\nAt this configuration:")
print(f"  - Utilization: {optimal['utilization']:.1%} (system is {'stable' if optimal['utilization'] < 1 else 'UNSTABLE'})")
print(f"  - Average wait time: {optimal['avg_wait']:.2f} minutes")
print(f"  - {optimal['pct_waited']:.1f}% of customers experience a wait")
print(f"\nRationale:")
if optimal['num_checkouts'] == min(checkout_configs):
    print("  Minimum configuration tested - consider reducing further")
elif optimal['num_checkouts'] == max(checkout_configs):
    print("  Maximum configuration tested - may need more lanes")
else:
    print(f"  Adding another lane would increase staff costs by £{STAFF_COST_PER_HOUR * SIM_HOURS:.2f}")
    print(f"  but only reduce wait costs marginally (diminishing returns)")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Extract data for plotting
lanes = [r['num_checkouts'] for r in results]
avg_waits = [r['avg_wait'] for r in results]
staff_costs = [r['staff_cost'] for r in results]
wait_costs = [r['wait_cost'] for r in results]
total_costs = [r['total_cost'] for r in results]
utilizations = [r['utilization'] for r in results]

# Plot 1: Cost breakdown (stacked bar)
width = 0.6
axes[0, 0].bar(lanes, staff_costs, width, label='Staff Costs', color='steelblue', alpha=0.8)
axes[0, 0].bar(lanes, wait_costs, width, bottom=staff_costs, label='Wait Costs', color='coral', alpha=0.8)
axes[0, 0].set_xlabel('Number of Checkout Lanes')
axes[0, 0].set_ylabel('Cost (£)')
axes[0, 0].set_title('Cost Breakdown by Number of Lanes')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3, axis='y')

# Plot 2: Total cost curve
axes[0, 1].plot(lanes, total_costs, marker='o', linewidth=2, markersize=10, color='purple')
optimal_idx = total_costs.index(min(total_costs))
axes[0, 1].plot(lanes[optimal_idx], total_costs[optimal_idx], 
                marker='*', markersize=20, color='gold', 
                label=f'Optimal: {lanes[optimal_idx]} lanes')
axes[0, 1].set_xlabel('Number of Checkout Lanes')
axes[0, 1].set_ylabel('Total Cost (£)')
axes[0, 1].set_title('Total Cost vs Number of Lanes')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Average wait time
axes[1, 0].plot(lanes, avg_waits, marker='s', linewidth=2, markersize=8, color='green')
axes[1, 0].set_xlabel('Number of Checkout Lanes')
axes[1, 0].set_ylabel('Average Wait Time (minutes)')
axes[1, 0].set_title('Wait Time vs Number of Lanes')
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Utilization
axes[1, 1].plot(lanes, utilizations, marker='^', linewidth=2, markersize=8, color='red')
axes[1, 1].axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='Critical (ρ=1)')
axes[1, 1].set_xlabel('Number of Checkout Lanes')
axes[1, 1].set_ylabel('Utilization (ρ)')
axes[1, 1].set_title('System Utilization')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Q2_Supermarket_Checkout_Results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'Q2_Supermarket_Checkout_Results.png'")
plt.show()
