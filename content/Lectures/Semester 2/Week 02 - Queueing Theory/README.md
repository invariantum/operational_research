# Semester 2 · Week 02 – Queueing Theory

Arrival and service distributions, Little's law, Kendall notation and the M/M/1 queue, worked in Excel.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `3 Tutorial` | Tutorial / practical sheet and any starter files | The practical |
| `4 Tutorial Answers` | Worked answers and answer notebooks | **Release after the practical** |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |

## 1 Lecture

- `Introduction to Queueing Theory.pdf`
- `M-M-1 queue derivation.pdf`

## 2 Lecture Demos

- `1 M-M-1 lecture example.xlsx`

## 3 Tutorial

- `Tutorial - Queueing Theory.pdf`
- `Tutorial Template.xlsx`

## 4 Tutorial Answers

- `Tutorial Answers.xlsx`

## Notes for staff

- Summary formulas corrected in `Tutorial Answers.xlsx` and `Tutorial Template.xlsx`: "Average Arrival Rate" and "Average Service Rate" (Question 1 O3:O4, Question 3 V3:V4) averaged the wrong columns and gave mean times over rows 2-356 only; they are now `1/AVERAGE(...)` of the inter-arrival and service-time columns over all 1000 rows. Question 3 V5:V6 averaged the running-average columns; they now average the per-customer times (M and Q). Answers now show 2.49 / 12.44 min (was 2.22 / 12.19) for the saved data; other sheets unchanged.
- In the template, V4-V6 show #DIV/0! until students fill in the service-time and waiting-time columns.
