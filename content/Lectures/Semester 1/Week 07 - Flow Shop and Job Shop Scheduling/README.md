# Semester 1 · Week 07 – Flow Shop and Job Shop Scheduling

Scheduling jobs on machines. In a *flow shop* every job visits the machines in the same order: Johnson's rule
finds the best order for two machines, and the Campbell, Dudek and Smith heuristic extends it to more. In a
*job shop* each job has its own machine order: it is written as a mixed-integer program with binary "which goes
first" variables and solved in Pyomo. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Flow shop slides (PDF); job shop notes as notebooks (`Notes`) and as a PDF | The lecture |
| `2 Lecture Demos` | Johnson's rule notebook and the Excel workbook used on the slides | Run live in the lecture |
| `3 Tutorial` | Flow shop tutorial sheet and job shop tutorial sheet | The practical |
| `4 Tutorial Answers` | Flow shop answers (PDF), flow shop Q4 notebook, job shop Q1–Q3 notebook | **Release after the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, HTML exports, older versions, a staff note on the answers | Staff only; edit here, then republish the PDF / notebook |
| `6 Further Reading` | Two introductions to constraint programming (Bockmayr and Reinert; Rodriguez-Carbonell) | Optional reading |

## Before you start

- **Weeks 05–06:** binary variables and "either/or" constraints with a big-M. The job shop model uses one binary
  variable per pair of operations to decide which goes first.
- **Maths:** sums and maxima, the number of orders of $n$ jobs ($n!$), reading a Gantt chart (one row per
  machine, time along the bottom).
