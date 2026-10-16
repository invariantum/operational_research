# Semester 1: start here

Semester 1 teaches **optimisation**: how to turn a real decision (what to make, where to build, which
route to drive) into a mathematical model, and how to solve it with Python. It runs from linear
programming in Week 02 to integer models for scheduling, routing and packing in Weeks 07–11.

Every Python example runs **in your web browser** on the course site. You do not install anything.

---

## 1. Before Week 01: set up (about 5 minutes)

1. Open the course site: <https://invariantum.github.io/operational_research/>. Use a recent Chrome,
   Edge or Firefox.
2. Open **`00_START_HERE.ipynb`** (top level of the site) and choose *Run → Run All Cells*. If every
   cell prints `OK`, all the Semester 1 notebooks will run. The first run downloads Python, so allow
   about a minute.
3. In every notebook, **run the first code cell first**. It installs what that notebook needs
   (Pyomo and the HiGHS solver from Week 03 on; `ipywidgets` in Week 01). Then use
   *Run → Run All Cells*, or run the cells one by one while you read.
4. **Save your work by downloading it.** Notebooks you change are kept only in this browser. To keep
   them, right-click the file → *Download*.

### What opens where

| File type | How to open it |
| --- | --- |
| `.ipynb` notebook | Double-click: it opens and runs in the browser |
| `.pdf` slides, sheets, answers | Double-click: it opens in the browser's PDF viewer (if it does not, right-click → *Download*) |
| `.md` notes and `README.md` files | Right-click → *Open With* → *Markdown Preview* (double-clicking shows the raw text) |
| `.xlsx` workbook (Weeks 02 and 07) | Download it and open it in desktop Excel. Week 02 needs the **Solver** add-in |
| `.pptx`, `.docx` | Editable originals for staff, in `5 Source Files`. You do not need them |

One exercise needs Google Colab: Week 07 job shop tutorial Q4–Q5 (Google OR-Tools does not run in a
browser).

---

## 2. How a week folder is organised

Every week uses the same numbered folders (a week only has the folders it needs):

| Folder | What is in it | When to use it |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and any lecture notes | Read before or during the lecture |
| `2 Lecture Demos` | Notebooks (and spreadsheets) shown in the lecture, numbered in the order they are used | Run them in number order |
| `3 Tutorial` | The tutorial sheet | The practical session |
| `4 Tutorial Answers` | Worked answers and answer notebooks | After you have tried the tutorial |
| `5 Source Files` | Editable originals, the scripts the notebooks were made from, MATLAB versions, older versions | Staff only; you can ignore it |
| `6 Further Reading` | Papers and case studies | Optional |

Each week also has a `README.md` that lists its files.

**A good routine for each week:** slides → lecture demos in number order → tutorial sheet → answers.

---

## 3. Week by week

