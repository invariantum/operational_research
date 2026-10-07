from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Decision variables (non-negative)
model.x = Var([0, 1], domain=NonNegativeReals)

# Objective function (maximize 5x0 + 7x1)
f = [5, 7]
model.obj = Objective(expr=sum(f[i] * model.x[i] for i in [0, 1]), sense=maximize)

# Constraints
model.c1 = Constraint(expr=3*model.x[0] + 2*model.x[1] <= 144)
model.c2 = Constraint(expr=model.x[0] >= 4*model.x[1])

# Print model before solving
print("Model formulation:")
model.pprint()

# Solve with GLPK
solver = SolverFactory('glpk')
results = solver.solve(model, tee=False)

# Check results
if (results.solver.status == SolverStatus.ok) and \
   (results.solver.termination_condition == TerminationCondition.optimal):
    print("\nOptimal solution found:")
    model.display()
else:
    print("\nSolver did not find an optimal solution. Status:", results.solver.status)