import numpy as np

# Do Johnson's rule recursively
def johnsons_rule_rec(M):
    
    def johnsons_rule_rec_inner(M, front, end):
        # if there are no more jobs to do, return the list
        if np.min(M) == np.inf:
            return front + end
        
        # find the index of the minimum element
        ind = np.unravel_index(np.argmin(M), M.shape)
        M[0, ind[1]] = np.inf
        M[1, ind[1]] = np.inf
        
        if ind[0] == 0:
            # add the job to the front of the list
            front.append(ind[1])
            return johnsons_rule_rec_inner(M, front, end)
        else:
            # add the job to the end of the list
            end.insert(0, ind[1])
            return johnsons_rule_rec_inner(M, front, end)
    
    # copy the list so we don't modify the original
    M = M.copy()
    return johnsons_rule_rec_inner(M, [], [])

# Do Johnson's rule iteratively
def johnsons_rule_iter(M):
    # copy the list so we don't modify the original
    M = M.copy()
    front = []
    end = []
    for _ in range(M.shape[1]):
        # if there are no more jobs to do, return the list
        if not np.min(M) == np.inf:
            # find the index of the minimum element
            ind = np.unravel_index(np.argmin(M), M.shape)
            M[0, ind[1]] = np.inf
            M[1, ind[1]] = np.inf

            if ind[0] == 0:
                # add the job to the front of the list
                front.append(ind[1])
            else:
                # add the job to the end of the list
                end.insert(0, ind[1])

    return front + end

if __name__ == "__main__":
    # Sample usage
    # Sample usage
    M = np.array([[2, 4, 6],
        [3, 3, 7]], dtype=float)
    print(johnsons_rule_rec(M))
    print(johnsons_rule_iter(M))

    M = np.array([[5, 8, 1, 4, 6],
        [2, 3, 11, 6, 7]], dtype=float)
    
    print(johnsons_rule_rec(M))
    print(johnsons_rule_iter(M))
