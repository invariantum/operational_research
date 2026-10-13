# Part B analysis (staff)

Tools for understanding or rebuilding the personalised datasets. Run them **on your computer**
(`conda activate 5cm522-or`, from the top of the staff folder). None of them changes the published data.

| Order | Command | What it shows |
|---|---|---|
| 1 | `python 02-coursework-part-b/analysis/compare_student_datasets.py` | Generates data for five dummy IDs in a temporary folder and compares multipliers, demand, opening costs and margins (`--ids 10001 20002` for your own list) |
| 2 | `python 02-coursework-part-b/analysis/demand_impact_demo.py` | How ±20% demand changes single-store profitability (`--student_id`, `--data_dir`) |
| 3 | `python 02-coursework-part-b/analysis/create_base_data.py` | Rebuilds the synthetic base pool into `analysis/output/base_data` (`--seed 2026` reproduces the published files). Never give this to students |

`variation-analysis-report.md` explains why personalised datasets lead to different optimal solutions.
Read it before answering "why is my answer different from my friend's?".
