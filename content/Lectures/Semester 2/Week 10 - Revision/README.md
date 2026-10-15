# Semester 2 · Week 10 – Revision

Revision for the in-class test: five selected questions with worked solutions, and code for four of them.

**Open first:** `3 Tutorial/Week 10 Revision Selected Questions.pdf`. Try each question, then check
`4 Tutorial Answers/Week 10 Revision Selected Questions - Solutions.pdf` and the notebooks.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | The original revision sheet | The session |
| `3 Tutorial` | The selected questions, reformatted | Practice |
| `4 Tutorial Answers` | Worked solutions, notebooks, the workbook for Q2 and Q5 | **After you have tried them** |
| `5 Source Files` | LaTeX sources and the original scripts | Staff only |

## The five questions

| Q | Topic | Answer files | Related week |
| --- | --- | --- | --- |
| 1 | GreenGrid: binary project selection | Solutions PDF; `GreenGrid - project selection (Pyomo).ipynb` | Semester 1 Week 05 (MIP) |
| 2 | Hock-Brooke: warehouse size by simulation | Solutions PDF (corrected); `Hock-Brooke - warehouse simulation.ipynb`; workbook sheet *Q2 - Simulation* | Weeks 01–02 (lookup-table simulation) |
| 3 | University library help desk (SimPy) | Solutions PDF; `University library - simulation (SimPy).ipynb` | Week 03 |
| 4 | F.B. Knight: transportation and transhipment | Solutions PDF; `F.B. Knight - transhipment (Pyomo).ipynb` | Semester 1 Week 08 (transhipment); Week 01 demo 6 |
| 5 | N&F: forecasting with additive and multiplicative seasonality | Solutions PDF; workbook sheets *Q1 Additive*, *Q1 Multiplicative* | Forecasting lectures (not on this site) |

`1 Lecture/Revision.pdf` points to lecture numbers in the module's running count: Lecture 5 = Semester 1 Week 05, Lecture 12 =
Semester 2 Week 01, Lecture 14 = Semester 2 Week 03. Lectures 19 and 20 fall in Semester 2 Weeks 08–09 (the handbook lists forecasting there), which have
no folder on this site.

## Notebooks and the original scripts

`5 Source Files/Python/greengrid_pyomo.py`, `fb_knight_mcfp_pyomo.py` and `uni_library_simpy.py` are kept unchanged. Their notebooks
are the same code split into steps. The library notebook adds a section at the end for parts (c) and (e): a table for 2, 3 and 4
advisers, and 200 replications. `Hock-Brooke - warehouse simulation.ipynb` is new and goes with the corrected Q2.

## Errata

| ID | Where | Error | Correct | Status |
| --- | --- | --- | --- | --- |
| C1 | Q2 Hock-Brooke: workbook *Q2 - Simulation* and *Q2 - Analysis*; Solutions PDF pp2–3 | The workbook had the Delivered and Demand tables swapped, and the demand values shifted down by one, so it simulated a different problem. The PDF's long-run costs (102.16 for 8 spaces …) and its answer "8 spaces" came from that. The PDF's 12-week table charged overflow on the closing stock | Data as set; space charged on the stock held during the week (opening + Monday delivery); expected cost over 52 weeks from empty. Capacity 9 ≈ **£243.78** per week; best ≈ **15 spaces (£221.56)**, with 14 and 16 within £1. Over 12 weeks the best is 11 spaces. Deliveries (mean 8.80) exceed demand (8.65), so stock builds up and there is no stable long-run average | Fixed: workbook *Q2 - Simulation* corrected (52-week average in M13); *Q2 - Analysis* and *Sheet1* (frozen runs of the old model) marked superseded; Solutions PDF rebuilt from the corrected `.tex`; new notebook |
| C17 | Q3(c) University library: "minimum number of advisers is 3" | Based on one run (seed 24), which happens to be a quiet day (about 70 students served, against 90 expected arrivals) | With 200 replications, 3 advisers average about 94% under 8 minutes and meet 97% on only about half the days; 4 advisers average about 99%. Erlang C: 92.0% (3) and 99.1% (4) | **Open: not changed, awaiting the module leader's decision.** The notebook shows both results |

## Notes for staff

- More revision material is in `Assignments/03-in-class-test/revision`.
- The page images `revision_page-1…7.png` were removed in an earlier review: they were exact renders of `1 Lecture/Revision.pdf`. The LaTeX build files (`.aux`, `.log`) were not migrated.
- To rebuild a solutions PDF: `pdflatex` the `.tex` in `5 Source Files/LaTeX` twice (packages: lmodern, booktabs, enumitem, tikz). Then copy the PDF to `4 Tutorial Answers`.
- `5 Source Files/LaTeX/README (Formatted Pack).md` lists where each file of the original pack now lives.
