clear all;
% define variables 
x1 = optimvar('x1',1,'LowerBound',0,'UpperBound',inf);
x2 = optimvar('x2',1,'LowerBound',0,'UpperBound',inf,'Type','integer');
% define objective function values (row vector)
f = [5 17];
% create optimisation problem 
prob = optimproblem('Objective',f(1)*x1+f(2)*x2,'ObjectiveSense','max');
% define the inequality constraints
c1 = 2*x1 + 3*x2 <= 60;
c2 = x1 + 2*x2 <= 25;
% add them to the optimisation problem
prob.Constraints.c1 = c1;
prob.Constraints.c2 = c2;

% convert the optimisation problem 
problem = prob2struct(prob);

% solve and return the solution, function value
[sol,fval] = intlinprog(problem)