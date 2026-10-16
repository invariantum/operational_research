# Semester 1 · Week 11 – Floor Planning

Floor planning (rectangle packing): place rectangles on a floor without overlaps, using as little space as
possible. Two rectangles do not overlap when *at least one* of four inequalities holds (left of, right of, below,
above); two binary variables per pair and a big-M choose which one. The model minimises the side of the smallest
square that holds every item (a *minimax* objective) and then lets each item rotate. Two variants fix the floor and
maximise the number of items or the area placed. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF); `Notes`: the Pyomo model of demo 1 in one piece, to read (`.md`) | The lecture |
| `2 Lecture Demos` | `1 Floor planning - minimise area.ipynb`, then two optional variants with a fixed floor (2 and 3) | Run live in the lecture; their *Try it* questions are this week's practice |
| `5 Source Files` | Editable slides (.pptx), the original script (`Python/model.py`), an HTML export of the notes, and the three MATLAB models the notebooks reproduce | Staff only; edit here, then republish the PDF |

## Before you start

- **Week 05:** binary variables and big-M "either/or" constraints. Here a pair of binaries chooses one of four
  constraints.
- **Week 07:** the job-shop model uses the same idea for two jobs on one machine (one goes first); floor planning
  does it in two dimensions.
- **Maths:** inequalities, the number of pairs $\binom{n}{2}$, and the idea of minimising the largest of several
  values.
- **Python:** a Pyomo model as in Weeks 03–05 (`Var`, `Constraint` with a rule, `Objective`,
  `SolverFactory('appsi_highs')`).

## Work through this week in order

Page numbers are those of the PDF in `1 Lecture`. The `.pptx` has a hidden slide 2, so its slide numbers are one
higher from page 2 on.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | Pages 2–4 | Warm-up: an LP, then the same problem with $x$ integer (optimum 13.917 at (2, 2.833)) |
| 2 | Pages 5–8 | The problem: tables $t_i$ with width $w_i$, height $h_i$ and corner $(x_i, y_i)$, which must not overlap |
| 3 | Pages 9–16 | Four ways for two tables not to overlap; binaries $x_{ij}, y_{ij}$ and a big-M switch on exactly one; $4\binom{n}{2}$ constraints |
| 4 | Pages 17–19 | The minimax objective: minimise $A^*$, the side of the smallest square. $A^* = 12$ for 4 and for 6 items |
| 5 | Pages 20–23 | Rotation: a binary $r_i$ swaps width and height; the four tables now fit in 11 × 11 |
| 6 | `2 Lecture Demos/1 Floor planning - minimise area.ipynb` | The rotation model in Pyomo for six items: **v = 12** (a 12 × 12 square). *Try it*: rotation off (12), the slides' four tables (11), the eight pieces of page 33 (5) |
| 7 | Pages 24–31 | A fixed floor $W \times H$ and connected items: minimise the rectilinear distance between their centres; a chemical-plant layout |
| 8 | Pages 32–34 | Back to packing: a person beats the solver (page 33), and why: $2^{2\binom{n}{2}}$ combinations of the pair binaries |
| 9 | *Optional:* `2 Lecture Demos/2 Floor planning - maximise number of items.ipynb` | Fixed 4 × 5 floor, seven items: at most **6** fit (area 21 > 20). **Allow 2–4 minutes** for the solve in the browser; its *Try it* adds the area as a constraint and solves in under a second |
| 10 | *Optional:* `2 Lecture Demos/3 Floor planning - maximise placed area.ipynb` | The six items on a 10 × 10 floor: area placed **100** (the whole floor), item 3 left out |
| 11 | Page 35 | Conclusion: packing is NP-hard |

Each notebook starts with the problem, how to run it and the expected result, explains every code cell, and ends
with a *What do you notice?* and a *Try it* question with hidden answers.

## By the end of this week you can

- write "rectangles $i$ and $j$ do not overlap" as four inequalities, of which at least one must hold;
- use two binary variables and a big-M to enforce exactly one of the four, and count the constraints for $n$ items;
- write and explain a minimax objective (the smallest enclosing square);
- add rotation with one binary per item, and adapt the model to a fixed floor where items may be left out;
- explain why these models slow down quickly as items are added, and how an extra valid constraint (total area)
  can speed them up.

**Next:** Semester 2, Week 01 (Introduction to Simulation). The modelling of Weeks 02–11 is assessed in coursework
part A (`Assignments/01-coursework-part-a`).

