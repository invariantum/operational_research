# Semester 1 · Week 02 – Linear Programming 1

Formulating linear programmes, solving them graphically, and solving them with SciPy's `linprog` and Excel Solver.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `3 Tutorial` | Tutorial / practical sheet and any starter files | The practical |
| `4 Tutorial Answers` | Worked answers and answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |

## Before you start

- **Maths:** Week 01's matrix form $Ax \le b$ and sketching a feasible region from linear inequalities.
- **Python:** none needed beyond Week 01. The notebooks are short and commented.
- **Excel:** desktop Excel with the **Solver** add-in (*File → Options → Add-ins → Excel Add-ins → Solver*),
  for the Excel demo and Tutorial Q4. Excel does not run on the course site.

## Work through this week in order

| Step | File | What it is for |
| --- | --- | --- |
| 1 | `1 Lecture/Week 2 - Linear Programming 1.pdf` | The lecture example (two products, one machine), the feasible region, the objective line, optimal vertices, binding constraints, infeasible, unbounded and multiple-optimum LPs, the canonical (matrix) form, and the switch from maximising to minimising |
| 2 | `2 Lecture Demos/1 LP with SciPy linprog.ipynb` | Run every cell: the lecture LP solved with `linprog`; the answer $(41.14, 10.29)$, profit £277.71, is slide 12's point B |
| 3 | `2 Lecture Demos/2 LP with Excel Solver.xlsx` | The same LP in Excel: download it, open *Data → Solver* and press *Solve* |
| 4 | `1 Lecture/Simplex Method 2 Variable Graphical Demo.pdf` | Optional: how the simplex method walks from vertex to vertex (A → B → C) |
| 5 | `3 Tutorial/Week 2 - Linear Programming - Tutorial.pdf` | Q1 graphically, Q2 in matrix form, Q3 in Python (copy the step 2 notebook and change `c`, `A_ub`, `b_ub`), Q4 in Excel (copy the step 3 workbook), Q5 manufacturing (medium), Q6 diet problem (hard; it is discussed at the start of Week 03) |
| 6 | `4 Tutorial Answers/` | Check your work after you have tried the questions: the PDF for Q1–Q6, a notebook for Q3, Q5a, Q5b, Q5c and Q6, and a workbook for Q4 |

## By the end of this week you can

- turn a short word problem into a linear programme: decision variables, objective, constraints, non-negativity;
- draw the feasible region of a two-variable LP and find the optimum by moving the objective line, or by
  checking the vertices;
- say which constraints are binding at a solution;
- recognise infeasible and unbounded LPs and LPs with many optimal solutions;
- write an LP in canonical form ($\max c^T x$ subject to $Ax \le b$, $x \ge 0$) and turn a maximisation into
  a minimisation by negating $c$;
- solve an LP with SciPy's `linprog` and with Excel Solver, and read the result (`linprog` prints
  $-$profit when you maximise).

**Next:** Week 03 (Linear Programming 2) solves the lecture LP and the Q6 diet problem again in Pyomo, then
adds integer variables. Tutorial Q5c already shows why whole-number answers need a different method.

## 1 Lecture

- `Simplex Method 2 Variable Graphical Demo.pdf`
- `Week 2 - Linear Programming 1.pdf`

## 2 Lecture Demos

- `1 LP with SciPy linprog.ipynb` (notebook)
- `2 LP with Excel Solver.xlsx`

## 3 Tutorial

- `Week 2 - Linear Programming - Tutorial.pdf`

## 4 Tutorial Answers

- `Q3 LP with linprog.ipynb` (notebook): $(x, y) = (0, 20)$, maximum 340 (also Q1).
- `Q4 LP with Excel Solver.xlsx`: the Q1 problem in the demo workbook's layout, with Solver set up; same answer.
- `Q5a Manufacturing - products X and Y.ipynb` (notebook): 50 of Y, profit £250.
- `Q5b Manufacturing - add product Z.ipynb` (notebook): 20 of Y and 20 of Z, profit £260.
- `Q5c Manufacturing - faster X.ipynb` (notebook): 22.22 of X, profit £266.67; the best whole-number plan
  earns £266.
- `Q6 Diet problem - parts a, b and c.ipynb` (notebook): (a) minimum cost £93.25; (b) unbounded;
  (c) maximum attractiveness 149.66, and minimum cost £136.52 under the same limits. Lists the binding
  constraints.
- `Week 2 - Linear Programming - Tutorial Answers.pdf`

## Notes for staff

