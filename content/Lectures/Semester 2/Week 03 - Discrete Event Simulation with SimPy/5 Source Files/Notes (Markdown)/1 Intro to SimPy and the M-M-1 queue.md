# Segment 1: Introduction to SimPy and Discrete-Event Simulation

## What is Discrete-Event Simulation?

**Discrete-Event Simulation (DES)** models systems where changes happen at specific points in time (events), not continuously.

**Examples:**
- Customers arriving at a bank (events: arrival, service start, service end)
- Patients in an emergency department (events: arrival, triage, treatment, discharge)
- Jobs on a production line (events: start processing, finish processing)

**Why use simulation?**
- Test "what-if" scenarios without disrupting real systems
- Understand complex systems with randomness
- Optimize operations (staffing, capacity, scheduling)
- Cheaper and safer than real-world experiments

---

## Part 1: A Complete Working Example

Let's start by seeing a complete SimPy simulation. Three customers arrive at a service center with two servers.

```python
import simpy

# 1. Create Environment
env = simpy.Environment()

# 2. Create Resource
server = simpy.Resource(env, capacity=2)

# 3. Define Process
def customer(env, name, server):
    print(f"{env.now}: {name} arrives")
    
    with server.request() as request:
        yield request
        print(f"{env.now}: {name} starts service")
        yield env.timeout(5)
        print(f"{env.now}: {name} finishes")

# 4. Create processes
env.process(customer(env, "Alice", server))
env.process(customer(env, "Bob", server))
env.process(customer(env, "Charlie", server))

# 5. Run simulation
env.run()
```

**Output:**
```
0: Alice arrives
0: Alice starts service
0: Bob arrives
0: Bob starts service
0: Charlie arrives
5: Alice finishes
5: Charlie starts service
5: Bob finishes
10: Charlie finishes
```

**What happened?**
- Alice and Bob got servers immediately (we have 2 servers)
- Charlie had to WAIT (both servers busy)
- When Alice finished, Charlie got the server
- This is queueing!

---

## Part 2: The Four Key Components

Every SimPy simulation has four parts:

### 1. Environment - The Clock

```python
env = simpy.Environment()
```

**What it does:**
- Keeps track of time (`env.now`)
- Runs the simulation

**Key commands:**
```python
env.now           # Check current time
env.run()         # Run until everything finishes
env.run(until=50) # Run for 50 time units
```

---

### 2. Resource - Things to Share

```python
server = simpy.Resource(env, capacity=2)
```

**What it is:**
- Something with limited capacity (servers, machines, parking spots)
- Processes compete for it
- If full, processes wait in a queue

**Key properties:**
```python
server.capacity        # How many can use it at once
server.count          # How many are using it now
len(server.queue)     # How many are waiting
```

---

### 3. Process - Things That Happen

```python
def customer(env, name, server):
    print(f"{env.now}: {name} arrives")
    
    with server.request() as request:
        yield request  # Wait for server
        yield env.timeout(5)  # Use server for 5 time units
```

**Key points:**
- Processes describe what entities DO (customers, jobs, vehicles)
- Must use `yield` to wait for things
- `yield request` = wait for resource
- `yield env.timeout(5)` = wait 5 time units

---

### 4. The Pattern - Request, Use, Release

```python
with server.request() as request:
    yield request              # WAIT for server
    # Now I have the server
    yield env.timeout(5)       # USE server
# Server automatically RELEASED here
```

This pattern is everywhere in SimPy:
1. Request the resource
2. Wait if it's busy (`yield request`)
3. Use it
4. Release it (automatic with `with`)

---

## Part 3: Building an M/M/1 Queue

Now let's build a realistic queueing system step by step.

### Step 1: One Customer

```python
import simpy

def customer(env, name, server):
    print(f"{env.now}: {name} arrives")
    with server.request() as request:
        yield request
        print(f"{env.now}: {name} starts service")
        yield env.timeout(5)
        print(f"{env.now}: {name} done")

env = simpy.Environment()
server = simpy.Resource(env, capacity=1)
env.process(customer(env, "Customer 1", server))
env.run()
```

**Output:**
```
0: Customer 1 arrives
0: Customer 1 starts service
5: Customer 1 done
```

Simple! One customer, no waiting.

---

### Step 2: Two Customers - See the Queue!

```python
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(customer(env, "Customer 1", server))
env.process(customer(env, "Customer 2", server))

env.run()
```

**Output:**
```
0: Customer 1 arrives
0: Customer 1 starts service
0: Customer 2 arrives
5: Customer 1 done
5: Customer 2 starts service
10: Customer 2 done
```

**Customer 2 waited!** The server was busy.

---

### Step 3: Random Arrivals

Real customers don't all arrive at once. They arrive randomly.

