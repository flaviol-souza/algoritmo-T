import time

from tracker import log_permutation, AlgorithmTracker

def algoritm_t_online(vector, stats:AlgorithmTracker):
    n = len(vector)
    a = list(vector)
    d = [-1] * n
    c = [0] * n
    stats.att_vector += (n * 3) +1
    stats.att_local += 1

    log_permutation(a)
    stats.permutations += 1

    i = 0
    stats.att_local += 1
    while i < n:
        stats.comparisons += 1

        stats.comparisons += 1
        if c[i] < i:

            target = a.index(i + 1)
            neighbor = target + d[target]
            stats.att_local += 2

            a[target], a[neighbor] = a[neighbor], a[target]
            stats.exchanges += 1
            stats.att_vector += 2

            c[i] += 1
            stats.att_vector += 1

            i = 0 
            stats.att_local += 1

            stats.permutations += 1
            log_permutation(a)
        
        else:
            d[i] = -d[i] 
            c[i] = 0
            i += 1
            stats.att_vector += 2
            stats.att_local += 1

def __transaction_table(stats:AlgorithmTracker, n):
    c = [0] * n
    d = [-1] * n
    stats.tab_att_vector += (n * 2)

    transactions = []
    stats.tab_att_local += 1

    i = 0
    stats.tab_att_local += 1

    while i < n:
        stats.tab_comparisons += 1

        stats.tab_comparisons += 1
        if c[i] < i:

            stats.tab_comparisons += 1
            if i % 2 == 0:
                idx_i, idx_j = i, c[i] 
            else:
                idx_i, idx_j = i, 0
            stats.tab_att_local += 2

            transactions.append((idx_i, idx_j))
            stats.tab_att_vector += 1

            c[i] += 1
            stats.tab_att_vector += 1

            i = 0
            stats.tab_att_local += 1
        
        else:
            d[i] = -d[i]
            c[i] = 0
            stats.tab_att_vector += 2

            i += 1
            stats.tab_att_local += 2
        
    return transactions

def algoritm_t_offline(vector, stats:AlgorithmTracker):
    n = len(vector)
    stats.att_vector += 1
    
    stats.start_build_table_time = time.perf_counter()
    transactions = __transaction_table(stats, n)
    stats.end_build_table_time = time.perf_counter()

    a = list(vector)
    stats.att_vector += n
    
    stats.permutations += 1
    log_permutation(a)

    for (idx_i, idx_j) in transactions:
        temp = a[idx_i]
        stats.att_local += 1 

        a[idx_i] = a[idx_j]
        a[idx_j] = temp
        stats.exchanges += 1
        stats.att_vector += 2 
        
        stats.permutations += 1
        log_permutation(a)