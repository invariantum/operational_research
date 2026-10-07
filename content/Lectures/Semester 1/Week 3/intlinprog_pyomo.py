from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the integer decision variables with lower and upper bounds
model.x = Var([0, 1], domain=NonNegativeIntegers)

# Define the objective function coefficients as a list
f = [2, 3.5]

# Define the objective function
model.obj = Objective(expr=sum(f[i] * model.x[i] for i in [0, 1]), sense=maximize)

# Define the inequality constraints
c1 = 3 * model.x[0] + 2 * model.x[1] <= 14
c2 = 2 * model.x[0] + 3 * model.x[1] <= 12.5
c3 = -model.x[0] + model.x[1] <= 1

# Add the constraints to the model
model.c1 = Constraint(expr=c1)
model.c2 = Constraint(expr=c2)
model.c3 = Constraint(expr=c3)

# Solve the integer optimization problem
solver = SolverFactory('glpk')
results = solver.solve(model, tee=False)  # Set tee=True to display solver output


# Check the solver status and print the results
if results.solver.status == SolverStatus.ok:
    if results.solver.termination_condition == TerminationCondition.optimal:
        print("Optimal solution found.")
        print("Objective value:", model.obj())
        print("Decision variables:")
        for i in [0, 1]:
            print(f"x[{i}] = {model.x[i].value}")
    else:
        print("Solver terminated with a non-optimal solution.")
else:
    print("Solver did not find a solution. Status:", results.solver.status)
    
    
