clear all;
% define binary variables 
x = optimvar('x',7,'LowerBound',0,'UpperBound',1,...
            'Type','integer');
% create optimisation problem 
prob = optimproblem('Objective',sum(x),'ObjectiveSense','min');
% define the inequality constraints
prob.Constraints.city1 = x(1)+x(2)+x(3) >= 1;
prob.Constraints.city2 = x(1)+x(2)+x(4) >= 1;
prob.Constraints.city3 = x(1)+x(3) >= 1;
prob.Constraints.city4 = x(2)+x(4)+x(5) >= 1;
prob.Constraints.city5 = x(4)+x(5)+x(6) >= 1;
prob.Constraints.city6 = x(5)+x(6)+x(7) >= 1;
prob.Constraints.city7 = x(6)+x(7) >= 1;

% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value
[sol,fval] = intlinprog(problem)  

