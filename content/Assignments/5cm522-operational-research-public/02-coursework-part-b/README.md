# Coursework Part B: demand forecasting and store-network optimisation (25%, Semester 2)

## What you have to do

You are an analyst for *Yodafone*:

1. Forecast the missing zone demand with machine learning.
2. Use an integer programme to decide which stores to reopen.
3. Present your recommendation in slides and a short video.

Every student gets a **different dataset** generated from their own student number, so your numbers won't
match anyone else's.

## Steps

1. Read **`assessment-brief-part-b.pdf`**. It has the deliverables, milestones, deadline and rubric.
2. Accept the GitHub Classroom invitation from the module page. You get your own copy of
   [`starter-repo/`](starter-repo/) as a GitHub repository.
3. Clone your repository and follow **`starter-repo/README.md`**: install VS Code and conda, then create
   the environment.
4. Open `notebook.ipynb`, set `STUDENT_ID` to your student number and run the data-generation cell.
   This creates your personal `data/` folder.
5. Work through milestones 1–5 in the notebook. Column meanings are in
   [`../docs/data-dictionary.md`](../docs/data-dictionary.md).
6. Commit and push your notebook, then submit the slides and video as the brief describes.

You only edit `notebook.ipynb`. Do not change `generate_data.py`, `base_data/` or `environment.yml`.

## Files

| Item | What it is |
|---|---|
| `assessment-brief-part-b.pdf` | The brief (read this) |
| `assessment-brief-part-b.docx` | Editable source of the brief (staff) |
| [`starter-repo/`](starter-repo/) | Exactly what each student receives as a GitHub repository |

```
starter-repo/
├── README.md          set-up guide (software, environment, first steps)
├── notebook.ipynb     the notebook you complete (milestones 1-5)
├── generate_data.py   creates your personalised dataset from your student number
├── environment.yml    the coursework conda environment ("5cm522")
├── base_data/         synthetic data pool the generator samples from
├── .gitignore         keeps the generated data/ out of your commits
└── .vscode/           turns off AI features in VS Code for this repository
```

**Just want a look first?** The starter notebook also runs on the
[course website](https://invariantum.github.io/operational_research/lab/index.html?path=Assignments/5cm522-operational-research-public/02-coursework-part-b/starter-repo/notebook.ipynb)
without installing anything. Do the coursework itself in your own repository: work in the browser is
not saved to GitHub.

On your computer you can also generate a dataset directly: `python generate_data.py --student_id 100000000`
(`100000000` is a dummy number; use your own).
