# 5CM522 Operational Research: assessments

All the assessment material for the University of Derby module **5CM522 Operational Research** (2025/26):
the briefs, the starter files students receive, worked solutions with runnable code, and the staff
marking material. Everything here is synthetic or anonymised; there is **no personal data** (see
[Privacy](#privacy)).

| Folder | Assessment | Weight | When | What a student hands in |
|---|---|---|---|---|
| [`01-coursework-part-a/`](01-coursework-part-a/) | Linear and integer programming | 25% | Semester 1 | A Word/PDF report with every answer, plus the Python code for each model, labelled by question (short viva afterwards) |
| [`02-coursework-part-b/`](02-coursework-part-b/) | Demand forecasting + store-network optimisation | 25% | Semester 2 | The completed `notebook.ipynb` (GitHub Classroom), a 5–6 slide PDF deck, a 10-minute video and an AI-use record (Blackboard) |
| [`03-in-class-test/`](03-in-class-test/) | Timed, open-book test: 4 hours, best 4 of 6 questions | 50% | May | The completed submission template (Word) plus every Excel/Python file used, labelled by question |

Each assessment folder has the same layout, and its `README.md` says what to open first and in which order:

| Sub-folder | What is in it | Who it is for |
|---|---|---|
| `brief/` | What the assessment asks (the brief, or the test paper), as PDF with its editable source | everyone; **read first** |
| `starter/` | What students start from: templates, the Part B starter repository, the test-day set-up check | students |
| `solutions/` | Model answers: written (PDF/Word) and as code, every example as a notebook (`.ipynb`) **and** a script (`.py`) | staff; students after the assessment |
| `staff/` | Marking guides, rubric and marking-grid templates, exam-day checklist | staff |
| `revision/` (in-class test only) | Practice papers with written answers and code | students |
| `tools/` (Part B only) | Staff tools for the personalised datasets | staff |

The top level also holds `requirements.txt` and `environment.yml` (one software environment for every
script and notebook), `tools/` (checks and PDF builder) and `CHANGELOG.md` (where every file came from).

---

## Where to start

| You are… | Open, in this order |
|---|---|
| A student, Part A | `01-coursework-part-a/README.md` → `brief/assessment-brief-part-a.pdf` → `starter/pyomo_starter_template.ipynb` |
| A student, Part B | `02-coursework-part-b/README.md` → `brief/assessment-brief-part-b.pdf` → `starter/README.md` |
| A student revising for the test | `03-in-class-test/README.md` → `revision/README.md` → `revision/practice-paper-a/` |
| Staff marking | the assessment's `README.md`, section *Staff* |
| Maintaining this folder | [Checks and maintenance](#checks-and-maintenance) below |

---

## Running the code

Every code example exists twice, with the same name: a **notebook** (`.ipynb`) and a plain **script**
(`.py`). Both give the same answers.

### A. In the browser: the course website (nothing to install)

1. Open <https://invariantum.github.io/operational_research/> and go to `Assignments`, then the folder you want.
2. Open a notebook (`.ipynb`). Run its **first cell**: it installs Pyomo, HiGHS and SimPy into the browser tab
   (about a minute the first time). Then use **Run → Run All Cells**.
3. Changes stay only in that browser. To keep a file, right-click it → *Download*.

Good to know:

- A `.py` file opens as text only in the browser; run the notebook with the same name instead.
- Use a normal browser window. In a private/incognito window (Firefox in particular) notebooks cannot
  read the data files next to them.
- Google OR-Tools has no browser version. The two examples that use it (Practice Paper B Question 1
  and the in-class test Question 6) solve the same job shop with Pyomo + HiGHS in the browser and get the
  same answer. The test-day `environment_check.ipynb` reports OR-Tools as missing there, as expected.
- Machine-learning results can differ in the last digits from a computer run, because the browser has
  a different scikit-learn version (Part B model solutions: same stores chosen, profit within about £150).

### B. On your computer

One-time set-up (Windows: use **Anaconda Prompt**; install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) first if needed):

```
cd "<path to>/content/Assignments"
conda env create -f environment.yml        # 5-10 minutes the first time
conda activate 5cm522-or                   # every time you open a new terminal
python tools/run_all_checks.py --quick     # last line should say: ALL CHECKS PASSED
```

Prefer pip? With Python 3.11: `python -m venv .venv`, activate it (`.venv\Scripts\activate` on Windows,
`source .venv/bin/activate` elsewhere), then `pip install -r requirements.txt`.

Then run a script with `python <file>.py` (from any folder), or open a notebook with `jupyter lab` or
VS Code (*Select Kernel* → `5cm522-or`). In a notebook the first cell does nothing on your computer.
Files the code writes go to an `output/` folder next to it, so published answer files are never overwritten.

> `highspy` is pinned below 1.13 on purpose: newer HiGHS clashes with the HiGHS inside OR-Tools 9.15
> when both are loaded. Don't upgrade it. (The repository's top-level `requirements.txt` is a different
> file: it builds the course website.)

**Google Colab:** upload the notebook (and any files next to it that it reads), run
`!pip install pyomo highspy simpy openpyxl` (add `ortools` for the in-class test), then *Run all*.

---

## Checks and maintenance

```
python tools/run_all_checks.py            # everything: personal-data scan + tests (a few minutes)
python tools/run_all_checks.py --quick    # skip running the notebooks
```

It works on a temporary copy and never changes your files. It checks that every script and notebook runs;
the Part B data generator is repeatable and personalised (and the solutions' copy is identical); the
published workbooks and worked-solution numbers match the code; the revision booklet matches the practice
papers; every `.tex` has its PDF; every Office file opens; and nothing personal is in the folder.

| Task | How |
|---|---|
| Edit a paper or written solution | Edit the `.tex`, then `python tools/build_pdfs.py` (needs MiKTeX/MacTeX/TeX Live) |
| Edit a code example | Edit the `.py` **and** the notebook with the same name, then run the checks |
| After editing Practice Paper A or B | `python 03-in-class-test/revision/full-revision-booklet/build_full_revision_booklet.py`, then rebuild the PDFs |
| Prepare next year's test | Replace the files in `03-in-class-test/brief`, `solutions` and `staff`; update `tools/tests/test_test_and_part_b_answer_files.py` if file names change |

Conventions: lower-case-hyphenated names for documents and folders, `snake_case` for Python; every PDF sits
next to its `.tex`/`.docx` source with the same name; notebooks are saved **without outputs** (the tests
enforce this, because outputs can contain local paths).

## Privacy

- This folder is **public**. Never add student submissions, marks, feedback, moderation records or
  scanned work. Use only dummy student numbers (`100000000`, `TEST001`).
- Before every commit run `python tools/scan_for_personal_data.py`; it must report *no findings*. To also
  check for specific names, keep a list **outside** the repository and add `--terms <file>`.
- The scan also looks inside Office files for hidden links (for example to a personal OneDrive) and author
  metadata.

© University of Derby. No open licence has been chosen, so all rights are reserved.
