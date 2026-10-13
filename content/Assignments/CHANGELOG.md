# Changelog

## 2026-10-13: Review, privacy clean-up and one folder per assessment

### Privacy
- **Hidden links to a staff OneDrive removed** from six Office files that were already public:
  `mock-paper-2023-24-answers.docx`, `mock-paper-2023-24-answers-workings.xlsx`,
  `sample-questions-2023-24-answers.docx`, `sample-questions-2023-24-answers-workings.xlsx`,
  `practice-paper-a-forecasting-worked.xlsx`, `practice-paper-a-q4-simulation-checker.xlsx`. They held the
  workbook's saved location (`x15ac:absPath`) and chart/external-workbook links pointing at a staff member's personal
  OneDrive folder (account name and internal folder names). Removed: the saved-location element, the unused
  external-workbook link, and the charts' links to their source workbooks. Every cell value, formula and
  chart (cached data) is unchanged (checked cell by cell and by rendering the documents).
- `tools/scan_for_personal_data.py` now also scans attribute values inside Office XML (where such links
  live); before, it removed all tags first and so could not see them.

### Structure: one folder per assessment
The separate student and staff folders were merged into one folder per assessment, each laid out the same way
(`brief/`, `starter/`, `solutions/`, `staff/`, plus `revision/` for the test and `tools/` for Part B), with one
`README.md` per assessment saying what it is about, what to open in which order, what students hand in, and how
to run the code. One `requirements.txt` / `environment.yml`, one `tools/` folder and one test suite replace the
two copies. The staff material stays public, as the module team decided.

| Old location (under `content/Assignments/`) | New location |
|---|---|
| `…-public/01-coursework-part-a/assessment-brief-part-a.*` | `01-coursework-part-a/brief/` |
| `…-public/03-revision/templates/pyomo_starter_template.ipynb` | `01-coursework-part-a/starter/` (+ new `.py`) |
| `…-staff-only/01-coursework-part-a/part-a-model-solutions.docx` | `01-coursework-part-a/solutions/` |
| `…-staff-only/01-coursework-part-a/part-a-marking-rubric-template.xlsx` | `01-coursework-part-a/staff/` |
| `…-public/02-coursework-part-b/assessment-brief-part-b.*`, `…-public/docs/data-dictionary.md` | `02-coursework-part-b/brief/` |
| `…-public/02-coursework-part-b/starter-repo/` | `02-coursework-part-b/starter/` |
| `…-staff-only/02-coursework-part-b/model-solution/` | `02-coursework-part-b/solutions/` (+ new `.py` for both notebooks) |
| `…-staff-only/02-coursework-part-b/analysis/` | `02-coursework-part-b/tools/` |
| `…-staff-only/02-coursework-part-b/marking/` | `02-coursework-part-b/staff/` |
| `…-staff-only/03-in-class-test-2026-05/paper/` | `03-in-class-test/brief/` |
| `…-staff-only/03-in-class-test-2026-05/student-setup/` | `03-in-class-test/starter/` (+ new `environment_check.py`) |
| `…-staff-only/03-in-class-test-2026-05/solutions/` | `03-in-class-test/solutions/` |
| `…-staff-only/03-in-class-test-2026-05/marking/`, `invigilation-checklist.docx`, `open-book-materials-guidance.md` | `03-in-class-test/staff/` |
| `…-public/03-revision/<paper>/` | `03-in-class-test/revision/<paper>/` |
| `…/scripts/`, `…/tests/` (two copies) | `tools/`, `tools/tests/` (one copy) |

### Code: every example as a notebook and a script, same results everywhere
- **New scripts** for the notebooks that had none: `mock_paper_2023_24_answers.py`,
  `sample_questions_2023_24_answers.py`, `pyomo_starter_template.py`, `notebook_solution_simple.py`,
  `notebook_solution_advanced.py`, `environment_check.py`. Each is the notebook's code, with `# %%` cell markers.
- **Notebooks split by question:** the Practice Paper A/B notebooks had all code in one cell guarded by
  `if __name__ == "__main__"`; they now have the shared code, then one cell per question (the automatic browser
  test had been passing them without running any question). The three booklet notebooks likewise.
