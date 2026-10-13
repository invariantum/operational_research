from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()
A = [
    [0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

no_vars = len(A[0])	# variables are the number of columns in a row

model.x = Var(range(no_vars), within=Binary)

# Create the optimization problem
model.obj = Objective(expr=sum(model.x[i] for i in range(no_vars)), sense=minimize)

# Define the inequality constraints
model.vertex = ConstraintList()
for i in range(no_vars):
    for j in range(no_vars):
        if A[i][j]:
            model.vertex.add(model.x[i] + model.x[j] >= 1)


# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()

