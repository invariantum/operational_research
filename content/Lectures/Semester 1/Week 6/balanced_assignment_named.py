from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()
#2 range arguments to give coordinates range(0)is collumn range (1) is row
workers = range(4)
jobs = range(4)
model.x = Var(workers, jobs, within=Binary)

time = [
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
]

# Create the optimization problem
#minimise the number cosen in regards to the weight
model.obj = Objective(expr=sum(sum(time[worker][job] * model.x[worker, job] for job in jobs) for worker in workers), sense=minimize)

# Define the equality constraints for workers and jobs
model.worker_constraints = ConstraintList()
model.job_constraints = ConstraintList()

#creates binary variables procedurally
for worker in workers:      # for each worker
    model.worker_constraints.add(sum(model.x[worker, job] for job in jobs) == 1)     # only assign a single job to a worker
    
for job in jobs:	    # for each job
    model.job_constraints.add(sum(model.x[worker, job] for worker in workers) == 1)  # only assign a single worker to a job


# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()

