# Semester 1 · Week 06 – Integer Linear Programming - Further Problems

More binary-variable models on graphs: set cover with costs (fire stations), vertex cover (security cameras),
matchings, and the assignment problem. The fire-station and assignment models are each written three ways in
Pyomo, from typed-out constraints to sets and dictionaries. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF), and last year's slides with the lecturer's handwritten notes (*annotated*, optional) | The lecture |
| `2 Lecture Demos` | Seven notebooks, numbered in the order the slides use them | Run live in the lecture |
| `4 Tutorial Answers` | One answer notebook for the tasks on the last slide | **Release after the practical** |
| `5 Source Files` | Editable originals: the two `.pptx` decks, the Python scripts the notebooks came from, staff notes | Staff only; edit here, then republish the PDF / notebook |
| `6 Further Reading` | *How Vodafone Uses Optimization* (talk slides by Rolf Bardeli, Vodafone): graph problems as integer programs in industry | Optional reading |

There is no tutorial sheet this week: the tasks are on the last slide of the lecture (PDF page 25).

## Before you start

- **Week 05:** binary variables, the fire-station set covering model (demo 3) and the vertex cover preview
  (demo 8). This week adds a cost to each fire station and a larger vertex cover example.
- **Maths:** sets and set notation ($e \in U$, $\{0, 1\}$), summation over a set ($\sum_{t \in S} c_t x_t$), a
  double sum ($\sum_{u} \sum_{v} c_{uv} x_{uv}$); a graph as vertices joined by edges.
- **Python and Pyomo:** a `ConcreteModel`, binary variables, an objective and constraints, solved with
  `SolverFactory('appsi_highs')`; Python lists, loops and dictionaries. Each notebook's first cell installs
  Pyomo and HiGHS; run it first.

## Work through this week in order

Page numbers are the pages of the lecture PDF.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | `1 Lecture/Week 6 - Integer Linear Programming - Further Problems.pdf`, pages 1–5 | The general set covering model and a small example (answer $\{a, d\}$) |
| 2 | Lecture PDF, pages 6–8 | Fire stations with running costs: the data, the model, the answer (cost 24) |
| 3 | `2 Lecture Demos/1 Costed fire stations.ipynb` | Page 7 typed into Pyomo, one constraint per city |
| 4 | `2 Lecture Demos/2 Costed fire stations - incidence matrix.ipynb` | The same model built from a 0/1 table (tutorial task 2) |
| 5 | `2 Lecture Demos/3 Costed fire stations - sets and dictionaries.ipynb` | The same model with named data and a constraint rule |
| 6 | Lecture PDF, pages 9–15 | Vertex cover; placing security cameras |
| 7 | `2 Lecture Demos/4 Security cameras - vertex cover.ipynb` | Pages 13–15: 4 cameras, with the graph entered as a matrix |
| 8 | Lecture PDF, pages 16–23 | Matchings, perfect matchings, and the assignment problem (pages 20–23) |
| 9 | `2 Lecture Demos/5 Balanced assignment.ipynb` | Page 22 in Pyomo: total time 13 |
| 10 | `2 Lecture Demos/6 Balanced assignment - named.ipynb` | The same model with named index sets |
| 11 | `2 Lecture Demos/7 Balanced assignment - sets and dictionaries.ipynb` | The same model with a dictionary of times and two rules |
| 12 | Lecture PDF, pages 24–25 | A 3 × 3 assignment (students and projects) and the tutorial tasks |
| 13 | `4 Tutorial Answers/Q5 Maximum set cover, edge cover and independent set.ipynb` | Check your work on task 5 after you have tried it |

Each notebook starts with the problem, how to run it and the expected result, explains every code cell, and ends
with a short *What do you notice?* or *Try it* question with a hidden answer.

In the browser, HiGHS prints its solver log even when the code says `tee=False`; the results are not affected.

## By the end of this week you can

- write a minimum-cost set cover: one binary variable per set, one "covered at least once" constraint per
  element;
- write the same Pyomo model three ways (typed-out constraints, an incidence matrix in a loop, sets with
  dictionaries and rules) and say when each is easiest to use;
- model vertex cover with one constraint $x_u + x_v \ge 1$ per edge, and enter a graph as a matrix;
- explain matchings and perfect matchings, and write the assignment problem with "one per row, one per column"
  equality constraints;
- recognise problems with several optimal answers (security cameras), where your selection may differ from the
  slides.

**Next:** Week 07 (Flow Shop and Job Shop Scheduling) uses binary variables again to order jobs on machines;
Week 08 returns to graphs (shortest paths and spanning trees).

## Lecture demos (`2 Lecture Demos`)

| Notebook | PDF pages | Shows | Result |
| --- | --- | --- | --- |
| `1 Costed fire stations` | 6–8 | Minimum-cost set cover, constraints typed out | 24: stations $a$, $b$, $d$ |
| `2 Costed fire stations - incidence matrix` | 6–8 | Constraints built from a 0/1 matrix | 24: stations $a$, $b$, $d$ |
| `3 Costed fire stations - sets and dictionaries` | 6–8 | Named data, `Constraint(cities, rule=...)` (cities numbered 1–5) | 24: stations A, B, D |
| `4 Security cameras - vertex cover` | 12–15 | Vertex cover, graph as an upper-triangular matrix | 4 cameras: corners 2, 4, 6, 8 (1, 3, 5, 7 is also optimal) |
| `5 Balanced assignment` | 20–23 | Assignment: one job per worker, one worker per job | 13: worker 1 → job 2, 2 → 1, 3 → 3, 4 → 4 |
| `6 Balanced assignment - named` | 20–23 | The same with named sets | 13, same assignment |
| `7 Balanced assignment - sets and dictionaries` | 20–23 | Dictionary of times, two constraint rules | 13, same assignment |

