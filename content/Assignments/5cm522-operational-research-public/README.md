# 5CM522 Operational Research — Student Materials (2025/26)

Everything a student needs for the assessments of the University of Derby module
**5CM522 Operational Research**:

| Assessment | Weight | When | Folder |
|---|---|---|---|
| Coursework Part A: linear and integer programming | 25% | Semester 1 | [`01-coursework-part-a/`](01-coursework-part-a/) |
| Coursework Part B: demand forecasting and store-network optimisation | 25% | Semester 2 | [`02-coursework-part-b/`](02-coursework-part-b/) |
| Timed in-class test: open book, 4 hours, best 4 of 6 questions | 50% | May | [`03-revision/`](03-revision/) (revision papers with solutions) |

> All data is synthetic and there is no personal data in this folder. The dates in the briefs are for 2025/26.
> **Module leader:** Dr Sam O'Neill (contact via the module page).

---

## 1. Start here: your route through the module

Work through the folders in number order. Each folder's `README.md` lists every file and says what to do.

| Step | When | Do this | Open |
|---|---|---|---|
| 1 | Week 1 | Get Python working (section 2), or just use the course website | [course website](https://invariantum.github.io/operational_research/) |
| 2 | Semester 1 | Read the Part A brief, then solve the models by hand, in Excel or with Pyomo | `01-coursework-part-a/assessment-brief-part-a.pdf`, then `03-revision/templates/pyomo_starter_template.ipynb` |
| 3 | Semester 2 | Read the Part B brief, accept the GitHub Classroom invitation, then follow the starter repository's README | `02-coursework-part-b/assessment-brief-part-b.pdf`, then `02-coursework-part-b/starter-repo/README.md` |
| 4 | Before the test | Revise with the practice papers in the order given in `03-revision/README.md` | `03-revision/README.md` |
| 5 | Test day | Bring your notes and code. AI tools are not allowed | — |

**Everything you read is a PDF.** You only need Python to *run* the notebooks and code.

---

## 2. Two ways to run the code

### A. In your web browser (no installation)

All the code in this folder also works on the **course website**: <https://invariantum.github.io/operational_research/>.

1. Open the site, double-click `Assignments` → `5cm522-operational-research-public`, then the folder you want.
2. Open a notebook (`.ipynb`). Run the **first cell** (it installs Pyomo, HiGHS and SimPy into the browser
   tab; allow about a minute the first time), then use **Run → Run All Cells**.
3. **Save your work by downloading it** (right-click the file → *Download*). Changes are kept only in that
   browser.

In the browser, a `.py` file only opens as text. Use the notebook with the same name instead
(for example `practice_paper_a_code.ipynb` rather than `practice_paper_a_code.py`).

Direct links:

| Notebook | Opens |
|---|---|
| Pyomo starter template | [open](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/5cm522-operational-research-public/03-revision/templates/pyomo_starter_template.ipynb) |
| Practice Paper A: all answers | [open](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/5cm522-operational-research-public/03-revision/practice-paper-a/practice_paper_a_code.ipynb) |
| Practice Paper B: all answers | [open](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/5cm522-operational-research-public/03-revision/practice-paper-b/practice_paper_b_code.ipynb) |
| Part B starter notebook (to look at only: do the coursework in your own repository) | [open](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/5cm522-operational-research-public/02-coursework-part-b/starter-repo/notebook.ipynb) |

### B. On your own computer (needed for Coursework Part B and for the test)

One-time setup, about 10 minutes:

1. **Install Miniconda** from <https://docs.conda.io/en/latest/miniconda.html>. Skip this if you already have
   Anaconda. No admin rights are needed.
2. **Open a terminal in this folder.** On Windows, open **Anaconda Prompt** and `cd` to the folder, e.g.
   `cd "C:\Users\<you>\Downloads\5cm522-operational-research-public"`. On macOS or Linux, use Terminal.
3. **Create the environment** (5–10 minutes the first time): `conda env create -f environment.yml`
4. **Activate it**, every time you open a new terminal: `conda activate 5cm522-or`
5. **Check it works:** `python scripts/run_all_checks.py --quick`. The last line should end with
   `ALL CHECKS PASSED`.

Then open notebooks with `jupyter lab` (or in VS Code: *Select Kernel* → `5cm522-or`) and run scripts
with `python <file>.py`. Scripts work from any folder.

> **Prefer pip?** With Python 3.11: `python -m venv .venv`, activate it
> (`.venv\Scripts\activate` on Windows, `source .venv/bin/activate` elsewhere), then
> `pip install -r requirements.txt`.
>
> **Why some packages come from pip inside `environment.yml`:** OR-Tools is not on conda for Windows,
> and HiGHS newer than 1.12 clashes with OR-Tools, so their versions are pinned. Don't upgrade `highspy`
> past 1.12.

---

## 3. What every folder and file is

```
5cm522-operational-research-public/
│
├── README.md                     ← this guide
├── CHANGELOG.md                  how this folder was prepared; old → new file names
├── environment.yml               software list for conda (one command installs everything)
├── requirements.txt              the same list for pip users
├── .gitignore / .gitattributes   keep generated files out of git; consistent line endings
│
├── 01-coursework-part-a/         COURSEWORK PART A: linear & integer programming (25%)
│   ├── README.md                       what to do, step by step
│   ├── assessment-brief-part-a.pdf     the brief (read this)
│   └── assessment-brief-part-a.docx    editable source of the brief
│
├── 02-coursework-part-b/         COURSEWORK PART B: forecasting + store-network optimisation (25%)
│   ├── README.md                       what to do, step by step
│   ├── assessment-brief-part-b.pdf     the brief (read this)
│   ├── assessment-brief-part-b.docx    editable source of the brief
│   └── starter-repo/                   exactly what each student receives (as a GitHub repository)
│       ├── README.md                   set-up guide: VS Code, conda, first steps
│       ├── notebook.ipynb              THE file you complete (milestones 1–5)
│       ├── generate_data.py            turns your student number into your personal dataset (do not edit)
│       ├── environment.yml             the coursework conda environment ("5cm522")
│       ├── base_data/                  synthetic data the generator samples from (do not edit)
│       ├── .gitignore                  stops the generated data/ folder being committed
│       └── .vscode/settings.json       turns off AI features in VS Code for this repository
│
├── 03-revision/                  REVISION FOR THE TIMED IN-CLASS TEST
│   ├── README.md                       topics and the order to use the papers in
│   ├── practice-paper-a/               ★ closest to the current test
│   ├── practice-paper-b/               ★ closest to the current test
│   ├── full-revision-booklet/          Papers A and B in one booklet (questions 1–12) + 3 extra solutions
│   ├── mock-paper-2023-24/             older mock paper with answers
│   ├── sample-questions-2023-24/       older practice questions with answers
│   └── templates/
│       └── pyomo_starter_template.ipynb    the smallest complete Pyomo + HiGHS model, to copy
│
├── docs/
│   └── data-dictionary.md        every column of the Part B data, with units
│
├── scripts/                      tools; you rarely need to open these
│   ├── run_all_checks.py         one command that checks the whole folder
│   ├── build_pdfs.py             rebuilds PDFs after a .tex file is edited
│   └── scan_for_personal_data.py checks nothing personal is in the folder before sharing
│
└── tests/                        the automatic checks run by run_all_checks.py
```

Folders that appear after you run things are safe to delete and never committed: `output/` (workbooks
written by the code), `starter-repo/data/` (your generated dataset), `__pycache__/`, `.ipynb_checkpoints/`.

### How files are named

| Pattern | Meaning |
|---|---|
| `<name>.pdf` | Ready to read or print |
| `<name>.docx` / `<name>.tex` | Editable source of the PDF with the same name |
| `…-solutions` / `…-answers` | Written solutions for the paper with the same name |
| `…-workings.xlsx` / `…-worked.xlsx` / `…-checker.xlsx` | Spreadsheet calculations behind the answers (open in Excel) |
| `<name>.ipynb` | Notebook: runs on the course website, in Jupyter, VS Code or Colab |
| `<name>.py` | The same code as a plain script: `python <name>.py` on your computer |
| `01-`, `02-`, `03-` | Use the folders in this order |

---

## 4. Checking that everything works

```
python scripts/run_all_checks.py            # full check, a few minutes
python scripts/run_all_checks.py --quick    # skip running the notebooks
```

It works on a temporary copy, so it never changes your files. It runs:

1. **A personal-data scan** for student/staff numbers, e-mail addresses, local user paths and author metadata.
2. **The tests in `tests/`**, which check that:
   - every script and notebook runs;
   - the Part B data generator is repeatable and personalised;
   - the forecasting workbooks match the code;
   - the revision booklet matches Practice Papers A and B;
   - every `.tex` has its PDF and every Office file opens.

A skipped test (missing package) counts as a failure. To allow skips, add `--allow-skips`.

Editing a paper (maintainers): edit the `.tex`, then run `python scripts/build_pdfs.py` (needs MiKTeX, MacTeX
or TeX Live). After editing Practice Paper A or B, first run
`python 03-revision/full-revision-booklet/build_full_revision_booklet.py`.

---

## 5. Troubleshooting

| Problem | Fix |
|---|---|
| Course website: a notebook says `ModuleNotFoundError` | Run the notebook's first cell, then the others |
| Course website: my changes disappeared | Work is kept only in that browser. Download files you change |
| `conda` is not recognised | Use **Anaconda Prompt** (Windows), or reopen the terminal after installing Miniconda |
| `ModuleNotFoundError: pyomo` / `simpy` / `ortools` on your computer | `conda activate 5cm522-or` |
| `No suitable Pyomo solver is available` | `pip install "highspy>=1.11,<1.13"` |
| Notebook can't find a kernel | `python -m ipykernel install --user --name 5cm522-or`, then choose that kernel |
| `FileNotFoundError: data/zones.csv` in the Part B notebook | Run the data-generation cell (section 1 of the notebook) first |
| Environment seems broken | `conda env remove -n 5cm522-or`, then `conda env create -f environment.yml` |

---

## 6. Privacy, reuse and changes

- There is **no personal data** in this folder. Before publishing a change, run
  `python scripts/scan_for_personal_data.py`. It must report *no findings*.
- Never add student submissions, marks, feedback or scanned work here.
- © University of Derby. No open licence has been chosen yet, so all rights are reserved.
- `CHANGELOG.md` records how the folder was prepared and where each file came from.
- Staff material (model answers, marking, the in-class test) is in the companion folder
  `5cm522-operational-research-staff-only`.
