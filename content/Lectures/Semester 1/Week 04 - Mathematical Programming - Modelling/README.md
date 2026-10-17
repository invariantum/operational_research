# Semester 1 · Week 04 – Mathematical Programming - Modelling

Writing models in Pyomo, slack variables, and choosing an objective when there are two aims (cost and
popularity) for the Icki-Toffee problem. Work through the folders in number order.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and the *Slack Variables* demonstration | The lecture |
| `2 Lecture Demos` | One notebook: linear expressions and constraints in Pyomo | Run live in the lecture |
| `3 Tutorial` | Tutorial 4 sheet | The practical |
| `4 Tutorial Answers` | Worked answers (PDF) and six answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals: `.pptx`, `.docx`, the Python scripts the notebooks came from, MATLAB versions | Staff only; edit here, then republish the PDF / notebook |
| `6 Further Reading` | Two R. E. D. Woolsey papers on real-world modelling | Optional reading |

## Before you start

- **Week 03:** the Icki-Toffee model (tutorial Q2): minimise cost (268) and maximise popularity (365). This week
  adds a weight cap and asks for a better objective.
- **Maths:** summation notation $\sum_i c_i x_i$; inequality constraints ($\le$, $\ge$).
- **Python and Pyomo:** a `ConcreteModel`, variables, an objective and constraints, solved with
  `SolverFactory('appsi_highs')` (Week 03 demos). Each notebook's first cell installs Pyomo and HiGHS; run it first.

## Work through this week in order

Page numbers are the pages of the lecture PDF.

| Step | File | What it is for |
| --- | --- | --- |
| 1 | `1 Lecture/Week 4 - Mathematical Programming - Modelling.pdf`, pages 1–4 | Why constraints use $\le$ / $\ge$ and not $<$; a sum $\sum_i a_i x_i$ is the matrix product $a^T x$ |
| 2 | `2 Lecture Demos/1 Pyomo expressions and constraints.ipynb` | Pages 5–6: build $10x_1 + 6x_2 + 8x_3 + 16x_4$ by hand or with `sum(...)`; make, replace and switch off constraints |
| 3 | Lecture PDF, pages 7–9 | Recap: the diet problem (Week 02 tutorial Q6a) in summation notation and Pyomo |
| 4 | Lecture PDF, pages 10–14 | Recap of the Icki-Toffee results; interpreting a model, opinion and preference |
| 5 | Lecture PDF, pages 15–16 | Extending the model: a weight cap of $1.5 \times 320$ g (this is tutorial Q1a) |
| 6 | Lecture PDF, pages 17–23 | Two aims in one objective: ratio (pp. 18–19), weighted (p. 20), normalised weighted (pp. 21–23) |
| 7 | Lecture PDF, pages 24–26 | Solve the LP first; the steps of modelling; under- and over-modelling |
| 8 | `1 Lecture/Slack Variables.pdf` | Slack variables: the unused amount of a $\le$ constraint; binding and non-binding constraints. Needed for tutorial Q2a ii |
| 9 | `3 Tutorial/Week 4 - Mathematical Programming - Modelling - Tutorial.pdf` | Q1 (Icki-Toffee: weight cap, then your own objective: copy a Week 03 Q2 notebook and change it), Q2 (two factories: separate models, then one combined model) |
| 10 | `4 Tutorial Answers/` | Check your work after you have tried the questions: the PDF, then the notebooks below |
| 11 | `6 Further Reading/` (optional) | Woolsey's case studies; the *Inflexible Steel Company* (mentioned on page 26) is in *A Novena to St. Jude* |

Each notebook starts with the problem, how to run it and the expected result, explains every code cell, and ends
with a short *What do you notice?* or *Try it* question with a hidden answer.

## By the end of this week you can

- explain why a model uses $\le$ / $\ge$, and write $\sum_i a_i x_i$ as $a^T x$ and as `sum(...)` in Pyomo;
- create, print, replace and deactivate constraints in Pyomo;
- extend a model with a new constraint (the weight cap) and explain why it changes some answers and not others;
- combine two aims into one objective (a ratio, a weighted sum, a normalised weighted sum) and explain how the
  weight $\alpha$ and the scale of the data change the answer;
- use slack to find unused capacity and to tell binding from non-binding constraints;
- show that planning two factories together can beat planning them separately.

