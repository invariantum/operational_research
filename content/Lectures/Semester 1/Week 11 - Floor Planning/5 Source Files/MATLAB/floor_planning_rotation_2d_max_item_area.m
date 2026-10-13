clear all; close all

%w = [4,3,6,7]';
%h = [5,7,4,7]';


% EXAMPLE 2
w = [4,3,6,7,3,2]';
h = [5,7,4,6,3,4]';

W = 10
H = 10

M = 9999;

no_items = length(w);
no_binary = nchoosek(no_items,2);

% Variables
x = optimvar('Ax',no_items,'LowerBound',0,'UpperBound',inf);
y = optimvar('Ay',no_items,'LowerBound',0,'UpperBound',inf);
xij = optimvar('xij',no_items,no_items,...
                'Type','integer','LowerBound',0,'UpperBound',1);
yij = optimvar('yij',no_items,no_items,...
                'Type','integer','LowerBound',0,'UpperBound',1);
r = optimvar('Ar',no_items,...
                'Type','integer','LowerBound',0,'UpperBound',1);
            
u = optimvar('u',no_items,...
                'Type','integer','LowerBound',0,'UpperBound',1);

% Objective
prob = optimproblem('ObjectiveSense','maximize');
prob.Objective = sum(u.*w.*h);

overlap_xij = optimconstr(no_binary);
overlap_xji = optimconstr(no_binary);
overlap_yij = optimconstr(no_binary);
overlap_yji = optimconstr(no_binary);
box_xi = optimconstr(no_binary);
box_yi = optimconstr(no_binary);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% non overlapping 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
k = 1;
for i = 1:no_items -1
    for j = i:no_items
        if i ~= j
            overlap_xij(k) = x(i) + (1-r(i))*w(i) +r(i)*h(i) <= ...
                                x(j) + M*(xij(i,j)+yij(i,j)) +M*(2-u(i)-u(j));
            overlap_xji(k) = x(j) + (1-r(j))*w(j) +r(j)*h(j) <= ...
                                x(i) + M*(1-xij(i,j)+yij(i,j)) +M*(2-u(i)-u(j));
                            
            overlap_yij(k) = y(i) + (1-r(i))*h(i) +r(i)*w(i) <= ...
                                y(j) + M*(1+xij(i,j)-yij(i,j)) +M*(2-u(i)-u(j));
            overlap_yji(k) = y(j) + (1-r(j))*h(j) +r(j)*w(j) <= ...
                                y(i) + M*(2-xij(i,j)-yij(i,j)) +M*(2-u(i)-u(j));
                            
            k = k + 1;
        
        end
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% box constraints
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
box_xi = x + (1-r).*w +r.*h <= W + M.*(1-u);
box_yi = y + (1-r).*h +r.*w <= H + M.*(1-u);


prob.Constraints.overlap_xij = overlap_xij;
prob.Constraints.overlap_xji = overlap_xji;
prob.Constraints.overlap_yij = overlap_yij;
prob.Constraints.overlap_yji = overlap_yji;
prob.Constraints.box_xi = box_xi;
prob.Constraints.box_yi = box_yi;


problem = prob2struct(prob);

[sol,fval,exitflag,output] = intlinprog(problem);
prob.Variables;


% plotting code
figure
ri = sol(1:no_items);
xsol=sol(no_items+1:no_items+1+2*no_items);
ui = sol(no_items+1+2*no_items:no_items+1+2*no_items+no_items);
for i=1:no_items
    x = xsol(i);
    y = xsol(i+no_items);
    wi = w(i);
    hi= h(i);
    if ui(i)
     if ri(i)
         disp('rotated')
         pgon = polyshape([x x+hi x+hi x],[y y y+wi y+wi]);
         [x x+hi x+hi x];
         [y y y+wi y+wi];
     else
        pgon = polyshape([x x+wi x+wi x],[y y y+hi y+hi]); 
        disp('not rotated')
        [x x+wi x+wi x];
        [y y y+hi y+hi];
     end
    end
    plot(pgon)
    hold on;
end
grid on
axis equal;
% update to for number of items 
legend({'1','2', '3', '4'},'Location','southwest');
xlabel('x') ;
ylabel('y') ;

