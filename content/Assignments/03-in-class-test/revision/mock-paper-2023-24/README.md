# Mock paper 2023/24 (older format)

**Questions:**
1. forecasting;
2. simulation;
3. transportation/transhipment;
4. inventory (EOQ, not a current focus);
5. linear programming.

## Steps

1. Attempt **`mock-paper-2023-24.pdf`**, or the same paper in the current style:
   `reformatted/mock-paper-2023-24-reformatted.pdf`.
2. Mark it against **`mock-paper-2023-24-answers.pdf`**, or
   `reformatted/mock-paper-2023-24-reformatted-solutions.pdf`.
3. Follow the Excel working in `mock-paper-2023-24-answers-workings.xlsx`.
4. Run **`mock_paper_2023_24_answers.ipynb`** on the
   [course website](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/03-in-class-test/revision/mock-paper-2023-24/mock_paper_2023_24_answers.ipynb),
   or `python mock_paper_2023_24_answers.py` on your computer. It has the
   Pyomo answers to the LP and transportation questions.

## Files

| File | What it is |
|---|---|
| `mock-paper-2023-24.pdf` / `.docx` | Original mock paper (5 questions) |
| `mock-paper-2023-24-answers.pdf` / `.docx` | Written answers |
| `mock-paper-2023-24-answers-workings.xlsx` | Excel workings: additive and multiplicative forecasting, simulation, inventory |
| `mock_paper_2023_24_answers.ipynb` | Pyomo answers to the LP and transportation/transhipment questions |
| `mock_paper_2023_24_answers.py` | The same code as a script for your computer (`python mock_paper_2023_24_answers.py`) |
| `reformatted/` | The same mock in the current paper style, with solutions (PDF only; the inventory question is removed) |

**Question 3a has two optimal plans.** The answer sheet (solved with GLPK) and the code (HiGHS) ship the
goods differently but both cost the minimum, 1830; the notebook checks this in the cell after Question 3a.
