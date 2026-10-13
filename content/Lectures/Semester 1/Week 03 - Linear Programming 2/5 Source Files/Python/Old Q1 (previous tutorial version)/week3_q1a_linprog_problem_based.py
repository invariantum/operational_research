from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the decision variables with lower and upper bounds
model.x = Var(range(2), domain=NonNegativeReals, bounds=(0, float('inf')))

# Define the objective function coefficients as a list
f = [5, 17]

# Define the objective function
model.obj = Objective(expr=sum(f[i] * model.x[i] for i in range(2)), sense=maximize)

# Define the inequality constraints
c1 = 2 * model.x[0] + 3 * model.x[1] <= 60
c2 = model.x[0] + 2 * model.x[1] <= 25

# Add the constraints to the model
model.c1 = Constraint(expr=c1)
model.c2 = Constraint(expr=c2)

# Solve the optimization problem
solver = SolverFactory('glpk')
results = solver.solve(model, tee=True)  # Set tee=True to display solver output

# Check the solver status and print the results
if results.solver.status == SolverStatus.ok:
    if results.solver.termination_condition == TerminationCondition.optimal:
        print("Optimal solution found.")
        print("Objective value:", model.obj())
        print("Decision variables:")
        for i in range(2):
            print(f"x[{i}] =", model.x[i].value)
    else:
        print("Solver terminated with a non-optimal solution.")
else:
    print("Solver did not find a solution. Status:", results.solver.status)
