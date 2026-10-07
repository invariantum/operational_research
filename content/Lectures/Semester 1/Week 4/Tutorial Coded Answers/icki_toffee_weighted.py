from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define integer variables
model.x = Var(range(12), domain=NonNegativeIntegers)

# Define objective function coefficients
cost = [12, 12, 12, 15, 13, 13, 16, 16, 15, 10, 18, 20]
pop = [10, 10, 8, 9, 5, 6, 7, 8, 10, 3, 8, 4]
fat = [20, 16, 10, 7, 6, 5, 13, 15, 18, 0, 19, 0]
cals = [100, 100, 80, 50, 60, 40, 80, 90, 80, 145, 120, 120]
weight = [24, 22, 15, 12, 10, 10, 14, 17, 20, 8, 20, 15]

# choose alpha between 0 and 1
alpha = 0


model.obj = Objective(
    expr=(1 - alpha) * sum(pop[i] * model.x[i] for i in model.x)
          - alpha * sum(cost[i] * model.x[i] for i in model.x),
    sense=maximize
)

# Define the inequality constraints
model.weight_min = Constraint(expr=sum(weight[i] * model.x[i] for i in model.x) >= 320)
model.weight_max = Constraint(expr=sum(weight[i] * model.x[i] for i in model.x) <= 1.5 * 320)
model.cals_max = Constraint(expr=sum(cals[i] * model.x[i] for i in model.x) <= 2850)
model.fat_weight_min = Constraint(expr=sum(fat[i] * model.x[i] for i in model.x) <= 0.45 * sum(weight[i] * model.x[i] for i in model.x))

# Solve the optimization problem
solver = SolverFactory('glpk')  # You can use a different solver here
solver.solve(model, tee=True)

# Print the model
model.pprint()

# Print the results
model.display()
