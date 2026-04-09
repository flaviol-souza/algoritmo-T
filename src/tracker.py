def log_permutation(p):
        pass #print("".join(map(str, p)))

class AlgorithmTracker:
    def __init__(self):
        self.att_local = 0  #atribuicoes locais
        self.att_vector = 0  #atribuicoes de vetor
        self.comparisons = 0   #comparacoes
        self.exchanges = 0     #trocas
        self.permutations = 0  #permutacoes
        self.memory_peak_kb = 0.0
        
        self.start_time = 0
        self.end_time = 0

        self.start_build_table_time = 0
        self.end_build_table_time = 0

    def duration_ms(self):
        return (self.end_time - self.start_time) * 1000
    
    def duration_build_table_ms(self):
        return (self.end_build_table_time - self.start_build_table_time) * 1000
    
    def duration_pure_execution_ms(self):
        return self.duration_ms() - self.duration_build_table_ms()
