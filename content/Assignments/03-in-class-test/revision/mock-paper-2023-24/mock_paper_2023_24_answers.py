"""Pyomo answers to the mock paper 2023/24 (Questions 3 and 5).

Plain-script version of `mock_paper_2023_24_answers.ipynb`; run it with `python mock_paper_2023_24_answers.py`.
The `# %%` lines mark the notebook cells (VS Code can run them one by one).
"""

# %% [markdown]
# ## Question 5b: solve the integer programme

# %%
from pyomo.environ import *

model = ConcreteModel()

model.x = Var(range(2), domain=NonNegativeIntegers) # x[0], x[1]

model.obj = Objective(expr=36*model.x[0]+34*model.x[1], sense=maximize)

model.constraint1 = Constraint(expr=4*model.x[0] + 3*model.x[1] <= 40)
model.constraint2 = Constraint(expr=0.2*model.x[0] + 0.3*model.x[1] <= 3)

print("Displaying model #################\n")
model.pprint()

# solve the optimisation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model, tee=False) # set tee=True to display solver output

print()

print("Displaying solution #################\n")
model.display()

# %% [markdown]
# ## Question 5d: add the 3 : 1 product ratio

# %%
from pyomo.environ import *

model = ConcreteModel()

model.x = Var(range(2), domain=NonNegativeIntegers) # x[0], x[1]

model.obj = Objective(expr=36*model.x[0]+34*model.x[1], sense=maximize)

model.constraint1 = Constraint(expr=4*model.x[0] + 3*model.x[1] <= 40)
model.constraint2 = Constraint(expr=0.2*model.x[0] + 0.3*model.x[1] <= 3)
model.constraint3 = Constraint(expr=model.x[1] == 3*model.x[0] )

print("Displaying model #################\n")
model.pprint()

# solve the optimisation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model, tee=False) # set tee=True to display solver output

print()

print("Displaying solution #################\n")
model.display()

# %% [markdown]
# ## Question 3a: FBK's optimal distribution plan

# %%
# Import Pyomo and the required components
from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define the sets for suppliers (i) and consumers (j)
model.Suppliers = ['A', 'B', 'C']
model.Consumers = ['X', 'Y', 'Z']

# Define the parameters as lists of lists (matrices)
supply = {'A': 100, 'B': 100, 'C': 100}  # Supply available at each supplier
demand = {'X': 70, 'Y': 80, 'Z': 150}  # Demand requirements at each consumer

# Cost to transport one unit from supplier i to consumer j
transport_cost = {
    ('A','X'): 8, ('A','Y'): 7, ('A','Z'): 5,
    ('B','X'): 12, ('B','Y'): 3, ('B','Z'): 9,
    ('C','X'): 10, ('C','Y'): 11, ('C','Z'): 7
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
# **Same cost, different plan.** The answer sheet was produced with the GLPK solver and shows A→X 70, A→Z 30, B→Y 80, B→Z 20, C→Z 100. HiGHS (used here, because it also runs in the browser) can return a different plan with the **same minimum cost of 1830**: this problem has more than one optimal solution. The next cell checks that the answer-sheet plan is feasible and costs the same.

# %%
answer_sheet_plan = {('A', 'X'): 70, ('A', 'Z'): 30, ('B', 'Y'): 80, ('B', 'Z'): 20, ('C', 'Z'): 100}
plan = {(i, j): answer_sheet_plan.get((i, j), 0) for i in model.Suppliers for j in model.Consumers}

plan_cost = sum(transport_cost[i, j] * amount for (i, j), amount in plan.items())
meets_supply = all(sum(plan[i, j] for j in model.Consumers) <= supply[i] for i in model.Suppliers)
meets_demand = all(sum(plan[i, j] for i in model.Suppliers) == demand[j] for j in model.Consumers)

print("Answer-sheet plan cost:", plan_cost)
print("Answer-sheet plan meets every supply and demand limit:", meets_supply and meets_demand)
print("Minimum cost found above:", model.objective())
print("Both plans are optimal:", meets_supply and meets_demand and abs(plan_cost - model.objective()) < 1e-6)

# %% [markdown]
# ## Question 3b: revised plan

# %%
# Import Pyomo and the required components
from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define the sets for suppliers (i) and consumers (j)
model.Suppliers = ['A', 'B', 'C']
model.Consumers = ['X', 'Y', 'Z']

# Define the parameters as lists of lists (matrices)
supply = {'A': 100, 'B': 100, 'C': 100}  # Supply available at each supplier
demand = {'X': 70, 'Y': 80, 'Z': 150}  # Demand requirements at each consumer

# Cost to transport one unit from supplier i to consumer j
transport_cost = {
    ('A','X'): 8, ('A','Y'): 7, ('A','Z'): 5,
    ('B','X'): 12, ('B','Y'): 3, ('B','Z'): 9,
    ('C','X'): 10, ('C','Y'): 11, ('C','Z'): 7
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

def ay_constraint_rule(model):
    return model.x['A', 'Z'] >= 5

model.bx_constraint = Constraint(rule=ay_constraint_rule)

def by_constraint_rule(model):
    return model.x['B', 'Y'] == 0

model.by_constraint = Constraint(rule=by_constraint_rule)

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
# ## Question 3c: transhipment through two new locations

# %%
# Import Pyomo and the required components
from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define the sets for suppliers (i) and consumers (j)
model.Suppliers = ['A', 'B', 'C']
model.Consumers = ['X', 'Y', 'Z']
model.Tranship = ['D1', 'D2']
model.Edges = [(i,j) for i in model.Suppliers for j in model.Tranship] + \
              [(j,i) for i in model.Consumers for j in model.Tranship]

# Define the parameters as lists of lists (matrices)
supply = {'A': 100, 'B': 100, 'C': 100}  # Supply available at each supplier
demand = {'X': 70, 'Y': 80, 'Z': 150}  # Demand requirements at each consumer

# Cost to transport one unit from supplier i to consumer j
transport_cost = {
    ('A','D1'): 4, ('B','D1'): 3, ('C','D1'): 6,
    ('A','D2'): 5, ('B','D2'): 2, ('C','D2'): 4,
    ('D1','X'): 4, ('D1','Y'): 5, ('D1','Z'): 2,
    ('D2','X'): 2, ('D2','Y'): 4, ('D2','Z'): 4
    }

# Create the variables using the list of tuples as indices
model.x = Var(model.Edges, within=NonNegativeReals)

# Define the objective function (minimize transportation costs)
def objective_rule(model):
    return sum(transport_cost[i, j] * model.x[i, j] for (i,j) in model.Edges)

# Define supply and demand constraints
def supply_constraint_rule(model, i):
    return sum(model.x[i, j] for j in model.Tranship)  <= supply[i]

def demand_constraint_rule(model, j):
    return sum(model.x[i, j] for i in model.Tranship)   == demand[j]

def tranship_constraint_rule(model, v):
    return sum(model.x[i,j] for (i,j) in model.Edges if j==v) - sum(model.x[i,j] for (i,j) in model.Edges if i==v) == 0


model.objective = Objective(rule=objective_rule, sense=minimize)
model.supply_constraint = Constraint(model.Suppliers, rule=supply_constraint_rule)
model.demand_constraint = Constraint(model.Consumers, rule=demand_constraint_rule)
model.tranship_constraint = Constraint(model.Tranship, rule=tranship_constraint_rule)

# Solve the transportation problem
solver = SolverFactory('appsi_highs')
results = solver.solve(model)

model.pprint()
model.display()
