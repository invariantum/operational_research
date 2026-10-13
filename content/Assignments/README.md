# Assignments: start here

5CM522 is assessed by two pieces of coursework (25% each) and a timed in-class test (50%).
This folder holds two self-contained folders:

| Folder | For | Open first |
|---|---|---|
| [`5cm522-operational-research-public/`](5cm522-operational-research-public/) | **Students:** the briefs, the Part B starter repository and the revision papers with solutions | [`5cm522-operational-research-public/README.md`](5cm522-operational-research-public/README.md) |
| [`5cm522-operational-research-staff-only/`](5cm522-operational-research-staff-only/) | **Staff:** model solutions, marking guides and templates, the May 2026 in-class test | [`5cm522-operational-research-staff-only/README.md`](5cm522-operational-research-staff-only/README.md) |

Both folders are laid out the same way. Numbered folders are used in order, each folder has a `README.md`
saying what to do step by step, and every PDF sits next to its source file.

| Step | Student folder | Staff folder |
|---|---|---|
| 01 | `01-coursework-part-a/`: Part A brief | `01-coursework-part-a/`: model answers, marking rubric |
| 02 | `02-coursework-part-b/`: Part B brief and `starter-repo/` | `02-coursework-part-b/`: model solutions, analysis tools, marking |
| 03 | `03-revision/`: practice papers for the in-class test | `03-in-class-test-2026-05/`: the paper, solutions, exam-day files, marking |

## Running the code

- **In the browser:** open a notebook (`.ipynb`) on the course website, run its first cell (it installs
  Pyomo, HiGHS and SimPy), then *Run All*. In the browser, `.py` files open as text only, so use the notebook
  with the same name. The in-class test code and `environment_check.ipynb` need Google OR-Tools, which has
  no browser version, so run those on a computer.
- **On a computer:** each folder has an `environment.yml`. Run `conda env create -f environment.yml`, then
  `conda activate 5cm522-or`, then `python scripts/run_all_checks.py` to confirm everything works.

## Notes for staff

- These folders are copies of the module team's local folders of the same names. To update them, change
  the local folder, run `python scripts/run_all_checks.py` in it, then copy it here unchanged.
- The hidden files in each folder (`.gitignore`, `.gitattributes`, `starter-repo/.vscode/`) are kept in
  the repository but left off the website: `jupyter_lite_config.json` at the top of the repository tells
  the site build to skip them.
- **This repository is public.** Everything in `5cm522-operational-research-staff-only/` can be read and
  downloaded by anyone. Move it to a private repository if the answers must stay confidential.
