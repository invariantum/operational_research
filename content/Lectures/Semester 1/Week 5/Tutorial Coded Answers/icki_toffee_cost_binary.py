from pyomo.environ import *

# Define integer variables
model = ConcreteModel()
model.x = Var(range(12), within=NonNegativeIntegers)
model.xb = Var(range(12), within=Binary)

# Define the objective function values
cost = [12, 12, 12, 15, 13, 13, 16, 16, 15, 10, 18, 20]

fat = [20, 16, 10, 7, 6, 5, 13, 15, 18, 0, 19, 0]
cals = [100, 100, 80, 50, 60, 40, 80, 90, 80, 145, 120, 120]
weight = [24, 22, 15, 12, 10, 10, 14, 17, 20, 8, 20, 15]

# Define the objective function
model.obj = Objective(expr=sum(cost[i] * model.x[i] for i in range(12)), sense=minimize)

# Define the inequality constraints
model.weight_min = Constraint(expr=sum(weight[i] * model.x[i] for i in range(12)) >= 320)
model.weight_max = Constraint(expr=sum(weight[i] * model.x[i] for i in range(12)) <= 1.5 * 320)
model.cals_max = Constraint(expr=sum(cals[i] * model.x[i] for i in range(12)) <= 2850)
model.fat_weight_min = Constraint(expr=sum(fat[i] * model.x[i] for i in range(12)) <= 0.45 * sum(weight[i] * model.x[i] for i in range(12)))

# Ensure that your selection has at least 6 different candies
model.variety = Constraint(expr=sum(model.xb[i] for i in range(12)) >= 6)

# Ensure your selection includes at least 3 of each of the selected candies.
model.selection_min = ConstraintList()
for i in range(12):
    model.selection_min.add(model.x[i] >= 3 * model.xb[i])

# Ensure your selection includes at most 6 of each of the selected candies.
model.selection_max = ConstraintList()
for i in range(12):
    model.selection_max.add(model.x[i] <= 6 * model.xb[i])

# Create a solver
solver = SolverFactory('glpk')
# Display the model
model.pprint()
# Solve the model
solver.solve(model)
# Display the results
model.display()