| Week | Topic | Read | Run | Practise | Builds on |
| --- | --- | --- | --- | --- | --- |
| 01 | Introduction to OR; vectors, matrices and inequalities | Slides | `1 Vectors and matrices in NumPy` (do this before the tutorial) | Tutorial notebook, Exercises 1–8 (Exercises 5–6 use desmos.com). Answers: one notebook | – |
| 02 | Linear Programming 1: formulation, graphical solution | Slides; *Simplex demo* PDF (optional) | `1 LP with SciPy linprog`; `2 LP with Excel Solver.xlsx` (desktop Excel) | Tutorial Q1–Q6 (Q4 in Excel). Answers: PDF, five notebooks and a Q4 workbook | Week 01 matrix form |
| 03 | Linear Programming 2: Pyomo, the diet problem, integer and mixed-integer LP | Slides | Demos 1–6 in order (the week's README gives the slide for each) | Tutorial Q1 (LP, ILP, MILP) and Q2 (Icki-Toffee). Answers: PDF and three notebooks | Week 02 lecture LP and diet problem |
| 04 | Mathematical Programming: Modelling | Slides; *Slack Variables* | `1 Pyomo expressions and constraints` | Tutorial Q1 (Icki-Toffee objectives), Q2 (two factories). Answers: PDF and six notebooks | Week 03 Icki-Toffee model |
| 05 | Mixed Integer Programming: binary variables | Slides | Demos 1–7; demo 8 (vertex cover) is a preview of Week 06 | Tutorial Q1 (knapsack), Q2 (fire stations), Q3 (Icki-Toffee). Answers: PDF and five notebooks | Weeks 03–04 |
| 06 | Integer LP: further problems (set cover, vertex cover, assignment) | Slides (the *annotated* version is last year's, optional) | Demos 1–7: each model is written three ways | No separate sheet: the tasks are on the last slide (demo 2 is the incidence-matrix version it asks for). Answers: one notebook (task 5) | Week 05 fire stations and vertex cover |
| 07 | Flow shop and job shop scheduling | Flow shop slides; *Job Shop Scheduling Notes (Short)* (the full notes add constraint programming; optional) | `1 Johnsons rule`; `2 Johnsons rule in Excel.xlsx`; the notes notebook | Flow shop tutorial Q1–Q4; job shop tutorial Q1–Q3 (Q4–Q5 in Colab). Answers: PDF, `Flow Shop Q4 MILP answers` and `Job Shop Q1-Q3 answers` | Weeks 05–06 binary variables |
| 08 | Networks: shortest paths (Dijkstra) and minimum spanning trees (Prim, Kruskal) | Slides; *Negative weight example*; *Dijkstra Algorithm* (optional) | No lecture notebooks: pen and paper | Tutorial Q1 (MST), Q2 (shortest path). Answers: two PDFs and `Q1-Q2 answers in Python` (steps of all three algorithms) | Week 06 graphs |
| 09 | Travelling Salesman Problem | Slides | `1 TSP with Pyomo` (the last cell is a genetic-algorithm heuristic; change its seed to see other runs) | No sheet: the tasks are on slide 22; do them in the demo notebook. Answers: one notebook (solve times, genetic-algorithm settings, research questions) | Weeks 05–06, 08 |
| 10 | Vehicle Routing Problem | Slides; `Notes/Routing Problems - Lecture Notes.md` | `1 TSP and VRP with Pyomo`, sections 1–3 | The notebook's *Try it* questions (answers are in the notebook) | Week 09 TSP and MTZ constraints |
| 11 | Floor planning (packing rectangles) | Slides; the Pyomo model notes | `1 Floor planning - minimise area`; 2 and 3 are optional variations (2 takes 3–4 minutes to solve in the browser) | No sheet | Week 05 binary variables |

The module handbook lists *Transportation and Transhipment* for Week 08 and *Inventory Modelling* for
Week 11. This year those weeks cover networks and floor planning, as above.

---

## 4. Examples that come back

Several problems are revisited with a new method, so it helps to keep earlier notebooks open:

| Example | Where it appears |
| --- | --- |
| Lecture LP (maximise 5x + 7y) | Week 02 demo 1 (linprog) and demo 2 (Excel) → Week 03 demo 1 (Pyomo) |
| Diet problem | Week 02 tutorial Q6 (linprog) → Week 03 demos 2–4 (Pyomo) |
| Icki-Toffee sweets | Week 03 Q2 → Week 04 Q1 (choosing an objective) → Week 05 Q3 (binary variables) |
| Fire stations (set covering) | Week 05 demo 3 and Q2 → Week 06 demos 1–3 (with building costs) |
| Vertex cover | Week 05 demo 8 → Week 06 demo 4 (security cameras) |
| TSP and the MTZ constraints | Week 09 notebook → Week 10 notebook, section 1 |
| Binary "either/or" (big-M) constraints | Week 05 → Week 07 job shop → Week 11 floor planning |

---

## 5. Things that can confuse

- **Question numbers.** The Week 03 slides and demos call the diet problem "Tutorial Question 5" and
  the manufacturing problem "Q4". On this year's Week 02 sheet they are **Q6** and **Q5**. The answer
  notebooks use this year's numbers.
- **More than one right answer.** Some problems have several optimal solutions with the same value
  (Week 03 Q2b, Week 04 Q1b, Week 05 Q3, Week 06 security cameras, Week 08 Q2a, Week 11). Your selection may
  differ from the answer sheet; the optimal value will match.
- **MATLAB screenshots.** Some answer sheets show MATLAB output. The Python notebooks give the same
  values.
- **linprog minimises.** To maximise with SciPy you minimise the negative, so the printed objective
  has the opposite sign (Week 02).
- **Do not mix SciPy's `linprog` and Pyomo in one browser notebook**: the browser kernel stops.
  The course notebooks keep them apart.

If a notebook fails, see the *If something fails* section at the end of `00_START_HERE.ipynb`.

---

## For staff

Each week's `README.md` ends with *Notes for staff* (what changed during the move, known issues).
The full teaching guide, with teaching order, prerequisites and pitfalls for every week, is
`Handbook/5CM522 Weekly Teaching Guide (Lectures).pdf`.
