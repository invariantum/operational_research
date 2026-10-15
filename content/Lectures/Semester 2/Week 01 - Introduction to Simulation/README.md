# Semester 2 · Week 01 – Introduction to Simulation

Why and how we simulate: coins and dice, a heated clothes rack, election forecasting, and queues worked by hand.

**Open first:** `1 Lecture/Introduction to Simulation.pdf`, then the demos in `2 Lecture Demos` in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides and the example handout (PDF) | The lecture |
| `2 Lecture Demos` | Notebooks and workbooks shown in the lecture, numbered in teaching order | Run live in the lecture |
| `3 Tutorial` | Tutorial sheet and the Excel layouts to copy | The practical |
| `4 Tutorial Answers` | Worked answers | **After the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx) and the original MATLAB scripts | Staff only |

## 1 Lecture

| File | What it is |
| --- | --- |
| `Introduction to Simulation.pdf` | Main slides: why simulate, coins and dice, queueing terms, the doctor's waiting room by hand (pp29–35), the "simple example" with lookup tables (pp36–38) |
| `Example Simulation.pdf` | One-page handout for the simple example: 30 customers drawn from tables |
| `Production Distribution Model.pdf` | Optional: a minimum-cost-flow model (with the lecturer's handwritten notes); goes with demo 6 |

## 2 Lecture Demos

| File | What it shows | Runs in |
| --- | --- | --- |
| `1 Coin toss simulation.ipynb` | Running percentage of heads settles at `p_heads` (law of large numbers) | Browser |
| `2 Dice simulation.ipynb` | Each face of a die tends to 1/6 | Browser |
| `3 Coin and dice simulations in Excel.xlsx` | The same experiments in Excel (slides pp12–14) | Excel (press F9) |
| `4 Heated clothes rack in Excel.xlsx` | Cost comparison of a heated rack and the heating (slide p10) | Excel |
| `5 Election simulation.ipynb` | Optional: Monte Carlo of a US election from polling margins | Browser |
| `6 Production-distribution (minimum-cost flow).ipynb` | Optional: the production-distribution LP in Pyomo; optimum £533,930 | Browser |

## 3 Tutorial

- `Tutorial - Introduction to Simulation.pdf`: Q1 by hand, Q2–Q3 in Excel, Q4 in Python.
- `Tutorial Example.xlsx`, `Tutorial Excel Sheets.xlsx`: worked layouts of the lookup-table method to copy.

## 4 Tutorial Answers

| File | Answers |
| --- | --- |
| `Tutorial - Introduction to Simulation - Answers.pdf` | Q1 (hand-worked table) |
| `Tutorial Answers.xlsx` | Q2 and Q3 in Excel |
| `Tutorial example answer.png` | Picture of a finished Excel layout |
| `Tutorial Q2-Q4 in Python.ipynb` | Q2–Q4 in Python, following the Excel formulas column by column (added for this site) |

## Notebooks and the original scripts

The original MATLAB scripts are kept unchanged in `5 Source Files/MATLAB`. The notebooks are Python versions:

| Notebook | MATLAB original | Differences |
| --- | --- | --- |
| 1 Coin toss | `unfair_coin_toss.m` | Percentages are plotted as 0–100 (MATLAB plotted 0–1 under a "Percentage" label); NumPy's random numbers differ from MATLAB's |
| 2 Dice | `dice.m` | Same experiment; different random numbers |
| 5 Election | `election_simulation.m` | Adds a fixed seed and a "Democrats win x%" line; state names stored as a list (see errata) |
| 6 Production-distribution | `production_distribution_model.m` | Pyomo + HiGHS instead of MATLAB's `optimproblem`; same optimum |

To run the MATLAB files: `dice.m` and `unfair_coin_toss.m` run in MATLAB or GNU Octave. `election_simulation.m` needs
`normrnd` (MATLAB Statistics Toolbox, or Octave with `pkg load statistics`). `production_distribution_model.m` needs the
MATLAB Optimization Toolbox; it does not run in Octave.

## Errata

| Where | Error | Correct | Status |
| --- | --- | --- | --- |
| *Introduction to Simulation* PDF p37 (`.pptx` slide 39), cumulative band for inter-arrival time 12 | 0.2–0.4 | **0.2–0.6** | Fixed in the `.pptx`; the PDF keeps the typo |
| `Tutorial Answers.xlsx`, sheet Q2, cell B10 (expected inter-arrival time) | 12.5 (only 4 of the 6 values were summed) | **15.15** minutes (utilisation 14.5 / 15.15 = 0.957) | Fixed |
| `election_simulation.m` | `states = [ … ]` joins the names into one 442-character string (unused); "Deleware"; `ones(no_trials)` draws 500 identical lines | `{ … }`; `ones(1, no_trials)` | Kept as the original; the notebook is correct |
| `election_simulation.m` line 3, source of the polling margins | projects.fivethirtyeight.com/polls/president-general/ | The page now redirects to ABC News, so the 2020 margins can no longer be checked against it | Note only |
| `Tutorial Excel Sheets.xlsx`, sheet *Uniform Arrivals and Service* | `INT(RAND()*(max−min)+min)` never reaches max; with max = 1 every service time is 0 | Use `RANDBETWEEN(min, max)` for whole numbers | Note only (demo sheet) |

## Notes for staff

- The tutorial sheet, the example handout and the production-distribution deck had no PDF; the PDFs were exported from the originals. The production-distribution PDF was exported so that the handwritten notes show.
- The production-distribution example is a minimum-cost flow problem; it also serves Semester 1 Week 08 (transhipment).
