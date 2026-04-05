from tracker import log_permutation, AlgorithmTracker

def algoritmo_p(n):
    stats = AlgorithmTracker()
    a = list(range(1, n + 1))
    d = [-1] * n
    stats.att_vector += (n * 2) + 1

    log_permutation(a)

    stats.permutations = 1
    while True:
        movivel = -1
        idx_movivel = -1
        stats.att_local += 2

        for i in range(n):
            stats.comparisons += 1 
            prox_idx = i + d[i]
            stats.att_local += 1
            
            stats.comparisons += 1 
            if 0 <= prox_idx < n:
                stats.comparisons += 1 
                if a[i] > a[prox_idx]:
                    stats.comparisons += 1 
                    if a[i] > movivel:
                        movivel = a[i]
                        idx_movivel = i
                        stats.att_local += 2
                        

        if idx_movivel == -1:
            stats.comparisons += 1
            break

        destino = idx_movivel + d[idx_movivel]
        stats.att_local += 1
        
        a[idx_movivel], a[destino] = a[destino], a[idx_movivel]
        d[idx_movivel], d[destino] = d[destino], d[idx_movivel]
        stats.exchanges += 1
        stats.att_vector += 4

        for i in range(n):
            stats.comparisons += 1
            stats.comparisons += 1
            if a[i] > movivel:
                d[i] = -d[i]
                stats.att_vector += 1
        
        stats.permutations += 1
        log_permutation(a)
    return stats