**Next:** Week 05 (Mixed Integer Programming) adds binary (yes/no) variables, which can force variety in the
Icki-Toffee box (Week 05 tutorial Q3), the issue left open on page 15.

## Lecture demo (`2 Lecture Demos`)

| Notebook | PDF pages | Shows |
| --- | --- | --- |
| `1 Pyomo expressions and constraints` | 5–6 | Linear expressions written by hand and with `sum(...)`; a constraint and an objective; replacing and deactivating constraints |

## Tutorial answers (`4 Tutorial Answers`)

All three Q1b notebooks include the Q1a weight cap ($\le 480$ g).

| Notebook | Question | Answer |
| --- | --- | --- |
| `Q1b Icki-Toffee - popularity per cost ratio` | Q1b | 8 Coconut Ice, 32 Lime sherbet, 8 Rose-water posy (480 g) |
| `Q1b Icki-Toffee - weighted objective` | Q1b | $\alpha = 0$: popularity 305 (several selections reach it); *Try it*: $\alpha = 0.6$ gives the minimum-cost box |
| `Q1b Icki-Toffee - normalised weighted objective` | Q1b | $\alpha = 0.59$: 9 Caramel softie, 10 Rose-water posy, 3 Grape bunch (cost 268); *Try it*: $\alpha = 0.5$ gives 24 Coconut Ice, 11 Rose-water posy |
| `Q2a Factory A` | Q2a i–ii | 10 standard, 8 deluxe, £220; unused hours: grinding 24, polishing 0 |
| `Q2a Factory B` | Q2a i–ii | 0 standard, 11 deluxe, £165; unused hours: grinding 27, polishing 9 |
| `Q2b Factories combined` | Q2b i–ii | A: 10 standard, 8 deluxe; B: 12 deluxe; £400 (vs £385); raw material 72 kg : 48 kg |

- `Week 4 - Mathematical Programming - Modelling - Tutorial - Answers.pdf`: Q1–Q2 worked by hand. Q1b is open
  ("justify your choice"), so the answers point to the notebooks.

## Notes for staff

- The lecture had no PDF; `1 Lecture/Week 4 - Mathematical Programming - Modelling.pdf` was exported from the .pptx.
- **Slide and page numbers.** The `.pptx` has a hidden blank slide 3 that the PDF leaves out, so from slide 4 on a
  `.pptx` slide number is one higher than the PDF page number. The README and the notebooks give PDF page numbers.
- A Windows `debug.log` was removed.
- Two scripts in `5 Source Files/Python` were fixed: a stray line `model.w` in `icki_toffee_cost_pop_ratio.py` and a stray line `era` in `pyomo_printing_demo.py`. Both made the original scripts crash.
- The notebooks use HiGHS (`SolverFactory('appsi_highs')`) so they run in the browser; the scripts in
  `5 Source Files/Python` still use GLPK for desktop use. Results match; for the weighted objective GLPK picks a
  different selection with the same popularity, 305.
- The MATLAB `icki_toffee_weighted.m` uses the opposite convention from the slides and the Python: there $\alpha$ is
  the weight on **popularity** (minimise $(1-\alpha)\,\text{cost} - \alpha\,\text{popularity}$), so its `alpha = 1`
  is the Python's `alpha = 0`. Both give popularity 305.
- The Q2 code prints *surplus* for unused hours; the *Slack Variables* slides call this **slack** (surplus is the
  excess over a $\ge$ limit). The notebooks explain this and the answers now say *slack*; the printed text is unchanged.
- **Notebooks (Oct 2026), text only.** Each notebook gained an opening cell (problem, how to run it, expected
  result), a short explanation above every code cell, a comment on each constraint row and a closing *What do you
  notice?* / *Try it* cell with a hidden answer. Wrong or unclear comments were fixed: "Define integer variables"
  above `NonNegativeReals` (demo), "Define objective function coefficients" above the constraint data (Q1b),
  `fat_weight_min` explained as an upper limit, the four-number "raw material for each factory" list (Q2b), and
  the expected Pyomo warning when the demo redefines `constraint1`. No code and no printed result changed.
