# Semester 2 · Week 03 – Discrete Event Simulation with SimPy

Discrete-event simulation with SimPy: the M/M/1 queue, a petrol station with several pumps and costs, and machine breakdowns.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `3 Tutorial` | Tutorial / practical sheet and any starter files | The practical |
| `4 Tutorial Answers` | Worked answers and answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |
| `6 Further Reading` | Papers and external material | Optional reading |

## 1 Lecture

- `Notes/1 Intro to SimPy and the M-M-1 queue.md`
- `Notes/2 Petrol station (M-M-c) and costs.md`
- `Notes/3 Machine breakdowns (pre-emption).md`
- `Notes/M-M-1 queue - three snapshots.md`
- `Simpy Basics.pdf`

## 2 Lecture Demos

- `1 Intro to SimPy and the M-M-1 queue.ipynb` (notebook)
- `2 Petrol station (M-M-c) and costs.ipynb` (notebook)
- `3 Machine breakdowns (pre-emption).ipynb` (notebook)
- `4 Machine breakdowns - full demo.ipynb` (notebook)

## 3 Tutorial

- `Practical - M-M-1 Queue.ipynb` (notebook)
- `Practical - M-M-1 Queue.pdf`
- `Tutorial Questions.pdf`

## 4 Tutorial Answers

- `Q1 Bank teller.ipynb` (notebook)
- `Q2 Supermarket checkout.ipynb` (notebook)
- `Q3 Call centre.ipynb` (notebook)
- `Q4 CNC machine.ipynb` (notebook)
- `Q5 Hospital emergency department.ipynb` (notebook)

## 6 Further Reading

- `Useful links.txt`

## Notes for staff

- The three segment notebooks are the ones last year's `TODO.txt` asked for; they are built from the segment notes.
- Session timings are in `5 Source Files/Staff Notes/Session Outline.md`.
- `5 Source Files/Python/segment_3_demo.py` was fixed: a breakdown can interrupt maintenance, which crashed the original at t = 402.64 with the fixed seed. The maintenance step now catches `simpy.Interrupt`.
- `Notes/3 Machine breakdowns (pre-emption).md` gained a missing `import numpy as np` in one code block.
- `1 Lecture/Simpy Basics.pdf` was exported from the `.pptx` (2 slides; slide 1 is blank and slide 2's animation shows in its final state).
- Q3 and Q5 answer notebooks: a `;` was added after the last plot command so the cell no longer prints `(0.0, 105.0)`.