- **First cell:** installs pinned versions in the browser only (`micropip`: `pyomo==6.10.1`, `simpy==4.1.2`;
  HiGHS from the browser's Python), keeps the browser-only Pyomo fixes, and does nothing on a computer (so
  it can no longer upgrade or change packages in a local environment).
- **In-class test Question 6 now runs in the browser:** without OR-Tools, `in_class_test_code.py` and
  `worked_solutions.ipynb` solve the job shop as a Pyomo + HiGHS integer programme. A deterministic tie-break
  (earliest start for each operation in job order) gives exactly the CP-SAT result: makespan 18, the schedule
  printed in `worked-solutions.pdf`, and "infeasible" for the deadline-and-downtime variant. The full output of
  `in_class_test_code.py` is identical with and without OR-Tools.
- **Mock paper Question 3a:** HiGHS returns a different, equally cheap plan (cost 1830) from the GLPK plan on the
  answer sheet. A new cell checks that the answer-sheet plan is feasible and also costs 1830. Section headings
  corrected (the LP cells are Question 5b/5d, not "Question 5"/"3a").
- `-0.0` no longer printed for zero shipments; Practice Paper A/B print the solver's name instead of a Python
  object address; `in_class_test_code.py` prints the workbook path relative to its folder (no local user path).
- Part B tools point at `solutions/` (was `model-solution/`).

### Verified
Each original from the module folder, its `.py` and its `.ipynb` were run and compared (locally, in Pyodide
314.0.0/314.0.7, and in a JupyterLite build of this site in Chromium): identical optimal values, solutions,
schedules and tables, apart from the alternative optimum above, floating-point noise in the last digit,
and scikit-learn-version differences in the browser for the Part B model solutions (same stores chosen).

---

## Earlier history: student folder (`5cm522-operational-research-public`)

*Paths in the earlier entries are relative to the old folders; the table at the top says where each one is now.*

### 2026-10-13: Runs on the course website; step-by-step READMEs

This folder is now published unchanged in the course repository (`content/Assignments/`), so it also
appears on the course website (JupyterLite), where notebooks run in the browser.

- **New notebooks** next to each solution script, so the code runs in the browser:
  - `practice_paper_a_code.ipynb`, `practice_paper_b_code.ipynb`;
  - `greengrid_pyomo.ipynb`, `northfield_transshipment_mcfp.ipynb`, `uni_library_simpy.ipynb`.

  The `.py` scripts are unchanged and remain the versions to run on a computer.
- **Install cell added** as the first cell of every notebook (`%pip install …`, plus small Pyomo
  adjustments that apply only in the browser). It replaces the old "Setup" note and is harmless in Jupyter,
  VS Code and Colab.
- **Starter notebook:** the data-generation cell now calls `generate_data.generate(...)` directly
  instead of starting `python generate_data.py` as a separate program, which the browser cannot do.
  The generated data is identical.
- **`practice_paper_b_code.py`:** without OR-Tools (as in the browser), the job-shop question is solved
  as a Pyomo + HiGHS integer programme. It gives the same makespan (19) and schedule as CP-SAT.
- **READMEs rewritten** so each folder says what the assessment is, what to do and in which order, and how to run
  each file in the browser or on a computer.

### 2026-10-13 — Full verification and environment fix

Every script and notebook was run in a clean Python 3.11 environment built from `requirements.txt`
(pyomo 6.10.1, highspy 1.12.0, OR-Tools 9.15.6755, SimPy 4.1.2): **40 tests pass, none skipped.**
The answers printed by the solution code were also compared with the written solutions and match.

- **Environment fixed.** OR-Tools is not published on conda-forge for Windows, so the old conda line
  (`ortools-python`) could not install there; the solver packages now come from pip inside
  `environment.yml`. HiGHS (`highspy`) 1.13+ clashes with the HiGHS bundled in OR-Tools 9.15 when both
  load in one Python process (Pyomo then reports no solver), so `highspy` is pinned to `>=1.11,<1.13`.
- Test for the Practice Paper A workbook now allows the helper moving-average cells the worked Excel version deliberately leaves blank.


### 2026-10-13 — Prepared for public sharing

Built from the original module folder (`Assignments/`), which was left unchanged.

#### Personal data removed
- Not included at all: student submissions and GitHub repositories, marks spreadsheets, grade
  breakdowns, moderation samples and archives, scanned exam booklets, per-student marking notes and
  moderation comparison tables.
