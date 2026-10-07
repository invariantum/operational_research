# Operational Research (5CM522)

Lecture slides, tutorials, worked answers and code for the **Operational Research** module, covering optimisation in Semester 1 and simulation in Semester 2.

[![Open in JupyterLite](https://jupyterlite.rtfd.io/en/latest/_static/badge.svg)](https://christsall99.github.io/operational_research/lab/index.html)

Click the badge to open the materials in **JupyterLite**, a full Jupyter environment that runs in your web browser. You don't need to install anything or create an account.

## What's covered

### Semester 1: Optimisation

| Week | Topic |
|------|-------|
| 1  | Introduction to Operational Research |
| 2  | Linear Programming 1 |
| 3  | Linear Programming 2 |
| 4  | Mathematical Programming: Modelling |
| 5  | Mixed Integer Programming |
| 6  | Integer Linear Programming: Further Problems |
| 7  | Scheduling: Flow Shop and Job Shop |
| 8  | Networks: Shortest Paths and Minimum Spanning Trees |
| 9  | Travelling Salesman Problem |
| 10 | Vehicle Routing Problem |
| 11 | Floor Planning |

### Semester 2: Simulation

| Week | Topic |
|------|-------|
| 1  | Introduction to Simulation |
| 2  | Introduction to Queueing Theory |
| 3  | Discrete Event Simulation with SimPy |
| 4  | Problem Structuring and Simulation Build |
| 5  | Coursework Release |
| 6  | Agent-Based Modelling with Mesa |
| 10 | Revision |

All materials are in [`content/Lectures`](content/Lectures), organised by semester and week.

## How to use these materials

- **Browse on GitHub.** Open any week's folder to view or download the slides (PDF/PowerPoint), tutorial sheets and answers.
- **Run in your browser.** Open the JupyterLite link above and go to `Lectures` in the file browser. Notebooks (`.ipynb`) open and run directly. Python scripts (`.py`) open in the editor, and you can paste their code into a notebook cell to run it.
- **Run on your own computer.** Click **Code → Download ZIP** at the top of this page and open the files with Python/Jupyter, Excel or MATLAB.

### Limits of the browser version

JupyterLite runs Python inside the browser using Pyodide. NumPy, pandas, Matplotlib, SciPy and NetworkX work. Some pure-Python packages are not preinstalled but can be added from a notebook cell, for example:

```python
%pip install simpy
```

Some things only work on your own computer:

- Pyomo models that call an external solver such as GLPK or CBC
- MATLAB (`.m`) files
- Excel workbooks, which need to be downloaded and opened in Excel

## Tools used in the module

Python (NumPy, SciPy, Pyomo, NetworkX, SimPy, Mesa, Matplotlib), Jupyter, Excel and MATLAB.

## Credits

The browser environment is built with [JupyterLite](https://github.com/jupyterlite/jupyterlite) from the [jupyterlite/demo](https://github.com/jupyterlite/demo) template. The template code is covered by the BSD-3-Clause licence in [`LICENSE`](LICENSE). The course materials are shared for educational use. Third-party papers included in some lecture folders remain the property of their authors.
