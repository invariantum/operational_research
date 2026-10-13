"""Environment check for the in-class test: Pyomo + HiGHS, Google OR-Tools and SimPy.

Run it on the computer you will use for the test; every check should print a result.

Plain-script version of `environment_check.ipynb`; run it with `python environment_check.py`.
The `# %%` lines mark the notebook cells (VS Code can run them one by one).
"""

# %% [markdown]
# ## 1. Pyomo + HiGHS

# %%
from pyomo.environ import *

# Model
model = ConcreteModel()

# Variable
model.x = Var(domain=NonNegativeReals)

# Objective
model.obj = Objective(expr=2 * model.x, sense=maximize)

# Constraint
model.con = Constraint(expr=model.x <= 5)

# Solve
solver = SolverFactory("appsi_highs")
solver.solve(model, tee=False)

# Display the model
model.pprint()

# Display the results
model.display()

# %% [markdown]
# ## 2. Google OR-Tools (CP-SAT)

# %%
import importlib

try:
    cp_model = importlib.import_module("ortools.sat.python.cp_model")
except ImportError:
    cp_model = None
    print("OR-Tools is NOT installed. On your computer run:")
    print('    pip install "ortools>=9.15,<9.16" "highspy>=1.11,<1.13"')
    print("(OR-Tools has no browser version, so this message is expected on the course website.)")

if cp_model is not None:
    """Minimal CP-SAT example to showcase calling the solver."""
    # Creates the model.
    model = cp_model.CpModel()

    # Creates the variables.
    var_upper_bound = max(50, 45, 37)
    x = model.new_int_var(0, var_upper_bound, "x")
    y = model.new_int_var(0, var_upper_bound, "y")
    z = model.new_int_var(0, var_upper_bound, "z")

    # Creates the constraints.
    model.add(2 * x + 7 * y + 3 * z <= 50)
    model.add(3 * x - 5 * y + 7 * z <= 45)
    model.add(5 * x + 2 * y - 6 * z <= 37)

    model.maximize(2 * x + 2 * y + 3 * z)

    # Creates a solver and solves the model.
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Maximum of objective function: {solver.objective_value}\n")
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("No solution found.")

# %% [markdown]
# ## 3. SimPy

# %%
import simpy

def simple_process(env):
    print("Start at", env.now)
    yield env.timeout(5)
    print("End at", env.now)

env = simpy.Environment()
env.process(simple_process(env))
env.run()
