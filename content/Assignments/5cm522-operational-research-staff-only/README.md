# 5CM522 Operational Research — Staff-Only Materials (2025/26)

Everything a member of staff needs to **run, mark and maintain** the assessments of the University of
Derby module **5CM522 Operational Research**: model solutions, marking guidance and templates, the
data-generation tools, and the complete May 2026 timed in-class test.

> **Who can see this folder:** it is published in the course repository and on the course website, next to
> the student folder, so anyone with the link can read it. It contains answers to assessments that may be
> reused. If they must stay confidential, keep this folder in a private repository instead.
> **No personal data:** no student names, numbers, marks or submissions. Completed marking sheets and
> moderation records belong in the university's systems, never in this folder.
> **Module leader:** Dr Sam O'Neill.

**Companion folder:** `5cm522-operational-research-public` holds the student-facing material — the
coursework briefs, the Part B starter repository and the revision papers. This folder does not repeat
those files; keep both folders side by side.

---

## Contents

1. [Quick start](#1-quick-start)
2. [What every folder and file is](#2-what-every-folder-and-file-is)
3. [Assessment calendar — what to use when](#3-assessment-calendar--what-to-use-when)
4. [Coursework Part A — running and marking](#4-coursework-part-a--running-and-marking)
5. [Coursework Part B — running and marking](#5-coursework-part-b--running-and-marking)
6. [Timed in-class test — before, during and after](#6-timed-in-class-test--before-during-and-after)
7. [Maintaining the materials](#7-maintaining-the-materials)
8. [Checks, troubleshooting and privacy](#8-checks-troubleshooting-and-privacy)

---

## 1. Quick start

### What to read first

| You are… | Read, in this order |
|---|---|
| Marking Coursework Part A | §4 → `01-coursework-part-a/README.md` |
| Marking Coursework Part B | §5 → `02-coursework-part-b/marking/README.md` (numbered reading order) |
| Running the in-class test | §6 → `03-in-class-test-2026-05/README.md` (before / on the day / after) |
| New to the module | §3 (the assessment calendar), then the sections above as each assessment comes up |

### Two ways to run the code

| Where | What runs there |
|---|---|
| **Course website** (<https://invariantum.github.io/operational_research/>, folder `Assignments/5cm522-operational-research-staff-only`), nothing to install | The two Part B model-solution notebooks. Run the first cell, then *Run All* |
| **Your computer** (setup below) | Everything, including the in-class test code (it needs Google OR-Tools, which has no browser version), the analysis scripts, the checks and the PDF builds |

### One-time setup on your computer

One-time setup (Windows: use **Anaconda Prompt**; install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) first if needed):

```
cd "<path to>\5cm522-operational-research-staff-only"
conda env create -f environment.yml        # 5-10 minutes the first time
conda activate 5cm522-or                   # every time you open a new terminal
python scripts/run_all_checks.py           # last line should end with: ALL CHECKS PASSED
```

Pip alternative (Python 3.11): `python -m venv .venv`, activate it, `pip install -r requirements.txt`.
Do not upgrade `highspy` beyond 1.12 — newer HiGHS clashes with OR-Tools 9.15 (see `environment.yml`).

All commands in this guide assume the environment is active and the terminal is in this folder.
Scripts can also be run from any other folder.

---

## 2. What every folder and file is

```
5cm522-operational-research-staff-only/
│
├── README.md                     ← this guide
├── CHANGELOG.md                  how the folder was prepared, verification results, old → new names
├── environment.yml / requirements.txt    software for every script, notebook and test
├── .gitignore / .gitattributes   keep generated files, marks and submissions out of git
│
├── 01-coursework-part-a/         PART A — linear & integer programming
│   ├── part-a-model-solutions.docx         model answers, Questions 1–3
│   ├── part-a-marking-rubric-template.xlsx blank marking sheet (one copy of the "Rubric" sheet per student)
│   └── README.md
│
├── 02-coursework-part-b/         PART B — Yodafone forecasting + store-network optimisation
│   ├── model-solution/                     self-contained worked solutions
│   │   ├── notebook_solution_simple.ipynb      random-forest forecast → fixed allocation → binary ILP
│   │   ├── notebook_solution_advanced.ipynb    same forecast → gravity allocation inside a MILP
│   │   ├── generate_data.py                    identical to the student copy (dataset from a student number)
│   │   ├── base_data/                          identical to the public base data
│   │   └── README.md
│   ├── analysis/                           tools for understanding / rebuilding the datasets
│   │   ├── compare_student_datasets.py         how much datasets differ between student numbers
│   │   ├── demand_impact_demo.py               how ±20% demand changes store profitability
│   │   ├── create_base_data.py                 rebuilds the synthetic base data (never give to students)
│   │   ├── variation-analysis-report.md        write-up of why student solutions must differ
│   │   └── README.md
│   └── marking/                            everything needed to mark Part B
│       ├── staff-marking-guide.md              ① 10–15 minute per-student workflow (start here)
│       ├── rubric-to-evidence-map.md           ② what evidence earns each band, per criterion
│       ├── marking-workflow-notes.md           ③ calibration, broken notebooks, concern logging
│       ├── per-student-marking-template.md     ④ copy once per student for notes
│       ├── feedback-comment-bank.md            ⑤ adaptable feedback sentences by criterion and band
│       ├── part-b-marking-grid-template.xlsx   ⑥ blank cohort grid with weighted criteria and totals
│       └── README.md
│
├── 03-in-class-test-2026-05/     TIMED IN-CLASS TEST (May 2026) — 4 hours, best 4 of 6 questions
│   ├── paper/
│   │   ├── in-class-test-2026-05.pdf       the question paper
│   │   └── in-class-test-2026-05.tex       its LaTeX source
│   ├── solutions/
│   │   ├── worked-solutions.pdf / .tex     written worked solutions
│   │   ├── in_class_test_code.py           coded solutions for all six questions (also runs in Colab)
│   │   ├── worked_solution_snippets.py     one-line access per question, e.g. q3_results()
│   │   ├── worked_solutions.ipynb          the same solutions as a notebook
│   │   └── forecasting-worked-solution.xlsx    Q5 forecasting tables (generated by the code)
│   ├── student-setup/                      files students get on the day
│   │   ├── submission-template.docx        the answer document they complete
│   │   └── environment_check.ipynb         they run this first to prove Pyomo/HiGHS, OR-Tools, SimPy work
│   ├── marking/
│   │   └── in-class-test-marking-grid-template.xlsx   marks per sub-part → question totals → best four
│   ├── invigilation-checklist.docx         step-by-step script for running the session
│   ├── open-book-materials-guidance.md     what students may use, and what to release when
│   └── README.md
│
├── scripts/
│   ├── run_all_checks.py         one command that checks the whole folder (scan + tests)
│   ├── build_pdfs.py             rebuild PDFs after editing a .tex file
│   └── scan_for_personal_data.py release gate: finds names/IDs/e-mails/paths/author metadata
│
└── tests/                        automatic checks used by run_all_checks.py
```

Folders that appear after running things — safe to delete, ignored by git: `output/`, `data/`,
`__pycache__/`, `.ipynb_checkpoints/`.

---

## 3. Assessment calendar — what to use when

| When | Task | Files |
|---|---|---|
| Before Part A is released | Publish the brief | public `01-coursework-part-a/` |
| Part A marking | Mark with the rubric; check against model answers | `01-coursework-part-a/` ([§4](#4-coursework-part-a--running-and-marking)) |
| Before Part B is released | Publish the brief; give students the starter repo (e.g. GitHub Classroom) | public `02-coursework-part-b/` |
| Part B marking | Reproduce each student's data, mark with the guide and grid | `02-coursework-part-b/` ([§5](#5-coursework-part-b--running-and-marking)) |
| Revision period | Release practice papers + **written** solutions only | public `03-revision/`; `open-book-materials-guidance.md` |
| In-class test day | Set-up check, paper, submission template, invigilation | `03-in-class-test-2026-05/` ([§6](#6-timed-in-class-test--before-during-and-after)) |
| After the test | Mark; release coded practice-paper solutions | `03-in-class-test-2026-05/marking/`, public `03-revision/` |

---

## 4. Coursework Part A — running and marking

There is no code to run for Part A.

1. Read the brief (public folder) and `part-a-model-solutions.docx`.
2. Make a working copy of `part-a-marking-rubric-template.xlsx` **outside this folder**. For each
   student, duplicate the `Rubric` sheet and name it after the student.
3. For each sub-question (rows Q1a–Q3d) enter a score out of 10 in the column of the grade band you
   award (F … A+). The `Mark` column converts it: score ÷ 10 × marks available.
4. Do the same for the three presentation rows (Appendix A rubric in the brief).
5. The sheet totals automatically: **Answers scaled to 85%** + **Presentation scaled to 15%** = final mark
   (cell K35). Write comments in the `Notes` column.
6. Enter final marks in the university's gradebook. Do not save completed sheets in this folder.

---

## 5. Coursework Part B — running and marking

### 5.1 Run the model solutions

```
cd 02-coursework-part-b/model-solution
jupyter lab
```
Open `notebook_solution_simple.ipynb` or `notebook_solution_advanced.ipynb` and **Run All**. They also run on the
course website with nothing installed: open them there, run the first cell, then *Run All*. The data cell
generates data for the dummy ID `TEST001` into `data/` (git-ignored); the rest forecast demand,
build the optimisation model, solve it with HiGHS and run sensitivity analysis.
Typical run time: under 30 seconds each.

| Notebook | Approach | Use it to |
|---|---|---|
| simple | Demand allocated once (all stores open, gravity weights) → each store's stand-alone profit → binary ILP; ±10% demand sensitivity | show the minimum acceptable modelling chain |
| advanced | Gravity allocation embedded in a MILP, so cannibalisation responds to which stores open; compared with the simple result | show what a top-band solution looks like |

### 5.2 Reproduce a particular student's dataset (when marking)

Each student's data is determined by their student number. To see exactly what a student saw:
```
python 02-coursework-part-b/model-solution/generate_data.py --student_id <student number> --out_dir "<a folder outside this repository>"
```
or change `STUDENT_ID` in the first cell of a model-solution notebook (on your own machine only —
**do not save** the notebook with a real number or its outputs). Same number → identical data, always.

### 5.3 Mark a submission

Follow `marking/staff-marking-guide.md`; in brief:

1. **Calibrate** on three repos (strong, middling, weak) before marking the cohort
   (`marking-workflow-notes.md`).
2. Per student (10–15 min): check completeness → check the notebook runs (Restart & Run All) →
   mark the five notebook criteria in rubric order using `rubric-to-evidence-map.md` → mark slides and
   video → write feedback from `feedback-comment-bank.md`, noting what kept each criterion below the
   next band. Keep notes in a copy of `per-student-marking-template.md`.
3. **Sanity-check unusually large profits** — a reported profit above
   `sum(true zone demand) × margin_per_unit` is impossible (details in the staff marking guide).
4. Record marks in a copy of `part-b-marking-grid-template.xlsx` (kept outside this folder):

   | Criterion | Max |
   |---|---|
   | Demand Modelling & Forecasting | 20 |
   | Decision Modelling & Optimisation | 20 |
   | Integration, Scenarios & Insight | 20 |
   | Understanding & Justification | 15 |
   | Technical Quality & Reproducibility | 5 |
   | Executive Communication (slides + video) | 20 |
   | **Total** (automatic) | **100** |

   Enter `NS` for non-submissions.

### 5.4 Analysis tools

```
python 02-coursework-part-b/analysis/compare_student_datasets.py                 # 5 dummy IDs compared
python 02-coursework-part-b/analysis/compare_student_datasets.py --ids 10001 20002
python 02-coursework-part-b/analysis/demand_impact_demo.py                       # profit at 0.8x–1.2x demand
python 02-coursework-part-b/analysis/demand_impact_demo.py --data_dir <a generated data folder>
python 02-coursework-part-b/analysis/create_base_data.py                         # → analysis/output/base_data
```
All of them work in temporary or `output/` folders and never change the published data.

### 5.5 Making a new dataset for a new cohort (optional)

`create_base_data.py --seed 2026` reproduces the current base data exactly. For a fresh pool, use a new
seed (`--seed 2027`), then copy the four files from `analysis/output/base_data/` into **both**
`model-solution/base_data/` here and `starter-repo/base_data/` in the public folder, re-run both model
notebooks, and run `python scripts/run_all_checks.py` in both folders. (The test that checks
`create_base_data.py` reproduces the published files runs it with the default seed 2026; if you switch seeds,
add `"--seed", "<new seed>"` to that call in `tests/test_answer_files.py`.)

---

## 6. Timed in-class test — before, during and after

### Before the test

1. **Release revision material** following `open-book-materials-guidance.md`: practice papers and their
   *written* solutions yes; *coded* practice-paper solutions only after the test; nothing from this
   `03-in-class-test-2026-05/` folder.
2. **Prepare the room machines / student laptops** with Anaconda. Students run
   `student-setup/environment_check.ipynb`; all three tests (Pyomo + HiGHS, OR-Tools, SimPy) must print
   results. If one fails, the notebook's first cell shows the install command:
   `pip install pyomo simpy "ortools>=9.15,<9.16" "highspy>=1.11,<1.13"`.
3. Put the paper (`paper/in-class-test-2026-05.pdf`), `submission-template.docx` and
   `environment_check.ipynb` where students can download them (the checklist uses OneDrive).

### On the day

Follow `invigilation-checklist.docx` step by step: students download the files (without opening the
paper), run the environment check, restart the kernel, hear what to submit, then open the paper and
begin. (The checklist's "Run install" step is now only needed if the environment check fails.)
4 hours; they answer any questions and the best four count; work goes in the submission template
with code and Excel files attached.

### After the test — marking

1. Make a copy of `marking/in-class-test-marking-grid-template.xlsx` outside this folder. Row 1 holds the
   maximum for each sub-part (each question totals 25); enter marks from row 3. Question totals and the
   **overall mark (best four questions)** calculate automatically.
2. Check answers against `solutions/worked-solutions.pdf`. To regenerate any number:
   ```
   python 03-in-class-test-2026-05/solutions/in_class_test_code.py        # all six questions
   ```
   or interactively, from the `solutions` folder:
   ```python
   import worked_solution_snippets as ws
   ws.q3_results()          # q1_results() … q6_results()
   ```
   The Q5 forecasting workbook is written to `solutions/output/`. `worked_solutions.ipynb` contains the
   same solutions step by step (it also runs in Google Colab, see its setup note). It does **not** run on the
   course website, because Question 6 needs Google OR-Tools.
3. Questions: 1 LP/integer production, 2 set covering, 3 transhipment, 4 help-desk simulation (SimPy),
   5 additive vs multiplicative forecasting, 6 flow-shop (Johnson) and job-shop (CP-SAT) scheduling.

---

## 7. Maintaining the materials

| Task | How |
|---|---|
| Edit a paper or worked solution | Edit the `.tex`, then `python scripts/build_pdfs.py` (needs MiKTeX/MacTeX/TeX Live); `--check` lists stale PDFs |
| Edit solution code | Run `python scripts/run_all_checks.py` — it confirms the code still runs and still matches the published workbook and the Q5 numbers in the worked solutions |
| Create next year's test | Copy `03-in-class-test-2026-05/` to e.g. `03-in-class-test-2027-05/`, edit the `.tex` and code, rebuild PDFs, and update the `TEST_SOLUTIONS` path at the top of `tests/test_answer_files.py` |
| Move material to the public folder after an assessment | Copy the files across, update both READMEs, and run `run_all_checks.py` in the public folder |
| Share this folder with someone new | Run `python scripts/scan_for_personal_data.py --terms <names.txt kept outside the folder>` first |

Conventions: lower-case-hyphenated names for documents and folders, `snake_case` for Python; each
`.pdf` sits next to its `.tex`/`.docx` source with the same name; notebooks are saved **without outputs**
(the tests enforce this, because outputs can contain local paths).

---

## 8. Checks, troubleshooting and privacy

### Checks
```
python scripts/run_all_checks.py            # everything (about a minute)
python scripts/run_all_checks.py --quick    # skip notebook execution
```
Runs the personal-data scan and the tests, on a temporary copy: every script and notebook runs; the
data generator is repeatable and leak-free; `create_base_data.py` reproduces the published data; the
in-class test workbook and worked-solution numbers match the code; every `.tex` has its PDF; every
Office file opens. Skipped tests (missing packages) count as failures unless `--allow-skips` is given.

### Troubleshooting
| Problem | Fix |
|---|---|
| `conda` not recognised | Use **Anaconda Prompt**, or reopen the terminal after installing |
| `ModuleNotFoundError` | `conda activate 5cm522-or` |
| `No suitable Pyomo solver is available` | `pip install "highspy>=1.11,<1.13"` |
| Solver fails only when OR-Tools is also imported | Same fix — highspy 1.13+ clashes with OR-Tools 9.15 |
| Notebook kernel missing | `python -m ipykernel install --user --name 5cm522-or` |
| `FileNotFoundError: data/zones.csv` in a model notebook | Run the first cell (data generation) first |
| `pdflatex not found` | Install MiKTeX / MacTeX / TeX Live, or use the committed PDFs |

### Privacy rules
- This folder is public in the course repository. Never put student submissions, marks, feedback,
  moderation samples or scanned booklets in it.
- Use only dummy IDs (`TEST001`, `100000000`) in anything saved here.
- Run the personal-data scan before sharing; it must report *no findings*.