- The coded answers were written for an earlier numbering of the sheet: `Question_4a–c.py` answer today's **Q5a–c** and `Question_5.py` answers **Q6a–c**. The notebooks are named by today's numbering.
- Week 3 demos 2–4 redo the diet problem (Q6) in Pyomo.
- The answers' Q5a sentence pointed to "the MATLAB code", which is not in this folder; it now names the notebook “Q5a Manufacturing - products X and Y” (.docx and PDF, Oct 2026). The output screenshots are still MATLAB's; the values match the notebooks.
- The notebooks' first cell no longer says "Pyomo models use HiGHS instead of GLPK": these notebooks use SciPy, not Pyomo.
- The `@author` line (a staff ID) was removed from the five `Question_*.py` scripts.
- **Corrections (Oct 2026), notebooks.** The comment "cost function (row vector) - to minimise we need the
  negatives" now says that `linprog` minimises, so to maximise we pass the negatives; in Q6 Part A (a cost,
  minimised as it is) it now says the costs are used as they are. Q6 gained a `# Part C` label, the binding
  constraints after (a) and (c) (they match the MATLAB screenshots: 1–3, and 2, 4, 5, 8, 10), and Part C
  with the cost objective (£136.52), because the question asks about both solutions. Every maximising
  notebook now says that `fval` is minus the profit. Removed: the `# -*- coding: utf-8 -*-` lines, and the
  demo's two empty cells and editor timing metadata. No existing printed numbers changed.
- **Added (Oct 2026), notebook explanations.** Each notebook now opens with the problem, how to run it and
  the expected result; has a short explanation above each code cell and a comment on every constraint row
  (Q6 Part C numbers its rows 1–10, as the binding-constraint list does); and ends with a "What do you
  notice?" question with a hidden answer (the demo and Q3 also have a "Try it" with answers). Only
  markdown cells and comments were added: code, saved outputs and printed results are unchanged.
- **Corrections (Oct 2026), slides.** The `.pptx` in `5 Source Files` was corrected, and
  `1 Lecture/Week 2 - Linear Programming 1.pdf` was re-exported from it in PowerPoint (17 Oct 2026), which
  also brought in the slide 1 author line and the slide 5 O/A/B labels and box. The Simplex demo PDF was
  re-exported the same day (content unchanged).
  - slide 11: "For example, should the number…" (it had a capital "Should");
  - slide 12: $P = £277.71$ (it said £277.72; $1944/7 = 277.714$), and "i.e. make at least 4 chairs for each
    table" (it said "make enough tables to go with chairs", the reverse of $x \ge 4y$ and of slide 11's
    "tables will not sell on their own");
  - slide 15: $41.14 \approx 4 \cdot 10.29$ (it said "=", but $4 \times 10.29 = 41.16$; exactly, $288/7 = 4 \cdot 72/7$);
  - slide 18: "anywhere on the line $3x + 2y = 144$ from (0, 72) to (48, 0)";
  - slide 19: "An optimal solution always lies on the boundary of the feasible region: at a vertex, or along a
    whole edge" and "If an optimal solution exists, one is always at a vertex" (it said the optimum "always
    exists at a vertex", which is false for the infeasible and unbounded cases on slides 16–17, and the
    first sentence was garbled);
  - slide 24: title capitalised; slide 25: the link text says "SciPy documentation" (it said "SciPy v1.11.3
    Manual", but the link opens the current docs); slide 26: "it is important to".
  - Not changed: the code on slide 25 is a picture, so its comment still says "to minimise we need the
    negatives".
  - Slides 11, 12, 15 and 18 also store a fallback picture of their main text box, which only programs
    without equation support (e.g. LibreOffice, Google Slides) show. On 17 Oct 2026 these four pictures
    were replaced by the same areas of the PowerPoint PDF export, so they show the corrected text too.
    PowerPoint redraws such a picture only when the text in that box changes (a plain re-save does not),
    so after editing one of these boxes, check it once in another program.
- **Corrections (Oct 2026), answers `.docx`** (`5 Source Files`; the PDF was re-exported, 17 Oct 2026):
  Q2's constraint now includes the vector $(x, y)^T$; Q5c's heading matches the sheet ("In addition to
  product Z, …") and adds that the best whole-number plan earns £266 (e.g. 20, 2, 2) and that the LP has
  other optimal solutions; 6b "you should get an output"; each "Please see the Python code" names its
  notebook; 6c gives the minimum cost under the new limits; the empty paragraph that made a blank last
  page was removed; Q4 says "You should get the same answer as 3): see the workbook “Q4 LP with Excel
  Solver”" (it said "a similar answer"); Q6 "basic restrictions" and "are given in Table 2".
- **Tutorial `.docx`** (`5 Source Files`; the PDF was re-exported, 17 Oct 2026): "I recommend using
  Spyder" now says that Q3, Q5 and Q6 run on the course site and Q4 needs desktop Excel with Solver;
  Q6 "basic restrictions" (it said "restriction") and "are given in Table 2" (it said "is given in table 2").
- **Added (Oct 2026):** `4 Tutorial Answers/Q4 LP with Excel Solver.xlsx`, made from the demo workbook
  (same layout and Solver set-up). Before that, Q4 had only "You should get a similar answer to 3)".