- Staff e-mail address removed from both assessment briefs (PDFs regenerated from the edited `.docx`).
- Office files: SharePoint custom XML (staff account e-mails), custom properties and author /
  last-modified-by metadata removed. PDFs: author/creator metadata removed.
- Example path with a staff user name replaced in the starter-repo README.
- `scripts/scan_for_personal_data.py` added as a release gate (reports no findings).

#### Kept out of the public folder (no personal data, but answers to assessments)
Part A model solutions and rubric, Part B model-solution notebooks, analysis scripts and marking
guidance, and the whole May 2026 in-class test. These are in the separate staff-only folder.

#### Code made runnable anywhere
- `generate_data.py`: base and output folders now default to locations next to the script (works from any
  working folder); `manifest.json` and console output use relative paths instead of absolute local paths;
  example student number replaced with the dummy `100000000`. **Generated data is byte-for-byte identical**
  to the original script's output (checked).
- Notebooks: outputs cleared (they contained local user paths), one standard kernel (`python3`),
  empty cells removed.
- Practice-paper code writes its forecasting workbook to `output/` so it can no longer overwrite the
  published answer workbook.
- Mock and sample-question notebooks and the Pyomo template: Colab/GLPK install cells replaced by a
  set-up note; solver switched from GLPK (separate install) to HiGHS (`appsi_highs`, installed with
  `highspy`); author headers with a staff user name removed.
- `build_full_revision_booklet.py`: updated to the new file names; a dead first draft of
  `extract_question_blocks` (which referenced an undefined function) removed. Output unchanged.

#### Final versions chosen where copies differed
| Kept | Instead of | Why |
|---|---|---|
| Practice Paper A solutions from `Revision/Practice Paper A/` | copy at top of `Revision/` | Newer: adds MST diagram, corrects the moving-average range and Q4 conclusion |
| Practice Paper A simulation checker (6/7/8/9 bays) | `_v2` (5/6/8 bays) | Matches the capacities the question asks for and the written solution |
| `Mock Exam/Mock Answers.xlsx` (2026) | 2024 copy at top of `Revision/` | Corrected formulas (fixed seasonal-index ranges, updated trend line) |
| Practice-paper PDFs rebuilt from the kept `.tex` | `build/` and `build_practice/` PDFs | Guarantees PDF = source; old builds still said "5 hours" |
| `Sample Questions 2324.docx` | `… - video.docx` | The video copy is the same paper with rough working notes added |

#### Removed as duplicates, drafts or clutter
Duplicate copies at the top of `Revision/`; `build_practice/` and `build/` folders; LaTeX `.aux`,
`.log`, `.synctex.gz`; `__pycache__/`, `.ipynb_checkpoints/`; empty `test.py` and `.Rhistory`;
`.brief.zip` and `.brief_docx_extracted/` (unzipped copy of the Part B brief); the solution repo's
superseded `notebook_template.ipynb`, `assignment_spec.md` and README (older drafts of the starter
material); `Test.ipynb` (failed draft of the environment check); `or_exam.yml` (merged into
`environment.yml`); `Coursework 1/TODO.txt`, `Timed Exam/Plan.txt`, `Revision Topics.txt`
(superseded by the READMEs).

#### Added
`README.md` files throughout, `docs/data-dictionary.md`, `environment.yml`, `requirements.txt`,
`.gitignore`, `.gitattributes`, `scripts/run_all_checks.py`, `scripts/build_pdfs.py`,
`scripts/scan_for_personal_data.py`, `tests/`.

