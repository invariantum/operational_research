# Semester 1 · Week 05 – Mixed Integer Programming

Binary (yes/no) variables: the knapsack problem, set covering (fire stations), logical conditions in a purchasing
problem ("if you order it, order at least 6", "at most two items", "item 1 or item 4"), and a first look at vertex
cover. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) | The lecture |
| `2 Lecture Demos` | Eight notebooks, numbered in the order the slides use them | Run live in the lecture |
| `3 Tutorial` | Tutorial 5 sheet | The practical |
| `4 Tutorial Answers` | Worked answers (PDF) and five answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals: `.pptx`, `.docx`, the Python scripts the notebooks came from, MATLAB versions of the tutorial answers | Staff only; edit here, then republish the PDF / notebook |

## Before you start

- **Week 03:** integer and mixed-integer LPs in Pyomo (`NonNegativeIntegers`), and the Icki-Toffee model
  (tutorial Q2). This week's demo 1 is the Week 03 integer LP again, as a review.
- **Week 04:** writing constraints with `sum(...)`, and the Icki-Toffee weight cap of $1.5 \times 320$ g
  (tutorial Q1a), which this week's Q3 keeps.
- **Maths:** summation notation $\sum_i c_i x_i$; reading a table of distances.
- **Python and Pyomo:** a `ConcreteModel`, variables, an objective and constraints, solved with
  `SolverFactory('appsi_highs')`. Each notebook's first cell installs Pyomo and HiGHS; run it first.

## Work through this week in order

Page numbers are the pages of the lecture PDF.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | `1 Lecture/Week 5 - Mixed Integer Programming.pdf`, pages 1–7 | Review: what a MILP is; the LP optimum $(1.9, 2.9)$ and why rounding it fails |
| 2 | `2 Lecture Demos/1 Integer LP.ipynb` | Page 8: the integer optimum $(3, 2)$, $P = 13$, in Pyomo |
| 3 | Lecture PDF, pages 9–12 | Binary variables; the knapsack problem and its model |
| 4 | `2 Lecture Demos/2 Knapsack problem.ipynb` | Page 13: 7 items, 10 kg, best value £170 |
| 5 | Lecture PDF, pages 14–19 | Set covering: from a table of driving times to one constraint per city |
| 6 | `2 Lecture Demos/3 Fire stations - set covering.ipynb` | Page 20: two stations, in cities 2 and 4 |
| 7 | `2 Lecture Demos/4 Purchasing - basic model.ipynb` | Pages 21–22: the purchasing LP (profit 84.44), before any binary variables |
| 8 | `2 Lecture Demos/5 Purchasing - binary variables.ipynb` | Pages 23–25: "if ordered, 6 to 10 kg" with $x_i \le 10\delta_i$, $x_i \ge 6\delta_i$ (profit 81.6) |
| 9 | `2 Lecture Demos/6 Purchasing - order at most two items.ipynb` | Pages 26–27: $\sum_i \delta_i \le 2$ (profit 80) |
| 10 | `2 Lecture Demos/7 Purchasing - item 1 or item 4.ipynb` | Pages 28–29: $\delta_1 + \delta_4 \le 1$ (profit 76.67) |
| 11 | `2 Lecture Demos/8 Minimum vertex cover.ipynb` (optional) | Not on the slides: a preview of Week 06. Every constraint covers one edge of a graph |
| 12 | `3 Tutorial/Week 5 - Mixed Integer Programming Tutorial.pdf` | Q1 (desert-island knapsack, three versions), Q2 (fire stations, 7 cities), Q3 (Icki-Toffee with variety rules, marked hard) |
| 13 | `4 Tutorial Answers/` | Check your work after you have tried the questions: the PDF, then the notebooks below |

Each notebook starts with the problem, how to run it and the expected result, explains every code cell, and ends
with a short *What do you notice?* or *Try it* question with a hidden answer.

In the browser, HiGHS prints its solver log even when the code says `tee=False`; the results are not affected.

## By the end of this week you can

