clear all;




% define integer variables 
x = optimvar('x',4,'LowerBound',0,'UpperBound',inf,'Type','integer');
% define objective function values (row vector)
profit = [10 15 10 15];
grind_a = [4 2 0 0];
polish_a = [2 5 0 0];
grind_b = [0 0 5 3];
polish_b = [0 0 5 6];
raw = [4 4 4 4]

% create optimisation problem 
prob = optimproblem('Objective',profit*x,'ObjectiveSense','max');
% define the inequality constraints
prob.Constraints.grinding_cap_factorya = grind_a*x <= 80;
prob.Constraints.polishing_cap_factorya = polish_a*x <= 60;
prob.Constraints.grinding_cap_factoryb = grind_b*x <= 60;
prob.Constraints.polishing_cap_factoryb = polish_b*x <= 75;
prob.Constraints.raw_cap = raw*x <= 120;


% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value, exitflag and output
[sol,fval,exitflag,output] = intlinprog(problem)  

%Raw material for each factory
% We can compute what s1,d1,s2,d2 used and then sum s1+d1 and s2+d2
used_raw = raw'.*sol