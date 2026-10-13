# Changelog

## 2026-10-13: Runs on the course website; step-by-step READMEs

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

## 2026-10-13 — Full verification and environment fix

Every script and notebook was run in a clean Python 3.11 environment built from `requirements.txt`
(pyomo 6.10.1, highspy 1.12.0, OR-Tools 9.15.6755, SimPy 4.1.2): **40 tests pass, none skipped.**
The answers printed by the solution code were also compared with the written solutions and match.

- **Environment fixed.** OR-Tools is not published on conda-forge for Windows, so the old conda line
  (`ortools-python`) could not install there; the solver packages now come from pip inside
  `environment.yml`. HiGHS (`highspy`) 1.13+ clashes with the HiGHS bundled in OR-Tools 9.15 when both
  load in one Python process (Pyomo then reports no solver), so `highspy` is pinned to `>=1.11,<1.13`.
- Test for the Practice Paper A workbook now allows the helper moving-average cells the worked Excel version deliberately leaves blank.


## 2026-10-13 — Prepared for public sharing

Built from the original module folder (`Assignments/`), which was left unchanged.

### Personal data removed
- Not included at all: student submissions and GitHub repositories, marks spreadsheets, grade
  breakdowns, moderation samples and archives, scanned exam booklets, per-student marking notes and
  moderation comparison tables.
- Staff e-mail address removed from both assessment briefs (PDFs regenerated from the edited `.docx`).
- Office files: SharePoint custom XML (staff account e-mails), custom properties and author /
  last-modified-by metadata removed. PDFs: author/creator metadata removed.
- Example path with a staff user name replaced in the starter-repo README.
- `scripts/scan_for_personal_data.py` added as a release gate (reports no findings).

### Kept out of the public folder (no personal data, but answers to assessments)
Part A model solutions and rubric, Part B model-solution notebooks, analysis scripts and marking
guidance, and the whole May 2026 in-class test. These are in the separate staff-only folder.

### Code made runnable anywhere
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

### Final versions chosen where copies differed
| Kept | Instead of | Why |
|---|---|---|
| Practice Paper A solutions from `Revision/Practice Paper A/` | copy at top of `Revision/` | Newer: adds MST diagram, corrects the moving-average range and Q4 conclusion |
| Practice Paper A simulation checker (6/7/8/9 bays) | `_v2` (5/6/8 bays) | Matches the capacities the question asks for and the written solution |
| `Mock Exam/Mock Answers.xlsx` (2026) | 2024 copy at top of `Revision/` | Corrected formulas (fixed seasonal-index ranges, updated trend line) |
| Practice-paper PDFs rebuilt from the kept `.tex` | `build/` and `build_practice/` PDFs | Guarantees PDF = source; old builds still said "5 hours" |
| `Sample Questions 2324.docx` | `… - video.docx` | The video copy is the same paper with rough working notes added |

### Removed as duplicates, drafts or clutter
Duplicate copies at the top of `Revision/`; `build_practice/` and `build/` folders; LaTeX `.aux`,
`.log`, `.synctex.gz`; `__pycache__/`, `.ipynb_checkpoints/`; empty `test.py` and `.Rhistory`;
`.brief.zip` and `.brief_docx_extracted/` (unzipped copy of the Part B brief); the solution repo's
superseded `notebook_template.ipynb`, `assignment_spec.md` and README (older drafts of the starter
material); `Test.ipynb` (failed draft of the environment check); `or_exam.yml` (merged into
`environment.yml`); `Coursework 1/TODO.txt`, `Timed Exam/Plan.txt`, `Revision Topics.txt`
(superseded by the READMEs).

### Added
`README.md` files throughout, `docs/data-dictionary.md`, `environment.yml`, `requirements.txt`,
`.gitignore`, `.gitattributes`, `scripts/run_all_checks.py`, `scripts/build_pdfs.py`,
`scripts/scan_for_personal_data.py`, `tests/`.

### Where each file came from
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
