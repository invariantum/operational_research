# Revision for the timed in-class test

Practice material for [the in-class test](../README.md). Each paper folder has the same files: the paper (PDF),
its written solutions (PDF), the code answers as a notebook **and** a script, and any spreadsheet workings.

The test is open book and lasts 4 hours. There are six questions, and your best four count.

Topics:
- linear programming;
- integer and binary modelling;
- simulation (Monte Carlo and SimPy);
- flow-shop and job-shop scheduling;
- networks (including the minimum spanning tree);
- transportation and transhipment;
- forecasting with additive and multiplicative models.

You may use your notes, code and files, but **not AI tools**.

## Use the materials in this order

| Step | Folder | What it is | Like the current test? |
|---|---|---|---|
| 1 | [`practice-paper-a/`](practice-paper-a/) | LP, binary modelling, MST, simulation, forecasting, transhipment | **Yes** |
| 2 | [`practice-paper-b/`](practice-paper-b/) | Flow/job-shop scheduling, maximum coverage, SimPy queue, forecasting, LP, transportation | **Yes** |
| 3 | [`full-revision-booklet/`](full-revision-booklet/) | Papers A and B in one booklet (questions 1–12), plus three short solution notebooks | **Yes** |
| 4 | [`mock-paper-2023-24/`](mock-paper-2023-24/) | Older mock: forecasting, simulation, transportation, inventory, LP | Partly |
| 5 | [`sample-questions-2023-24/`](sample-questions-2023-24/) | Older practice: LP, simulation, transportation, inventory, moving averages | Partly |
| any time | [`../../01-coursework-part-a/starter/`](../../01-coursework-part-a/starter/) | `pyomo_starter_template`: the smallest Pyomo + HiGHS model, to start your own | — |

Inventory modelling (EOQ) in the older materials is **not** a focus of the current test.

## How to revise with each paper

1. **Attempt** the paper from its PDF, by hand, in Excel or in Python, under time pressure if you can.
2. **Mark** your attempt against the written solutions (`…-solutions.pdf` / `…-answers.pdf`).
3. **Run** the reference code to see one way of solving it in Python: the notebook (`.ipynb`) on the
   [course website](https://invariantum.github.io/operational_research/) or on your computer, or the
   `.py` script on your computer (see [Running the code](../../README.md#running-the-code)). Then check the spreadsheet workings (`.xlsx`).
4. **Practise recognising** *which* OR method fits a problem from its wording, not just its numbers.

## Files in each paper folder

| Pattern | Meaning |
|---|---|
| `<paper>.pdf` | Question paper (`.tex` / `.docx` is its editable source) |
| `<paper>-solutions.pdf` / `-answers.pdf` | Written solutions |
| `*.xlsx` | Spreadsheet workings (forecasting, simulation checks) |
| `*.ipynb` | Reference solution as a notebook: runs on the course website, in Jupyter, VS Code or Colab |
| `*.py` (same name) | The same code as a script for your computer; files it writes go to `output/` |

The written solutions and these files are released before the test; the coded practice-paper
answers may be held back until after it (see the module page).
