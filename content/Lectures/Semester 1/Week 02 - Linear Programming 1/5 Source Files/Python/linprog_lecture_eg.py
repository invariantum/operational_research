from scipy.optimize import linprog

# cost function (row vector) - to minimise we need the negatives
c = [-5, -7]

# linear inequalities 
# (no. rows in A = no. rows in b)
A_ub = [[3, 2],
        [-1, 4]]
b_ub = [144, 0] 

#  call the linprog function
results = linprog(c, A_ub, b_ub)

print(results.message)
# if results are a success then print out the optimal solution
if results.success:
    for k in range(len(results.x)):
        print(f"x[{k+1}] = {results.x[k]:.2f}")
    print(f"fval = {results.fun:.2f}")        
        
