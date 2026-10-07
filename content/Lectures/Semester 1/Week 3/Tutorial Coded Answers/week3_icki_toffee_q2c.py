from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the integer decision variables with lower and upper bounds
model.x = Var(range(12), domain=NonNegativeIntegers, bounds=(0, float('inf')))

# Define the objective function coefficients as a list
pop = [10, 10, 8, 9, 5, 6, 7, 8, 10, 3, 8, 4]

# Define the objective function
model.obj = Objective(expr=sum(pop[i] * model.x[i] for i in range(12)), sense=maximize)

# Define the constraints
fat = [20, 16, 10, 7, 6, 5, 13, 15, 18, 0, 19, 0]
cals = [100, 100, 80, 50, 60, 40, 80, 90, 80, 145, 120, 120]
weight = [24, 22, 15, 12, 10, 10, 14, 17, 20, 8, 20, 15]

# Define the constraints
model.weight_min = Constraint(expr=sum(weight[i] * model.x[i] for i in range(12)) >= 320)
model.cals_max = Constraint(expr=sum(cals[i] * model.x[i] for i in range(12)) <= 2850)
model.fat_weight_min = Constraint(expr=sum(fat[i] * model.x[i] for i in range(12)) <= 0.45 * sum(weight[i] * model.x[i] for i in range(12)))

# Solve the integer optimization problem
solver = SolverFactory('glpk')
results = solver.solve(model, tee=True)  # Set tee=True to display solver output

# Check the solver status and print the results
if results.solver.status == SolverStatus.ok:
    if results.solver.termination_condition == TerminationCondition.optimal:
        print("Optimal solution found.")
        print("Objective value:", model.obj())
        print("Decision variables:")
        for i in range(12):
            print(f"x[{i}] =", model.x[i].value)
    else:
        print("Solver terminated with a non-optimal solution.")
else:
    print("Solver did not find a solution. Status:", results.solver.status)