## Tutorial

There is no tutorial sheet this week. Practise with the *Try it* questions at the end of the three notebooks; the
answers are in the notebooks (click *Answer*).

## Notes for staff

- The handbook lists *Inventory Modelling* for Week 11; this folder holds the Floor Planning lecture instead.
- Notebooks 2 and 3 are Python ports of the MATLAB *max items* and *max item area* models
  (`5 Source Files/MATLAB`), with the same data and constraints. Optima: 6 of 7 items (all 7 need area 21 > 20) and
  placed area 100 (the whole floor; only leaving out item 3, area 24, makes that possible).
- **Big-M (checked Oct 2026).** The ports use `M = W + H + max(w, h)` instead of MATLAB's 9999, and no time limit
  (the *max items* MATLAB file stops after 10 s). An earlier note said M = 9999 made the solver report a wrong
  optimum of 5 items; this was **not reproduced**: with M = 9999 the browser (Pyodide 314.0.0, HiGHS 1.13.1) and a
  desktop (HiGHS 1.13.1 and 1.15.1) all find 6 items with a valid layout. The smaller M is kept as good practice.
  The *minimise area* notebook keeps 9999: the browser prints `v= 12.0`, a desktop `v= 11.999999` (rounding).
- **Results checked (Oct 2026).** `model.py` with GLPK and demo 1 both give v = 12, in Pyodide and
  on a desktop (different, equally good layouts). Also reproduced with HiGHS: the slides' four tables give 12
  without rotation and 11 with rotation; the eight pieces of *Mums Know Best!* give 5 (about 9 s in the browser).
- **Solve times.** Demo 2 about 2 minutes in the automatic Pyodide test (under a minute on a desktop); the others a
  few seconds. With the *Try it* area constraint demo 2 takes under a second.
- `model.py`, `Notes/Floor Planning - Pyomo Model.md` and the HTML export were fixed earlier: `cm.get_cmap` (removed
  in Matplotlib 3.9) became `plt.get_cmap`, and the HTML export no longer links a stylesheet on the author's
  computer. The notes `.md` still names GLPK; it is a reading copy, and the notebooks use HiGHS.
- **Notebook text (Oct 2026).** All three demos gained an opening cell (problem, how to run it, expected result), a
  note above each code cell, a comment on each constraint, and *What do you notice?* / *Try it* cells. The code and
  the results are unchanged. Demo 3's solve comment now says the
  MATLAB file has no time limit (it said 10 s), and demo 2's big-M comment no longer claims a false optimum.
  Notebooks 2 and 3 were given cell ids.
- **Removed (Oct 2026):** `1 Lecture/Notes/Floor Planning - Pyomo Model.ipynb`, a one-cell notebook made from the
  notes `.md`. Its code was the same as demo 1's (it also gave v = 12), so it duplicated demo 1 without the
  explanations.
- **MATLAB files (not changed; not run).** In the two *max* files `plot(pgon)` is outside `if ui(i)`, so a left-out
  item redraws the previous one (and an error follows if item 1 is left out); the legends list 4 names for 6 items
  (*min area*, *max item area*) and 6 for 7 (*max items*).
- **Lecture slides (Oct 2026).** The `.pptx` in `5 Source Files` was corrected; **the PDF has not been re-exported
  yet** (PDF page = slide − 1): 7–8 the fourth table is $t_4$ (it said $t_5$); 7 "finds the smallest square that
  holds them all" (it said "minimises the squared area"), "its position"; 14 "two tables don't overlap exactly when
  at least one of these 4 constraints holds"; 18 "known as a minimax problem … the upper bound $A^*$ on the
  left-hand sides"; 22 "width and height are swapped"; 27 *Boundary constraints* (it said *Minimax constraints*,
  but there is no $A^*$ there) and "if the items did not have to stay within a boundary"; 28 $Dy_{ij}$ (it said
  $Dy$). The text on slides 7, 8, 14, 18, 27 and 28 sits in boxes with equations that keep a stored picture of the
  old text, which only LibreOffice and old viewers show. **Re-export from PowerPoint.**
- Slide 5 (PDF page 4) shows `fval = -13.9167`: `intlinprog` minimises, so it reports $-P$. This is part of a
  screenshot and was not changed; mention it when presenting. Slide 2 is a hidden blank slide.