- **Corrections (Oct 2026), lecture slides.** The `.pptx` in `5 Source Files` was corrected and the PDF in
  `1 Lecture` re-exported from it in PowerPoint (17 Oct 2026) (`.pptx` slide numbers, PDF pages in brackets):
  - slide 8 (p. 7): vitamin B constraint $14x_5$ (it said $12x_5$); vitamin C constraint $10x_9$ (it said
    $10x_{10}$). Week 03 had the same error;
  - slide 24 (p. 23): the last column is now $\alpha = 0.16$ and the text says "$\alpha < 1/6$ (≈ 0.167) return the
    Maximise popularity model" (it said 0.17; at $\alpha = 0.17$ the model picks 30 Coconut Ice, 6 Rose-water posy
    and 4 Grape bunch, popularity 304);
  - slide 11 (p. 10): "at least 320g", "at most 45%", "at most 2850 calories" (it said "more than" / "less than");
  - slide 17 (p. 16): "affected"; slide 26 (p. 25): "etc."; slide 27 (p. 26): "R.E.D. Woolsey";
  - slide 19 (p. 18): heading "Maximise the sum of each candy's popularity per unit cost" (it said "… of the
    selection", but $\sum_i (P_i/C_i) x_i$ is not the selection's total popularity ÷ total cost);
  - slides 8–10 (pp. 7–9): "Week 2 Tutorial Q6a" (it said "Tutorial Question 5a", the old numbering);
  - slide 21 (p. 20): "For a 40/60 split (40% popularity, 60% cost)".
  - slides 22–23 (pp. 21–22): Lime sherbet's normalised difference is $0.6 - 0.65 = -0.05$ (it said −0.5). The
    results do not change. **Corrected in the `.pptx` after the 17 Oct export: re-export the PDF.**
  - Not changed (pictures): the code on slides 6–7 says "Define integer variables" above `NonNegativeReals`; the
    code on slide 10 uses GLPK.
  - Always edit and export the `.pptx` in PowerPoint: LibreOffice cannot draw equations inside table cells (on
    pp. 10, 11, 16, 18–23 its table headers show a tiny copy of the table instead of the column names).
  - Slides 8, 22, 23 and 24 also store fallback pictures (of the equations text box, the tables and the text under
    the slide 24 table) that only programs without equation support (e.g. LibreOffice, Google Slides) show. On
    17 Oct 2026 these were replaced by the same areas of the PowerPoint PDF export, with the slides 22–23 Lime
    sherbet cell redrawn as −0.05, so they show the corrected text too; the slide 24 fallback box is wider than the
    text box, because in PowerPoint the last line runs past it. PowerPoint redraws such a picture only when the
    text in that box changes (a plain re-save does not), so after editing one of these boxes, check it once in
    another program.
- **Corrections (Oct 2026), `Slack Variables.pptx`** (the PDF in `1 Lecture` was re-exported in PowerPoint,
  17 Oct 2026): slide 2 "$P = 5 \cdot 0 + 4 \cdot 0 = 0$" (it said $7 \cdot 0$; the objective is $5x + 4y$);
  slide 10 "Used for ≤ (less than or equal to) constraints" and "≥ (greater than or equal to)". The fallback
  pictures of these two text boxes (see above) were replaced the same way on 17 Oct 2026.
- **Corrections (Oct 2026), tutorial and answers `.docx`** (`5 Source Files`; the PDFs were re-exported from them
  in Word on 17 Oct 2026): Q1 now says "at least" 320 g, "at most" 45% fat and "at most" 2850 calories (as in
  Week 03); Q2 "its products", "for each factory to maximise its profit", and the missing ")" in Q2a ii. Answers
  only: the Colab link (it needs a sign-in and had GLPK code) now points to the course site; "popularity per cost
  ratio" (it said "population"), "normalised weighted objective", "greater than", "last week's"; Q2a ii says
  *slack* instead of *surplus*; and a new table under Q1b lists the selections from the notebooks.
- **After the 17 Oct export** (**re-export both PDFs**): the tutorial sheet now has the "* Medium / ** Hard" key
  of the other weeks' sheets (Q1b is marked *). In the answers, the note under the Q1b table uses † (not *) and
  says which objective its α thresholds belong to: 0.59 and 1/6 are for the normalised weighted objective; the
  plain weighted objective switches at about 0.42 (minimum cost) and 0.09 (maximum popularity).
- The answers' Q2b combined model pads factory A's and B's constraint rows with yellow-on-yellow terms (e.g.
  "+5s₁+3d₁") to line up the columns. They are invisible in the PDF but appear if the text is copied; left as is.