- **Python:** lists, tuples, dictionaries and loops; a NumPy array and `np.argmin` (Johnson's rule notebook).
- **Pyomo:** a `ConcreteModel`, variables, an objective, `ConstraintList`, solved with
  `SolverFactory('appsi_highs')`. Each Pyomo notebook's first cell installs Pyomo and HiGHS; run it first.

## Work through this week in order

Page numbers are the pages of `1 Lecture/Week 7 - Flow Shop Scheduling.pdf`.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | Slides, pages 1–7 | One machine: makespan versus completion time; shortest processing time first (SPT) minimises the sum of completion times (proof) |
| 2 | Slides, pages 8–14 | The flow shop, makespan and idle time, $n!$ possible orders, Johnson's rule |
| 3 | `2 Lecture Demos/1 Johnsons rule.ipynb` | Johnson's rule in Python, on both slide examples |
| 4 | Slides, pages 15–20, with `2 Lecture Demos/2 Johnsons rule in Excel.xlsx` (sheets *Example 1/2*, *Makespan 1/2*, *Gantt 1/2*) | The worked examples: makespan 40 → 30 and 19 → 18; computing a makespan step by step |
| 5 | Slides, pages 21–24, with sheets *More than 2 stages* and *Gantt more than 2* | More than two machines: reduce to two (Campbell, Dudek and Smith), 52 → 46 |
| 6 | `3 Tutorial/Week 7 - Flow Shop Scheduling - Tutorial.pdf` | Flow shop Q1–Q4 |
| 7 | `4 Tutorial Answers/Week 7 - Flow Shop Scheduling - Tutorial - Answers.pdf`, the workbook's *Tutorial* and *Gantt 5 machines* sheets, `4 Tutorial Answers/Flow Shop Q4 MILP answers.ipynb` | Check your flow shop answers (Q4: the best orders found by a mixed-integer program) |
| 8 | `1 Lecture/Notes/Job Shop Scheduling Notes (Short).ipynb` (or the PDF `1 Lecture/Week 7 - Job Shop Scheduling Notes.pdf`) | The job shop problem, its MILP and the Pyomo model: $C_{\max} = 11$ |
| 9 | `3 Tutorial/Week 7 - Job Shop Scheduling Tutorial.pdf`, Q1–Q3 | Adapt the Pyomo code from the notes; it runs in the browser |
| 10 | `4 Tutorial Answers/Job Shop Q1-Q3 answers.ipynb` | Check your job shop answers: 12, 16, 18 |
| 11 | Job shop tutorial Q4–Q5 | N-queens and employee scheduling on the Google OR-Tools site, in Google Colab |
| 12 | *Optional:* `1 Lecture/Notes/Job Shop Scheduling Notes.ipynb`, `6 Further Reading` | Constraint programming and a cryptarithmetic puzzle |

Each notebook starts with the problem, how to run it and the expected result, explains every code cell, and ends
with a short *Try it* or *What do you notice?* question with a hidden answer.

In the browser, HiGHS prints its solver log even when the code does not ask for it; the results are not affected.

## By the end of this week you can

- explain makespan, completion time and idle time, and why shortest processing time first minimises the total
  completion time on one machine;
- apply Johnson's rule to a two-machine flow shop by hand, in Python and in Excel, and compute the makespan and
  idle times of any order;
- use Johnson's rule as a heuristic for more than two machines (Campbell, Dudek and Smith), and explain why its
  answer need not be optimal;
- write a job shop (or flow shop) as a mixed-integer program with big-M "which goes first" constraints and solve
  it in Pyomo;
- recognise problems with several optimal schedules, where your start times may differ from the answers while the
  makespan matches.

**Next:** Week 08 (Networks: shortest paths and minimum spanning trees). Big-M "either/or" constraints come back
in Week 11 (floor planning).

## Lecture demos and notes

| File | Slides | Shows | Result |
| --- | --- | --- | --- |
| `2 Lecture Demos/1 Johnsons rule` | 13–20 | Johnson's rule, recursive and iterative versions | `[0, 2, 1]` = P R Q (Example 2); `[2, 3, 4, 1, 0]` = R S T Q P (Example 1) |
| `2 Lecture Demos/2 Johnsons rule in Excel.xlsx` | 15–24 | Makespan tables and Gantt charts for every slide example | 40 → 30; 19 → 18; 52 → 46 (A and D, or A+B and C+D) or 48 (A+B+C and B+C+D) |
| `1 Lecture/Notes/Job Shop Scheduling Notes (Short)` | – | Job shop MILP in Pyomo, 3 jobs on 3 machines | $C_{\max} = 11$ |
| `1 Lecture/Notes/Job Shop Scheduling Notes` | – | The same, plus constraint programming and cryptarithmetic | $C_{\max} = 11$ |

Open the `.ipynb` notes to read and run them (each `.md` is the source of its notebook). *Short* is this year's
lecture version, the same as the PDF; the full notes add constraint programming and a cryptarithmetic example.

## Tutorial answers

| Question | Answer | Where |
| --- | --- | --- |
| Flow shop Q1 | R S P Q T: makespan 30, idle time 5 on A and 3 on B (total 8) | Answers PDF; workbook sheet *Tutorial* |
| Flow shop Q2 | T Q R S P or T P Q R S (P's times tie, so it can go early or late): makespan 74 | Answers PDF; *Tutorial* |
| Flow shop Q3 | Original order 75. Heuristics: machines A and E → R Q P T S, **66**; A+B / D+E and A+B+C / C+D+E → R T Q S P, 68. The optimum is **64** (e.g. R P T Q S) | Answers PDF; *Tutorial* and *Gantt 5 machines*; Q4 notebook |
| Flow shop Q4 | A mixed-integer program over job orders: 30, 74, 64 | `Flow Shop Q4 MILP answers.ipynb` |
| Job shop Q1–Q3 | Optimal makespans 12, 16, 18 | `Job Shop Q1-Q3 answers.ipynb` |
| Job shop Q4–Q5 | Reading exercises on the OR-Tools site (Colab) | No model answer |

## Notes for staff

- The `Week 7 - …` files are this year's versions. Last year's (2023-24) slides and notes are in `5 Source Files/Previous Versions`.
- Job shop answers were rewritten in Pyomo so they run in the browser. The old OR-Tools script did not run, and its Problem 1 data did not match the tutorial; the optimum for Q1 is **12** (Q2 = 16, Q3 = 18).
- Job shop tutorial Q1 printed J2's machine sequence as M1, M3, M2. M3 was a typo: the problem has three machines (M0–M2) and each job visits each machine once, so it is now M1, M0, M2 in the tutorial PDF, its `.md`/`.ipynb`/HTML sources and the answers. With the typo the optimum was 11; corrected, it is 12 (Oct 2026).
- Job shop tutorial Q4–Q5 are reading exercises on the Google OR-Tools website and need Google Colab.
- Renamed by content: `slides.pdf` -> `6 Further Reading/Introduction to Constraint Programming (Rodriguez-Carbonell, UPC).pdf`; the old "Flow Shop Scheduling (old slides annotated)" file that was really Bockmayr and Reinert's notes -> `6 Further Reading/Integer vs Constraint Programming (Bockmayr and Reinert).pdf`.
- A second copy of the flow shop tutorial PDF (identical bytes) was removed.
- The two job shop HTML exports had their notebook links updated to the new paths.
- The annotated flow shop slides in `Previous Versions` date from February 2021, hence "2020-21" in the name.
- The old OR-Tools answer script (`Previous Versions/jss_tutorial_answers_ortools …py`) was removed in Oct 2026: it did not run, had the wrong Q1 data and is replaced by the Pyomo answers.
- `1 Johnsons rule.ipynb` (Oct 2026): job numbers are converted with `int()`, so the browser prints `[0, 2, 1]` instead of `[np.int64(0), …]`; the orders are unchanged. Its header no longer mentions Pyomo (the notebook uses NumPy only).
- **Flow shop answers, Q3 (Oct 2026).** The sheet called 66 (R Q P T S, machines A and E) the "best known order".
  It is the best of the Campbell, Dudek and Smith orders, but checking all 5! = 120 orders gives **64** (e.g.
  R P T Q S; 63 if each machine may use a different order, which is no longer a flow shop). The A+B / D+E network
  processed the jobs as R T S Q P (72), while Johnson's rule gives R T Q S P (68). The `.docx` text now says this,
  and the workbook's *Tutorial* sheet (rows 63–82) was reordered to R T Q S P (68, values recalculated). **The
  picture of that network on page 5 of the answers still shows R T S Q P = 72** (it is an image):
  `5 Source Files/NOTE - Q3 network picture on page 5.txt` explains how to replace it from the corrected workbook,
  which sentence to shorten afterwards, and the numbers the new picture must show; then re-export the answers PDF.
  Delete the note when that is done. The answers also gained a Q4 answer (the new notebook), "74 for both orders" in Q2, and the
  title "Flow Shop Scheduling Tutorial – Answers" (it said "Semester 2 - Tutorial 1").
- **Slides (Oct 2026).** The `.pptx` in `5 Source Files` was corrected and the PDF re-exported from PowerPoint
  (17 Oct 2026) as `1 Lecture/Week 7 - Flow Shop Scheduling.pdf`, named like the other weeks' lecture PDFs (it was
  `… - Slides.pdf`). Changes (slide = PDF page): 13 "Everything else is NP-hard" (it said "in NP"); 11 "to complete all
  jobs"; 24 the sum $1 + 2 + \dots + (m-1)$ (a "+" was missing); 2 completion time defined as the time a job is
  finished; 3 "(total completion time)" (it said "Overall Processing Time"); 4 "of the same length"; 12
  "permutations?"; 22 "Campbell, Dudek and Smith". Slide 12 briefly also said "NP-Hard problems (in general, from 3
  machines on)", but the longer line wrapped and pushed the next line onto the box below; it was shortened back to
  "NP-Hard problems" on 17 Oct (slide 13 says when the problem is NP-hard). **Re-export the slides PDF from
  PowerPoint once more for this slide.**
