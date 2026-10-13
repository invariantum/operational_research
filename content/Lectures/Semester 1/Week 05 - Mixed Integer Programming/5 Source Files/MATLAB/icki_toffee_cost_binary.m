clear all;
% define integer variables 
x = optimvar('x',12,'LowerBound',0,'UpperBound',inf,'Type','integer');
xb = optimvar('xb',12,'LowerBound',0,'UpperBound',1,'Type','integer');
% define objective function values (row vector)
cost = [12 12 12 15 13 13 16 16 15 10 18 20];

fat = [20 16 10 7 6 5 13 15 18 0 19 0];
cals = [100 100 80 50 60 40 80 90 80 145 120 120];
weight = [24 22 15 12 10 10 14 17 20 8 20 15];

% create optimisation problem 
prob = optimproblem('Objective',cost*x,'ObjectiveSense','min');
% define the inequality constraints
prob.Constraints.weight_min = weight*x >= 320;
prob.Constraints.weight_max = weight*x <= 1.5*320;
prob.Constraints.cals_max = cals*x <= 2850;
prob.Constraints.fat_weight_min = fat*x <= 0.45*weight*x;

% Ensure that your selection has at least 6 different candies
prob.Constraints.variety = sum(xb) >= 6;
% Ensure your selection includes at least 3 of each of the selected candies.
prob.Constraints.selection_min = x >= 3*xb;
% Ensure your selection includes at most 6 of each of the selected candies.
prob.Constraints.selection_max = x <= 6*xb;


% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value, exitflag and output
[sol,fval,exitflag,output] = intlinprog(problem);
prob.Variables
% Print out x values
sol(1:end/2)
% Print out delta (binary) variables
sol(end/2+1:end)
% Print out minimum cost
fval