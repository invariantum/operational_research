# Semester 2: start here

Semester 2 is about **simulation**: building a model of a system that has randomness in it (a bank queue, an emergency
department, a machine that breaks down, a town of agents) and using it to answer "what if?" questions.

The path through the semester:

1. **Week 01:** simulation by hand and in Excel (coins, dice, a queue worked with a pencil).
2. **Week 02:** queueing theory. The M/M/1 formulas tell you what the simulations should give.
3. **Week 03:** discrete-event simulation in Python with SimPy, from one server to several servers, priorities and breakdowns.
4. **Week 04:** structuring a messy real problem (an ED), then building its simulation step by step.
5. **Week 05:** Coursework Part B is released.
6. **Week 06:** agent-based models with Mesa.
7. **Week 10:** revision for the in-class test.

Every notebook runs **in your web browser** on the course site. You install nothing.

---

## 1. Set up once (about 5 minutes)

1. Open the course site, <https://invariantum.github.io/operational_research/>, in a recent Chrome, Edge or Firefox.
2. In the file list on the left, double-click **`00_START_HERE.ipynb`**, then choose *Run → Run All Cells*. When every cell
   prints `OK`, your browser can run all the course notebooks. The first run downloads Python, so allow about a minute.
3. Come back to this guide: in the file list, open `Lectures`, then `Semester 2`, right-click `README.md` and choose *Open With → Markdown Preview*.

## 2. How to run a notebook

1. Double-click the `.ipynb` file. It opens with the **results already shown**: these are the verified answers.
2. Run the **first code cell** (click it, then press Shift+Enter). In notebooks that need extra packages (SimPy,
   Pyomo + HiGHS or Mesa), this cell starts with `# Run this cell first` and installs them; the first time takes up to
   half a minute. Notebooks that use only NumPy, pandas and Matplotlib need no install.
3. Then choose *Run → Run All Cells*, or run the cells one at a time with Shift+Enter while you read. Your numbers will match
   the saved ones, because the notebooks use a fixed random seed. Change the seed to see other runs.
4. **Save your work by downloading it.** Changes are kept only in this browser. Right-click the file → *Download*.

If something goes wrong, see *If something fails* at the end of `00_START_HERE.ipynb`.

### What opens where

