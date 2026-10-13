# M = [5 8 2 4 5;
     3 3 7 9 3];


M = [4 6 2 3 5;
     1 2 3 4 3];

[no_r,no_c] = size(M);

front = [];
back = [];
for i=1:no_c
    [min_val,idx]=min(M(:));
    [row,col]=ind2sub(size(M),idx);
    [row,col]
    if row ==1
        front = [front col]
    else
        % add job 3 to [2 5] -> [3 2 5]
        back = [col back]
    end
    M(:, col) = 9999;
end
optimal_sequence = [front back];
optimal_sequence
