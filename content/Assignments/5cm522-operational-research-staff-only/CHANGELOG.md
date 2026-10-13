# Changelog

## 2026-10-13: Runs on the course website; step-by-step READMEs

This folder is now published unchanged in the course repository (`content/Assignments/`), next to the
student folder, and appears on the course website (JupyterLite).

- **Part B model-solution notebooks run in the browser:**
  - the data cell now calls `generate_data.generate(...)` directly (same data as the command line);
  - a first install cell was added;
  - a browser-only fix stops Pyomo's multiprocessing import hook breaking scikit-learn, which has no
    multiprocessing support in the browser.
- **The in-class test code still needs a computer**, because Question 6 uses OR-Tools, which has no
  browser build. The READMEs say so.
- **READMEs rewritten:** reading order per role, two ways to run, and before / on the day / after for the
  in-class test. The "do not publish" note is replaced by a statement that the folder is public, as the
  module team decided.

## 2026-10-13 — Full verification and environment fix

Every script and notebook was run in a clean Python 3.11 environment built from `requirements.txt`
(pyomo 6.10.1, highspy 1.12.0, OR-Tools 9.15.6755, SimPy 4.1.2): **31 tests pass, none skipped.**
The answers printed by the solution code were also compared with the written solutions and match.

- **Environment fixed.** OR-Tools is not published on conda-forge for Windows, so the old conda line
  (`ortools-python`) could not install there; the solver packages now come from pip inside
  `environment.yml`. HiGHS (`highspy`) 1.13+ clashes with the HiGHS bundled in OR-Tools 9.15 when both
  load in one Python process (Pyomo then reports no solver), so `highspy` is pinned to `>=1.11,<1.13`.
- `worked-solutions.tex` (and its PDF) pointed at the old `Assignments/Timed Exam/...` file locations; updated to the new names.
- Marking notes referred to `Marking.xlsx`; now refer to `part-b-marking-grid-template.xlsx`.
- `environment_check.ipynb`: install instruction changed to the pip command that works on Windows.
- The written Q5 forecast table differs from the code in the 4th decimal (rounded intermediate values); the test now allows 0.01.


## 2026-10-13 — Prepared as a clean staff-only folder

Built from the original module folder (`Assignments/`), which was left unchanged. Companion to
the public folder `5cm522-operational-research-public`.

### Personal data removed
- Not included at all: student submissions, marks spreadsheets, grade breakdowns, moderation
  samples and archives, scanned booklets, per-student marking notes, moderation comparison tables,
  the final moderation record and handover summary (all name individual students).
- Part A rubric: only the blank `Template` sheet kept (renamed `Rubric`); the 13 student sheets and
  an "Overall Marks" sheet listing seven people from another cohort were dropped. The weighting
  labels were corrected to 85% / 15% to match the sheet's own formulas.
- Part B and in-class-test marking grids rebuilt **blank** (same columns and formulas, no students).
- Office/PDF metadata cleaned as in the public folder; scripts no longer contain a staff user path.

### Code made runnable anywhere
- `generate_data.py`: base and output folders now default to locations next to the script (works from any
  working folder); `manifest.json` and console output use relative paths instead of absolute local paths;
  example student number replaced with the dummy `100000000`. **Generated data is byte-for-byte identical**
  to the original script's output (checked).
- Notebooks: outputs cleared (they contained local user paths), one standard kernel (`python3`),
  empty cells removed.
- Part B analysis scripts (originally `test_*.py` with a hardcoded absolute path to a staff user folder) renamed to say
  what they do, now resolve paths relative to the repository and work in temporary folders.
  `test_variations_simple.py` dropped - it only re-read the last generated dataset and is superseded by
  `compare_student_datasets.py`.
- `create_base_data.py` now writes to `analysis/output/` by default instead of overwriting `base_data/`;
  with seed 2026 it reproduces the published base data.
- `in_class_test_code.py` writes its workbook to `solutions/output/`.
- `environment_check.ipynb`: fixed a `NameError` (`pyo.SolverFactory` with `pyo` never imported) and
  switched to `appsi_highs`; the in-notebook `conda install` cell became an instruction.
- `worked_solutions.ipynb`: Colab install cell turned into a set-up note.

### Final versions chosen where copies differed
| Kept | Instead of | Why |
|---|---|---|
| `forecasting-worked-solution.xlsx` regenerated from `in_class_test_code.py` | `Timed Exam/in_class_test_forecasting.xlsx` (hand-edited, 2 June) and `In-Class Test Code/in_class_test_forecasting.xlsx` (older code) | The hand-edited Excel version used a different trend/seasonal-index calculation and **disagrees with the published worked solutions** (e.g. MSE 455.0 vs 558.4); the regenerated workbook matches them exactly |
| `.tex` sources with PDFs rebuilt from them | `build/` PDFs | Guarantees PDF = source |
| `in_class_test_code.py` / snippets from `In-Class Test Code/` | `5CM522 May 2026 - In-Class Test Worked Solutions.md` | Same content as the `.tex` worked solutions |

