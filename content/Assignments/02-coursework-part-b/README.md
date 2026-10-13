# Coursework Part B: demand forecasting and store-network optimisation (25%, Semester 2)

**What it is about.** Students are analysts for the fictional retailer *Yodafone*. They (1) forecast the
missing zone demand with machine learning, (2) build an integer programme that decides which stores to
reopen, (3) test scenarios, and (4) present a recommendation. Every student gets a **different dataset**,
generated from their own student number, so no two answers match.

**What a student hands in** (deadline and weights in the brief):

| # | Deliverable | Where |
|---|---|---|
| 1 | Completed `notebook.ipynb` that runs top to bottom (80%) | pushed to their GitHub Classroom repository |
| 2 | Executive slide deck, 5–6 slides, PDF | Blackboard |
| 3 | Narrated video, 10 ± 1 minutes | Blackboard |
| 4 | Record of how AI tools were used (prompts or chat link) | Blackboard |

## Students: what to do, in order

| Step | Open | Do |
|---|---|---|
| 1 | `brief/assessment-brief-part-b.pdf` | Read the task, milestones, deliverables and rubric |
| 2 | the module page | Accept the GitHub Classroom invitation: you get your own copy of [`starter/`](starter/) |
| 3 | `starter/README.md` | Install VS Code and conda, create the environment from `starter/environment.yml` |
| 4 | `starter/notebook.ipynb` | Set `STUDENT_ID` to your student number and run the data-generation cell: it creates your `data/` folder |
| 5 | `brief/data-dictionary.md` | Look up what each column means, with units |
| 6 | `starter/notebook.ipynb` | Work through milestones 1–5, then the reflection and summary; commit and push |
| 7 | slides, video, AI record | Submit on Blackboard |

Only edit `notebook.ipynb`. Do not change `generate_data.py`, `base_data/` or `environment.yml`.

**Just want a look first?** The starter notebook also runs on the
[course website](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/02-coursework-part-b/starter/notebook.ipynb)
with nothing installed. Do the coursework in your own repository, though: work on the website is not saved
to GitHub. On a computer you can also generate a dataset directly:
`python starter/generate_data.py --student_id 100000000` (a dummy number; use your own).

## Staff

### 1. Run the model solutions

| Order | Notebook (script) | Approach |
|---|---|---|
| 1 | `solutions/notebook_solution_simple.ipynb` (`.py`) | Random-forest forecast → demand allocated once (all stores open) → each store's stand-alone profit → binary ILP; ±10% demand sensitivity. The minimum acceptable modelling chain |
| 2 | `solutions/notebook_solution_advanced.ipynb` (`.py`) | Same forecast → gravity allocation inside a MILP, so cannibalisation responds to which stores open; compared with the simple result. What a top-band answer looks like |

Both generate the data for the dummy ID `TEST001` into `solutions/data/` (git-ignored), then forecast,
optimise with HiGHS and plot; under 30 seconds each. They run on the
[course website](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/02-coursework-part-b/solutions/notebook_solution_simple.ipynb)
or on a computer (`python solutions/notebook_solution_simple.py`). Results for `TEST001`: simple 55 of 80
stores, profit £8.80M; advanced 46 stores, £9.83M. (In the browser the last digits of the profit differ
slightly because of a different scikit-learn version; the stores chosen are the same.)

`solutions/` carries its own copy of `generate_data.py` and `base_data/`, so it works on its own; the
checks make sure the copy stays identical to `starter/`.

### 2. Reproduce one student's dataset (when marking)

```
python starter/generate_data.py --student_id <student number> --out_dir "<a folder outside this repository>"
```

Same number → identical data, always. Never commit real student numbers, generated data or outputs.

### 3. Mark, in this order

| Step | File (in `staff/`) | Use |
|---|---|---|
| 1 | `staff-marking-guide.md` | The 10–15 minute per-student workflow and the profit sanity ceiling |
| 2 | `rubric-to-evidence-map.md` | What evidence earns each band, per criterion |
| 3 | `marking-workflow-notes.md` | Calibration on three scripts first; broken notebooks; alternative methods; logging concerns |
| 4 | `per-student-marking-template.md` | Copy once per student for notes (outside this repository) |
| 5 | `feedback-comment-bank.md` | Feedback sentences to adapt, by criterion and band |
| 6 | `part-b-marking-grid-template.xlsx` | Blank cohort grid with the six weighted criteria and an automatic total; copy it outside this repository. `NS` = non-submission |

Weights: Demand Modelling 20, Decision Modelling 20, Integration & Scenarios 20, Understanding &
Justification 15, Technical Quality 5, Executive Communication (slides + video) 20.

### 4. Dataset tools (`tools/`, computer only)

| Command (from this folder) | What it shows |
|---|---|
| `python tools/compare_student_datasets.py` | Data for five dummy IDs side by side: multipliers, demand, costs, margins (`--ids 10001 20002` for your own list) |
| `python tools/demand_impact_demo.py` | How ±20% demand changes single-store profitability (`--student_id`, `--data_dir`) |
| `python tools/create_base_data.py` | Rebuilds the synthetic base pool into `tools/output/base_data` (`--seed 2026` reproduces the published files). Never give this to students |

`tools/variation-analysis-report.md` explains why personalised datasets lead to different optimal solutions:
read it before answering "why is my answer different from my friend's?". For a new cohort with a fresh
pool, use a new seed, copy the four files into **both** `starter/base_data/` and `solutions/base_data/`,
re-run both model notebooks and the checks (and update the seed used in
`tools/tests/test_test_and_part_b_answer_files.py`).

## Files

| Path | What it is |
|---|---|
| `brief/assessment-brief-part-b.pdf` | The brief (`.docx` is its editable source) |
| `brief/data-dictionary.md` | Every column of the base and personalised data, with units |
| `starter/` | Exactly what each student receives as a GitHub repository: `README.md`, `notebook.ipynb`, `generate_data.py`, `base_data/`, `environment.yml`, `.gitignore` (keeps `data/` out of commits), `.vscode/` (turns off AI features) |
| `solutions/` | Two model-solution notebooks and their scripts, with their own `generate_data.py` and `base_data/` (staff) |
| `staff/` | Marking guide, rubric map, workflow notes, templates, comment bank, marking grid (staff) |
| `tools/` | Dataset comparison and rebuild tools, variation report (staff) |
