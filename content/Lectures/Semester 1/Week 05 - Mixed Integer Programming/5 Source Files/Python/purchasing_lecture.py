from pyomo.environ import *

# Define cost and profit as lists
cost = [10, 12, 9, 5, 13]
profit = [5, 3, 4, 3, 3]

# Create a concrete model
model = ConcreteModel()

# Define the decision variables with upper bounds
model.x = Var(range(5), within=NonNegativeReals, bounds=(0, 10))

# Define the objective function
model.obj = Objective(expr=sum(profit[i] * model.x[i] for i in range(5)), sense=maximize)

# Define the inequality constraint
model.cost_max = Constraint(expr=sum(cost[i] * model.x[i] for i in range(5)) <= 160)

# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()

