from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()
model.x = Var(range(4), range(4), within=Binary)

w = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
]

# Create the optimization problem
model.obj = Objective(expr=sum(sum(w[i][j] * model.x[i, j] for j in range(4)) for i in range(4)), sense=minimize)

# Define the equality constraints for workers and jobs
model.worker_constraints = ConstraintList()
model.job_constraints = ConstraintList()

for i in range(4):
    model.worker_constraints.add(sum(model.x[i, j] for j in range(4)) == 1)
    
for j in range(4):
    model.job_constraints.add(sum(model.x[i, j] for i in range(4)) == 1)


# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()