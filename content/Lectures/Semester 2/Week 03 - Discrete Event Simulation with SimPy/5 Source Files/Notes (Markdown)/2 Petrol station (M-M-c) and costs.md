# Segment 2: Petrol Station with Multiple Pumps

## Overview

In this segment, we extend the basic M/M/1 queue to model a petrol (gas) station with multiple pumps. This introduces the concept of **parallel servers** and demonstrates how capacity affects system performance.

## The Problem

A petrol station has several fuel pumps. Cars arrive randomly, use an available pump to refuel, then leave. If all pumps are busy, cars wait in a queue.

**Key Questions:**
- How many pumps should the station have?
- What's the trade-off between pump costs and customer wait times?
- How does utilization change with different numbers of pumps?

## M/M/c Queue

This is an **M/M/c** queue:
- **First M:** Markovian (exponential) arrivals
- **Second M:** Markovian (exponential) service times
- **c:** Number of servers (pumps)

When c > 1, we have **parallel servers** serving from a single queue.

## Building the Simulation

### Complete Code

```python
import simpy
import random
import matplotlib.pyplot as plt

# Data collection
wait_times = []
system_times = []
queue_lengths = []

def car(env, name, gas_station, fuel_time_mean):
    """A car arrives, waits for pump, refuels, and leaves."""
    
    arrival_time = env.now
    print(f"{env.now:.2f}: {name} arrives")
    
    # Record queue length at arrival
    queue_lengths.append(len(gas_station.queue))
    
    # Request a pump
    with gas_station.request() as request:
        yield request
        
        # Record wait time
        wait_time = env.now - arrival_time
        wait_times.append(wait_time)
        
        if wait_time > 0:
            print(f"{env.now:.2f}: {name} starts refueling (waited {wait_time:.2f} min)")
        else:
            print(f"{env.now:.2f}: {name} starts refueling (no wait)")
        
        # Refuel (exponential service time)
        fuel_time = random.expovariate(1.0 / fuel_time_mean)
        yield env.timeout(fuel_time)
        
        # Record total system time
        system_time = env.now - arrival_time
        system_times.append(system_time)
        
        print(f"{env.now:.2f}: {name} finishes and leaves")

def car_generator(env, gas_station, arrival_rate, fuel_time_mean):
    """Generate cars arriving at the station."""
    
    car_number = 0
    while True:
        # Wait for next car
        yield env.timeout(random.expovariate(arrival_rate))
        
        car_number += 1
        env.process(car(env, f"Car {car_number}", gas_station, fuel_time_mean))

def run_simulation(num_pumps, sim_time, arrival_rate, fuel_time_mean, random_seed=42):
    """Run a single simulation and return statistics."""
    
    # Reset data collection
    global wait_times, system_times, queue_lengths
    wait_times = []
    system_times = []
    queue_lengths = []
    
    # Setup
    random.seed(random_seed)
    env = simpy.Environment()
    gas_station = simpy.Resource(env, capacity=num_pumps)
    
    # Start generator
    env.process(car_generator(env, gas_station, arrival_rate, fuel_time_mean))
    
    # Run
    env.run(until=sim_time)
    
    # Return statistics
    return {
        'num_pumps': num_pumps,
        'total_cars': len(wait_times),
        'avg_wait': sum(wait_times) / len(wait_times) if wait_times else 0,
        'max_wait': max(wait_times) if wait_times else 0,
        'avg_system_time': sum(system_times) / len(system_times) if system_times else 0,
        'avg_queue_length': sum(queue_lengths) / len(queue_lengths) if queue_lengths else 0,
        'max_queue_length': max(queue_lengths) if queue_lengths else 0,
        'pct_waited': 100 * sum(1 for w in wait_times if w > 0) / len(wait_times) if wait_times else 0
    }

# Simulation parameters
SIM_TIME = 500        # Minutes
ARRIVAL_RATE = 0.4    # Cars per minute (1 every 2.5 minutes)
FUEL_TIME = 5.0       # Average refueling time (minutes)

# Run with different numbers of pumps
print("="*70)
print("PETROL STATION SIMULATION")
print("="*70)

results = []
for num_pumps in range(1, 6):
    stats = run_simulation(num_pumps, SIM_TIME, ARRIVAL_RATE, FUEL_TIME)
    results.append(stats)
    
    print(f"\n{num_pumps} Pump(s):")
    print(f"  Cars served: {stats['total_cars']}")
    print(f"  Average wait: {stats['avg_wait']:.2f} min")
    print(f"  Maximum wait: {stats['max_wait']:.2f} min")
    print(f"  Average queue length: {stats['avg_queue_length']:.2f} cars")
    print(f"  Cars that waited: {stats['pct_waited']:.1f}%")
```

