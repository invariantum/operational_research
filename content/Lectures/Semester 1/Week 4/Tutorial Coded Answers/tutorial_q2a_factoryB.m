clear all;

%Factory B
%5s+3d<=60
%5s+6d<=75
%4s+4d<=45

%P=10s+15d


% define integer variables 
x = optimvar('x',2,'LowerBound',0,'UpperBound',inf,'Type','integer');
% define objective function values (row vector)
profit = [10 15];
grind = [5 3];
polish = [5 6];
raw = [4 4]

% create optimisation problem 
prob = optimproblem('Objective',profit*x,'ObjectiveSense','max');
% define the inequality constraints
prob.Constraints.grinding_cap = grind*x <= 60;
prob.Constraints.polishing_cap = polish*x <= 75;
prob.Constraints.raw_cap = raw*x <= 45;


% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value, exitflag and output
[sol,fval,exitflag,output] = intlinprog(problem)  

surplus_grind = 60 - grind*sol
surplus_polish = 75 - polish*sol
surplus_raw = 45 - raw*sol