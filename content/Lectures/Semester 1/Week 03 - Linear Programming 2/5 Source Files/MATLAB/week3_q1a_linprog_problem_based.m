clear all;
% define variables 
x = optimvar('x',2,'LowerBound',0,'UpperBound',inf);
% define objective function values (row vector)
f = [5 17];
% create optimisation problem 
prob = optimproblem('Objective',f*x,'ObjectiveSense','max');
% define the inequality constraints
c1 = 2*x(1) + 3*x(2) <= 60;
c2 = x(1) + 2*x(2) <= 25;
% add them to the optimisation problem
prob.Constraints.c1 = c1;
prob.Constraints.c2 = c2;

% convert the optimisation problem 
problem = prob2struct(prob);

prob.ObjectiveSense
prob.Objective
fn = fieldnames(prob.Constraints);
disp('Subject to:')
for i=1:numel(fn)
    disp(prob.Constraints.(fn{i}))
end

% solve and return the solution, function value
[sol,fval] = linprog(problem)