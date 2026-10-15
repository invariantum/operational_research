# Semester 2: start here

Semester 2 teaches **simulation**: how to model a system that has randomness in it (a queue at a bank, an
emergency department, a factory machine that breaks down) and use the model to answer "what if" questions.
It starts with coins, dice and queues worked by hand and in Excel (Weeks 01–02), moves to discrete-event
simulation in Python with SimPy (Weeks 03–04), and finishes with agent-based modelling (Week 06) and
revision for the in-class test (Week 10).

Every Python example runs **in your web browser** on the course site. You do not install anything.

---

## 1. Before Week 01: set up (about 5 minutes)

1. Open the course site: <https://invariantum.github.io/operational_research/>. Use a recent Chrome,
   Edge or Firefox.
2. Open **`00_START_HERE.ipynb`** (top level of the site) and choose *Run → Run All Cells*. If every
   cell prints `OK`, all the Semester 2 notebooks will run (section 4 of it is a tiny SimPy simulation).
   The first run downloads Python, so allow about a minute.
3. In every notebook, **run the first code cell first**. It installs what that notebook needs
   (SimPy from Week 03 on; Pyomo and the HiGHS solver for the two optimisation notebooks). Then use
   *Run → Run All Cells*, or run the cells one by one while you read.
4. **Save your work by downloading it.** Notebooks you change are kept only in this browser. To keep
   them, right-click the file → *Download*.
5. **Weeks 01, 02 and 10 also use Excel.** Download the `.xlsx` files and open them in desktop Excel
   (LibreOffice Calc also works). They use `RAND()`, so press **F9** to re-run the simulation.

### What opens where

| File type | How to open it |
| --- | --- |
| `.ipynb` notebook | Double-click: it opens and runs in the browser |
| `.pdf` slides, sheets, answers | Double-click: it opens in the browser's PDF viewer (if it does not, right-click → *Download*) |
| `.md` notes and `README.md` files | Right-click → *Open With* → *Markdown Preview* (double-clicking shows the raw text) |
| `.html` slides (Week 06) | Double-click: it shows as one long scrolling page. Press *Trust HTML* (or download it and open it in your browser) to page through it as slides |
| `.xlsx` workbook (Weeks 01, 02, 10) | Download it and open it in desktop Excel |
| `.png` image | Double-click |
| `.pptx`, `.docx`, `.tex`, `.m`, `.py` | Originals for staff, in `5 Source Files`. You do not need them |

---

## 2. How a week folder is organised

Every week uses the same numbered folders (a week only has the folders it needs):

| Folder | What is in it | When to use it |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and any lecture notes | Read before or during the lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in the order they are used | Run them in number order |
| `3 Tutorial` | The tutorial sheet, and any starter workbook or notebook | The practical session |
| `4 Tutorial Answers` | Worked answers and answer notebooks | After you have tried the tutorial |
| `5 Source Files` | Editable originals, the scripts the notebooks were made from, MATLAB versions, older versions | Staff only; you can ignore it |
| `6 Further Reading` | Papers, case studies and links | Optional |

Each week also has a `README.md` that lists its files.

**A good routine for each week:** slides → lecture demos in number order → tutorial sheet → answers.

---

## 3. Week by week

| Week | Topic | Read | Run | Practise | Builds on |
| --- | --- | --- | --- | --- | --- |
| 01 | Introduction to simulation: why simulate, coins and dice, queues by hand | *Introduction to Simulation* slides; *Example Simulation* handout (slides 38–40). *Production Distribution Model* slides are optional | Demos 1–4 in order: `1 Coin toss` and `2 Dice` notebooks, then the same experiments in Excel (`3 …`, `4 Heated clothes rack …`). Optional: `5 Election simulation`; `6 Production-distribution` (an optimisation example, goes with the optional slides) | Tutorial Q1 by hand, Q2–Q3 in Excel (`Tutorial Example.xlsx` and `Tutorial Excel Sheets.xlsx` show the layout), Q4 in Python (a new notebook; `2 Dice` is a worked answer to Q4a). Answers: PDF, `Tutorial Answers.xlsx`, `Tutorial example answer.png` | – |
| 02 | Queueing theory: arrival and service distributions, Little's law, Kendall notation, the M/M/1 queue | *Introduction to Queueing Theory* slides; *M-M-1 queue derivation* (optional) | `1 M-M-1 lecture example.xlsx` (Excel; simulated vs theoretical values) | Tutorial Q1–Q3 in `Tutorial Template.xlsx`. Answers: `Tutorial Answers.xlsx` (Q1 theory: Wq = 1.5 min, W = 3 min) | Week 01 Excel simulation |
| 03 | Discrete-event simulation with SimPy: M/M/1, several servers and costs, breakdowns | *Simpy Basics* slides; `Notes/M-M-1 queue - three snapshots.md` | Demos 1–3 in order (each is the lecture notes plus runnable code); `4 Machine breakdowns - full demo` if time allows | `Practical - M-M-1 Queue` notebook (in the lecture), then `Tutorial Questions.pdf` Q1–Q5 in a notebook of your own. Answers: five notebooks, `Q1` … `Q5` | Week 02 M/M/1 formulas |
| 04 | Problem structuring (soft OR) and building a simulation live | ED slides: first the *slides 1-8 (Soft OR introduction)* PDF, then *Emergency Department*; the *annotated* PDF is the in-class version; *GORS* exercise is an alternative session | `1 Emergency department simulation` (built in stages in the session) | `Problem Structuring Worksheet.pdf` Parts A–C. Answers: *Possible Answers* PDF | Week 03 priority and pre-emption |
| 05 | Coursework Part B released | The brief in `Assignments/02-coursework-part-b`; the Vodafone case study (optional) | – | The coursework | Weeks 01–04 |
| 06 | Agent-based modelling (Mesa): Game of Life, Schelling, wealth, traffic, SIR | The HTML slides | The demos are online and linked from the slides (py.cafe Mesa examples, a Google Colab notebook, playgameoflife.com); they do not run on this site | Predict-then-run questions on the slides; no sheet | Weeks 01–03 (randomness, simulation runs) |
| 07–09 | No folders on this site | | | | |
| 10 | Revision for the in-class test | `Revision.pdf` (all questions) | – | `Week 10 Revision Selected Questions.pdf` Q1–Q5. Answers: *Solutions* PDF, three notebooks (GreenGrid, University library, F.B. Knight), `Questions 2 and 5 … .xlsx` | All of Semester 2, plus Semester 1 integer programming and transhipment |

