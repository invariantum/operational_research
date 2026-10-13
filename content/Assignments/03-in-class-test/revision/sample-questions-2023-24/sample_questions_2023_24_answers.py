"""Pyomo answers to the sample questions 2023/24 (Questions 1 and 3).

Plain-script version of `sample_questions_2023_24_answers.ipynb`; run it with `python sample_questions_2023_24_answers.py`.
The `# %%` lines mark the notebook cells (VS Code can run them one by one).
"""

# %% [markdown]
# ## Question 1a

# %%
from pyomo.environ import *

model = ConcreteModel()

model.x = Var(range(2), domain=NonNegativeReals)

model.obj = Objective(expr=5*model.x[0]+7*model.x[1], sense=maximize)

model.constraint1 = Constraint(expr=model.x[0] + 3*model.x[1] <= 60)
model.constraint2 = Constraint(expr=4*model.x[0] + model.x[1] <= 75)
model.constraint3 = Constraint(expr=model.x[0] +model.x[1] <= 27)

print("Displaying model #################\n")
model.pprint()

# solve the optimisation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model, tee=False) # set tee=True to display solver output

print()

print("Displaying solution #################\n")
model.display()

# %% [markdown]
# ## Question 1b

# %%
from pyomo.environ import *

model = ConcreteModel()

model.x = Var(range(2), domain=NonNegativeReals)

model.obj = Objective(expr=5*model.x[0]+7*model.x[1], sense=maximize)

model.constraint1 = Constraint(expr=model.x[0] + 3*model.x[1] <= 60)
model.constraint2 = Constraint(expr=4*model.x[0] + model.x[1] <= 75)
model.constraint3 = Constraint(expr=model.x[0] +model.x[1] <= 27)
model.constraint4 = Constraint(expr=model.x[0] >= (3/2)*model.x[1])

print("Displaying model #################\n")
model.pprint()

# solve the optimisation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model, tee=False) # set tee=True to display solver output

print()

print("Displaying solution #################\n")
model.display()

# %% [markdown]
# ## Question 1c

# %%
from pyomo.environ import *

model = ConcreteModel()

model.x = Var(range(2), domain=NonNegativeReals)

model.obj = Objective(expr=5*model.x[0]+7*model.x[1], sense=maximize)

model.constraint1 = Constraint(expr=model.x[0] + 3*model.x[1] <= 60)
model.constraint2 = Constraint(expr=4*model.x[0] + model.x[1] <= 75)
model.constraint3 = Constraint(expr=model.x[0] +model.x[1] <= 27)
model.constraint4 = Constraint(expr=model.x[0] >= (3/2)*model.x[1])
model.constraint5 = Constraint(expr=10*model.x[0]+12*model.x[1]<=250)

print("Displaying model #################\n")
model.pprint()

# solve the optimisation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model, tee=False) # set tee=True to display solver output

print()

print("Displaying solution #################\n")
model.display()

# %% [markdown]
# ## Question 3b

# %%
# Import Pyomo and the required components
from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define the sets for suppliers (i) and consumers (j)
model.Suppliers = ['A', 'B', 'C']
model.Consumers = ['X', 'Y', 'Z']

# Define the parameters as lists of lists (matrices)
supply = {'A': 100, 'B': 200, 'C': 100}  # Supply available at each supplier
demand = {'X': 70, 'Y': 80, 'Z': 110}  # Demand requirements at each consumer

# Cost to transport one unit from supplier i to consumer j
transport_cost = {
    ('A','X'): 5, ('A','Y'): 8, ('A','Z'): 6,
    ('B','X'): 3, ('B','Y'): 14, ('B','Z'): 5,
    ('C','X'): 2, ('C','Y'): 15, ('C','Z'): 3
}

# Define decision variables as a matrix
model.x = Var(model.Suppliers, model.Consumers, within=NonNegativeReals)

# Define the objective function (minimize transportation costs)
def objective_rule(model):
    return sum(transport_cost[i, j] * model.x[i, j] for i in model.Suppliers for j in model.Consumers)

model.objective = Objective(rule=objective_rule, sense=minimize)

# Define supply and demand constraints
def supply_constraint_rule(model, i):
    return sum(model.x[i, j] for j in model.Consumers) <= supply[i]

model.supply_constraint = Constraint(model.Suppliers, rule=supply_constraint_rule)

def demand_constraint_rule(model, j):
    return sum(model.x[i, j] for i in model.Suppliers) == demand[j]

model.demand_constraint = Constraint(model.Consumers, rule=demand_constraint_rule)

# Solve the transportation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model)

model.display()

# Display the results
if results.solver.termination_condition == TerminationCondition.optimal:
    print("Optimal solution found:")
    print("Objective Value =", model.objective())
    for i in model.Suppliers:
        for j in model.Consumers:
            print(f"Amount transported from Supplier{i} to Consumer{j}: {model.x[i, j].value + 0.0}")
else:
    print("No optimal solution found")

# %% [markdown]
# ## Question 3c

