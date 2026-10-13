clear all;
% define integer variables 
x = optimvar('x',12,'LowerBound',0,'UpperBound',inf,'Type','integer');
% define objective function values (row vector)
pop = [10 10 8 9 5 6 7 8 10 3 8 4];


fat = [20 16 10 7 6 5 13 15 18 0 19 0];
cals = [100 100 80 50 60 40 80 90 80 145 120 120];
weight = [24 22 15 12 10 10 14 17 20 8 20 15];
% create optimisation problem 
prob = optimproblem('Objective',pop*x,'ObjectiveSense','max');
% define the inequality constraints
prob.Constraints.weight_min = weight*x >= 320;
prob.Constraints.cals_max = cals*x <= 2850;
prob.Constraints.fat_weight_min = fat*x <= 0.45*weight*x;


% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value, exitflag and output
[sol,fval,exitflag,output] = intlinprog(problem)  