---

## 4. How the materials connect

| Example or idea | Where it appears |
| --- | --- |
| Random sampling with a lookup table | Week 01 tutorial (Excel) → Week 02 tutorial (Excel) → Week 10 Q2 inventory simulation (Excel) |
| The M/M/1 queue | Week 01 queue by hand → Week 02 formulas and Excel → Week 03 demo 1, the practical and Q1 (SimPy) → Week 10 Q3 library help desk |
| Several servers (M/M/c) and costs | Week 03 demo 2 (petrol station) → Week 03 Q2–Q3 → Week 04 doctors in the ED |
| Priority and pre-emption (breakdowns, urgent patients) | Week 03 demos 3–4 and Q4–Q5 → Week 04 ED simulation stages 4–5 |
| The emergency department | Week 03 Q5 (answer notebook) → Week 04 workshop and live build |
| Minimum-cost flow / transhipment | Week 01 demo 6 → Week 10 Q4 F.B. Knight (both Pyomo; also Semester 1 Week 08) |
| Binary selection with a budget | Semester 1 Week 05 → Week 10 Q1 GreenGrid (Pyomo) |

Which file goes with which:

| Week | Slides or sheet | Notebook or workbook |
| --- | --- | --- |
| 01 | *Introduction to Simulation*, slide 11 | `4 Heated clothes rack in Excel.xlsx` |
| 01 | *Introduction to Simulation*, slides 12–15 | `3 Coin and dice simulations in Excel.xlsx`, `1 Coin toss`, `2 Dice` |
| 01 | *Production Distribution Model* | `6 Production-distribution (minimum-cost flow)` |
| 01 | Tutorial Q2–Q3 | `Tutorial Example.xlsx` and `Tutorial Excel Sheets.xlsx` (worked layouts) → `Tutorial Answers.xlsx` |
| 02 | Slides 16–26 (M/M/1 example, servers in series) | `1 M-M-1 lecture example.xlsx` |
| 02 | Tutorial Q1–Q3 | `Tutorial Template.xlsx` → `Tutorial Answers.xlsx` |
| 03 | *Practical - M-M-1 Queue* (PDF and notebook are the same exercise) | `Practical - M-M-1 Queue.ipynb` |
| 03 | *Tutorial Questions* Q1–Q5 | `Q1 Bank teller` … `Q5 Hospital emergency department` |
| 04 | ED slides 18–24 (Part C) | `1 Emergency department simulation` |
| 10 | Selected Questions Q1, Q3, Q4 | `GreenGrid …`, `University library …`, `F.B. Knight …` notebooks |
| 10 | Selected Questions Q2, Q5 | `Questions 2 and 5 - forecasting and simulation.xlsx` |

---

## 5. Things that can confuse

- **Your numbers will not match the answers exactly.** The Excel workbooks re-draw their random numbers
  every time they recalculate. Compare the shape of the results and long-run averages with the
  theoretical values, not individual cells. The notebooks use a fixed seed, so everyone gets the same run;
  change or remove the seed to see other runs.
- **The Week 03 practical PDF says "Open Google Colab".** On this site you are already in the notebook:
  run the install cell and follow the steps. Colab also works if you prefer it.
- **Week 03 Tutorial Questions have no starter notebook.** Create one (*File → New → Notebook*), and make
  its first cell `%pip install simpy`.
- **The Q1–Q5 answer notebooks save a picture** (for example `Q1_Bank_Teller_Results.png`) next to the
  notebook. On this site it is saved in your browser only; you can ignore or download it.
