# Full revision booklet

All twelve questions from Practice Papers A and B in one continuously numbered booklet. Use it once you
have done the two papers separately, or instead of them.

## Steps

1. Attempt **`full-revision-booklet.pdf`** (questions 1–12).
2. Mark it against **`full-revision-booklet-solutions.pdf`**.
3. Run the three short solution notebooks. Each works on the
   [course website](https://invariantum.github.io/operational_research/) or on your computer:

| Notebook (script) | Question type | From |
|---|---|---|
| `greengrid_pyomo.ipynb` (`.py`) | GreenGrid Energy project selection: binary programme | Paper A |
| `northfield_transshipment_mcfp.ipynb` (`.py`) | Northfield Relief transhipment as a minimum-cost flow | Paper A |
| `uni_library_simpy.ipynb` (`.py`) | University library help-desk queue simulation (SimPy) | Paper B |

## Other files

| File | What it is |
|---|---|
| `full-revision-booklet.tex`, `full-revision-booklet-solutions.tex` | LaTeX sources of the two PDFs |
| `build_full_revision_booklet.py` | Maintainers only: rebuilds both `.tex` files from the practice-paper sources |

After editing a practice paper, rebuild the booklet and its PDFs on your computer:

```bash
python build_full_revision_booklet.py
python ../../scripts/build_pdfs.py 03-revision
```
The automatic tests fail if the booklet no longer matches the practice papers.
