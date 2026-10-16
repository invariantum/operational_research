# Semester 1 · Week 10 – Vehicle Routing Problem

From the travelling salesman problem (TSP) to vehicle routing: several tours that all start and end at a depot,
customers with a demand, vehicles with a capacity, and two objectives, the total distance and the longest route.
The models are mixed-integer linear programs (MILPs) solved in Pyomo. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and the lecture notes (`Notes/`, with a PDF copy) | The lecture |
| `2 Lecture Demos` | `1 TSP and VRP with Pyomo.ipynb`: the three models of the lecture on one 8-node example | Run in the lecture; its *Try it* questions are this week's practice |
| `5 Source Files` | Editable slides (.pptx), HTML exports of the notes, an earlier draft of the notes | Staff only; edit here, then republish the PDFs |
| `6 Further Reading` | The two original papers: Miller, Tucker and Zemlin (1960) and Christofides (1976) | Optional |

## Before you start

- **Week 09:** the TSP as a MILP and the Miller–Tucker–Zemlin (MTZ) constraints
  $u_i - u_j + 1 \le (n-1)(1 - x_{ij})$. This week starts from that model.
- **Week 05:** binary variables and big-M constraints (a constraint switched on or off by a binary variable).
- **Week 08:** networks: nodes, arcs and arc costs.
- **Python:** a Pyomo model as in Weeks 03–05 (`Var`, `Constraint` with a rule, `Objective`,
  `SolverFactory('appsi_highs')`).

## Work through this week in order

Slide numbers are those of the `.pptx`. Slide 2 is hidden, so in the PDF the page number is the slide number minus 1.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | Slides 3–5 | The TSP reminder: one arc in and one arc out of every city still allows *subtours* |
| 2 | Slides 6–13 | The MTZ constraints: why they force one tour, why city 1 is left out, why $M = n - 1$, the compact model |
| 3 | `1 Lecture/Notes/Routing Problems - Lecture Notes.md`, sections *Travelling Salesman Problem* and *Explaining the MTZ Subtour Constraint* | The same argument in more detail, with Pyomo code |
| 4 | Slides 14–17 | Several tours from city 1: relax city 1's constraints and fix the number of arcs leaving it |
| 5 | Slides 18–24 | The vehicle routing problem (VRP): what "optimal" means, demand and capacity, minimise the total distance |
| 6 | Slides 25–28 | The flow model with capacity, and why its flow constraints already rule out subtours |
| 7 | `2 Lecture Demos/1 TSP and VRP with Pyomo.ipynb`, sections 1–2 | TSP without MTZ: **233.4** (subtours), with MTZ: **281.4** (one tour); VRP, total distance: **327.6** with two full vehicles |
| 8 | Slides 29–33 | Deliver as quickly as possible: one copy of the network per vehicle, minimise the longest route $C_{Max}$ |
| 9 | Notebook section 3, *What do you notice?* and *Try it* | Longest route **137.4** with three vehicles (total 362.5). Questions on capacity, fleet size, an extra customer and the cost of balancing; answers are hidden in the notebook |
| 10 | Slides 34–35; notes sections *Limitations of the Model* and *NP-Hard Problems and Heuristic Solutions* | Routing on a subgraph, extensions (time windows, mixed fleets), heuristics such as nearest neighbour |
| 11 | *Optional:* `6 Further Reading` | The original MTZ paper (1960) and Christofides' survey of the VRP (1976) |

The notes are Markdown: right-click → *Open With* → *Markdown Preview*. `1 Lecture/Lecture Notes - Routing Problems.pdf`
is a PDF copy of the same notes.

## By the end of this week you can

- explain why the MTZ constraints remove subtours, why city 1 is left out of them and why $M = n - 1$ is enough;
- turn the TSP into a model with $m$ tours from a depot;
- write the capacitated VRP with flow variables $f_{ij}$, and explain why flow conservation with positive demands
  rules out subtours;
- write the minimax VRP with per-vehicle variables $x_{ijk}$, $f_{ijk}$ and $C_{Max}$, and explain why each vehicle
  must leave every location it enters;
- solve both models in Pyomo and compare them: the total distance against the length of the longest route.

**Next:** Week 11 (Floor Planning): binary variables again, this time to stop rectangles from overlapping.

## Practice answers

The week has no tutorial sheet; the practice questions are at the end of the demo notebook, with hidden answers.

| Question | Answer |
| --- | --- |
| Why does model 2 use only two vehicles? | Every route drives out of the depot and back, so fewer routes are shorter in total: two full vehicles (15 + 15 = 30) give 327.6 |
| `capacity = 12` | Two vehicles carry only 24 < 30, so model 2 uses three routes, total 362.5; models 1 and 3 do not change |
| `num_vehicles = 2`, `capacity = 14` | 2 × 14 = 28 < 30: infeasible. The model-2 cell stops with "A feasible solution was not found" |
| Customer 9 at (60, 70), demand 2 | TSP 288.8; model 2 total 363.8 (three routes); model 3 longest route still 137.4 |
| Model 2 vs model 3 | Balancing adds 34.9 to the total (+10.7 %) and cuts the longest route by 35.4 (−20.5 %) |

A route may be printed in the opposite direction; its length is the same.

## Notes for staff

