# Semester 2 · Week 04 – Problem Structuring and Simulation Build

Soft OR and problem structuring on a messy emergency-department (ED) case, then building and testing a simulation of it.

**Open first:** `1 Lecture/Problem Structuring and Modelling - Emergency Department - slides 1-8 (Soft OR introduction).pdf`, then `… Emergency Department.pdf`.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) | The workshop |
| `2 Lecture Demos` | The ED simulation, built in stages and as the full model | The live build |
| `3 Tutorial` | Problem-structuring worksheet | The workshop |
| `4 Tutorial Answers` | Possible answers to the worksheet | **After the workshop** |
| `5 Source Files` | Editable originals, the original script, staff notes, an earlier draft | Staff only |

## 1 Lecture

| File | What it is |
| --- | --- |
| `… - slides 1-8 (Soft OR introduction).pdf` | Show first: what soft OR and problem structuring are |
| `Problem Structuring and Modelling - Emergency Department.pdf` | The ED case and the modelling steps (slides 1–2, 9–13, 15–27; slide 14 is a blank whiteboard) |
| `… (annotated).pdf` | The same deck as written on in class |
| `GORS - Intro to Soft OR and Problem Structuring Exercise.pdf` | An alternative session from the Government OR Service |

## 2 Lecture Demos

| Notebook | What it shows |
| --- | --- |
| `1 Building the ED simulation in stages.ipynb` | The live build: one queue → triage → patient types → priority → pre-emption → experiments, with the question to ask at each stage (added for this site, from the staff notes) |
| `2 Emergency department simulation (full model).ipynb` | The finished model: triage, three priorities with pre-emption, arrivals that vary by time of day, 2–5 doctors over 40 replications with 95% confidence intervals, and costs (corrected, see errata) |

## 3 Tutorial and 4 Tutorial Answers

- `3 Tutorial/Problem Structuring Worksheet.pdf`: Parts A–C.
- `4 Tutorial Answers/Problem Structuring Worksheet - Possible Answers.pdf`.

## Notebooks and the original script

`5 Source Files/Python/hospital_sim.py` is kept unchanged. The full-model notebook is the same code split into steps, with one correction (C10 below).

## Errata

| ID | Where | Error | Correct |
| --- | --- | --- | --- |
| C10 | `hospital_sim.py` / full model, doctor and triage utilisation | Busy time was added only when a patient was discharged, so treatment still in progress at the end of the shift was left out: 2 doctors 0.66, triage 0.35 | Counted as it happens: **0.72, 0.53, 0.40, 0.32** for 2–5 doctors; triage **0.41**. Waits and costs are unchanged. Waits are averaged over patients who were seen, so with 2 doctors (where some patients are still waiting at 12 h) the true waits are a little longer |

## Notes for staff

- A minute-by-minute session plan and the live-build script are in `5 Source Files/Staff Notes`. Notebook 1 follows the live-build script; its code fragments were assembled into runnable stages.
- The handbook lists *Agent Based Modelling* for this week; this folder holds the problem-structuring session.
- The Markdown worksheet in `5 Source Files/Previous Versions` is an earlier draft whose questions differ from the PDF worksheet.
- `GORS … .pdf` and `Problem Structuring Worksheet.pdf` were exported from the `.pptx` / `.docx` in `5 Source Files`. Both ED PDFs predate the deck's last edit (26 Feb 2026); re-export them if the deck changes.
