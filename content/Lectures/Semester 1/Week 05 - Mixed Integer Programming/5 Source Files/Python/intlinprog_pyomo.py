from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define the integer decision variables with lower and upper bounds
model.x = Var([0, 1], domain=NonNegativeIntegers)

# Define the objective function coefficients as a list
f = [2, 3.5]

# Define the objective function
model.obj = Objective(expr=sum(f[i] * model.x[i] for i in [0, 1]), sense=maximize)

# Add the constraints to the model
model.c1 = Constraint(expr=3 * model.x[0] + 2 * model.x[1] <= 14)
model.c2 = Constraint(expr=2 * model.x[0] + 3 * model.x[1] <= 12.5)
model.c3 = Constraint(expr=-model.x[0] + model.x[1] <= 1)

# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()
