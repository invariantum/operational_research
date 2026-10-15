# Semester 2 · Week 01 – Introduction to Simulation

Why and how we simulate: coins, dice, a heated clothes rack, election forecasting, and queues by hand.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `3 Tutorial` | Tutorial / practical sheet and any starter files | The practical |
| `4 Tutorial Answers` | Worked answers and answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |

## 1 Lecture

- `Example Simulation.pdf`
- `Introduction to Simulation.pdf`
- `Production Distribution Model.pdf`

## 2 Lecture Demos

- `1 Coin toss simulation.ipynb` (notebook)
- `2 Dice simulation.ipynb` (notebook)
- `3 Coin and dice simulations in Excel.xlsx`
- `4 Heated clothes rack in Excel.xlsx`
- `5 Election simulation.ipynb` (notebook)
- `6 Production-distribution (minimum-cost flow).ipynb` (notebook)

## 3 Tutorial

- `Tutorial - Introduction to Simulation.pdf`
- `Tutorial Example.xlsx`
- `Tutorial Excel Sheets.xlsx`

## 4 Tutorial Answers

- `Tutorial - Introduction to Simulation - Answers.pdf`
- `Tutorial Answers.xlsx`
- `Tutorial example answer.png`

## Notes for staff

- The notebooks are Python versions of last year's MATLAB demos (kept in `5 Source Files/MATLAB`).
- The tutorial sheet, the example handout and the production-distribution deck had no PDF; PDFs were exported from the originals.
- The production-distribution deck has handwritten (ink) notes on 9 of its 11 slides. The first PDF export dropped them; `1 Lecture/Production Distribution Model.pdf` was re-exported so the handwriting shows. The `.pptx` in `5 Source Files` stays as the editable original.
- The production-distribution example is a minimum-cost flow problem and also serves Semester 1 Week 8 (transhipment).
- Coin toss notebook: the plot shows percentages (0-100); the MATLAB version plotted fractions (0-1) under a "Percentage" label.
- Election notebook: it adds a "Democrats win x% of simulations" line and a fixed seed (the MATLAB version was unseeded). The NumPy and MATLAB random streams differ, so seeded numbers will not match MATLAB's.
