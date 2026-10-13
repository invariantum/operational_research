clear all; close all;
% Repeats the experiment with the same random numbers
% comment the rng(*) line out for random results each run
rng(1)

% number of trials to repeat
no_trials = 500;

% generate random integers between 1 and 6 and see ...
trials = randi(6,no_trials,1);

% define a blank matrix to store cumulative trial count
cumulative_count = zeros(no_trials,6);
% count the number of times we see a 1, 2, 3,... and store 
% e.g. cumulative_count(:,2) = cumsum(trials == 2)
for i=1:6
    cumulative_count(:,i) = cumsum(trials == i)
end

% transform the cumulative count into a percentage
cumulative_per = cumulative_count./[1:no_trials]'*100

% plot the no. heads and no. tails seen
figure(1)
for i=1:6
    plot(cumulative_count(:,i))
    hold on
end
hold off
xlabel('Trials')
ylabel('No. Outcomes')
title('No. Outcomes per Trial')
legend('No. 1s', 'No. 2s', 'No. 3s', 'No. 4s', 'No. 5s', 'No. 6s')

% plot the percentage no. heads and no. tails seen
figure(2)
for i=1:6
    plot(cumulative_per(:,i))
    hold on
end
hold off
xlabel('Trials')
ylabel('Percentage')
title('Percentage of Outcomes per Trial')
legend('No. 1s', 'No. 2s', 'No. 3s', 'No. 4s', 'No. 5s', 'No. 6s')