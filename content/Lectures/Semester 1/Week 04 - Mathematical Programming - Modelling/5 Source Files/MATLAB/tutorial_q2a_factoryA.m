clear all;

%Factory A
%4s+2d<=80
%2s+5d<=60
%4s+4d<=75

%P=10s+15d


% define integer variables 
x = optimvar('x',2,'LowerBound',0,'UpperBound',inf,'Type','integer');
% define objective function values (row vector)
profit = [10 15];
grind = [4 2];
polish = [2 5];
raw = [4 4]

% create optimisation problem 
prob = optimproblem('Objective',profit*x,'ObjectiveSense','max');
% define the inequality constraints
prob.Constraints.grinding_cap = grind*x <= 80;
prob.Constraints.polishing_cap = polish*x <= 60;
prob.Constraints.raw_cap = raw*x <= 75;


% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value, exitflag and output
[sol,fval,exitflag,output] = intlinprog(problem)  

surplus_grind = 80 - grind*sol
surplus_polish = 60 - polish*sol
surplus_raw = 75 - raw*sol