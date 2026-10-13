from pyomo.environ import *

# Define cost and profit as lists
cost = [10, 12, 9, 5, 13]
profit = [5, 3, 4, 3, 3]

# Create a concrete model
model = ConcreteModel()

# Define the decision variables and binary variables
model.x = Var(range(5), within=NonNegativeReals)
model.b = Var(range(5), within=Binary)

# Define the objective function
model.obj = Objective(expr=sum(profit[i] * model.x[i] for i in range(5)), sense=maximize)

# Define the constraints
model.cost_max = Constraint(expr=sum(cost[i] * model.x[i] for i in range(5)) <= 160)
model.select = ConstraintList()
model.lower_order = ConstraintList()

for i in range(5):
    model.select.add(model.x[i] <= 10 * model.b[i])
    model.lower_order.add(model.x[i] >= 6 * model.b[i])

# Create a solver
solver = SolverFactory('glpk')
# Display the model
model.pprint()
# Solve the model
solver.solve(model, tee=True)
# Display the results
model.display()

