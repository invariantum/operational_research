# Semester 2 · Week 03 – Discrete Event Simulation with SimPy

Discrete-event simulation with SimPy: the M/M/1 queue, a petrol station with several pumps and costs, and machine breakdowns (pre-emption).

**Open first:** `1 Lecture/Simpy Basics.pdf`, then `2 Lecture Demos/1 Intro to SimPy and the M-M-1 queue.ipynb`.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and a short note | The lecture |
| `2 Lecture Demos` | The lecture notes as runnable notebooks, in teaching order | The lecture |
| `3 Tutorial` | The M/M/1 practical (notebook and PDF) and the tutorial questions | The practical |
| `4 Tutorial Answers` | Answer notebooks Q1–Q5 | **After the practical** |
| `5 Source Files` | Original scripts and notes (unchanged), slides source, staff notes, an earlier draft | Staff only |
| `6 Further Reading` | Links | Optional |

## 1 Lecture

- `Simpy Basics.pdf`: the two SimPy slides (exported from the `.pptx`).
- `Notes/M-M-1 queue - three snapshots.md`: the event queue and server at three moments (open with *Markdown Preview*).

## 2 Lecture Demos (run in this order)

| Notebook | What it covers |
| --- | --- |
| `1 Intro to SimPy and the M-M-1 queue.ipynb` | Environment, processes, `timeout`, `Resource`; an M/M/1 bank; utilisation ρ |
| `2 Petrol station (M-M-c) and costs.ipynb` | Several pumps (M/M/c), queue length, pump vs waiting costs |
| `3 Machine breakdowns (pre-emption).ipynb` | `PreemptiveResource`, interrupts, MTBF/MTTR, total cost of ownership (corrected, see errata) |
| `4 Machine breakdowns - full demo.ipynb` | Optional: the complete breakdown script with maintenance, printed event by event (corrected) |

## 3 Tutorial

- `Practical - M-M-1 Queue.ipynb`: the in-lecture practical, written for this site. `Practical - M-M-1 Queue.pdf` is the original Colab handout (same exercise).
- `Tutorial Questions.pdf`: Q1–Q5. There is no starter notebook: *File → New → Notebook*, and make the first cell `%pip install simpy`.

## 4 Tutorial Answers

| Notebook | Question | Notes |
| --- | --- | --- |
| `Q1 Bank teller.ipynb` | M/M/1 at 15, 18, 20 customers/hour | Simulation vs M/M/1 formulas |
| `Q2 Supermarket checkout.ipynb` | M/M/c with costs, 2–6 lanes | Ends with a 200-replication check (errata) |
| `Q3 Call centre.ipynb` | Staffing for 80% answered within 2 minutes | Ends with a 200-replication check (errata) |
| `Q4 CNC machine.ipynb` | Breakdowns, profit by reliability | Corrected (errata) |
| `Q5 Hospital emergency department.ipynb` | Two patient types, priority and pre-emption | Corrected (errata) |

The answer notebooks save their 2 × 2 chart as a PNG (for example `Q1_Bank_Teller_Results.png`) next to the notebook. On the
site it is saved in your browser only; right-click it → *Download* to keep it.

## Notebooks and the original scripts

The original scripts and notes are kept **unchanged** in `5 Source Files/Python` and `5 Source Files/Notes (Markdown)`.
The notebooks split the scripts into steps with short explanations, draw each chart in a single cell (otherwise the browser
shows empty charts), and carry the corrections below.

| Notebook | Original | Corrections in the notebook |
| --- | --- | --- |
| Demos 1, 2 | `Notes (Markdown)/1 …`, `2 ….md` | None (the notes word for word, plus an install cell) |
| Demo 3 | `Notes (Markdown)/3 Machine breakdowns (pre-emption).md` | C2; adds the missing `import numpy as np` |
| Demo 4 | `Python/segment_3_demo.py` | C2; maintenance catches `simpy.Interrupt` (the original crashes at t = 402.64) |
| Practical | `Notes (Markdown)/Practical - M-M-1 Queue.md` | Steps 1–2 rewritten for this site instead of Colab |
| Q1–Q5 | `Python/Q1_Bank_Teller.py` … `Q5_Hospital_ED.py` | Q2: replications added (C5). Q3: replications added (C6). Q4: C2. Q5: C2 and C3 |

## Errata

| ID | Where | Error | Correct |
| --- | --- | --- | --- |
| C2 | Notes 3 and demo 3; `segment_3_demo.py` and demo 4; Q4; Q5 | A job (or patient) interrupted by a breakdown (or an urgent patient) goes on working *inside the same* `with request()` block. By then it has lost the resource, so it works during the repair, and two jobs can run at once on one machine | Request the resource again after each interrupt. This is the pattern the Week 04 model uses. Effects: demo 3's cheapest MTBF is **20 h** ($89,181), not 15 h ($53,804); in demo 4 with MTBF 20 h, the average completion time is **42.17 h**, not 13.04 h; in Q4 scenario E, **68 parts and £32,127**, not 69 and £32,623; Q5's printed results do not change for seed 42 |
| C3 | Q5, utilisation | Divided by 60 twice: 1.2%, 0.8%, 0.6%, 0.5% | **75.0%, 50.0%, 37.5%, 30.0%** for 2–5 doctors (load = 4/h × 22.5 min = 1.5 doctors) |
| C5 | Q2, "optimal number of lanes" | 4 lanes (£221.64), from one seeded run | **5 lanes** on average: £262.6 ± 1.8 vs £287.8 ± 7.6 for 4 lanes over 500 runs (the Erlang-C formula gives 264.6 vs 306.5) |
| C6 | Q3, minimum agents | 4 (normal) and 5 (peak), from one run | Erlang C: 3 and 4 agents give 80.7% and 80.8%, which just meets 80%. Over 500 runs they meet it on average (82.9%) but on only about 2 days in 3. 4 / 5 / 3 is the cautious schedule; 3 / 4 / 3 is the minimum on average |

## Notes for staff

- Session timings: `5 Source Files/Staff Notes/Session Outline.md`.
- The HTML exports of the notes were removed in an earlier review because they were renders of the Markdown notes. The exception is `5 Source Files/Previous Versions/3 Machine breakdowns (pre-emption) - earlier draft.html`, an earlier draft with a shorter cost analysis, which is kept.
- `1 Lecture/Simpy Basics.pdf` was exported from the `.pptx` (2 slides; slide 1 is blank, and slide 2's animation shows in its final state).
- `6 Further Reading/Useful links.txt` names three notebooks: they are demos 1–3 above. Its external link is the SimPy introduction by J. C. Kantor (Notre Dame CBE 30338): <https://jckantor.github.io/cbe30338-2021/07.01-Introduction-to-Simpy.html>.
