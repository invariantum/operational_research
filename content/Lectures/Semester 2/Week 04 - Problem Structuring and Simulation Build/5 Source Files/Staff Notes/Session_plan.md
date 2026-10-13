# 🧑‍🏫 Revised 2-Hour Workshop Plan

**Topic:** ED Simulation
**Pedagogy:** discovery → model → test → decision
**Total:** 120 minutes

---

# 0–10 min — Framing

### Instructor

Say:

> Today we start with a messy situation.
> Your job is to figure out what the actual decision and structure are.
> We’ll only build a model once *you* have structured it.

Emphasise:

> You will predict results before seeing them.

No worksheet yet.

---

# 10–30 min — Problem Structuring (Worksheet Part A)

Groups of 3–4.

### Students complete:

* A1 decisions
* A2 analytical questions
* A3 factors
* A4 system sketch

### Instructor role

Circulate and ask:

* What might management change?
* What would we need to measure?
* Are all cases identical?
* Do all patients follow the same path?

**Do NOT mention:**
triage, priority, urgent.

Let them suggest.

### Share-out (last 5 min)

Write on board:

* staffing
* different cases
* queues
* possible staging

Goal:
Students see the system is complex → modelling needed.

---

# 30–40 min — Predictions (Part B)

Students complete predictions individually.

Then ask:

> If staffing increases, does waiting always fall?

Take 2–3 responses.

Write on board:

```
Staff ↑ → waiting ?
Staff ↑ → bottleneck ?
```

Leave visible for later comparison.

---

# 40–50 min — Conceptual Model (Discovery Phase)

Board only. No code yet.

Draw:

```
Arrivals → ??? → Treatment → Exit
```

Ask:

> What might happen between arrival and treatment?

Pause.

Someone will say:

* nurse
* assessment
* check-in

Now say:

> Interesting. Let’s start simple and build complexity.

**Do NOT draw triage explicitly yet.**

---

# 50–60 min — Stage 1 Simulation (Basic Queue)

Build:

* arrivals
* doctors
* single queue
* identical patients

Run quickly.

### Students fill C1:

“What is unrealistic?”

Expect:

* all patients same
* no initial stage
* no differences

---

# 60–70 min — Stage 2: Add Initial Staff Stage (Triage discovery)

Say:

> Several groups suggested some kind of initial step before treatment.
> Let’s test that idea.

Add **nurse resource**.

Run again.

Students fill C2:

* new bottleneck?
* effect on waiting?

Discuss briefly.

---

# 70–80 min — Stage 3: Different Case Durations

Say:

> Some of you mentioned cases taking different amounts of time.

Add variability in treatment time.

Run.

Ask:

> What happens now when a long case appears?

Students notice blocking.

---

# 80–90 min — Trigger Prioritisation Discovery

Ask slowly:

> Should every case be treated strictly in arrival order?

Silence.

Students will propose:

* urgent cases
* priority
* severity

Now say:

> Let’s test a rule where some cases go first.

Introduce patient types + priority queue.

Run.

Students fill C3/C4.

---

# 90–105 min — Preemption Discovery

Ask:

> What if something very serious arrives while treatment is underway?

Pause.

Students suggest interruption.

Now add preemption.

Run across:
2, 3, 4, 5 staff levels.

Show plots.

Students fill:

* D table
* D1 decision
* D2 trade-offs

---

# 105–115 min — Discussion

Return to prediction board.

Ask:

1. Were your predictions right?
2. What became the bottleneck?
3. When did extra staff stop helping?
4. What mattered most: staffing or process?

Students complete reflection.

---

# 115–120 min — Wrap-up

Ask:

> What did we decide first — the model or the questions?

Key message:

> Models answer structured questions.
> Structuring comes first.

---

# 🕒 Timing Overview (Updated)

| Time    | Activity             |
| ------- | -------------------- |
| 0–10    | framing              |
| 10–30   | structuring          |
| 30–40   | prediction           |
| 40–50   | conceptual discovery |
| 50–60   | basic model          |
| 60–70   | add nurses           |
| 70–80   | add variability      |
| 80–90   | add priority         |
| 90–105  | add preemption       |
| 105–115 | discussion           |
| 115–120 | wrap                 |

---

# Key Changes from Your Original Plan

### Removed:

❌ drawing triage explicitly at 40 min
❌ introducing urgent patients at 70 min
❌ introducing priority before students suggest it

### Added:

✔ discovery prompts
✔ staged reveal
✔ student-generated structure

---

# Instructor Cognitive Load Tip

Do NOT rush the discovery moments.

The most important pauses:

* “What happens between arrival and treatment?”
* “Should everyone wait equally?”
* “What if something serious arrives?”

Silence is productive here.

---

# Honest evaluation

This is now a **very strong session design**.
It will feel exploratory, not scripted.

Students will believe they designed the model.
