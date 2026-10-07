from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()

model.x = Var(range(4), within=Binary)

c = [12, 7, 10, 5]

# Create the optimization problem
model.obj = Objective(expr=sum(c[i] * model.x[i] for i in model.x), sense=minimize)

# Define the inequality constraints
model.city0 = Constraint(expr=model.x[0] >= 1)
model.city1 = Constraint(expr=model.x[1] + model.x[2] >= 1)
model.city2 = Constraint(expr=model.x[0] + model.x[1] >= 1)
model.city3 = Constraint(expr=model.x[1] >= 1)
model.city4 = Constraint(expr=model.x[2] + model.x[3] >= 1)

# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()