## Analyzing Results

### Visualizing Performance vs Capacity

```python
# Extract data for plotting
pump_counts = [r['num_pumps'] for r in results]
avg_waits = [r['avg_wait'] for r in results]
avg_queues = [r['avg_queue_length'] for r in results]
pct_waited = [r['pct_waited'] for r in results]

# Create visualizations
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Plot 1: Average wait time
axes[0, 0].plot(pump_counts, avg_waits, marker='o', linewidth=2, markersize=8)
axes[0, 0].set_xlabel('Number of Pumps')
axes[0, 0].set_ylabel('Average Wait Time (min)')
axes[0, 0].set_title('Wait Time vs Number of Pumps')
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Average queue length
axes[0, 1].plot(pump_counts, avg_queues, marker='s', linewidth=2, markersize=8, color='orange')
axes[0, 1].set_xlabel('Number of Pumps')
axes[0, 1].set_ylabel('Average Queue Length (cars)')
axes[0, 1].set_title('Queue Length vs Number of Pumps')
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Percentage who waited
axes[1, 0].bar(pump_counts, pct_waited, color='green', alpha=0.7)
axes[1, 0].set_xlabel('Number of Pumps')
axes[1, 0].set_ylabel('% of Cars That Waited')
axes[1, 0].set_title('Percentage of Cars That Waited')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Plot 4: Utilization
lambda_rate = ARRIVAL_RATE
mu_rate = 1 / FUEL_TIME
utilizations = [100 * lambda_rate / (num_pumps * mu_rate) for num_pumps in pump_counts]

axes[1, 1].plot(pump_counts, utilizations, marker='^', linewidth=2, markersize=8, color='red')
axes[1, 1].axhline(y=100, color='black', linestyle='--', label='100% (unstable)')
axes[1, 1].set_xlabel('Number of Pumps')
axes[1, 1].set_ylabel('Utilization (%)')
axes[1, 1].set_title('System Utilization')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

## Understanding the Results

### System Utilization

**Utilization (ρ)** measures how busy the system is:

ρ = λ / (c × μ)

Where:
- λ = arrival rate (cars/minute)
- c = number of servers (pumps)
- μ = service rate (1/average service time)

In our example:
- λ = 0.4 cars/min
- μ = 1/5 = 0.2 cars/min per pump

| Pumps | Utilization | Status |
|-------|-------------|--------|
| 1     | 200%        | Unstable! Queue grows forever |
| 2     | 100%        | Critical - right at limit |
| 3     | 67%         | Stable |
| 4     | 50%         | Stable, low utilization |
| 5     | 40%         | Stable, very low utilization |

### Diminishing Returns

Notice how adding pumps helps, but with diminishing returns:

- **1 → 2 pumps:** Huge improvement (system becomes stable)
- **2 → 3 pumps:** Significant improvement
- **3 → 4 pumps:** Moderate improvement
- **4 → 5 pumps:** Small improvement

**Question:** Is the 5th pump worth the cost?

## Cost-Benefit Analysis

Let's add costs to understand the optimal number of pumps.

```python
def calculate_daily_cost(num_pumps, avg_wait_time, total_cars):
    """Calculate total daily operating cost."""
    
    # Pump costs
    pump_lease_cost = 50  # $ per pump per day
    pump_maintenance = 20  # $ per pump per day
    total_pump_cost = num_pumps * (pump_lease_cost + pump_maintenance)
    
    # Customer wait time cost (lost goodwill, future business)
    wait_cost_per_minute = 0.50  # $ value per minute of customer wait
    total_wait_cost = total_cars * avg_wait_time * wait_cost_per_minute
    
    # Total cost
    total_cost = total_pump_cost + total_wait_cost
    
    return {
        'pump_cost': total_pump_cost,
        'wait_cost': total_wait_cost,
        'total_cost': total_cost
    }

# Calculate costs for each configuration
print("\n" + "="*70)
print("COST ANALYSIS")
print("="*70)

