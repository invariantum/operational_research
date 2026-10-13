from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the decision variables with lower and upper bounds and types
model.x1 = Var(domain=NonNegativeReals, bounds=(0, float('inf')))
model.x2 = Var(domain=NonNegativeIntegers, bounds=(0, float('inf')))

# Define the objective function coefficients as a list
f = [5, 17]

# Define the objective function
model.obj = Objective(expr=f[0] * model.x1 + f[1] * model.x2, sense=maximize)

# Define the inequality constraints
c1 = 2 * model.x1 + 3 * model.x2 <= 60
c2 = model.x1 + 2 * model.x2 <= 25

# Add the constraints to the model
model.c1 = Constraint(expr=c1)
model.c2 = Constraint(expr=c2)

# Solve the mixed-integer optimization problem
solver = SolverFactory('glpk')
results = solver.solve(model, tee=True)  # Set tee=True to display solver output

# Check the solver status and print the results
if results.solver.status == SolverStatus.ok:
    if results.solver.termination_condition == TerminationCondition.optimal:
        print("Optimal solution found.")
        print("Objective value:", model.obj())
        print("Decision variables:")
        print("x1 =", model.x1.value)
        print("x2 =", model.x2.value)
    else:
        print("Solver terminated with a non-optimal solution.")
else:
    print("Solver did not find a solution. Status:", results.solver.status)