#### Where each file came from
| New location | Original file (under `Assignments/`) |
|---|---|
| `01-coursework-part-a/assessment-brief-part-a.docx` | `Coursework 1/CW Part A/Assessment Brief - Coursework Part A (5CM522) 2526.docx` |
| `02-coursework-part-b/assessment-brief-part-b.docx` | `Coursework 1/CW Part B/Assessment Brief - Coursework Part B (5CM522) 2526.docx` |
| `02-coursework-part-b/starter-repo/README.md` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/README.md` |
| `02-coursework-part-b/starter-repo/environment.yml` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/environment.yml` |
| `02-coursework-part-b/starter-repo/generate_data.py` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/generate_data.py` |
| `02-coursework-part-b/starter-repo/notebook.ipynb` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/notebook.ipynb` |
| `02-coursework-part-b/starter-repo/.gitignore` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/.gitignore` |
| `02-coursework-part-b/starter-repo/.gitattributes` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/.gitattributes` |
| `02-coursework-part-b/starter-repo/.vscode/settings.json` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/.vscode/settings.json` |
| `02-coursework-part-b/starter-repo/base_data/margins_base.json` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/base_data/margins_base.json` |
| `02-coursework-part-b/starter-repo/base_data/stores_base.csv` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/base_data/stores_base.csv` |
| `02-coursework-part-b/starter-repo/base_data/zones_base.csv` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/base_data/zones_base.csv` |
| `02-coursework-part-b/starter-repo/base_data/zone_store_dist_base.csv` | `Coursework 1/CW Part B/5CM522-Coursework-2-main/base_data/zone_store_dist_base.csv` |
| `03-revision/practice-paper-a/practice-paper-a.tex` | `Timed Exam/Revision/Practice Paper A/Practice Paper A.tex` |
| `03-revision/practice-paper-a/practice-paper-a-solutions.tex` | `Timed Exam/Revision/Practice Paper A/Practice Paper A - Solutions.tex` |
| `03-revision/practice-paper-a/practice_paper_a_code.py` | `Timed Exam/Revision/Practice Paper A/practice_paper_a_code.py` |
| `03-revision/practice-paper-a/practice-paper-a-forecasting-worked.xlsx` | `Timed Exam/Revision/Practice Paper A/practice_paper_a_forecasting.xlsx` |
| `03-revision/practice-paper-a/practice-paper-a-q4-simulation-checker.xlsx` | `Timed Exam/Revision/Practice Paper A/practice_paper_a_q4_simulation_checker.xlsx` |
| `03-revision/practice-paper-b/practice-paper-b.tex` | `Timed Exam/Revision/Practice Paper B/Practice Paper B.tex` |
| `03-revision/practice-paper-b/practice-paper-b-solutions.tex` | `Timed Exam/Revision/Practice Paper B/Practice Paper B - Solutions.tex` |
| `03-revision/practice-paper-b/practice_paper_b_code.py` | `Timed Exam/Revision/Practice Paper B/practice_paper_b_code.py` |
| `03-revision/practice-paper-b/practice-paper-b-forecasting.xlsx` | `Timed Exam/Revision/Practice Paper B/practice_paper_b_forecasting.xlsx` |
| `03-revision/mock-paper-2023-24/mock-paper-2023-24.docx` | `Timed Exam/Revision/Mock Exam/Mock Paper 2324.docx` |
| `03-revision/mock-paper-2023-24/mock-paper-2023-24.pdf` | `Timed Exam/Revision/Mock Exam/Mock Paper 2324.pdf` |
| `03-revision/mock-paper-2023-24/mock-paper-2023-24-answers.docx` | `Timed Exam/Revision/Mock Exam/Mock Paper 2324 - Answers.docx` |
| `03-revision/mock-paper-2023-24/mock-paper-2023-24-answers.pdf` | `Timed Exam/Revision/Mock Exam/Mock Paper 2324 - Answers.pdf` |
| `03-revision/mock-paper-2023-24/mock-paper-2023-24-answers-workings.xlsx` | `Timed Exam/Revision/Mock Exam/Mock Answers.xlsx` |
| `03-revision/mock-paper-2023-24/mock_paper_2023_24_answers.ipynb` | `Timed Exam/Revision/Mock Exam/OR_Mock_Exam_Answers_24.ipynb` |
| `03-revision/mock-paper-2023-24/reformatted/mock-paper-2023-24-reformatted.pdf` | `Timed Exam/Revision/Mock Exam/build/Mock Paper 2324.pdf` |
| `03-revision/mock-paper-2023-24/reformatted/mock-paper-2023-24-reformatted-solutions.pdf` | `Timed Exam/Revision/Mock Exam/build/Mock Paper 2324 - Solutions.pdf` |
| `03-revision/sample-questions-2023-24/sample-questions-2023-24.docx` | `Timed Exam/Revision/Sample Questions/Sample Questions 2324.docx` |
| `03-revision/sample-questions-2023-24/sample-questions-2023-24.pdf` | `Timed Exam/Revision/Sample Questions/Sample Questions 2324.pdf` |
| `03-revision/sample-questions-2023-24/sample-questions-2023-24-answers.docx` | `Timed Exam/Revision/Sample Questions/Sample Questions 2324 - Answers.docx` |
| `03-revision/sample-questions-2023-24/sample-questions-2023-24-answers.pdf` | `Timed Exam/Revision/Sample Questions/Sample Questions 2324 - Answers.pdf` |
| `03-revision/sample-questions-2023-24/sample-questions-2023-24-answers-workings.xlsx` | `Timed Exam/Revision/Sample Questions/Sample Questions Answers 2 4 5.xlsx` |
| `03-revision/sample-questions-2023-24/sample_questions_2023_24_answers.ipynb` | `Timed Exam/Revision/Sample Questions/Sample_Answers.ipynb` |
| `03-revision/full-revision-booklet/full-revision-booklet.tex` | `Timed Exam/Revision/Full Revision Booklet/Full Revision Booklet.tex` |
| `03-revision/full-revision-booklet/full-revision-booklet-solutions.tex` | `Timed Exam/Revision/Full Revision Booklet/Full Revision Booklet - Solutions.tex` |
| `03-revision/full-revision-booklet/build_full_revision_booklet.py` | `Timed Exam/Revision/Full Revision Booklet/build_full_revision_booklet.py` |
| `03-revision/full-revision-booklet/greengrid_pyomo.py` | `Timed Exam/Revision/Full Revision Booklet/greengrid_pyomo.py` |
| `03-revision/full-revision-booklet/northfield_transshipment_mcfp.py` | `Timed Exam/Revision/Full Revision Booklet/northfield_transshipment_mcfp.py` |
| `03-revision/full-revision-booklet/uni_library_simpy.py` | `Timed Exam/Revision/Full Revision Booklet/uni_library_simpy.py` |
| `03-revision/templates/pyomo_starter_template.ipynb` | `Timed Exam/Revision/Pyomo_Template.ipynb` |
| `01-coursework-part-a/assessment-brief-part-a.pdf` | regenerated from the edited .docx |
| `02-coursework-part-b/assessment-brief-part-b.pdf` | regenerated from the edited .docx |
| `03-revision/**/*.pdf for .tex sources` | rebuilt from the .tex with scripts/build_pdfs.py |