- **Job shop notes (Oct 2026), `.md` and `.ipynb`.** Full notes: the integer programming example was unbounded
  (two of the three OR-Tools constraints were missing; now $2x + 7y + 3z \le 50$, $3x - 5y + 7z \le 45$,
  $5x + 2y - 6z \le 37$, optimum 35 at $(7, 3, 5)$); OR + IS + FUN = TRUE has **9** letters (it said 8); the solver
  is HiGHS (it said GLPK); CSP notation made consistent ($D_i$, $c_i$, $R_i$). Both notes: "Solving as a MILP", a
  note that the saved output is one of several optimal schedules, a note on the picture's 0-based numbering, and
  smaller wording fixes. The two unused images `eg_constraint.png` and `example_int_prog.png` (the second showed
  the unbounded example) were removed. The Short notes PDF was re-exported from its `.md` (17 Oct 2026; long code
  lines now wrap instead of being cut off), and again after the solver-list change below.
- **Notebooks (Oct 2026).** Every notebook gained an opening cell (problem, how to run it, expected result), an
  explanation above each code cell, comments on each constraint group and a closing *Try it* / *What do you
  notice?* cell with a hidden answer. In the notes notebooks these cells exist only in the `.ipynb` (not in the
  `.md`), and the dead `cdn.mathjax.org` script tags were dropped from the notebooks only. Wrong comments fixed in
  `1 Johnsons rule` ("if there are no more jobs to do, return the list" above a check that does not return).
  `Job Shop Q1-Q3 answers` (and its `.py`) rounds start times when printing, so the browser shows `0` instead of
  `8.12049e-14`; the model cell of both notes (notebook and `.md`) does the same, so it shows `0.00` instead of
  `-0.00` (17 Oct 2026). The `.md` notes now try `appsi_highs` first, like the notebooks, so the code in the `.md`
  and the PDF is the same as the code students run. No other code or printed result changed.
- **New (Oct 2026):** `4 Tutorial Answers/Flow Shop Q4 MILP answers.ipynb` answers flow shop Q4 with a
  permutation flow shop MILP (one binary per pair of jobs): 30, 74, 64. It has no `.py` source.
- **Job shop tutorial (Oct 2026), `.md`, `.ipynb` and HTML.** "Colaboratory" (it said "Collabatory", 3×), "check
  that it is indeed feasible and that it appears to be optimal", and a sentence saying Q1–Q3 can be done in the
  browser with the notes' Pyomo code. The tutorial PDF was re-exported from the `.md` (17 Oct 2026).
- **Flow shop tutorial (Oct 2026), `.docx`.** Q3: "a good exercise to try in Excel" (it said "on to try on
  Excel"). The PDF was re-exported from Word (17 Oct 2026).
- **MATLAB (Oct 2026).** `johnsons_rule_demo.m` commented out an alternative table with `#`, which MATLAB does
  not accept; it now uses `%`.
- **HTML exports** in `5 Source Files/HTML Exports`: the two notes exports were regenerated from the current
  `.md` files (17 Oct 2026); the tutorial export carries the fixes above. They load KaTeX's stylesheet from
  jsdelivr, so the maths displays correctly only when online.
