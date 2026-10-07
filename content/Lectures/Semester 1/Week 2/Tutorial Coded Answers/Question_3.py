# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 13:25:18 2023

@author: tcsr529
"""

from scipy.optimize import linprog

# cost function (row vector) - to minimise we need the negatives
c = [-5, -17]

# linear inequalities 
# (no. rows in A = no. rows in b)
A_ub = [[2, 3],
        [1, 1]]
b_ub = [60, 25]     

#  call the linprog function
results = linprog(c, A_ub, b_ub)

print(results.message)
# if results are a success then print out the optimal solution
if results.success:
    for k in range(len(results.x)):
        print(f"x[{k+1}] = {results.x[k]:.2f}")
    print(f"fval = {results.fun:.2f}")  
        