```python
import random

def customer_generator(env, server):
    """Generate customers arriving randomly"""
    customer_num = 0
    while True:
        # Random time until next customer
        yield env.timeout(random.expovariate(0.5))
        
        customer_num += 1
        env.process(customer(env, f"Customer {customer_num}", server))

# Setup
random.seed(42)
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)

env.process(customer_generator(env, server))
env.run(until=50)  # Run for 50 time units
```

Now customers arrive at random times throughout the simulation!

---

### Step 4: Random Service Times

```python
def customer(env, name, server):
    arrival = env.now
    print(f"{env.now:.1f}: {name} arrives")
    
    with server.request() as request:
        yield request
        
        wait = env.now - arrival
        print(f"{env.now:.1f}: {name} starts (waited {wait:.1f} min)")
        
        # Random service time
        service_time = random.expovariate(1.0 / 3.0)
        yield env.timeout(service_time)
```

Both arrivals AND service times are random - realistic!

---

## Part 4: Collecting Data

To analyze results, collect data during the simulation.

```python
# Global list to store wait times
wait_times = []

def customer(env, name, server):
    arrival = env.now
    
    with server.request() as request:
        yield request
        
        wait = env.now - arrival
        wait_times.append(wait)  # Save the wait time
        
        service_time = random.expovariate(1.0 / 3.0)
        yield env.timeout(service_time)

def customer_generator(env, server):
    customer_num = 0
    while True:
        yield env.timeout(random.expovariate(0.25))
        customer_num += 1
        env.process(customer(env, f"Customer {customer_num}", server))

# Run simulation
random.seed(42)
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)
env.process(customer_generator(env, server))
env.run(until=500)

# Analyze
print(f"Total customers: {len(wait_times)}")
print(f"Average wait: {sum(wait_times)/len(wait_times):.2f} minutes")
print(f"Max wait: {max(wait_times):.2f} minutes")
```

---

## Part 5: System Stability

**Critical concept:** Utilization (ρ) = Arrival Rate / Service Rate

```python
arrival_rate = 0.25      # 1 customer every 4 minutes
service_rate = 1.0 / 3.0 # 1 customer every 3 minutes

ρ = arrival_rate / service_rate  # 0.75
```

**If ρ < 1:** System is stable ✓
**If ρ ≥ 1:** Queue grows forever! System crashes ✗

**Try this:**
```python
arrival_rate = 0.4  # Faster arrivals
service_rate = 1.0 / 3.0

ρ = 0.4 / 0.333 = 1.2  # > 1, UNSTABLE!
```

Run the simulation and watch the queue explode!

---

## The Complete M/M/1 Example

Here's the full working code:

```python
import simpy
import random

wait_times = []

def customer(env, name, server, service_mean):
    arrival = env.now
    
    with server.request() as request:
        yield request
        wait_times.append(env.now - arrival)
        
        yield env.timeout(random.expovariate(1.0 / service_mean))

def customer_generator(env, server, arrival_rate, service_mean):
    customer_num = 0
    while True:
        yield env.timeout(random.expovariate(arrival_rate))
        customer_num += 1
        env.process(customer(env, f"Customer {customer_num}", server, service_mean))

# Parameters
ARRIVAL_RATE = 0.25
SERVICE_TIME = 3.0

# Run
random.seed(42)
env = simpy.Environment()
server = simpy.Resource(env, capacity=1)
env.process(customer_generator(env, server, ARRIVAL_RATE, SERVICE_TIME))
env.run(until=500)

# Results
print(f"Customers served: {len(wait_times)}")
print(f"Average wait: {sum(wait_times)/len(wait_times):.2f} min")
print(f"Utilization: {ARRIVAL_RATE / (1/SERVICE_TIME):.2f}")
```

---

## Key Takeaways

### The Four Essentials
1. **Environment** - `env = simpy.Environment()` - the clock
2. **Resource** - `simpy.Resource(env, capacity=n)` - limited capacity
3. **Process** - functions with `yield` - what entities do
4. **Pattern** - request → wait → use → release

### Critical Commands
```python
yield env.timeout(5)      # Wait 5 time units
yield server.request()    # Wait for resource
env.now                   # Current time
env.run(until=100)        # Run simulation
```

### The Request Pattern
```python
with server.request() as request:
    yield request         # Wait if busy
    yield env.timeout(5)  # Use it
# Automatically released
```

### Check Stability
```python
ρ = arrival_rate / service_rate
# Must have ρ < 1 for stable system
```

---

## Practice Exercise

Modify the M/M/1 code to:
1. Use 2 servers instead of 1
2. Compare average wait times
3. What happens to utilization?

**Hint:** Just change `capacity=1` to `capacity=2`

---
