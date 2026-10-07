from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()

workers = [1,2,3,4]
jobs = [1,2,3,4]

model.x = Var(workers, jobs, within=Binary)

job_time = {
    (1,1): 9, (1,2):2, (1,3): 9, (1,4):2, 
    (2,1): 6, (2,2):4, (2,3): 3, (2,4):7, 
    (3,1): 5, (3,2):8, (3,3): 1, (3,4):8, 
    (4,1): 7, (4,2):6, (4,3): 9, (4,4):4
    }

# Create the optimization problem
model.obj = Objective(expr=sum(sum(job_time[w, j] * model.x[w, j] for w in workers) for j in jobs), sense=minimize)

def worker_constraint(model, w):
    return sum(model.x[w, j] for j in jobs) == 1

def job_constraint(model, j):
    return sum(model.x[w, j] for w in workers) == 1

model.worker_constraint = Constraint(workers, rule=worker_constraint)
model.job_constraint = Constraint(jobs, rule=job_constraint)


# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()