# Semester 1 · Week 03 – Linear Programming 2

Pyomo modelling, the diet problem, and a first look at integer and mixed-integer programmes.
Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and the 2-variable simplex demo | The lecture |
| `2 Lecture Demos` | Six notebooks, numbered in the order the slides use them | Run live in the lecture |
| `3 Tutorial` | Tutorial 3 sheet | The practical |
| `4 Tutorial Answers` | Worked answers (PDF) and answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals: `.pptx`, `.docx`, the Python scripts the notebooks came from, MATLAB versions | Staff only; edit here, then republish the PDF / notebook |

## Before you start

- **Week 02:** the lecture LP (maximise $5x + 7y$), its graphical solution, and the diet problem (Week 02
  tutorial Q6). This week solves both again in Pyomo.
- **Maths:** summation notation, $\sum_i c_i x_i$ (the lecture introduces it with the diet problem).
- **Python:** lists, `for` loops and `sum(...)`. Each notebook's first cell installs Pyomo and the HiGHS
  solver; run it first.

## Work through this week in order

Page numbers are the pages of the lecture PDF.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | `1 Lecture/Week 3 - Linear Programming 2.pdf`, pages 1–5 | Review of Week 02: the LP model, canonical (matrix) form, the `linprog` solution |
| 2 | `1 Lecture/Simplex Method 2 Variable Graphical Demo.pdf` | Optional: how the simplex method walks from vertex to vertex (the same demo as Week 02) |
| 3 | `2 Lecture Demos/1 LP with Pyomo.ipynb` | Page 6: the same LP in Pyomo; $(41.14, 10.29)$, $P = 277.71$ |
| 4 | `2 Lecture Demos/2 Diet problem 5a - minimise cost.ipynb` | Pages 7–11: the diet problem in summation notation and Pyomo; minimum cost 93.25 |
| 5 | `2 Lecture Demos/3 Diet problem 5b - unbounded.ipynb` | Pages 12–13: maximise attractiveness; the solver reports *unbounded*, and why |
| 6 | `2 Lecture Demos/4 Diet problem 5c - the fix.ipynb` | Pages 14–15: minimum and maximum limits give a sensible diet; attractiveness 149.66 |
| 7 | Lecture PDF, pages 16–22 | Manufacturing problem and the Desmos demo: rounding an LP answer is not the same as the best whole-number answer |
| 8 | `2 Lecture Demos/5 Integer LP.ipynb` | Page 23: integer variables; $(3, 2)$, $P = 13$ |
| 9 | `2 Lecture Demos/6 Mixed-integer LP.ipynb` | Pages 24–25: one integer and one continuous variable; $(2, 2.833)$, $P = 13.917$ |
| 10 | `3 Tutorial/Week 3 - Linear Programming 2 - Tutorial.pdf` | Q1 (LP, ILP and MILP: copy demo 5 or 6 and change the numbers), Q2 Icki-Toffee (medium/hard: copy demo 2's structure, with integer variables) |
| 11 | `4 Tutorial Answers/` | Check your work after you have tried the questions: the PDF for Q1–Q2, and three notebooks |

Each notebook starts with the problem, how to run it and the expected result, explains every code cell,
and ends with a short *What do you notice?* or *Try it* question with a hidden answer.

## By the end of this week you can

- write an LP in Pyomo: a `ConcreteModel`, variables with a domain, an objective and constraints, solved
  with `SolverFactory('appsi_highs')`;
- read Pyomo's output: variable values, the objective, and which constraints are binding;
- write a model with summation notation ($\sum_i c_i x_i$) and code it with `sum(...)` over lists of data;
- recognise an unbounded LP from the solver's message, explain why it happens, and fix the model by
  adding the missing limits;
- explain why rounding an LP solution may be infeasible or not optimal;
- solve integer (ILP) and mixed-integer (MILP) programmes by changing the variables' domain, and compare
  LP ≥ MILP ≥ ILP for a maximisation.

**Next:** Week 04 (Mathematical Programming: Modelling) uses the Icki-Toffee model again to compare
objectives (Q2d's question: is maximising total popularity the right aim?) and adds slack variables.

## Lecture demos (`2 Lecture Demos`)

| Notebook | PDF pages | Shows |
| --- | --- | --- |
| `1 LP with Pyomo` | 6 | The lecture LP written in Pyomo |
| `2 Diet problem 5a - minimise cost` | 7–11 | Week 2 tutorial Q6a (the slides' Q5a) in Pyomo |
| `3 Diet problem 5b - unbounded` | 12–13 | Maximising attractiveness: the solver reports *unbounded* |
| `4 Diet problem 5c - the fix` | 14–15 | Adding limits on fat and vitamins gives a sensible diet |
| `5 Integer LP` | 23 | Same constraints, integer variables |
| `6 Mixed-integer LP` | 24–25 | One integer and one continuous variable |

## Tutorial answers (`4 Tutorial Answers`)

| Notebook | Question | Answer |
| --- | --- | --- |
| `Q1 LP, ILP and MILP` | Q1, Q1a, Q1b | LP 270 at (7.5, 10); ILP 264 at (7, 10); MILP 270 at (7.5, 10) |
| `Q2b Icki-Toffee - minimise cost` | Q2b | Minimum cost 268 (several selections reach it) |
| `Q2c Icki-Toffee - maximise popularity` | Q2c | 5 Coconut Ice, 50 Lime Sherbet, 5 Grape Bunch; weight 635 g |

- `Week 3 - Linear Programming 2 - Tutorial - Answers.pdf`: Q1–Q2, with Pyomo output.

## Notes for staff

- **Slide and page numbers.** The `.pptx` has a hidden blank slide 3 that the PDF leaves out, so from slide 4
  on a `.pptx` slide number is one higher than the PDF page number. The README and the notebooks give PDF
  page numbers.
- **Q1 answers were rewritten for the current tutorial.** The old Q1 scripts solve a different problem
  (maximise 5x + 17y with 2x + 3y ≤ 60, x + 2y ≤ 25) from an earlier version of the sheet. They are kept in
  `5 Source Files/Python/Old Q1 (previous tutorial version)`; the MATLAB Q1 files are the same old version.
- The notebooks use HiGHS (`SolverFactory('appsi_highs')`) so they run in the browser; the scripts in
  `5 Source Files/Python` still use GLPK for desktop use.
- The editable simplex demo (`.pptx`) is in Week 2; only its PDF is repeated here.
- Demos 2–4 follow the slides' numbering (*Tutorial Question 5a–c*); on this year's Week 2 sheet the diet problem is **Q6**.
- To change a demo, edit the notebook directly. To rebuild one from its script instead, run
  `python tools/convert_to_notebooks.py "<path to the .py>"` and move the new notebook into place.
- `Tutorial Coded Answers.zip` was removed: it held the same eight scripts as the loose files (identical apart from Windows line endings).
- A Windows `debug.log` was removed.
- `5 Source Files/Python/Week2_question_5b_pyomo.py` was edited: it now solves with `load_solutions=False` and prints the termination condition, because HiGHS stops with an error when asked to load a solution from an unbounded model. The original is in the pre-migration course folder.
- The answers PDF's Q2b side note was first added directly to the PDF; the PDF was re-exported from the .docx on 17 Oct 2026, so the two now match.
- Notebooks 1 and 6: the comment above the solver line now says HiGHS (it said GLPK).
- Demos 2–4: the titles now give this year's question numbers (Week 2 tutorial Q6a–c) next to the slides' Q5a–c.
- **Notebooks (Oct 2026), text only.** Each notebook gained an opening cell (problem, how to run it,
  expected result), a short explanation above every code cell, a comment on each constraint row and a
  closing *What do you notice?* / *Try it* cell with a hidden answer. Wrong comments were fixed: "variables
  with lower and upper bounds" (demo 5, Q2b, Q2c: no upper bound is set), "# Define the constraints" above
  the data lists (Q2b, Q2c), "Set tee=True" where it is already True; the Q2b/Q2c constraint
  `fat_weight_min` is explained as an upper limit on fat. Slide references are now PDF pages. No code and
  no printed result changed.
- **Corrections (Oct 2026), slides.** The `.pptx` in `5 Source Files` was corrected and the PDF in
  `1 Lecture` re-exported from it in PowerPoint (17 Oct 2026) (`.pptx` slide numbers, PDF pages in brackets):
  - slide 10 (p. 9): vitamin B constraint $14x_5$ (it said $12x_5$); vitamin C constraint $10x_9$ (it
    said $10x_{10}$). The notebooks were already right;
  - slide 19 (p. 18): $P^* = 262.22$ (it said 262.62; $11.5 \cdot 80/9 + 160 = 262.22$);
  - slide 20 (p. 19): "if you round", "round down,", "you get a profit of £262", "Ten pounds might not…";
  - slide 22 (p. 21): the non-optimal points (1, 2) and (2, 2) are labelled $P = 9$, $P = 11$ (not $P^*$);
  - slide 14 (p. 13): title "Tutorial Question 5b";
  - slide 6 (p. 5): "we call linprog with the negated objective, c = [-5, -7]" (it said "using -f");
  - slide 27 (p. 26): the Colab link (it needs a sign-in) now points to the course site and the
    `2 Lecture Demos` folder.
  - Not changed (pictures): the code on slides 7, 24 and 26 says GLPK; slide 16's code comment says
    "minimise total cost" for a maximisation; slide 6's comment says "to minimise we need the negatives".
    Always edit and export the `.pptx` in PowerPoint.
- **Corrections (Oct 2026), tutorial and answers `.docx`** (`5 Source Files`; the PDFs were re-exported from them
  in Word on 17 Oct 2026): Q2 now says the selection must weigh "at least" 320 g, with fat "at most" 45% and
  "at most" 2850 calories (it said "more than" / "less than", but the model uses ≥ / ≤ and the Q2c answer
  uses exactly 2850 calories). Answers only: Q2a no longer adds "Is this a good selection?" (not on the
  sheet; Q2d asks it), and Q2b's heading has the sheet's `**`.
