"""Pyomo starter template: the smallest complete Pyomo + HiGHS model.

Copy it and change the numbers, variables and constraints for your own model.

Plain-script version of `pyomo_starter_template.ipynb`; run it with `python pyomo_starter_template.py`.
The `# %%` lines mark the notebook cells (VS Code can run them one by one).
"""

# %%
from pyomo.environ import *

model = ConcreteModel()

model.x = Var(range(2), domain=NonNegativeReals)

model.obj = Objective(expr=5*model.x[0]+7*model.x[1], sense=maximize)

model.constraint1 = Constraint(expr=3*model.x[0] + 2*model.x[1] <= 144)
model.constraint2 = Constraint(expr=model.x[0] >= 4*model.x[1])

print("Displaying model #################\n")
model.pprint()

# solve the optimisation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model, tee=False) # set tee=True to display solver output

print()

print("Displaying solution #################\n")
model.display()