- explain why rounding an LP solution does not give the integer optimum;
- model a yes/no decision with a binary variable, and write the knapsack and set covering problems;
- turn a table of distances into set covering constraints;
- link a binary variable to an amount ($x_i \le U\delta_i$, $x_i \ge L\delta_i$) to model "if you order it, order
  between $L$ and $U$";
- write logical conditions with binary variables: "at most $k$ items" ($\sum_i \delta_i \le k$) and "not both"
  ($\delta_1 + \delta_4 \le 1$);
- recognise problems with several optimal answers, where your selection may differ from the answer sheet.

**Next:** Week 06 (Integer Linear Programming - Further Problems) returns to the fire stations with building
costs (demos 1–3) and to vertex cover with security cameras (demo 4), and adds the assignment problem.

## Lecture demos (`2 Lecture Demos`)

| Notebook | PDF pages | Shows | Result |
| --- | --- | --- | --- |
| `1 Integer LP` | 8 | Integer variables (`NonNegativeIntegers`) | $x = 3$, $y = 2$, $P = 13$ |
| `2 Knapsack problem` | 11–13 | Binary variables, one capacity constraint | £170: items 5 and 7 (items 4 and 7 also give £170) |
| `3 Fire stations - set covering` | 14–20 | One "at least one station" constraint per city | 2 stations: cities 2 and 4 |
| `4 Purchasing - basic model` | 21–22 | The LP before binary variables | 84.44: items 1 and 4 (10 kg each), 1.11 kg of item 3 |
| `5 Purchasing - binary variables` | 23–25 | Minimum order of 6 kg with $\delta_i$ | 81.6: items 1 and 3 (6 kg each), 9.2 kg of item 4 |
| `6 Purchasing - order at most two items` | 26–27 | $\sum_i \delta_i \le 2$ | 80: items 1 and 4 (10 kg each), £150 spent |
| `7 Purchasing - item 1 or item 4` | 28–29 | $\delta_1 + \delta_4 \le 1$ | 76.67: item 1 (10 kg), 6.67 kg of item 3 |
| `8 Minimum vertex cover` | – | Vertex cover as set covering (preview of Week 06) | 3 vertices (several optimal sets) |

## Tutorial answers (`4 Tutorial Answers`)

| Notebook | Question | Answer |
| --- | --- | --- |
| `Q1a Desert island knapsack` | Q1a | 270: items 4, 5 and 7 (15 kg) |
| `Q1b Desert island knapsack` | Q1b | 350: five of item 7 |
| `Q1c Desert island knapsack` | Q1c | 250: items 1, 2, 3, 7 and 8 |
| `Q2 Fire stations - set covering` | Q2 | 3 stations; the notebook shows cities 1, 2, 6 and the answer sheet 3, 4, 7 (both are optimal) |
| `Q3 Icki-Toffee - binary variables` | Q3 | Cost 310; several selections reach it (see the notebook) |

- `Week 5 - Mixed Integer Programming Tutorial - Answers.pdf`: the three questions formulated by hand; the
  solutions are MATLAB screenshots, which the notebooks reproduce.

## Notes for staff

- **Slide and page numbers.** The `.pptx` has three hidden slides (3, 22 and 23) that the PDF leaves out, so
  `.pptx` slides 4–21 are PDF pages 3–20 and slides 24–32 are PDF pages 21–29. The README and the notebooks give
  PDF page numbers. Hidden slides 22–23 (general set covering) are not used; their example also has a cover of
  two sets, $\{s_1, s_4\}$.
- The answers (.docx and PDF) gained a side note on Q3: two different selections both cost 310. The PDF was edited
  directly, so its wording differs slightly from the .docx; re-export the PDF from the .docx.
- The answer screenshots show MATLAB output; the notebooks in `4 Tutorial Answers` give the same optimal values.
  With HiGHS the Q2 and Q3 selections differ from the screenshots (both optimal); vertex cover (demo 8) also has
  several optimal sets, and the browser and desktop versions of HiGHS pick different ones.
- The notebooks use HiGHS (`SolverFactory('appsi_highs')`) so they run in the browser; the scripts in
  `5 Source Files/Python` still use GLPK for desktop use. Optimal values match.
