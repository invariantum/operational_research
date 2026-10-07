from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define integer variables
model.x = Var(range(4), domain=NonNegativeReals)
# define a vector
cost = [10, 6, 8, 16]
# define a linear inequality constraint
model.constraint1 = Constraint(expr=sum(cost[i] * model.x[i] for i in model.x) >= 120)
# pretty print the constraint
model.constraint1.pprint()


print(10*model.x[0] + 6*model.x[1] + 8*model.x[2] + 16*model.x[3])

print()


print(sum(cost[i] * model.x[i] for i in model.x))


volume = [100, 60, 85, 160]
weight = [1.05, 2.6, 3.8, 1.6]

print(sum(cost[i] * model.x[i] for i in model.x))
print()
era
# Objective function
model.obj = Objective(expr=sum(cost[i] * model.x[i] for i in model.x), sense=maximize)
model.obj.pprint()

print()

# Define a constraint
model.constraint1 = Constraint(expr=sum(cost[i] * model.x[i] for i in model.x) >= 32)
model.constraint1.pprint()

print()

# # Define the inequality constraints
model.constraint2 = Constraint(expr=sum(weight[i] * model.x[i] for i in model.x) <= 100)
model.constraint2.pprint()

# set the constraint to off
model.constraint2.deactivate()
model.constraint2.pprint()