---

## Earlier history: staff folder (`5cm522-operational-research-staff-only`)

### 2026-10-13: Runs on the course website; step-by-step READMEs

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

### 2026-10-13 — Full verification and environment fix

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


### 2026-10-13 — Prepared as a clean staff-only folder

Built from the original module folder (`Assignments/`), which was left unchanged. Companion to
the public folder `5cm522-operational-research-public`.

#### Personal data removed
- Not included at all: student submissions, marks spreadsheets, grade breakdowns, moderation
  samples and archives, scanned booklets, per-student marking notes, moderation comparison tables,
  the final moderation record and handover summary (all name individual students).
- Part A rubric: only the blank `Template` sheet kept (renamed `Rubric`); the 13 student sheets and
  an "Overall Marks" sheet listing seven people from another cohort were dropped. The weighting
  labels were corrected to 85% / 15% to match the sheet's own formulas.
- Part B and in-class-test marking grids rebuilt **blank** (same columns and formulas, no students).
- Office/PDF metadata cleaned as in the public folder; scripts no longer contain a staff user path.

#### Code made runnable anywhere
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

#### Final versions chosen where copies differed
| Kept | Instead of | Why |
|---|---|---|
| `forecasting-worked-solution.xlsx` regenerated from `in_class_test_code.py` | `Timed Exam/in_class_test_forecasting.xlsx` (hand-edited, 2 June) and `In-Class Test Code/in_class_test_forecasting.xlsx` (older code) | The hand-edited Excel version used a different trend/seasonal-index calculation and **disagrees with the published worked solutions** (e.g. MSE 455.0 vs 558.4); the regenerated workbook matches them exactly |
| `.tex` sources with PDFs rebuilt from them | `build/` PDFs | Guarantees PDF = source |
| `in_class_test_code.py` / snippets from `In-Class Test Code/` | `5CM522 May 2026 - In-Class Test Worked Solutions.md` | Same content as the `.tex` worked solutions |

#### Where each file came from
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