## Tutorial (last slide, PDF page 25)

| Task | Answer |
| --- | --- |
| 1. Study the models and the Python code | The seven demos |
| 2. Code the costed fire stations with an incidence matrix | Demo 2 |
| 3–4. Gurobi modelling examples: pick one and code it in Pyomo | Open-ended, no model answer |
| 5. Maximum set cover, minimum edge cover, maximum independent set | `Q5 Maximum set cover, edge cover and independent set`: 4 cities with two stations; 4 corridors; 4 corners |

## Notes for staff

- **Slide and page numbers.** The plain `.pptx` has three hidden slides (2 "Blank Slide", 10–11 edge covering),
  so `.pptx` slide 1 is PDF page 1, slides 3–9 are pages 2–8 and slides 12–28 are pages 9–25. The *annotated*
  PDF includes the hidden slides, so its page numbers are the `.pptx` slide numbers.
- **The annotated deck is last year's lecture with handwritten notes.** It uses the older notation ($x_s$,
  $s \in S$). Its `.pptx` is an earlier draft than its PDF (its last slide still says "MATLAB code" and
  "Homework"); keep it for the ink, but edit only the plain deck. The corrections below are not in the
  annotated deck.
- **Security cameras.** The slides call corners 2, 4, 6, 8 the "MATLAB Solution" (page 14) and 1, 3, 5, 7
  "Another possibility" (page 15). These are the only two minimum covers. HiGHS (browser and desktop) picks
  2, 4, 6, 8; the GLPK script in `5 Source Files/Python` picks 1, 3, 5, 7.
- The notebooks use HiGHS (`SolverFactory('appsi_highs')`) so they run in the browser; the scripts in
  `5 Source Files/Python` still use GLPK for desktop use. Optimal values match.
- Staff note from last year (`5 Source Files/Staff Notes/Notes for 2526.txt`): *Include Pyomo Modelling*.
  The demos now do this.
- **Notebooks (Oct 2026).** Each notebook gained an opening cell (problem, how to run it, expected result), a
  short explanation above every code cell, comments on each data row and constraint, and a closing *What do you
  notice?* / *Try it* cell with a hidden answer. Wrong or unclear comments were fixed: "# Define the binary
  variables" above cells that define data or sets (demos 1–7), the index comment in demo 6 (it said the first
  index is the column; it is the worker, a row), "creates binary variables" above the constraint loops (demo 6),
  and the typo "modelm" (demo 2). Demo 3's constraint was renamed `cover_constraint` (it was `cover_constaint`),
  here and in `costed_firestation_sets_dictionaries.py`, so `pprint()` shows the new name. No other printed
  result changed.
- **Data correction (Oct 2026), demo 7 and `balanced_assignment_sets_dictionaries.py`.** Worker 1's times for
  jobs 3 and 4 were 9 and 2; the table on the slides (and demos 5–6) has 7 and 8. Corrected. The optimal
  assignment and total (13) are the same before and after.
- **Corrections (Oct 2026), lecture slides.** The plain `.pptx` in `5 Source Files` was corrected; **the PDF in
  `1 Lecture` has not been re-exported yet** (`.pptx` slide numbers, PDF pages in brackets):
  - slide 4 (p. 3): "$t \in S$ – a given set $t$" (it said "set $s$");
  - slides 6 and 8 (pp. 5, 7): "$x_t \in \{0,1\}$" (it said $x_s$; the model uses $x_t$);
  - slide 25 (p. 22): the first constraint sums over $v \in J$ (it said $v \in j$);
  - slide 27 (p. 24): the students in the right-hand graph are s1, s2, s3 (all three said s1);
  - slide 28 (p. 25): "Minimum Edge Cover" (it said "Maximum"; the minimum is the problem on hidden slides
    10–11; all the edges together would be a maximum cover); task 5 "Try coding the problems below yourself."
    and "Look up other problems, such as:" (it said "Try coding these yourself." and "such as.").
  - smaller fixes: slides 7–9 (pp. 6–8) "fire station(s)" (it said "firestation"); slides 23, 24, 26
    (pp. 20, 21, 23) "bipartite"; slide 25 (p. 22) "Pick 1 per row and 1 per column"; slide 15 (p. 12) the
    example is "adapted from" brilliant.org (their version is an art gallery, not a school); hidden slide 11
    "Find the minimum number of edges" (it said "Find a the").
  - Not changed (pictures): the graph pictures on slides 14, 16, 22 and 25 (pp. 11, 13, 19, 22) come from the
    Vodafone talk in `6 Further Reading`. The one on slide 14 (p. 11) is the talk's general "from a graph to
    an integer program" picture (node variables, edge variables, labels); only its *Example 2* box is vertex
    cover.
  - The edited equations (slides 4, 6, 8 and 25) also keep a stored picture of the old text, which only
    LibreOffice and old viewers show. **Re-export from PowerPoint.**
