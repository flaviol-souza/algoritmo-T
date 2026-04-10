import time

from tracker import log_permutation, AlgorithmTracker

def algoritm_t_online(vector, stats:AlgorithmTracker):
    
    a = list(vector)
    n = len(a)
    d = [-1] * n
    stats.transactions = []
    stats.att_vector += (n *2)

    log_permutation(a)

    while True:
        mobile = -1
        idx_mobile = -1
        stats.att_local += 2

        for i in range(n):
            stats.comparisons += 1
            prox = i + d[i]
            stats.att_local += 1

            stats.comparisons += 1
            if prox >= 0:

                stats.comparisons += 1
                if prox < n:

                    stats.comparisons += 1
                    if a[i] > a[prox]:

                        stats.comparisons += 1
                        if a[i] > mobile:
                            mobile = a[i]
                            idx_mobile = i
                            stats.att_local += 2

        stats.comparisons += 1
        if idx_mobile == -1:
            break

        destination = idx_mobile + d[idx_mobile]
        stats.att_local += 1

        stats.transactions.append((idx_mobile, destination))
        stats.att_vector += 1
    
        a[idx_mobile], a[destination] = a[destination], a[idx_mobile]
        d[idx_mobile], d[destination] = d[destination], d[idx_mobile]
        stats.exchanges += 1
        stats.att_vector += 4

        for i in range(n):
            stats.comparisons += 1
            if a[i] > mobile:
                d[i] = -d[i]
                stats.att_vector += 1

        log_permutation(a)

def __transaction_table(stats:AlgorithmTracker, n):
    a = list(range(1, n + 1))
    direction = [-1] * n
    stats.tab_att_vector += (n * 2)

    transactions = []
    stats.tab_att_local += 1

    while True:
        mobile = -1
        idx_mobile = -1
        stats.tab_att_local += 2

        for i in range(n):
            stats.tab_comparisons += 1
            prox_idx = i + direction[i]
            stats.tab_att_local += 1

            stats.tab_comparisons += 1
            if 0 <= prox_idx < n:

                stats.tab_comparisons += 1
                if a[i] > a[prox_idx]:

                    stats.tab_comparisons += 1
                    if a[i] > mobile:
                        mobile = a[i]
                        idx_mobile = i
                        stats.tab_att_local += 2
        
        stats.tab_comparisons += 1
        if idx_mobile == -1:
            break
        
        prox = idx_mobile + direction[idx_mobile]
        stats.tab_att_local += 1

        transactions.append((idx_mobile, prox))
        stats.tab_att_vector += 1

        a[idx_mobile], a[prox] = a[prox], a[idx_mobile]
        stats.tab_exchanges += 1
        stats.tab_att_vector += 2

        direction[idx_mobile], direction[prox] = direction[prox], direction[idx_mobile]
        stats.tab_att_vector += 2

        for i in range(n):
            stats.tab_comparisons += 1
            if a[i] > mobile:
                direction[i] = -direction[i]
                stats.tab_att_vector += 1

    stats.transactions = transactions

def algoritm_t_offline(vector, stats:AlgorithmTracker):
    n = len(vector)
    
    stats.start_build_table_time = time.perf_counter()
    __transaction_table(stats, n)
    stats.end_build_table_time = time.perf_counter()

    a = list(vector)
    stats.att_vector += n
    
    log_permutation(a)

    for (idx_i, idx_j) in stats.transactions:
        temp = a[idx_i]
        stats.att_local += 1 

        a[idx_i] = a[idx_j]
        a[idx_j] = temp
        stats.exchanges += 1
        stats.att_vector += 2 
        
        log_permutation(a)