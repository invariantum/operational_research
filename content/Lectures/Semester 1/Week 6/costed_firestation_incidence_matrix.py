from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()
model.x = Var(range(4), within=Binary)

# Define the incidence matrix for the constraints
A = [
    [1, 0, 0, 0],
    [0, 1, 1, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 1]
]

no_cities = len(A)
no_stations = len(A[0])

c = [12, 7, 10, 5]

# Create the optimization problem
model.obj = Objective(expr=sum(c[station] * model.x[station] for station in range(no_stations)), sense=minimize)



# Create a list of constraints based on the incidence matrix
model.constraints = ConstraintList()
for city in range(no_cities):
    constraint_expr = sum(A[city][station] * model.x[station] for station in range(no_stations)) >= 1
    model.constraints.add(constraint_expr)

# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the modelm
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()


