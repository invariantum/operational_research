clear all; close all;
% Repeats the experiment with the same random numbers
% comment the rng(*) line out for random results each run
rng(1)

% probability of heads
p_heads = 0.5;
% number of trials to repeat
no_trials = 500;

% generate 500 random numbers between 0 and 1 and see ...
% if they are less than p_heads 
trials = rand(no_trials,1) < p_heads;

% get cumulative count of no. heads seen and calculate no. tails
no_heads = cumsum(trials);
no_tails = [1:no_trials]' - cumsum(trials);

% compute the percentage for each trial of heads and tails seen
per_heads = no_heads./[1:no_trials]';
per_tails = no_tails./[1:no_trials]';

% plot the no. heads and no. tails seen
figure(1)
plot(no_heads)
hold on
plot(no_tails)
hold off
xlabel('Trials')
ylabel('Cumulative No.')
title('Cumulative Outcomes')
legend('No. Heads', 'No. Tails')

% plot the percentage no. heads and no. tails seen
figure(2)
plot(per_heads)
hold on
plot(per_tails)
hold off
xlabel('Trials')
ylabel('Percentage')
title('Percentage of Outcomes')
legend('No. Heads', 'No. Tails')