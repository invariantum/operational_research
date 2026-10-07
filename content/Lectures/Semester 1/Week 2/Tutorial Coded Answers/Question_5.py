# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:25:18 2023

@author: tcsr529
"""

from scipy.optimize import linprog

# Part A

# cost function (row vector) - to minimise we need the negatives
c = [10, 6, 8, 16, 8, 3, 6, 8, 12, 12]

# linear inequalities 
# (no. rows in A = no. rows in b)
A_ub = [[-18, -8, -22, -6, 0, 0, -8, -4, 0, -12],
        [-4, -6, -10, -12, -14, 0, 0, 0, -6, -20],
        [0, -22, 0, 0, 0, -20, 0, -8, -10, 0],
        [-6, -14, 0, -6, -10, -8, -6, 0, -12, -4],
        [0, 0, 8, 0, 0, 6, 20, 40, 0, 0]]
b_ub = [-100, -120, -200, -80, 300]   

#  call the linprog function
results = linprog(c, A_ub, b_ub)

print(results.message)
# if results are a success then print out the optimal solution
if results.success:
    for k in range(len(results.x)):
        print(f"x[{k+1}] = {results.x[k]:.2f}")
    print(f"fval = {results.fun:.2f}")  
        

#Part B
# attractiveness cost function - note we are minimising...
a = [-6, -1, -5, -5, -6, -4, -10, -10, -6, -7]

#  call the linprog function
results = linprog(a, A_ub, b_ub)

print(results.message)
# if results are a success then print out the optimal solution
if results.success:
    for k in range(len(results.x)):
        print(f"x[{k+1}] = {results.x[k]:.2f}")
    print(f"fval = {results.fun:.2f}")       


# linear inequalities 
# (no. rows in A = no. rows in b)
A_ub = [[-18, -8, -22, -6, 0, 0, -8, -4, 0, -12],
        [18, 8, 22, 6, 0, 0, 8, 4, 0, 12],
        [-4, -6, -10, -12, -14, 0, 0, 0, -6, -20],
        [4, 6, 10, 12, 14, 0, 0, 0, 6, 20],
        [0, -22, 0, 0, 0, -20, 0, -8, -10, 0],
        [0, 22, 0, 0, 0, 20, 0, 8, 10, 0],
        [-6, -14, 0, -6, -10, -8, -6, 0, -12, -4],
        [6, 14, 0, 6, 10, 8, 6, 0, 12, 4],
        [0, 0, -8, 0, 0, -6, -20, -40, 0, 0],
        [0, 0, 8, 0, 0, 6, 20, 40, 0, 0]
        ]
b_ub = [-100, 100*1.2, -120, 120*1.2, -200, 200*1.2, -80, 80*1.2, -300/1.2, 300]

#  call the linprog function
results = linprog(a, A_ub, b_ub)

print(results.message)
# if results are a success then print out the optimal solution
if results.success:
    for k in range(len(results.x)):
        print(f"x[{k+1}] = {results.x[k]:.2f}")
    print(f"fval = {results.fun:.2f}")  
        