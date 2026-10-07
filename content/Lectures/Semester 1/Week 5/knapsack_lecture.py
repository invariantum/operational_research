from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the binary variables
model.x = Var(range(7), within=Binary)

# Define objective function values and weights
value = [10, 10, 10, 100, 100, 130, 70]
weight = [2, 2, 2, 6, 6, 8, 3]
W = 10

# Define the objective function
model.obj = Objective(expr=sum(value[i] * model.x[i] for i in range(7)), sense=maximize)

# Define the capacity constraint
model.capacity = Constraint(expr=sum(weight[i] * model.x[i] for i in range(7)) <= W)

# Create a solver
solver = SolverFactory('glpk')
# Display the model
model.pprint()
# Solve the model
solver.solve(model)
# Display the results
model.display()