### Where each file came from
| New location | Original file (under `Assignments/`) |
|---|---|
| `01-coursework-part-a/part-a-model-solutions.docx` | `Coursework 1/CW Part A/Assignment Part A Solutions.docx` |
| `02-coursework-part-b/model-solution/generate_data.py` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/generate_data.py` |
| `02-coursework-part-b/model-solution/notebook_solution_simple.ipynb` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/notebook_solution_simple.ipynb` |
| `02-coursework-part-b/model-solution/notebook_solution_advanced.ipynb` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/notebook_solution_advanced.ipynb` |
| `02-coursework-part-b/model-solution/base_data/margins_base.json` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/base_data/margins_base.json` |
| `02-coursework-part-b/model-solution/base_data/stores_base.csv` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/base_data/stores_base.csv` |
| `02-coursework-part-b/model-solution/base_data/zones_base.csv` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/base_data/zones_base.csv` |
| `02-coursework-part-b/model-solution/base_data/zone_store_dist_base.csv` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/base_data/zone_store_dist_base.csv` |
| `02-coursework-part-b/analysis/create_base_data.py` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/create_base_data.py` |
| `02-coursework-part-b/analysis/compare_student_datasets.py` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/test_student_variations.py` |
| `02-coursework-part-b/analysis/demand_impact_demo.py` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/test_impact_analysis.py` |
| `02-coursework-part-b/analysis/variation-analysis-report.md` | `Coursework 1/CW Part B/5CM522-Coursework-Solution-main/VARIATION_ANALYSIS_REPORT.md` |
| `02-coursework-part-b/marking/staff-marking-guide.md` | `Coursework 1/CW Part B/staff_facing_marking_help.md` |
| `02-coursework-part-b/marking/marking-workflow-notes.md` | `Coursework 1/CW Part B/marking_workflow_notes.md` |
| `02-coursework-part-b/marking/rubric-to-evidence-map.md` | `Coursework 1/CW Part B/moderation_supporting_notes/rubric_to_evidence_map.md` |
| `02-coursework-part-b/marking/feedback-comment-bank.md` | `Coursework 1/CW Part B/moderation_supporting_notes/feedback_comment_bank.md` |
| `02-coursework-part-b/marking/per-student-marking-template.md` | `Coursework 1/CW Part B/moderation_supporting_notes/per_student_marking_template.md` |
| `03-in-class-test-2026-05/paper/in-class-test-2026-05.tex` | `Timed Exam/5CM522 May 2026 - In-Class Test LaTeX.tex` |
| `03-in-class-test-2026-05/solutions/worked-solutions.tex` | `Timed Exam/5CM522 May 2026 - In-Class Test Worked Solutions.tex` |
| `03-in-class-test-2026-05/solutions/worked_solutions.ipynb` | `Timed Exam/In-Class Test Code/5CM522 May 2026 - In-Class Test Worked Solutions.ipynb` |
| `03-in-class-test-2026-05/solutions/in_class_test_code.py` | `Timed Exam/In-Class Test Code/in_class_test_code.py` |
| `03-in-class-test-2026-05/solutions/worked_solution_snippets.py` | `Timed Exam/In-Class Test Code/worked_solution_snippets.py` |
| `03-in-class-test-2026-05/solutions/forecasting-worked-solution.xlsx` | regenerated by `in_class_test_code.py` (see above) |
| `03-in-class-test-2026-05/student-setup/submission-template.docx` | `Timed Exam/Submission Template.docx` |
| `03-in-class-test-2026-05/student-setup/environment_check.ipynb` | `Timed Exam/Jupyter Template.ipynb` |
| `03-in-class-test-2026-05/invigilation-checklist.docx` | `Timed Exam/Instructions to give to students.docx` |
| `03-in-class-test-2026-05/open-book-materials-guidance.md` | `Timed Exam/Open Book Materials Guidance - May 2026.md` |
| `01-coursework-part-a/part-a-marking-rubric-template.xlsx` | Template sheet of `Coursework 1/CW Part A/2526 Marking Scheme.xlsx` |
| `02-coursework-part-b/marking/part-b-marking-grid-template.xlsx` | new, columns from `Coursework 1/CW Part B/Marking.xlsx` |
| `03-in-class-test-2026-05/marking/in-class-test-marking-grid-template.xlsx` | new, columns and formulas from `Timed Exam/Marking.xlsx` |
| `*.pdf for .tex sources` | rebuilt with scripts/build_pdfs.py |
