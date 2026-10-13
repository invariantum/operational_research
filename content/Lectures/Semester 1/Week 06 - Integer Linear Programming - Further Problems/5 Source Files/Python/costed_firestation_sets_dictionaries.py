from pyomo.environ import *

# Define the binary variables
model = ConcreteModel()

firestations = ['A','B','C','D']
cities = [1,2,3,4,5]

# variable to represent if fire station is selected
model.x = Var(firestations, within=Binary)

cost = {'A': 12, 'B': 7, 'C': 10, 'D': 5}
covers = {
    'A': [1,3],
    'B': [2,3,4],
    'C': [2,5],
    'D': [5]
    }

# Create the optimization problem
model.obj = Objective(expr=sum(cost[station] * model.x[station] for station in firestations), sense=minimize)

def cover_constraint(model, city):
    return sum(model.x[s] for s in firestations if city in covers[s]) >= 1

model.cover_constaint = Constraint(cities, rule=cover_constraint)

# Create a solver
solver = SolverFactory('glpk')

# Display the model
model.pprint()

# Solve the model
solver.solve(model, tee=False)  # Set tee=True to display solver output

# Display the results
model.display()


