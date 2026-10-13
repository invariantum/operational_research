clear all;


x = optimvar('x',12,14,'LowerBound',0,'UpperBound',inf);
% define objective function values (row vector)

%           1  2  3  4  5  6  7  8  9  10 11 12 13 14
balance = [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0;
            0  0  0  0  0  0  0  0  0  0  0  0  0  0;
            -1 0  0  0  0  0  0  1  0  0  1  0  0  0;
            -1 0  0  0  0  0  0  0  1  0  0  1  0  0;
            0  -1 0  0  0  0  0  1  0  0  1  0  0  0;
            0  -1 0  0  0  0  0  0  1  0  0  1  0  0;
            0  -1 0  0  0  0  0  0  0  1  0  0  0  0;
            0  0  -1 0  -1 0  0  0  0  0  0  0  1  0;
            0  0  0 -1  0  -1 0  0  0  0  0  0  1  0;
            0  0  0  0  0  0  -1 0  0  0  0  0  1  0;
            0  0  -1 0  -1 0  0  0  0  0  0  0  0  1;
            0  0  0 -1  0 -1  0  0  0  0  0  0  0  1]
        
%           1  2  3  4  5  6  7  8  9  10 11 12 13 14
cost =  zeros(12,14);
% cost of production 
cost(1,3) = 1000;
cost(1,4) = 1200;
cost(2,5) = 900;
cost(2,6) = 1100;
cost(2,7) = 1500;

% cost of transportation
cost(3,8) = 4;
cost(3,11) = 5;
cost(4,9) = 3;
cost(4,12) = 6;
cost(5,8) = 5;
cost(5,11) = 6;
cost(6,9) = 4;
cost(6,12) = 3;
cost(7,10) = 4;
        
% create optimisation problem 
prob = optimproblem('Objective',sum(sum(cost.*x)),'ObjectiveSense','min');
% define the equality constraints
% sum the rows
prob.Constraints.balance = [];
% for i = 1:size(balance,1)
%     prob.Constraints.balance(end+1) = sum(balance(i, :).*x(i,:)) == 0
% end
prob.Constraints.balance(1) =  -x(1, 3) + x(3, 8) + x(3, 11) == 0;
prob.Constraints.balance(2) =  -x(1, 4) + x(4, 9) + x(4, 12) == 0;
prob.Constraints.balance(3) =  -x(2, 5) + x(5, 8) + x(5, 11) == 0;
prob.Constraints.balance(4) =  -x(2, 6) + x(6, 9) + x(6, 12) == 0;
prob.Constraints.balance(5) =  -x(2, 7) + x(7, 10) == 0;
prob.Constraints.balance(6) =  -x(3, 8) - x(5, 8) + x(8, 13) == 0;
prob.Constraints.balance(7) =  -x(4, 9) - x(6, 9) + x(9, 13) == 0;
prob.Constraints.balance(8) =  -x(7, 10) + x(10, 13) == 0;
prob.Constraints.balance(9) =  -x(3, 11) - x(5, 11) + x(11, 14) == 0;
prob.Constraints.balance(10) =  -x(4, 12) - x(6, 12) + x(12, 14) == 0;

prob.Constraints.supply = [];
prob.Constraints.supply(1) = x(1,3) <= 150;
prob.Constraints.supply(2) = x(1,4) <= 120;
prob.Constraints.supply(3) = x(2,5) <= 100;
prob.Constraints.supply(4) = x(2,6) <= 150;
prob.Constraints.supply(5) = x(2,7) <= 100;

prob.Constraints.demand = [];
prob.Constraints.demand(1) = x(8,13) >= 100;
prob.Constraints.demand(2) = x(9,13) >= 80;
prob.Constraints.demand(3) = x(10,13) >= 70;
prob.Constraints.demand(4) = x(11,14) >= 100;
prob.Constraints.demand(5) = x(12,14) >= 130;

show(prob)

% convert the optimisation problem 
problem = prob2struct(prob);
% solve and return the solution, function value
[sol,fval] = linprog(problem);
%
reshape(sol, 12, 14)

