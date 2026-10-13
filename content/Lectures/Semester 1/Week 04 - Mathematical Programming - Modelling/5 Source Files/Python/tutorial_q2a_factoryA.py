from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define integer variables
model.x = Var(range(2), domain=NonNegativeIntegers)

# Define objective function coefficients
profit = [10, 15]

# Define coefficients for constraints
grind = [4, 2]
polish = [2, 5]
raw = [4, 4]

# Objective function
model.obj = Objective(expr=sum(profit[i] * model.x[i] for i in model.x), sense=maximize)

# Define the inequality constraints
model.grinding_cap = Constraint(expr=sum(grind[i] * model.x[i] for i in model.x) <= 80)
model.polishing_cap = Constraint(expr=sum(polish[i] * model.x[i] for i in model.x) <= 60)
model.raw_cap = Constraint(expr=sum(raw[i] * model.x[i] for i in model.x) <= 75)

# Solve the optimization problem
solver = SolverFactory('glpk')  # You can use a different solver here
solver.solve(model, tee=True)

# Print the model
model.pprint()

# Print the results
model.display()

# Calculate surpluses
surplus_grind = 80 - sum(grind[i] * value(model.x[i]) for i in model.x)
surplus_polish = 60 - sum(polish[i] * value(model.x[i]) for i in model.x)
surplus_raw = 75 - sum(raw[i] * value(model.x[i]) for i in model.x)

print("Surplus in grinding capacity:", surplus_grind)
print("Surplus in polishing capacity:", surplus_polish)
print("Surplus in raw material capacity:", surplus_raw)