for stats in results:
    # Scale to full day (24 hours = 1440 minutes)
    daily_cars = stats['total_cars'] * (1440 / SIM_TIME)
    
    costs = calculate_daily_cost(
        stats['num_pumps'],
        stats['avg_wait'],
        daily_cars
    )
    
    print(f"\n{stats['num_pumps']} Pump(s):")
    print(f"  Pump costs: ${costs['pump_cost']:.2f}/day")
    print(f"  Wait costs: ${costs['wait_cost']:.2f}/day")
    print(f"  TOTAL COST: ${costs['total_cost']:.2f}/day")
```

### Visualizing Cost Trade-offs

```python
# Prepare cost data
pump_costs = []
wait_costs = []
total_costs = []

for stats in results:
    daily_cars = stats['total_cars'] * (1440 / SIM_TIME)
    costs = calculate_daily_cost(stats['num_pumps'], stats['avg_wait'], daily_cars)
    pump_costs.append(costs['pump_cost'])
    wait_costs.append(costs['wait_cost'])
    total_costs.append(costs['total_cost'])

# Plot cost breakdown
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Stacked bar chart
ax1.bar(pump_counts, pump_costs, label='Pump Costs', alpha=0.8)
ax1.bar(pump_counts, wait_costs, bottom=pump_costs, label='Wait Costs', alpha=0.8)
ax1.set_xlabel('Number of Pumps')
ax1.set_ylabel('Daily Cost ($)')
ax1.set_title('Cost Breakdown by Number of Pumps')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Total cost curve
ax2.plot(pump_counts, total_costs, marker='o', linewidth=2, markersize=10, color='purple')
optimal_idx = total_costs.index(min(total_costs))
ax2.plot(pump_counts[optimal_idx], total_costs[optimal_idx], 
         marker='*', markersize=20, color='gold', 
         label=f'Optimal: {pump_counts[optimal_idx]} pumps')
ax2.set_xlabel('Number of Pumps')
ax2.set_ylabel('Total Daily Cost ($)')
ax2.set_title('Total Cost vs Number of Pumps')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"\nOptimal configuration: {pump_counts[optimal_idx]} pumps")
print(f"Minimum daily cost: ${min(total_costs):.2f}")
```

## Key Insights

### The Optimization Problem

This is a classic **capacity planning** problem:
- **Too few pumps:** High wait costs (unhappy customers)
- **Too many pumps:** High capital/operating costs (wasted capacity)
- **Goal:** Find the sweet spot that minimizes total cost

### Parallel Servers vs Single Server

**Single fast server vs Multiple slower servers:**
- Multiple servers provide **redundancy** (one can break, others still work)
- Multiple servers **reduce variability** in wait times
- But multiple servers have **higher capital costs**

### Real-World Extensions

In practice, you'd also consider:
- **Peak vs off-peak hours** (time-varying arrival rates)
- **Different customer types** (cars vs trucks need different service times)
- **Service level agreements** ("95% of customers wait <5 minutes")
- **Space constraints** (physical room for pumps)
- **Revenue considerations** (lost sales if customers leave due to long waits)

## Experimentation

### Try These Variations

1. **Higher arrival rate (0.6 cars/min)**
   - What happens to the optimal number of pumps?
   - At what point does the system become unstable?

2. **Variability in service times**
   - What if some cars take much longer? (Use `random.uniform(3, 8)`)
   - How does this affect wait times?

3. **Customer abandonment**
   - What if customers leave if queue is >3 cars?
   - How much revenue is lost?

4. **Time-varying arrivals**
   - More cars during morning/evening rush (6-9am, 4-7pm)
   - Should you staff differently during peaks?

## Key Takeaways

1. **Parallel servers** are modeled with `capacity=c` in SimPy
2. **Utilization must be <100%** for system stability: ρ = λ/(cμ) < 1
3. **Diminishing returns** - each additional server helps less
4. **Optimization** balances capacity costs vs waiting costs
5. **Cost models** turn simulation into business decisions

## Discussion Questions

1. What is the optimal number of pumps for this petrol station?
2. How would the optimal number change if wait costs doubled?
3. What if the station is open 24 hours but most traffic is during daytime?
4. How would you model a situation where some pumps are diesel-only?

---

**Next:** Segment 3 - Machines with Breakdowns (Interrupts)