- **Week 10 Q3(c)** asks for 2, 3 and 4 advisers: change `ADVISERS` in the library notebook and run it again.
- **Week 10 Q5 (forecasting)** uses moving averages and seasonal indices. There is no forecasting lecture
  folder on this site; use the solutions PDF and the workbook.
- **Weeks 07–09** have no folders here. The module handbook lists the Beer Game, system dynamics,
  forecasting and time series for those weeks; check with your lecturer.

If a notebook fails, see the *If something fails* section at the end of `00_START_HERE.ipynb`.

---

## 6. Running the examples on your own computer (optional)

Everything in section 3 runs on the site. To run the Python on your own computer instead, in VS Code,
PyCharm, Spyder, JupyterLab or Anaconda:

1. Install Python 3.10 or newer (for example Anaconda, or python.org).
2. Install the packages once, in a terminal (or Anaconda Prompt):
   ```bash
   pip install numpy matplotlib simpy pyomo highspy jupyter
   ```
3. **Notebooks:** download the `.ipynb` (right-click → *Download*) and open it in VS Code (with the
   Jupyter extension), JupyterLab or Anaconda's Jupyter. The first cell's `%pip install …` also works
   there; it does nothing if the package is already installed. The browser-only fixes in the Pyomo
   notebooks switch themselves off outside the browser.
4. **Scripts:** the `.py` files in each week's `5 Source Files/Python` are the same code as the
   notebooks (see the table below). Run them with `python Q1_Bank_Teller.py`, or with the *Run* button in
   your IDE. Plots open in a window; the Q1–Q5 scripts also save a `.png` in the folder you run them from.
   The Pyomo scripts use the HiGHS solver from `highspy`; no other solver is needed.
5. **Week 06 Mesa demos:** these are online. To run Mesa locally: `pip install mesa solara`, then copy an
   example from the py.cafe link in the slides.
6. **MATLAB originals (Week 01, `5 Source Files/MATLAB`):** need MATLAB. `dice.m` and
   `unfair_coin_toss.m` use only base MATLAB (they should also run in a recent version of the free GNU
   Octave; not tested);
   `election_simulation.m` uses `normrnd` (Statistics Toolbox; in Octave, `pkg load statistics`);
   `production_distribution_model.m` uses `optimproblem` (MATLAB Optimization Toolbox; it does not run in
   Octave). The notebooks replace all four.

### Notebooks and the files they came from

All 18 Semester 2 notebooks run on the site.

| Notebook | Came from | What is different |
| --- | --- | --- |
| Week 01 `1 Coin toss`, `2 Dice`, `5 Election`, `6 Production-distribution` | MATLAB `unfair_coin_toss.m`, `dice.m`, `election_simulation.m`, `production_distribution_model.m` | Rewritten in Python (NumPy, Matplotlib; Pyomo + HiGHS for 6). Same experiments and the same optimum (£533,930 for 6). Seeded random numbers differ from MATLAB's; the coin plot shows percentages (0–100) where MATLAB used proportions; the election notebook adds a fixed seed and a "Democrats win x%" line |
| Week 03 demos `1`–`3` | `5 Source Files/Notes (Markdown)` segment notes | The notes word for word, with their code in runnable cells and an install cell first |
| Week 03 `Practical - M-M-1 Queue` | `5 Source Files/Notes (Markdown)/Practical - M-M-1 Queue.md` (also the PDF) | Install cell added; Steps 1–2 rewritten for this site instead of Google Colab |
| Week 03 `4 Machine breakdowns - full demo` | `5 Source Files/Python/segment_3_demo.py` | Same code (the script was fixed first: a breakdown during maintenance no longer crashes it), split into cells; install cell |
| Week 03 `Q1`–`Q5` | `5 Source Files/Python/Q1_Bank_Teller.py` … `Q5_Hospital_ED.py` | Same code, split into cells; install cell. Q3 and Q5 add one `;` so a plot cell does not print `(0.0, 105.0)` |
| Week 04 `1 Emergency department simulation` | `5 Source Files/Python/hospital_sim.py` | Same code, split into cells; install cell |
| Week 10 `GreenGrid …`, `F.B. Knight …` | `5 Source Files/Python/greengrid_pyomo.py`, `fb_knight_mcfp_pyomo.py` | Same code; the install cell also adapts Pyomo to the browser (only in the browser) |
| Week 10 `University library …` | `5 Source Files/Python/uni_library_simpy.py` | Same code, split into cells; install cell |

What does **not** run on the site: the Excel workbooks (desktop Excel), the Week 06 Mesa demos (online
links, or locally as in step 5) and the MATLAB originals (MATLAB). None of these is a notebook.

---

## For staff

Each week's `README.md` ends with *Notes for staff* (what changed during the move, known issues).
The full teaching guide, with teaching order, prerequisites and pitfalls for every week, is
`Handbook/5CM522 Weekly Teaching Guide (Lectures).pdf`.
