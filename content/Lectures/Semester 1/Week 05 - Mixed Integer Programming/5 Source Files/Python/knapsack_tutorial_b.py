from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define binary variables
model.x = Var(range(8), within=NonNegativeIntegers)

# Define the objective function values
value = [10, 50, 40, 100, 100, 130, 70, 80]
weight = [2, 3, 2, 6, 6, 8, 3, 5]
W = 15

# Define the objective function
model.obj = Objective(expr=sum(value[i] * model.x[i] for i in range(8)), sense=maximize)

# Define the capacity constraint
model.capacity = Constraint(expr=sum(weight[i] * model.x[i] for i in range(8)) <= W)

# Create a solver
solver = SolverFactory('glpk')
# Display the model
model.pprint()
# Solve the model
solver.solve(model)
# Display the results
model.display()
