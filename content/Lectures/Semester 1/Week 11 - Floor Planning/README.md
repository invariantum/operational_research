# Semester 1 · Week 11 – Floor Planning

Packing rectangles into the smallest floor area: non-overlap constraints with binary variables, and rotation.

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `5 Source Files` | Editable originals (.pptx, .docx, .md), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |

## 1 Lecture

- `Notes/Floor Planning - Pyomo Model.ipynb`
- `Notes/Floor Planning - Pyomo Model.md`
- `Week 11 - Floor Planning.pdf`

## 2 Lecture Demos

- `1 Floor planning - minimise area.ipynb` (notebook)
- `2 Floor planning - maximise number of items.ipynb` (notebook, optional: port of the MATLAB *max items* model)
- `3 Floor planning - maximise placed area.ipynb` (notebook, optional: port of the MATLAB *max item area* model)

## Notes for staff

- The handbook lists *Inventory Modelling* for Week 11; this folder holds the Floor Planning lecture instead.
- Notebooks 2 and 3 are Python ports of the MATLAB *max items* and *max item area* models (`5 Source Files/MATLAB`), with the same data and constraints. Optima: 6 of 7 items (proved: all 7 need area 21 > 20) and placed area 100 (= the whole floor).
- The ports use a tight big-M, `M = W + H + max(w, h)`, instead of MATLAB's 9999. With 9999 the solver can report a wrong optimum (5 items instead of 6) because of numerical tolerance. The *minimise area* notebook still uses 9999 and gets the right answer (12), but the same fix is recommended there.
- `model.py` and `Notes/Floor Planning - Pyomo Model.md` were fixed: `cm.get_cmap` (removed in Matplotlib 3.9) became `plt.get_cmap`.
- The HTML export in `5 Source Files/HTML Exports` still links a stylesheet on the author's computer (`file:///c:/Users/...`); it displays without it.
