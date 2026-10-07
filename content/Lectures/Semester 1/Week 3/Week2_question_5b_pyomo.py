from pyomo.environ import *

# Define the attractiveness values as a list
a = [6, 1, 5, 5, 6, 4, 10, 10, 6, 7]

# Define the vitamin and fat values as lists
vita = [18, 8, 22, 6, 0, 0, 8, 4, 0, 12]
vitb = [4, 6, 10, 12, 14, 0, 0, 0, 6, 20]
vitc = [0, 22, 0, 0, 0, 20, 0, 8, 10, 0]
vitd = [6, 14, 0, 6, 10, 8, 6, 0, 12, 4]
fat = [0, 0, 8, 0, 0, 6, 20, 40, 0, 0]

no_vars = len(a)

# Create a concrete model
model = ConcreteModel()

# Define the decision variables
model.x = Var(range(no_vars), domain=NonNegativeReals)

# Define the objective function
model.obj = Objective(expr=sum(a[i] * model.x[i] for i in range(no_vars)), sense=maximize)

# Define constraints
model.vita_min = Constraint(expr=sum(vita[i] * model.x[i] for i in range(no_vars)) >= 100)
model.vitb_min = Constraint(expr=sum(vitb[i] * model.x[i] for i in range(no_vars)) >= 120)
model.vitc_min = Constraint(expr=sum(vitc[i] * model.x[i] for i in range(no_vars)) >= 200)
model.vitd_min = Constraint(expr=sum(vitd[i] * model.x[i] for i in range(no_vars)) >= 80)
model.fat_max = Constraint(expr=sum(fat[i] * model.x[i] for i in range(no_vars)) <= 300)

# Solve the optimization problem
solver = SolverFactory('glpk')
results = solver.solve(model, tee=True)  # Set tee=True to display solver output

# # Check the solver status and print the results
# if results.solver.status == SolverStatus.ok:
#     if results.solver.termination_condition == TerminationCondition.optimal:
#         print("Optimal solution found.")
#         print("Objective value:", model.obj())
#         print("Decision variables:")
#         for i in range(no_vars):
#             print(f"x[{i}] = {model.x[i].value}")
#     else:
#         print("Solver terminated.")
# else:
#     print("Solver did not find a solution. Status:", results.solver.status)

