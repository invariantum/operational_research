"""
Question 3: Call Center Capacity Planning (M/M/c Queue)
Simulation to determine staffing requirements for different time periods.
"""

import simpy
import random
import numpy as np
import matplotlib.pyplot as plt

# Global data collection
wait_times = []
system_times = []

def caller(env, name, agents, service_rate):
    """Caller arrives, waits for agent, gets served, and leaves."""
    arrival_time = env.now
    
    with agents.request() as request:
        yield request
        
        # Record wait time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        # Service time (call handling time - exponential)
        service_time = random.expovariate(service_rate)
        yield env.timeout(service_time)
        
        # Record total system time
        system_time = env.now - arrival_time
        system_times.append(system_time)

def caller_generator(env, agents, arrival_rate, service_rate):
    """Generate callers arriving at the call center."""
    caller_number = 0
    while True:
        # Wait for next caller
        yield env.timeout(random.expovariate(arrival_rate))
        
        caller_number += 1
        env.process(caller(env, f"Caller {caller_number}", agents, service_rate))

def run_simulation(num_agents, arrival_rate, service_rate, sim_time, random_seed=42):
    """Run a single simulation and return statistics."""
    
    # Reset global data
    global wait_times, system_times
    wait_times = []
    system_times = []
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    agents = simpy.Resource(env, capacity=num_agents)
    
    # Start generator
    env.process(caller_generator(env, agents, arrival_rate, service_rate))
    
    # Run simulation
    env.run(until=sim_time)
    
    # Calculate statistics
    total_callers = len(wait_times)
    avg_wait = np.mean(wait_times) if wait_times else 0
    max_wait = max(wait_times) if wait_times else 0
    
    # Service level: percentage waiting < 2 minutes
    callers_under_2min = sum(1 for w in wait_times if w < 2)
    pct_under_2min = 100 * callers_under_2min / total_callers if total_callers > 0 else 0
    
    # Calculate utilization
    utilization = arrival_rate / (num_agents * service_rate)
    
    return {
        'num_agents': num_agents,
        'utilization': utilization,
        'total_callers': total_callers,
        'avg_wait': avg_wait,
        'max_wait': max_wait,
        'pct_under_2min': pct_under_2min,
        'meets_target': pct_under_2min >= 80
    }

# Simulation parameters
SIM_TIME = 480  # 8 hours in minutes
SERVICE_TIME_MEAN = 8  # minutes
SERVICE_RATE = 1 / SERVICE_TIME_MEAN  # calls per minute per agent

# Three time periods with different arrival rates
periods = {
    'Normal Hours': {'arrival_rate': 12/60, 'description': '12 calls/hour'},
    'Peak Hours': {'arrival_rate': 18/60, 'description': '18 calls/hour (50% higher)'},
    'Off-Peak Hours': {'arrival_rate': 8.4/60, 'description': '8.4 calls/hour (30% lower)'}
}

# Agent configurations to test
agent_configs = [2, 3, 4, 5]

print("="*90)
print("CALL CENTER CAPACITY PLANNING (M/M/c QUEUE)")
print("="*90)
print(f"Average call handling time: {SERVICE_TIME_MEAN} minutes")
print(f"Simulation time: {SIM_TIME} minutes (8 hours)")
print(f"Service level target: 80% of callers wait < 2 minutes")
print()

all_results = {}

for period_name, period_data in periods.items():
    print(f"\n{'='*90}")
    print(f"{period_name.upper()}: {period_data['description']}")
    print(f"{'='*90}")
    
    arrival_rate = period_data['arrival_rate']
    results = []
    
    for num_agents in agent_configs:
        stats = run_simulation(num_agents, arrival_rate, SERVICE_RATE, SIM_TIME)
        results.append(stats)
        
        meets = "✓ MEETS TARGET" if stats['meets_target'] else "✗ BELOW TARGET"
        print(f"\n{num_agents} Agents:")
        print(f"  Utilization (ρ): {stats['utilization']:.3f}")
        print(f"  Total callers: {stats['total_callers']}")
        print(f"  Average wait: {stats['avg_wait']:.2f} minutes")
        print(f"  Maximum wait: {stats['max_wait']:.2f} minutes")
        print(f"  % waiting < 2 min: {stats['pct_under_2min']:.1f}% {meets}")
    
    # Find minimum agents needed
    meeting_target = [r for r in results if r['meets_target']]
    if meeting_target:
        min_agents = min(meeting_target, key=lambda x: x['num_agents'])
        print(f"\n>>> Minimum agents needed: {min_agents['num_agents']} (achieves {min_agents['pct_under_2min']:.1f}%)")
    else:
        print(f"\n>>> WARNING: Target not met with up to {max(agent_configs)} agents!")
    
    all_results[period_name] = results

# Staffing recommendations
print("\n" + "="*90)
print("STAFFING RECOMMENDATIONS")
print("="*90)