# %%
# Import Pyomo and the required components
from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define the sets for suppliers (i) and consumers (j)
model.Suppliers = ['A', 'B', 'C']
model.Consumers = ['X', 'Y', 'Z']

# Define the parameters as lists of lists (matrices)
supply = {'A': 100, 'B': 200, 'C': 100}  # Supply available at each supplier
demand = {'X': 70, 'Y': 80, 'Z': 110}  # Demand requirements at each consumer

# Cost to transport one unit from supplier i to consumer j
transport_cost = {
    ('A','X'): 5, ('A','Y'): 8, ('A','Z'): 6,
    ('B','X'): 3, ('B','Y'): 14, ('B','Z'): 5,
    ('C','X'): 2, ('C','Y'): 15, ('C','Z'): 3
}

# Define decision variables as a matrix
model.x = Var(model.Suppliers, model.Consumers, within=NonNegativeReals)

# Define the objective function (minimize transportation costs)
def objective_rule(model):
    return sum(transport_cost[i, j] * model.x[i, j] for i in model.Suppliers for j in model.Consumers)

model.objective = Objective(rule=objective_rule, sense=minimize)

# Define supply and demand constraints
def supply_constraint_rule(model, i):
    return sum(model.x[i, j] for j in model.Consumers) <= supply[i]

model.supply_constraint = Constraint(model.Suppliers, rule=supply_constraint_rule)

def demand_constraint_rule(model, j):
    return sum(model.x[i, j] for i in model.Suppliers) == demand[j]

model.demand_constraint = Constraint(model.Consumers, rule=demand_constraint_rule)

def bx_constraint_rule(model):
    return model.x['B', 'X'] <= 60

model.bx_constraint_rule = Constraint(rule=bx_constraint_rule)

def bz_constraint_rule(model):
    return model.x['B', 'Z'] == 0

model.bz_constraint_rule = Constraint(rule=bz_constraint_rule)

# Solve the transportation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model)

model.display()

# Display the results
if results.solver.termination_condition == TerminationCondition.optimal:
    print("Optimal solution found:")
    print("Objective Value =", model.objective())
    for i in model.Suppliers:
        for j in model.Consumers:
            print(f"Amount transported from Supplier{i} to Consumer{j}: {model.x[i, j].value + 0.0}")
else:
    print("No optimal solution found")

# %% [markdown]
# ## Question 3d

# %%
# Import Pyomo and the required components
from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define the sets for suppliers (i) and consumers (j)
model.Suppliers = ['A', 'B', 'C']
model.Consumers = ['X', 'Y', 'Z']
model.Tranship = ['D']
model.Edges = [(i,j) for i in model.Suppliers for j in model.Tranship] + \
    [(i,j) for i in model.Tranship for j in model.Consumers] + \
    [(i,j) for i in model.Suppliers for j in model.Consumers]

# Define the parameters as lists of lists (matrices)
supply = {'A': 100, 'B': 200, 'C': 100}  # Supply available at each supplier
demand = {'X': 70, 'Y': 80, 'Z': 110}  # Demand requirements at each consumer

# Cost to transport one unit from supplier i to consumer j
transport_cost = {
    ('A','X'): 5, ('A','Y'): 8, ('A','Z'): 6,
    ('B','X'): 3, ('B','Y'): 14, ('B','Z'): 5,
    ('C','X'): 2, ('C','Y'): 15, ('C','Z'): 3,
    ('A','D'): 4, ('B','D'): 2, ('C','D'): 3,
    ('D','X'): 3, ('D','Y'): 4, ('D','Z'): 3
    }

# Create the variables using the list of tuples as indices
model.x = Var(model.Edges, within=NonNegativeReals)

# Define the objective function (minimize transportation costs)
def objective_rule(model):
    return sum(transport_cost[i, j] * model.x[i, j] for (i,j) in model.Edges)

# Define supply and demand constraints
def supply_constraint_rule(model, i):
    return sum(model.x[i, j] for j in model.Tranship) + sum(model.x[i, j] for j in model.Consumers) <= supply[i]

def demand_constraint_rule(model, j):
    return sum(model.x[i, j] for i in model.Tranship) + sum(model.x[i, j] for i in model.Suppliers)  == demand[j]

def tranship_constraint_rule(model, v):
    return sum(model.x[i,j] for (i,j) in model.Edges if j==v) - sum(model.x[i,j] for (i,j) in model.Edges if i==v) == 0

def bx_constraint_rule(model):
    return model.x['B', 'X'] <= 60

model.bx_constraint_rule = Constraint(rule=bx_constraint_rule)

def bz_constraint_rule(model):
    return model.x['B', 'Z'] == 0

model.objective = Objective(rule=objective_rule, sense=minimize)
model.supply_constraint = Constraint(model.Suppliers, rule=supply_constraint_rule)
model.demand_constraint = Constraint(model.Consumers, rule=demand_constraint_rule)
model.tranship_constraint = Constraint(model.Tranship, rule=tranship_constraint_rule)

# Solve the transportation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model)

model.pprint()
model.display()
