# 5CM522 Operational Research

[![Open in JupyterLite](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://invariantum.github.io/operational_research/lab/index.html?path=00_START_HERE.ipynb)

Teaching materials and runnable Python examples for **5CM522 Operational Research**
(Level 5, 20 credits, University of Derby; module leader Dr Sam O'Neill).

The examples run **in your web browser** with [JupyterLite](https://jupyterlite.readthedocs.io):
no installation, no account, nothing to configure.

➡️ **Open the course site: <https://invariantum.github.io/operational_research/>**

Start with **`00_START_HERE.ipynb`**: it installs the optimisation and simulation packages and checks
that everything works.

---

## Course map

Every week folder has the same layout, used only as far as the week needs it:

| Folder | What is in it | When |
| --- | --- | --- |
| `1 Lecture` | Slides (PDF) and lecture notes | The lecture |
| `2 Lecture Demos` | Notebooks and spreadsheets shown in the lecture, numbered in teaching order | Run live in the lecture |
| `3 Tutorial` | Tutorial / practical sheet and starter files | The practical |
| `4 Tutorial Answers` | Worked answers and answer notebooks | Release after the practical |
| `5 Source Files` | Editable originals (.pptx, .docx), the scripts the notebooks came from, MATLAB, older versions, staff notes | Staff only |
| `6 Further Reading` | Papers and external material | Optional |

Each week also has a `README.md` listing its files and any notes for staff.

**New to Semester 1?** Read `Lectures/Semester 1/README.md` first: what to do each week, in which order, and how the weeks connect.

**New to Semester 2?** Read `Lectures/Semester 2/README.md` first, in the same way.

| Semester 1 | Notebooks | Tools |
| --- | --- | --- |
| `Week 01 - Introduction to Operational Research` | 3 | NumPy, Matplotlib, ipywidgets |
| `Week 02 - Linear Programming 1` | 6 | SciPy `linprog`, Excel Solver |
| `Week 03 - Linear Programming 2` | 9 | Pyomo + HiGHS |
| `Week 04 - Mathematical Programming - Modelling` | 7 | Pyomo + HiGHS |
| `Week 05 - Mixed Integer Programming` | 13 | Pyomo + HiGHS |
| `Week 06 - Integer Linear Programming - Further Problems` | 8 | Pyomo + HiGHS |
| `Week 07 - Flow Shop and Job Shop Scheduling` | 5 | NumPy, Pyomo + HiGHS, Excel |
| `Week 08 - Networks - Shortest Paths and MST` | – | Slides and worked answers |
| `Week 09 - Travelling Salesman Problem` | 1 | Pyomo + HiGHS |
| `Week 10 - Vehicle Routing Problem` | 1 | Pyomo + HiGHS |
| `Week 11 - Floor Planning` | 4 | Pyomo + HiGHS |

| Semester 2 | Notebooks | Tools |
| --- | --- | --- |
| `Week 01 - Introduction to Simulation` | 5 | NumPy, pandas, Pyomo + HiGHS, Excel |
| `Week 02 - Queueing Theory` | 2 | NumPy, Excel |
| `Week 03 - Discrete Event Simulation with SimPy` | 10 | SimPy |
| `Week 04 - Problem Structuring and Simulation Build` | 2 | SimPy |
| `Week 05 - Coursework Part B Release` | – | Brief in `Assignments/02-coursework-part-b` |
| `Week 06 - Agent Based Modelling` | 5 | Mesa |
| `Week 10 - Revision` | 4 | Pyomo + HiGHS, SimPy, NumPy |

`Assignments/` holds one folder per assessment (see `Assignments/README.md`): `01-coursework-part-a`,
`02-coursework-part-b` and `03-in-class-test` (with its revision papers). Each has the same layout (`brief/`,
`starter/`, `solutions/`, `staff/`) and a `README.md` that says what to do, in order.

Open the `.ipynb` notebooks: in the browser a `.py` file opens as text only (the original scripts are kept in
each week's `5 Source Files/Python`). Excel examples (`.xlsx`) need Excel. Week 06 notebooks install Mesa the same way (`%pip install mesa networkx`). Every notebook is checked
automatically on each push (see *Automatic notebook test* below).

## Using the site

1. Open the site, double-click a folder, then a notebook.
2. Run the first code cell (it installs Pyomo, HiGHS and/or SimPy), then *Run → Run All Cells*.
3. **Save your work by downloading it.** Notebooks you change are stored only in this browser;
   clearing browser data or switching computer loses them. Right-click the file → *Download*.

Use a recent Chrome, Edge or Firefox. The first run downloads Python and the packages (tens of
megabytes), so allow a minute; later runs in the same browser are faster.

The same notebooks also run in Google Colab and in Anaconda Jupyter. The first cell uses
`%pip install`, which works in all three.

## Repository layout

```
.github/workflows/deploy.yml          builds the site and publishes it to GitHub Pages on every push to main
.github/workflows/test-notebooks.yml  runs every notebook in Pyodide and reports failures
requirements.txt                      packages used to BUILD the site (not the course code)
jupyter_lite_config.json              site build settings (keeps .vscode/ folders off the site; .git* files are excluded by default)
tools/convert_to_notebooks.py         turns course .py scripts into browser-ready notebooks
tools/test_notebooks_pyodide.mjs      the notebook tester used by test-notebooks.yml
content/                              everything here appears on the site
  00_START_HERE.ipynb                 environment check, run first
  Handbook/                           module handbook and module descriptor
  Lectures/Semester 1/README.md       start-here guide: reading order and how the weeks connect
  Lectures/Semester 1/Week 01 … 11/   one folder per week, layout above
  Lectures/Semester 2/README.md       start-here guide: reading order, how the weeks connect, running locally
  Lectures/Semester 2/Week 01 … 10/   one folder per week, layout above
  Assignments/                        01-coursework-part-a/, 02-coursework-part-b/, 03-in-class-test/
```

## For maintainers

### Publishing
Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the site with
`jupyter lite build --contents content` and deploys it to GitHub Pages. The first time, enable
**Settings → Pages → Build and deployment → Source: GitHub Actions**. A build takes a few minutes;
watch it under the **Actions** tab. You can also start a build by hand from that tab
(*Build and Deploy → Run workflow*).

**Everything inside `content/` is published and downloadable**, including any answer files.
Keep staff-only material (solutions, exam papers) out of this repository, or in a private one.

### Adding a new example
1. Put the `.py` file in the week's `2 Lecture Demos` (or `4 Tutorial Answers`) folder.
2. Convert it:
   ```bash
   python tools/convert_to_notebooks.py "content/Lectures/Semester 1/Week 05 - Mixed Integer Programming/2 Lecture Demos/my_model.py"
   ```
   This writes `my_model.ipynb` beside it, adds the install cell and the browser fixes, switches GLPK/CBC to
   HiGHS (`SolverFactory('appsi_highs')`) and splits the script into cells. Then move the `.py` into
   `5 Source Files/Python` and give the notebook a numbered name (`9 My model.ipynb`).
   Add `--force` to rebuild a notebook that already exists, `--markdown` to convert `.md` notes that contain
   ```` ```python ```` blocks, or `--patch-notebooks` to fix existing notebooks in place.
   Scripts inside any `… Source Files` folder are skipped.
3. Add the new file to the week's `README.md`, then commit and push; the site rebuilds itself.

### Automatic notebook test
`.github/workflows/test-notebooks.yml` runs every notebook in `00_START_HERE.ipynb`, `Lectures/`
and `Assignments/` inside Pyodide (the same engine as the site) on every push. Results appear
on the run's **Summary** page; a red cross means a notebook needs fixing, not that the site is down.
To run it yourself (needs Node.js 22 and an unpacked
[Pyodide release](https://github.com/pyodide/pyodide/releases)):
```bash
node tools/test_notebooks_pyodide.mjs --pyodide path/to/pyodide content/Lectures
```
A cell tagged `raises-exception` may fail on purpose; notebooks that import OR-Tools are skipped.

### What is different in the browser, and how the notebooks handle it
| Browser limitation | Effect | How it is handled |
| --- | --- | --- |
| No external programs | GLPK/CBC cannot run | Notebooks use HiGHS (`SolverFactory('appsi_highs')`); optimal values are unchanged, but where a problem has several optimal solutions HiGHS may report a different one from the answer sheets |
| Packages not bundled with Pyodide | `ModuleNotFoundError` for Pyomo, SimPy, ipywidgets | First cell runs `%pip install …` |
| No threads | Pyomo's HiGHS interface fails with "can't start new thread" | First cell of every Pyomo notebook switches off Pyomo's output capture in the browser only |
| Notebook output returns `None` from `write()` | `model.pprint()` / `model.display()` fail with a `TypeError` | The same first cell adapts Pyomo's printing in the browser only |
| One copy of HiGHS per kernel | SciPy `linprog`/`milp` and Pyomo + HiGHS in the **same** notebook crash the kernel | Keep them in separate notebooks; the converter adds a warning if it sees both |
| No OR-Tools build | OR-Tools code cannot run | Job-shop answers rewritten in Pyomo (Week 07, `Job Shop Q1-Q3 answers.ipynb`); the converter flags any other OR-Tools notebook |

`tools/convert_to_notebooks.py` applies the first five automatically, both to new conversions and
(with `--patch-notebooks`) to existing notebooks.

### Running locally (optional)
```bash
python -m pip install -r requirements.txt
jupyter lite build --contents content --output-dir dist
jupyter lite serve --output-dir dist      # then open http://localhost:8000
```

## Credits

Course materials: 5CM522 module team, University of Derby.
Site template: [jupyterlite/demo](https://github.com/jupyterlite/demo) (BSD-3-Clause, see `LICENSE`).
