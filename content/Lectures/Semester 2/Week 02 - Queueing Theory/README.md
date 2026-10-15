# Semester 2 · Week 02 – Queueing Theory

Arrival and service distributions, Little's law, Kendall notation and the M/M/1 queue, in Excel and in Python.

**Open first:** `1 Lecture/Introduction to Queueing Theory.pdf`, then `2 Lecture Demos/2 Queueing examples in Python.ipynb`.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides and the M/M/1 derivation notes (PDF) | The lecture |
| `2 Lecture Demos` | The Excel M/M/1 workbook and a Python notebook of the slide examples | Lecture |
| `3 Tutorial` | Tutorial sheet and the Excel template | The practical |
| `4 Tutorial Answers` | Answers in Excel and in Python | **After the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx) | Staff only |

## 1 Lecture

| File | What it is |
| --- | --- |
| `Introduction to Queueing Theory.pdf` | Slides: distributions, Little's law, Kendall notation, M/M/1 formulas (p14), the λ = 0.5, μ = 4 example (pp15–16), costs (pp17–21), servers in series (pp24–25) |
| `M-M-1 queue derivation.pdf` | Optional: sampling exponential times and the derivation of the M/M/1 formulas (see errata) |

## 2 Lecture Demos

| File | What it shows | Runs in |
| --- | --- | --- |
| `1 M-M-1 lecture example.xlsx` | M/M/1 simulated with `-mean*LN(RAND())`; running average of time in system against 1/(μ−λ). Edit D3 (mean inter-arrival) and H3 (mean service) | Excel (F9 to re-run) |
| `2 Queueing examples in Python.ipynb` | The slide examples in Python: exponential sampling, the M/M/1 example, the cost comparison, servers in series, and simulation against theory across ρ (added for this site) | Browser |

## 3 Tutorial

- `Tutorial - Queueing Theory.pdf`: Q1–Q3 in Excel, Q4 the same in Python.
- `Tutorial Template.xlsx`: the formulas are set up; fill in the λ and μ values (the template opens with placeholders λ = 1, μ = 10 in Q1 and λ = 10 in Q2–Q3).

## 4 Tutorial Answers

| File | Answers |
| --- | --- |
| `Tutorial Answers.xlsx` | Q1–Q3 in Excel. Q1 theory: Wq = 1.5 min, W = 3 min |
| `Tutorial answers in Python.ipynb` | Q4: Q1–Q3 repeated in Python with the same recursion (added for this site) |

## Errata

| Where | Error | Correct | Status |
| --- | --- | --- | --- |
| Slides p19 (λ = 0.5, μ = 2) | "Customers have waited for 4.5 minutes" in total over 100 arrivals | About **16.5 minutes** expected (Wq = λ/(μ(μ−λ)) = 0.167 min per customer); a total of 4.5 or less happens in under 1% of runs | Note. The expected costs are £91.2 (μ = 4), £91.8 (μ = 2) and £147.6 (μ = 1), so "case 2 is cheapest" (p21) holds only for that run. Demo 2 shows both |
| Derivation p2, the exponential CDF | F(x) = 1 − λe^(−λx) | **F(x) = 1 − e^(−λx)** (the next lines use the right form) | Note |
| Derivation p5, the two rearranged equations | [P_{t+δt}(0) − P_{t+δt}(0)]/δt and [P_{t+δt}(n) − P_{t+δt}(n)]/δt | **[P_{t+δt}(n) − P_t(n)]/δt** | Note |
| Derivation p5 | "the general state n where n > 1" | **n ≥ 1** | Note |
| Derivation p6 | "mean number of customers in the queue" | **in the system** (N = λ/(μ−λ)) | Note |
| `Tutorial Answers.xlsx`, Q3 "Average Time in Queue" | Counts queueing at stage 1 only | Label now says "(stage 1 only)"; all three stages ≈ the same here, because stages 2–3 are faster | Fixed (label) |
| Running-average columns in both workbooks | Row n averaged the first n + 1 customers | Row n averages the first n | Fixed |
| Summary cells (rates, averages) in both workbooks | Averaged the wrong columns | Fixed during the migration (see below) | Fixed |

## Notes for staff

- Summary formulas corrected in `Tutorial Answers.xlsx` and `Tutorial Template.xlsx` (migration review): "Average Arrival Rate" and "Average Service Rate" (Q1 O3:O4, Q3 V3:V4) averaged the wrong columns over rows 2–356 only. They are now `1/AVERAGE(...)` of the inter-arrival and service-time columns over all 1,000 rows. Q3 V5:V6 averaged the running-average columns; they now average the per-customer times. The saved answers show 2.49 / 12.44 min (was 2.22 / 12.19).
- In the template, the summary cells show `#DIV/0!` until students fill in the service-time and waiting-time columns.
- The derivation notes say their MATLAB code is "on Course Resources"; that code is not in the course files. `2 Queueing examples in Python.ipynb` reproduces Figures 3, 4, 10 and 11.
