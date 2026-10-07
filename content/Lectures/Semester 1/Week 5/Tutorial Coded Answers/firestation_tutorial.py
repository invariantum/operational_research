from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the binary variables
model.x = Var(range(7), within=Binary)

# Define the objective function
model.obj = Objective(expr=sum(model.x[i] for i in range(7)), sense=minimize)

# Define the inequality constraints
model.city1 = Constraint(expr=model.x[0] + model.x[1] + model.x[2] >= 1)
model.city2 = Constraint(expr=model.x[0] + model.x[1] + model.x[3] >= 1)
model.city3 = Constraint(expr=model.x[0] + model.x[2] >= 1)
model.city4 = Constraint(expr=model.x[1] + model.x[3] + model.x[4] >= 1)
model.city5 = Constraint(expr=model.x[3] + model.x[4] + model.x[5] >= 1)
model.city6 = Constraint(expr=model.x[4] + model.x[5] + model.x[6] >= 1)
model.city7 = Constraint(expr=model.x[5] + model.x[6] >= 1)

# Create a solver
solver = SolverFactory('glpk')
# Display the model
model.pprint()
# Solve the model
solver.solve(model)
# Display the results
model.display()
