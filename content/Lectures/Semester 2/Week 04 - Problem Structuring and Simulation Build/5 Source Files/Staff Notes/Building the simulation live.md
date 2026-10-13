# 🧑‍🏫 Instructor Live-Build Version

You will build the model in **6 stages**.

Each stage runs and produces output.

Students see how modelling choices affect results.

---

# ⏱ Suggested pacing (Year 2)

| Stage | Time |
| ----- | ---- |

1. Basic queue | 10 min |
2. Add triage | 10 min |
3. Add patient types | 10 min |
4. Add priority | 10 min |
5. Add preemption | 15 min |
6. Add experiments | 15 min |

---

# Stage 1 — Basic ED (single queue)

**Goal:** show baseline queue behaviour.

No triage.
No priority.

```python
import simpy
import random

SIM_TIME = 12 * 60

def patient(env, doctors):
    arrival = env.now

    with doctors.request() as req:
        yield req
        wait = env.now - arrival
        service = random.expovariate(1/25)
        yield env.timeout(service)

def arrivals(env, doctors):
    while True:
        yield env.timeout(random.expovariate(4/60))
        env.process(patient(env, doctors))

env = simpy.Environment()
doctors = simpy.Resource(env, capacity=2)

env.process(arrivals(env, doctors))
env.run(until=SIM_TIME)
```

Ask students:

> What assumptions are unrealistic?

They will say:

* no triage
* all patients same
* no urgency

Perfect.

---

# Stage 2 — Add triage

Explain:

> ED is not one queue.
> Patients are filtered first.

Add triage resource.

```python
triage = simpy.Resource(env, capacity=1)
```

Modify patient:

```python
def patient(env, triage, doctors):

    with triage.request() as req:
        yield req
        yield env.timeout(random.uniform(4,8))

    with doctors.request() as req:
        yield req
        yield env.timeout(random.expovariate(1/25))
```

Ask:

> What is the bottleneck now?

Run with 1 triage nurse.

Students see:
triage utilisation high.

---

# Stage 3 — Add patient types

Now introduce:

* critical
* urgent
* standard

```python
def sample_type():
    r = random.random()
    if r < 0.1:
        return "critical"
    elif r < 0.4:
        return "urgent"
    return "standard"
```

Service times:

```python
SERVICE = {
    "critical": 40,
    "urgent": 30,
    "standard": 20
}
```

Modify patient:

```python
ptype = sample_type()
service = random.expovariate(1/SERVICE[ptype])
```

Ask:

> Should they all wait in same queue?

Students: no.

---

# Stage 4 — Add priority queue

Replace:

```python
doctors = simpy.Resource(...)
```

with:

```python
doctors = simpy.PriorityResource(...)
```

Priority mapping:

```python
PRIORITY = {
    "critical": 0,
    "urgent": 1,
    "standard": 2
}
```

Request:

```python
with doctors.request(priority=PRIORITY[ptype]) as req:
```

Run.

Ask:

> What problem still exists?

Students notice:

* urgent waits behind standard already being treated

Perfect transition.

---

# Stage 5 — Add preemption (key moment)

Replace resource:

```python
doctors = simpy.PreemptiveResource(env, capacity=c)
```

Add resume logic:

```python
remaining = service

while remaining > 0:
    try:
        with doctors.request(priority=PRIORITY[ptype], preempt=True) as req:
            yield req
            start = env.now
            yield env.timeout(remaining)
            remaining = 0
    except simpy.Interrupt:
        served = env.now - start
        remaining -= served
```

Explain visually on board:

Doctor treating standard
→ critical arrives
→ interrupt
→ resume later

This is the moment the model feels real.

Students love this bit.

---

# Stage 6 — Add experiments

Now wrap simulation:

```python
for d in [2,3,4,5]:
    run_sim(d)
```

Plot:

* wait times
* utilisation
* cost

Ask:

> How many doctors should we hire?

Now it's an OR decision problem.

---

# Teaching script (what you say)

At each stage ask:

### After Stage 1

> What’s unrealistic?

### After Stage 2

> Where is congestion?

### After Stage 3

> Should all patients be equal?

### After Stage 4

> Is priority enough?

### After Stage 5

> What policy decisions exist?

### After Stage 6

> What is optimal staffing?

---

# Why this works

Students see:

* modelling is iterative
* realism added deliberately
* simulation answers policy questions
* complexity grows logically

Not magic.

---