- `2 Lecture Demos/1 TSP and VRP with Pyomo.ipynb` is a companion notebook written for this repository. Slide 36 used
  to link to a separate Google Colab notebook (https://colab.research.google.com/drive/1BLPImK2TcdCrTaTN2-N6b2z3QNdUXpMe),
  which is not in the repository; it now links to this notebook on the course site (Oct 2026).
- **Notebook text (Oct 2026).** The title cell gives the problem, how to run it and the expected results; a cell
  before the data explains the data and helper functions; models 1 and 2 have a comment for each constraint; a
  *What do you notice?* question and answers to the four *Try it* questions were added. The code is unchanged. The
  expected results were checked in Pyodide 314.0.0 (HiGHS 1.13.1) and on a desktop (HiGHS 1.15.1).
- **In the browser** the test run printed HiGHS's full solver log after every solve (the first cell switches off
  Pyomo's output capture); a desktop prints nothing. Check whether the log shows on the course site.
- **Lecture slides (Oct 2026).** The `.pptx` was corrected; **the PDF has not been re-exported yet**:
  6 $r_k$ is the city visited $k$-th (it said "the order in which city $j$ is visited"), and $u_i$ "need not equal the
  position". 7 $u_j > u_i$ (it said $u_j > u_j$). 8, 11, 12 the MTZ constraint is $u_i - u_j + 1 \le M(1 - x_{ij})$:
  the slides had $u_j - u_i$, which gives $u_i > u_j$, the opposite of what slides 6–7 ask for. 9 "an increasing
  sequence". 10 $k = r_n$ (it said $k = 1$). 12 no "1 < … < 1"; $M \ge u_{r_n} - u_{r_2} + 1 \ge n - 1$.
  16 several chains, each joined to location 1 (the slide said the chain *must* start and end at 1, then "Instead").
  20 "Royal Mail", "There is no capacity", the parcel sentence reworded. 21, 31 the depot is location 1 (it said 0).
  21 $m$ vehicles (it said $K$). 22 it is the depot constraint that is relaxed. 23 with the triangle inequality one
  vehicle is always among the best. 24 "deliver". 25, 32 $V$ includes the depot; 25 $x_{ij}$ has no $k$.
  27 subtours are impossible if every $q_i > 0$ (zero demands allow them too). 28 says which model the example uses.
  31 $q_i$ (it said $d_i$). 36 links to the notebook on the course site. As in Week 09, the boxes with equations keep a
  stored picture of the old text, which only LibreOffice and old viewers show. **Re-export from PowerPoint.**
- **Slide 33 (Full Model) is a picture and was not corrected.** Fix it at its source and paste it again: the labels of
  the first two constraints are swapped ($\sum_j x_{ijk}$ counts the arcs *leaving* $i$); "less than $Q_{max}$" should
  be $C_{Max}$; "Length of a route is less than vehicle capacity" should be "the load on an arc is at most the vehicle
  capacity"; and the constraint "if vehicle $k$ enters location $i$ then it must leave location $i$" belongs in the
  model, not under "Optional" (without it the route lengths, and so $C_{Max}$, mean nothing; the notebook's `mm.cont`
  and the notes include it). Slide 27's picture labels "Flow conservation for $j$, $k$, $i$" mean $r_j$, $r_k$, $r_i$.
- **Lecture notes (Oct 2026).** `Routing Problems - Lecture Notes.md` was corrected: the minimax model (the same four
  points as slide 33), "$u_i$ orders the cities", the $r_k$ definition, $r_2$ / $r_n$, the $M \ge n-1$ chain, $m$ tours,
  $q_i \le 0$, "$Q$ is the largest number of locations one vehicle can visit", minimum-cost flow (it said
  "multi-commodity flow"), typos and British spelling. Its Pyomo code now runs: the TSP printout used an undefined
  `cities`, model 1 overwrote the node set with the vehicles and had no `u`, model 2 used undefined `Qmax` and `c`, and
  both called GLPK; they now use HiGHS and reproduce the notebook's 327.6 and 137.4. The two "PLACEHOLDER IMAGE"
  lines, the author's "currently working on these notes" note and a dead MathJax `<script>` were removed.
- **`1 Lecture/Lecture Notes - Routing Problems.pdf` is out of date** (March 2025): it still shows the placeholder
  label "dsad" on three MTZ constraints and the errors above. **Re-export it from the `.md`** (the current PDF was printed
  from a browser, Edge).
- `5 Source Files/HTML Exports` holds VS Code HTML exports of both notes. They predate the October 2026 corrections
  (apart from the "dsad" labels and image links, fixed earlier); re-export them from VS Code if you want them current.
  Their images point to `1 Lecture/Notes/assets`.
- `5 Source Files/Previous Versions/Routing - Short Notes for the Lecture (earlier draft).md` was in `1 Lecture/Notes`
  until October 2026. It is a shorter, earlier draft of the full notes, and its minimax model is wrong: the objective
  is $Q_{Max}$ and the route length adds up the flows $f_{ijk}$ instead of the distances $c_{ij}x_{ijk}$.
- Removed in Oct 2026: `5 Source Files/Images/Routing.jpeg`, a full-page image of the old notes (it still showed
  "dsad"); and earlier, an older export of the slides (March 2025) and an older HTML export of the notes.
