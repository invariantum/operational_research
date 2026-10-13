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

## Lecture demos (`2 Lecture Demos`)

| Notebook | Slides | Shows |
| --- | --- | --- |
| `1 LP with Pyomo` | 7 | The lecture LP written in Pyomo |
| `2 Diet problem 5a - minimise cost` | 8–12 | Week 2 tutorial Q5a in Pyomo |
| `3 Diet problem 5b - unbounded` | 13–14 | Maximising attractiveness: the solver reports *unbounded* |
| `4 Diet problem 5c - the fix` | 15–16 | Adding limits on fat and vitamins gives a sensible diet |
| `5 Integer LP` | 24 | Same constraints, integer variables |
| `6 Mixed-integer LP` | 25–26 | One integer and one continuous variable |

## Tutorial answers (`4 Tutorial Answers`)

| Notebook | Question | Answer |
| --- | --- | --- |
| `Q1 LP, ILP and MILP` | Q1, Q1a, Q1b | LP 270 at (7.5, 10); ILP 264 at (7, 10); MILP 270 at (7.5, 10) |
| `Q2b Icki-Toffee - minimise cost` | Q2b | Minimum cost 268 |
| `Q2c Icki-Toffee - maximise popularity` | Q2c | 5 Coconut Ice, 50 Lime Sherbet, 5 Grape Bunch; weight 635 g |

## Notes for staff

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
- `5 Source Files/Python/Week2_question_5b_pyomo.py` was edited: it now solves with `load_solutions=False` and prints the termination condition, because HiGHS stops with an error when asked to load a solution from an unbounded model. The original is in the baseline repository.
- The answers PDF's side note (Q2b alternative optimum) was added directly to the PDF, so its wording differs slightly from the .docx ("on the left" vs "above"). Re-export the PDF from the .docx to bring them in line.
- Notebooks 1 and 6: the comment above the solver line now says HiGHS (it said GLPK).