- In the browser, HiGHS prints its log even with `tee=False` (the first cell switches off Pyomo's output capture,
  which needs threads). The notebooks say so.
- Slides 26, 27, 29 and 31 of the `.pptx` showed the cost column again under "Expected Profit"; corrected to 5, 3,
  4, 3, 3 (as on slides 24–25 and in the notebooks). The lecture PDF was re-exported on 12 Oct 2026 and shows the
  corrected values.
- **Notebooks (Oct 2026), text only.** Each notebook gained an opening cell (problem, how to run it, expected
  result), a short explanation above every code cell, a comment on each constraint row and a closing *What do you
  notice?* / *Try it* cell with a hidden answer. Wrong or unclear comments were fixed: "with lower and upper
  bounds" above `NonNegativeIntegers` (demo 1, there is no upper bound), "Define binary variables" above
  `NonNegativeIntegers` (Q1b), the vertex-cover constraints named `city1`–`city5` (they are edges), and
  `fat_weight_min` explained as an upper limit (Q3). No code and no printed result changed.
- **Corrections (Oct 2026), lecture slides.** The `.pptx` in `5 Source Files` was corrected; **the PDF in
  `1 Lecture` has not been re-exported yet** (`.pptx` slide numbers, PDF pages in brackets):
  - slide 14 (p. 13): the sums run to 7, the number of items (they said 6);
  - slide 27 (p. 24): "$\delta_i$ – 1 if item $i$ picked, 0 if item $i$ not picked" (it was the wrong way round;
    the text below it already used $\delta_i = 1$ for "chosen");
  - slides 15–19 (pp. 14–18): driving time from city 5 to city 1 is 30 (it said 20, but city 1 to city 5 is 30);
    the answer is unchanged, as both are over 15 minutes;
  - slide 15 (p. 14): "within 15 minutes of each city" (it said "near 15 minutes");
  - slides 24, 26–28 (pp. 21, 23–25): minimum order "at least 6" (it said "greater than 6", but the model uses
    $x_i \ge 6\delta_i$);
  - slides 29–30 (pp. 26–27): "at most 2 items" (it said "a most");
  - slides 25–27, 29, 31 (pp. 22–24, 26, 28): table headings "Cost (per kg)" and "Expected Profit (per kg)" as on
    slide 24 (they said "(kg)" or "(g)"); slide 25 (p. 22): "$P_i$ - Profit (per kg) for item $i$", "$c_i$ - Cost
    (per kg) for item $i$" (it said "per item");
  - smaller fixes: slide 5 (p. 4) the examples now include $-x + y \le 1$, as on pages 5–8; slide 7 (p. 6)
    $P = 9$ and $P = 11$ without the star, which marks the optimum; slides 17, 19 and 21 (pp. 16, 18, 20) the sum
    runs from $i = 1$ to 6; slides 13–14 (pp. 12–13) "Weight (kg)".
  - Not changed (pictures): the code on slides 9, 14, 21, 28, 30 and 32 uses GLPK; slide 9 says "Define the
    integer decision variables with lower and upper bounds" (there is no upper bound) and shows a MATLAB output box
    (`sol`, `fval = -13`) next to the Pyomo code.
  - The edited equations (slides 5, 7, 14, 17, 19, 21 and 27) also keep a stored picture of the old text, which
    only LibreOffice and old viewers show. **Re-export from PowerPoint**, as on 12 Oct. Check that slide 5 still
    fits now that each example has a third constraint.
- **Corrections (Oct 2026), tutorial and answers `.docx`** (`5 Source Files`; **the PDFs have not been
  re-exported yet**): Q3 now says "at least 320g", "at most 45%" and "at most 2850 calories" (as in Weeks 03–04;
  the model uses $\ge$ and $\le$). Answers only: the Q1 objective sums run to 8, the number of items (they said
  6); the empty box above the other Q1 sums is gone; "$s_i$ – survival value of item $i$" (it said "(kg)"); and
  the Q3 formulation gained the missing weight cap $\sum_i W_i x_i \le 480$ (the code already had it; it does not
  change the answer).