recommendations = {}
for period_name, results in all_results.items():
    meeting_target = [r for r in results if r['meets_target']]
    if meeting_target:
        min_agents = min(meeting_target, key=lambda x: x['num_agents'])
        recommendations[period_name] = min_agents['num_agents']
        print(f"\n{period_name}:")
        print(f"  Recommended agents: {min_agents['num_agents']}")
        print(f"  Expected utilization: {min_agents['utilization']:.1%}")
        print(f"  Service level achieved: {min_agents['pct_under_2min']:.1f}%")
    else:
        recommendations[period_name] = max(agent_configs)
        print(f"\n{period_name}:")
        print(f"  WARNING: Need more than {max(agent_configs)} agents to meet target")

# Create summary table
print("\n" + "="*90)
print("SUMMARY TABLE")
print("="*90)
print(f"{'Period':<20} {'Arrival Rate':<15} {'Min Agents':<12} {'Comments':<30}")
print("-"*90)
for period_name in periods.keys():
    arr_rate = periods[period_name]['arrival_rate'] * 60
    min_agents = recommendations.get(period_name, '?')
    
    if period_name in all_results:
        meeting = [r for r in all_results[period_name] if r['meets_target']]
        if meeting:
            comment = f"Achieves {meeting[0]['pct_under_2min']:.1f}% service level"
        else:
            comment = "Target not met - need more agents"
    else:
        comment = ""
    
    print(f"{period_name:<20} {arr_rate:<15.1f} {min_agents!s:<12} {comment:<30}")

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: Average wait time vs agents for all periods
for period_name, results in all_results.items():
    agents = [r['num_agents'] for r in results]
    avg_waits = [r['avg_wait'] for r in results]
    axes[0, 0].plot(agents, avg_waits, marker='o', linewidth=2, markersize=8, label=period_name)

axes[0, 0].axhline(y=2, color='red', linestyle='--', linewidth=2, label='Target (2 min)')
axes[0, 0].set_xlabel('Number of Agents')
axes[0, 0].set_ylabel('Average Wait Time (minutes)')
axes[0, 0].set_title('Wait Time vs Number of Agents')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Service level (% under 2 min) vs agents
for period_name, results in all_results.items():
    agents = [r['num_agents'] for r in results]
    pct_under_2 = [r['pct_under_2min'] for r in results]
    axes[0, 1].plot(agents, pct_under_2, marker='s', linewidth=2, markersize=8, label=period_name)

axes[0, 1].axhline(y=80, color='red', linestyle='--', linewidth=2, label='Target (80%)')
axes[0, 1].set_xlabel('Number of Agents')
axes[0, 1].set_ylabel('% Callers Waiting < 2 min')
axes[0, 1].set_title('Service Level Achievement')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].set_ylim([0, 105])

# Plot 3: Utilization for each period
period_names = list(periods.keys())
colors = ['blue', 'red', 'green']

for i, (period_name, results) in enumerate(all_results.items()):
    agents = [r['num_agents'] for r in results]
    utils = [r['utilization'] for r in results]
    axes[1, 0].plot(agents, utils, marker='^', linewidth=2, markersize=8, 
                    label=period_name, color=colors[i])

axes[1, 0].axhline(y=1.0, color='black', linestyle='--', linewidth=2, label='Critical (ρ=1)')
axes[1, 0].set_xlabel('Number of Agents')
axes[1, 0].set_ylabel('Utilization (ρ)')
axes[1, 0].set_title('System Utilization by Period')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Recommended staffing levels (bar chart)
recommended_agents = [recommendations.get(p, 0) for p in period_names]
axes[1, 1].bar(range(len(period_names)), recommended_agents, 
               color=colors, alpha=0.7, edgecolor='black', linewidth=2)
axes[1, 1].set_xlabel('Time Period')
axes[1, 1].set_ylabel('Recommended Number of Agents')
axes[1, 1].set_title('Recommended Staffing Schedule')
axes[1, 1].set_xticks(range(len(period_names)))
axes[1, 1].set_xticklabels([p.replace(' Hours', '') for p in period_names], rotation=15)
axes[1, 1].grid(True, alpha=0.3, axis='y')

# Add values on bars
for i, v in enumerate(recommended_agents):
    axes[1, 1].text(i, v + 0.1, str(v), ha='center', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('Q3_Call_Center_Results.png', dpi=300, bbox_inches='tight')
print("\nVisualization saved as 'Q3_Call_Center_Results.png'")
plt.show()

# Final recommendation
print("\n" + "="*90)
print("FINAL STAFFING SCHEDULE")
print("="*90)
print("\nRecommended agent allocation:")
print(f"  • Off-Peak Hours: {recommendations.get('Off-Peak Hours', 'TBD')} agents")
print(f"  • Normal Hours: {recommendations.get('Normal Hours', 'TBD')} agents")
print(f"  • Peak Hours: {recommendations.get('Peak Hours', 'TBD')} agents")
print("\nThis schedule maintains the 80% service level target across all periods")
print("while minimizing staffing costs through dynamic allocation.")
