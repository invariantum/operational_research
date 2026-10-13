# M/M/1 Queue: System Snapshots

## Snapshot 1: T = 5.8

```
EVENT QUEUE:
┌────────────────────────────┐
│ (6.5, customer_1)          │
│ (8.3, generator)           │
└────────────────────────────┘

SERVER QUEUE:
┌────────────────────────────┐
│ Customer 2                 │
│ Customer 3                 │
└────────────────────────────┘

SERVER: BUSY
┌────────────────────────────┐
│ Customer 1                 │
│ (finishing soon)           │
└────────────────────────────┘
```

---

## Snapshot 2: T = 6.5

```
EVENT QUEUE:
┌────────────────────────────┐
│ (8.3, generator)           │
│ (10.0, customer_2)         │
└────────────────────────────┘

SERVER QUEUE:
┌────────────────────────────┐
│ Customer 3                 │
└────────────────────────────┘

SERVER: BUSY
┌────────────────────────────┐
│ Customer 2                 │
│ (just started)             │
└────────────────────────────┘
```

**What changed from T=5.8:**
- Customer 1: Finished, left system
- Customer 2: Server Queue → Event Queue → Server
- Customer 3: Moved to front of Server Queue

---

## Snapshot 3: T = 8.3

```
EVENT QUEUE:
┌────────────────────────────┐
│ (10.0, customer_2)         │
│ (11.0, generator)          │
└────────────────────────────┘

SERVER QUEUE:
┌────────────────────────────┐
│ Customer 3                 │
│ Customer 4                 │
└────────────────────────────┘

SERVER: BUSY
┌────────────────────────────┐
│ Customer 2                 │
│ (50% done)                 │
└────────────────────────────┘
```

**What changed from T=6.5:**
- Customer 4: Arrived, entered Server Queue
- Customer 2: Still being served (halfway done)
- Customer 3: Still waiting in Server Queue
