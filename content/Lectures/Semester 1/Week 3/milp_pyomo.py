from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Decision variables
model.x1 = Var(domain=NonNegativeIntegers, bounds=(0, float('inf')))
model.x2 = Var(domain=NonNegativeReals, bounds=(0, float('inf')))

# Objective function (maximize 2x1 + 3.5x2)
f = [2, 3.5]
model.obj = Objective(expr=f[0]*model.x1 + f[1]*model.x2, sense=maximize)

# Constraints
model.c1 = Constraint(expr=3*model.x1 + 2*model.x2 <= 14)
model.c2 = Constraint(expr=2*model.x1 + 3*model.x2 <= 12.5)
model.c3 = Constraint(expr=-model.x1 + model.x2 <= 1)

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
