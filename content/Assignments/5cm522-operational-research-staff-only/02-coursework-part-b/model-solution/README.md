# Part B model solutions

Two complete worked solutions to the coursework.

1. Open a notebook:
   - **on the course website**, with nothing to install: run the first cell, then *Run All* (about a minute);
   - **or on your computer** (`conda activate 5cm522-or`, then `jupyter lab`).
2. The data cell generates the dataset for the dummy ID `TEST001` into `data/` (git-ignored). The other
   cells forecast demand, build the optimisation model, solve it with HiGHS and run sensitivity analysis.

| File | Approach |
|---|---|
| `notebook_solution_simple.ipynb` | Random-forest demand forecast; demand allocated once (all stores open, gravity weights); binary ILP choosing stores with positive stand-alone profit; ±10% demand sensitivity. Shows the minimum acceptable modelling chain |
| `notebook_solution_advanced.ipynb` | Same forecast; gravity allocation inside a MILP so cannibalisation responds to which stores open; compared with the simple approach. Shows what a top-band solution looks like |
| `generate_data.py` | Identical to the student copy in the public starter repository |
| `base_data/` | Identical to the public base data |

**Reproducing a student's dataset:** set `STUDENT_ID` in the data cell to their number, or run
`python generate_data.py --student_id <number> --out_dir <folder outside the repository>`. Do this
on your own machine only, and never save a notebook with a real number or its outputs.
