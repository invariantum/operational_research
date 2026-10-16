# Semester 1 · Week 09 – Travelling Salesman Problem

The travelling salesman problem (TSP): visit every city exactly once and return to the start, as cheaply as
possible. Why it is hard (the number of tours grows like $(n-1)!/2$), why the obvious integer program allows
*subtours*, and how the Miller–Tucker–Zemlin (MTZ) constraints remove them. The model is solved in Pyomo and then
compared with a heuristic, a genetic algorithm. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Lecture slides (PDF) | The lecture |
| `2 Lecture Demos` | `1 TSP with Pyomo.ipynb`: the MTZ model on 4 and 20 cities, and a genetic algorithm on 35 | Run live in the lecture; the tutorial uses it too |
| `4 Tutorial Answers` | Answers to the tutorial on slide 22: solve times, genetic-algorithm settings, research questions | **Release after the practical** |
| `5 Source Files` | Editable original of the slides (.pptx) | Staff only; edit here, then republish the PDF |

## Before you start

- **Weeks 05–06:** binary variables and the assignment problem. The TSP's "one arc out of and one arc into every
  city" constraints are assignment constraints.
- **Week 08:** networks. Cities are vertices; the distances are edge weights.
- **Maths:** factorials, sums over a set, "for all" ($\forall$), and an inequality that is switched on or off by a
  binary variable (as in Week 05's big-M constraints).
- **Python:** a Pyomo model as in Weeks 03–05 (`Var`, `Constraint` with a rule, `Objective`,
  `SolverFactory('appsi_highs')`).

## Work through this week in order

Slide numbers are those of the `.pptx` in `5 Source Files`; the PDF in `1 Lecture` will match once it is
re-exported (see *Notes for staff*).

| Step | File | What it is for |
| --- | --- | --- |
| 1 | Slides 1–2 | The problem: $n$ cities, costs $c_{ij}$, the cheapest closed tour |
| 2 | Slides 3–8 | Why it is hard: $(n-1)!/2$ tours (3 for 4 cities, about $2.6 \times 10^{19}$ for 22), brute force $O(n!)$, NP-completeness and P vs NP |
| 3 | Slides 9–11 | Applications, the TSP in the news, William Cook's TSP pages |
| 4 | Slides 12–14 | A first MILP: one arc out of and one arc into every city. It allows subtours |
| 5 | Slides 15–19 | The MTZ constraints $u_i - u_j + 1 \le (n-1)(1 - x_{ij})$ and why they leave a single tour |
| 6 | `2 Lecture Demos/1 TSP with Pyomo.ipynb` (slide 20) | The MTZ model in Pyomo: 4 cities (length **80**); 20 cities with MTZ (**407.97**) and without it (10 two-city subtours); a genetic algorithm on 35 cities (**599.24**; the optimum is 518.52) |
| 7 | Slide 21 | Heuristics: good tours without a proof that they are optimal; a visualisation video |
| 8 | Slide 22 (tutorial) | 1. In the demo notebook, grow the problem and change the genetic algorithm's settings. 2. Research: why the TSP is hard, NP-hard, combinatorial optimisation |
| 9 | `4 Tutorial Answers/Tutorial answers (slide 22).ipynb` | Solve times for 5 to 35 cities, five genetic-algorithm settings compared with the optimum, and answers to the research questions |
| 10 | *Optional:* slide 23 | Bill Cook's public lecture *Optimal Tours: The Traveling Salesman Problem* (about an hour) |

Both notebooks start with the problem, how to run them and the expected results, and explain every code cell. The
demo ends with a *What do you notice?* and a *Try it* question with hidden answers.

## By the end of this week you can

- state the TSP, count its tours, $(n-1)!/2$ for $n$ cities, and explain why trying them all is hopeless;
- say in a sentence what NP, NP-complete and NP-hard mean, and why a polynomial-time TSP algorithm would settle
  P vs NP;
- write the TSP as a MILP with binary $x_{ij}$, explain why "one arc in, one arc out" is not enough (subtours), and
  add the MTZ constraints;
- build and solve the model in Pyomo and read the tour from the solution;
- explain the difference between an exact method (the MILP: optimal, but slow as $n$ grows) and a heuristic (the
  genetic algorithm: fast, but with no guarantee).

**Next:** Week 10 (Vehicle Routing Problem): several vehicles, each with its own tour from a depot, built on the same
MTZ constraints. Section 1 of `1 TSP and VRP with Pyomo.ipynb` repeats this week's model, and Week 10's
`6 Further Reading` has the original MTZ paper (Miller, Tucker and Zemlin, 1960).

## Tutorial answers

| Question | Answer | Where |
| --- | --- | --- |
| 1. When does the MILP become unreasonable? | In the browser: 30 cities about 6 s, 35 about 20 s, 40 about 2.5 minutes (a desktop is several times faster). Time grows steeply and unevenly | Answers notebook, part 1(a) |
| 1. Genetic-algorithm settings | Demo settings: 15.6 % above the optimum 518.52; more mutation (0.8) 10.5 %; no crossover 35.7 % | Part 1(b) |
| 1. Larger problems than the MILP? | It returns a tour quickly for any size, but with no guarantee of quality | Part 1(b) |
| 2. Research | Why the TSP is hard, NP / NP-complete / NP-hard, combinatorial optimisation | Part 2 |

**More than one right answer.** Solve times depend on the computer, and the genetic algorithm's results on the seed
and the settings; the MILP's tour lengths do not change. A tour and its reverse are the same tour.

## Notes for staff

- The notebook's saved outputs (including the 4-city GLPK log and four plots) were cleared.
- The genetic-algorithm cell now fixes the seed (`random.seed(1)`, Oct 2026), so every run prints the same tour, length 599.24. Without a seed the length changed on every run (the old saved output was 625.16; test runs gave 704.08 and 573.67).
- The notebook gained a title cell and a short note before each code cell (Oct 2026); the empty last cell was removed. The code cells are unchanged.
- **Plot fix (Oct 2026).** `print_solution` and `plot_tsp_solution` drew an arc only if `value(x[i, j]) == 1`.
  HiGHS returns some chosen arcs as 0.9999999, so in the browser the 20-city tour plot missed one edge (16–12) and on
  a desktop three. Both now test `> 0.5`. No printed number changed.
- **Notebook text (Oct 2026).** The title cell now gives the problem, how to run it and the expected results; the
  model's constraints, the solver line and the genetic algorithm have comments; a *What do you notice?* and a *Try
  it* cell were added at the end. The code is otherwise unchanged.
- HiGHS prints the 4-city tour as 1 → 2 → 4 → 3 → 1; the original GLPK output had the reverse, 1 → 3 → 4 → 2 → 1
  (same length, 80). The `u` values differ too: the model gives `u` no bounds.
- **New (Oct 2026):** `4 Tutorial Answers/Tutorial answers (slide 22).ipynb` (no `.py` source). Its tour lengths
  are HiGHS's results within its default 0.01 % optimality gap; the solve times quoted in it and above are from the
  Pyodide 314.0.0 test run and a desktop run, and vary between computers.
- **The PDF in `1 Lecture` is older than the `.pptx`.** It was exported in February 2025; the `.pptx` was changed in
  November 2025: slide 10 is now titled *TSP in the news…* (PDF: *Santa TSP*), the PDF's page 12 *Visualisation* is
  now slide 21 *Heuristics* (after *Pyomo Code*), and *Pyomo Code* gained "Let's try and solve larger and larger
  problems…". **Re-export the PDF from PowerPoint.**
- **Lecture slides (Oct 2026).** The `.pptx` in `5 Source Files` was corrected; **the PDF has not been re-exported
  yet**: 7 NP is "nondeterministic polynomial time" (it said "Non-polynomial"); "NP" means a solution can be
  *checked* in polynomial time and "complete" means among the hardest problems in NP (the slide had it the other way
  round and said a polynomial-time algorithm *cannot* exist, which is the open P vs NP question); finding the
  shortest tour is NP-hard. 18 the edge into city 1 comes from $r_n$, so $k = r_n$ (it said $k = 1$), and city 1
  (it said city $i$) is left out of the MTZ constraints. 17 "an increasing sequence of $u_i$". 12 "$x_{ij} = 1$ if
  the edge … is used (0 otherwise)", "Why is this formulation wrong?". 4 "3! possible routes". 5 "the time taken
  grows roughly like $n!$". 6 the *Washington Post* article is of 5 February 2018 (it said 15th). 20 and 22 point
  to the notebook on the course site (they said Blackboard and a Google Colab copy that needs a sign-in). The text on
  slides 4–7, 12, 17 and 18 sits in boxes with equations that keep a stored picture of the old text, which only
  LibreOffice and old viewers show. **Re-export from PowerPoint.**
