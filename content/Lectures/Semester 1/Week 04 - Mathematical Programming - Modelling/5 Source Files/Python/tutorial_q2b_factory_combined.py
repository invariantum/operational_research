from pyomo.environ import *

# Create a Concrete Model
model = ConcreteModel()

# Define integer variables
model.x = Var(range(4), domain=NonNegativeIntegers)

# Define objective function coefficients
profit = [10, 15, 10, 15]

# Define coefficients for constraints
grind_a = [4, 2, 0, 0]
polish_a = [2, 5, 0, 0]
grind_b = [0, 0, 5, 3]
polish_b = [0, 0, 5, 6]
raw = [4, 4, 4, 4]

# Objective function
model.obj = Objective(expr=sum(profit[i] * model.x[i] for i in model.x), sense=maximize)

# Define the inequality constraints
model.grinding_cap_factorya = Constraint(expr=sum(grind_a[i] * model.x[i] for i in model.x) <= 80)
model.polishing_cap_factorya = Constraint(expr=sum(polish_a[i] * model.x[i] for i in model.x) <= 60)
model.grinding_cap_factoryb = Constraint(expr=sum(grind_b[i] * model.x[i] for i in model.x) <= 60)
model.polishing_cap_factoryb = Constraint(expr=sum(polish_b[i] * model.x[i] for i in model.x) <= 75)
model.raw_cap = Constraint(expr=sum(raw[i] * model.x[i] for i in model.x) <= 120)

# Solve the optimization problem
solver = SolverFactory('glpk')  # You can use a different solver here
solver.solve(model, tee=True)

# Print the model
model.pprint()

# Print the results
model.display()

# Calculate used raw material for each factory
used_raw = [raw[i] * value(model.x[i]) for i in model.x]
print("Used raw material for each factory:", used_raw)
