# Semester 1 · Week 09 – Travelling Salesman Problem

The TSP, why it is hard, the subtour problem and the Miller–Tucker–Zemlin formulation in Pyomo.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |

## 1 Lecture

- `Travelling Salesman Problem.pdf`

## 2 Lecture Demos

- `1 TSP with Pyomo.ipynb` (notebook)

## Notes for staff

- The notebook's saved outputs (including the 4-city GLPK log and four plots) were cleared, as listed in the root `FIXES_README.md` (M2).
- The genetic-algorithm cell uses Python's `random` without a seed, so the tour length changes on every run (the old saved output was 625.16; two test runs gave 704.08 and 573.67). Add `random.seed(...)` if students should see the same number.