| File | How to open it |
| --- | --- |
| `.ipynb` notebook | Double-click: it opens and runs in the browser |
| `.pdf` slides, sheets, answers | Double-click (if it doesn't open, right-click → *Download*) |
| `.md` notes and `README.md` files | Right-click → *Open With* → *Markdown Preview* |
| `.html` slides (Week 06) | Double-click; press *Trust HTML* for slide mode, or download and open it in your browser |
| `.xlsx` workbooks (Weeks 01, 02, 10) | Download, then open in Excel or LibreOffice Calc; press **F9** to re-run the random numbers |

## 3. How each week folder is organised

| Folder | What is in it | When to use it |
| --- | --- | --- |
| `1 Lecture` | Slides and notes | Before or during the lecture |
| `2 Lecture Demos` | Notebooks and workbooks from the lecture, **numbered in the order to use them** | During or after the lecture |
| `3 Tutorial` | The tutorial sheet and any template | The practical |
| `4 Tutorial Answers` | Worked answers | After you have tried the tutorial |
| `5 Source Files` | The original scripts (`Python/`, `MATLAB/`), editable slides and sheets, staff notes. You can ignore it | Staff, or to run on your own computer |
| `6 Further Reading` | Papers and links | Optional |

Each week's `README.md` lists every file, says what to open first, and has an **Errata** section for any corrected result.

**A good routine for each week:** slides → lecture demos in number order → tutorial sheet → answers.

---

## 4. Week by week: what to read and run, in order

| Week | You learn | 1. Read | 2. Run | 3. Practise, then check |
| --- | --- | --- | --- | --- |
| **01** Introduction to Simulation | Why simulate; random sampling; a queue by hand; lookup tables | `Introduction to Simulation.pdf`; `Example Simulation.pdf` | Demos `1 Coin toss`, `2 Dice`, then the Excel demos `3`, `4`. Optional: `5 Election`, `6 Production-distribution` (with `Production Distribution Model.pdf`) | Tutorial Q1 by hand, Q2–Q3 in Excel, Q4 in Python → `Tutorial Answers.xlsx`, `Tutorial Q2-Q4 in Python.ipynb` |
| **02** Queueing Theory | Exponential and Poisson; Little's law; Kendall notation; M/M/1 formulas | `Introduction to Queueing Theory.pdf`; optional `M-M-1 queue derivation.pdf` | `1 M-M-1 lecture example.xlsx`, `2 Queueing examples in Python.ipynb` | Tutorial Q1–Q3 in `Tutorial Template.xlsx`, Q4 in Python → `Tutorial Answers.xlsx`, `Tutorial answers in Python.ipynb` |
| **03** Discrete-event simulation with SimPy | Processes and resources; M/M/1 and M/M/c; costs; priority and pre-emption | `Simpy Basics.pdf`; `Notes/M-M-1 queue - three snapshots.md` | Demos `1` → `2` → `3` (each is the lecture notes with runnable code); `4` if time allows | `Practical - M-M-1 Queue.ipynb` in class, then `Tutorial Questions.pdf` Q1–Q5 in a new notebook → answers `Q1` … `Q5` |
| **04** Problem structuring and simulation build | Soft OR; from a messy situation to a model | `… slides 1-8 (Soft OR introduction).pdf`, then `… Emergency Department.pdf` | `1 Building the ED simulation in stages`, then `2 Emergency department simulation (full model)` | `Problem Structuring Worksheet.pdf` Parts A–C → `… Possible Answers.pdf` |
| **05** Coursework Part B | | `Assignments/02-coursework-part-b/README.md` and the brief | | The coursework |
| **06** Agent-based modelling | Agents, local rules, emergence | The HTML slides | `1 Game of Life` → `5 SIR epidemic`, each as its model comes up on the slides | Predict-then-run questions on the slides and in the notebooks |
| 07–09 | No folders on this site. The module handbook lists the Beer Game, system dynamics and forecasting; ask your lecturer | | | |
| **10** Revision | Mixed exam-style questions | `Revision.pdf` | — | `Week 10 Revision Selected Questions.pdf` Q1–Q5 → Solutions PDF, four notebooks, `Questions 2 and 5 … .xlsx` |

## 5. How the weeks connect

| Idea | Where it appears |
| --- | --- |
| Sampling from a table of probabilities | W01 tutorial (Excel and Python) → W02 tutorial → W10 Q2 Hock-Brooke |
| The M/M/1 queue | W01 queue by hand → W02 formulas, Excel and Python → W03 demo 1, the practical and Q1 → W10 Q3 library |
| Several servers (M/M/c) and costs | W03 demo 2 (petrol station) → W03 Q2–Q3 → W04 doctors in the ED |
| Priority and pre-emption | W03 demos 3–4, Q4–Q5 → W04 ED stages 4–5 |
| One run is not enough: replications | W03 Q2, Q3 (end of each notebook) → W04 full model (40 replications) → W10 Q3(e) and Q2 |
| Minimum-cost flow / transhipment | W01 demo 6 → W10 Q4 F.B. Knight (also Semester 1 Week 08) |
| Binary selection with a budget | Semester 1 Week 05 → W10 Q1 GreenGrid |

## 6. Known limitations and how to work around them

| What | Why | What to do |
| --- | --- | --- |
| Excel workbooks | The browser cannot recalculate Excel formulas | Download them and use Excel or LibreOffice. W01 and W02 also have Python versions |
| MATLAB originals (W01 `5 Source Files/MATLAB`) | MATLAB doesn't run in a browser | Use the W01 notebooks, which replace all four. To run the originals, see the W01 README |
| Week 06 Solara web apps (py.cafe links) | They are separate web apps | Use the five Week 06 notebooks, or the online links (internet needed) |
| Files a notebook saves (for example the W03 answer charts) | They are saved in your browser only | Right-click the file → *Download* |
| Pyomo notebooks print a solver log | HiGHS writes its progress in the browser | Ignore it; the results follow it |

## 7. Corrections (errata)

Some results in the original materials were wrong. They are corrected in the notebooks and workbooks; PDFs that can't be
edited are listed in the week README. **Check the Errata section of a week before you compare your answers with a PDF.** The
main ones:

| Week | What was corrected |
| --- | --- |
| 01 | Slide p37 cumulative band (0.2–0.6); tutorial answers: expected inter-arrival time 15.15, not 12.5 |
| 02 | Cost example on slide p19; typos in the derivation notes; workbook formulas |
| 03 | Breakdown/pre-emption models (demos 3–4, Q4, Q5): interrupted jobs now queue again; Q5 utilisation; Q2 and Q3 answers checked with replications |
| 04 | ED model utilisation (0.72, not 0.66, for 2 doctors) |
| 10 | Q2 Hock-Brooke rebuilt with the right data (about 15 spaces over a year); Q3(c) library: 4 advisers, not 3 |

## 8. Running on your own computer (optional)

1. Install Python 3.10 or newer (Anaconda or python.org).
2. In a terminal (or Anaconda Prompt): `pip install numpy pandas matplotlib simpy pyomo highspy mesa networkx jupyter`
3. Download a notebook (right-click → *Download*) and open it in JupyterLab, VS Code (with the Jupyter extension) or
   Anaconda's Jupyter. The first cell's `%pip install …` also works there.
4. The original scripts are in each week's `5 Source Files/Python`; run them with `python Q1_Bank_Teller.py`. They are the
   unchanged originals, so they do **not** include the corrections; the notebooks do. Each week README lists the differences.

---

## For staff

- Each week README ends with *Notes for staff* (what changed during the move, known issues).
- The full teaching guide (teaching order, prerequisites and pitfalls for every week) is
  `Handbook/5CM522 Weekly Teaching Guide (Lectures).pdf`.
- The notebooks are checked automatically on every push (Pyodide, the same engine as the site): see the repository README,
  *Automatic notebook test*.
