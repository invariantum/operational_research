clear all;
% define binary variables 
x = optimvar('x',8,'LowerBound',0,'UpperBound',1,'Type','integer');
% define objective function values (row vector)
value = [10 50 40 100 100 130 70 80];
weight = [2 3 2 6 6 8 3 5];
W = 15;
% create optimisation problem 
prob = optimproblem('Objective',value*x,'ObjectiveSense','max');
% define the inequality constraints
prob.Constraints.capacity = weight*x <= W;

% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value
[sol,fval] = intlinprog(problem)  

