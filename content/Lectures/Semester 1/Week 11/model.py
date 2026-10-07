from pyomo.environ import *
import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cm

# Data
w = np.array([4,3,6,7,3,2])
h = np.array([5,7,4,6,3,4])

# w = np.array([4,3,6,7])
# h = np.array([5,7,4,7])

M = 9999

no_items = len(w)
no_binary = int(comb(no_items,2))

# Model
model = ConcreteModel()

# Sets
model.I = RangeSet(no_items)
model.J = RangeSet(no_items)

# Parameters
model.w = Param(model.I, initialize=lambda model, i: w[i-1])
model.h = Param(model.I, initialize=lambda model, i: h[i-1])

# Variables
model.x = Var(model.I, within=NonNegativeReals)
model.y = Var(model.I, within=NonNegativeReals)
model.v = Var(within=NonNegativeReals)
model.xij = Var(model.I, model.J, within=Binary)
model.yij = Var(model.I, model.J, within=Binary)
model.r = Var(model.I, within=Binary)

# Objective
model.obj = Objective(expr=model.v, sense=minimize)

# Constraints
def overlap_xij_rule(model, i, j):
    if i < j:
        return model.x[i] + (1-model.r[i])*model.w[i] + model.r[i]*model.h[i] <= model.x[j] + M*(model.xij[i,j]+model.yij[i,j])
    
    return Constraint.Skip
    
model.overlap_xij = Constraint(model.I, model.J, rule=overlap_xij_rule)

def overlap_xji_rule(model, i, j):
    if i < j:
        return model.x[j] + (1-model.r[j])*model.w[j] + model.r[j]*model.h[j] <= model.x[i] + M*(1-model.xij[i,j]+model.yij[i,j])
    
    return Constraint.Skip
model.overlap_xji = Constraint(model.I, model.J, rule=overlap_xji_rule)

def overlap_yij_rule(model, i, j):
    if i < j:
        return model.y[i] + (1-model.r[i])*model.h[i] + model.r[i]*model.w[i] <= model.y[j] + M*(1+model.xij[i,j]-model.yij[i,j])
        
    return Constraint.Skip

model.overlap_yij = Constraint(model.I, model.J, rule=overlap_yij_rule)

def overlap_yji_rule(model, i, j):
    if i < j:
        return model.y[j] + (1-model.r[j])*model.h[j] + model.r[j]*model.w[j] <= model.y[i] + M*(2-model.xij[i,j]-model.yij[i,j])
    
    return Constraint.Skip
model.overlap_yji = Constraint(model.I, model.J, rule=overlap_yji_rule)

def box_xi_rule(model, i):
    return model.x[i] + (1-model.r[i])*model.w[i] + model.r[i]*model.h[i] <= model.v
model.box_xi = Constraint(model.I, rule=box_xi_rule)

def box_yi_rule(model, i):
    return model.y[i] + (1-model.r[i])*model.h[i] + model.r[i]*model.w[i] <= model.v
model.box_yi = Constraint(model.I, rule=box_yi_rule)

# used to switch off rotation
def rotation_off(model, i):
    return model.r[i] <= 0

# uncomment this to switch off rotation
#model.rotation_off = Constraint(model.I, rule=rotation_off)

# Solve
solver = SolverFactory('glpk')
solver.solve(model, tee=True)

model.display()
model.pprint()

# Print the value of the variables at the optimum
for i in model.I:
    print("x[",i,"]=", model.x[i].value)
    print("y[",i,"]=", model.y[i].value)
    print("r[",i,"]=", model.r[i].value)
print("v=", model.v.value)

fig, ax = plt.subplots()

cmap = cm.get_cmap('Pastel1')  # Can be any colormap available in matplotlib

for i in range(1, no_items+1):
    x = model.x[i].value
    y = model.y[i].value
    wi = w[i-1]
    hi = h[i-1]
    color = cmap(i/no_items)  # Get the color from the colormap
    if model.r[i].value:
        print('rotated')
        rect = patches.Rectangle((x,y),hi,wi,linewidth=2,edgecolor='k',facecolor=color)
    else:
        print('not rotated')
        rect = patches.Rectangle((x,y),wi,hi,linewidth=2,edgecolor='k',facecolor=color)
    ax.add_patch(rect)

plt.grid(True)
plt.axis('equal')
plt.legend([str(x) for x in range(1, no_items+1)], loc='lower left')
plt.xlabel('x')
plt.ylabel('y')
plt.show()
