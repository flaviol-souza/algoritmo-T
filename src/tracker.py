def log_permutation(p):
        pass #print("".join(map(str, p)))

class AlgorithmTracker:
    def __init__(self):
        self.attributions = 0  #atribuicoes
        self.att_local = 0  #atribuicoes locais
        self.att_vector = 0  #atribuicoes de vetor
        self.comparisons = 0   #comparacoes
        self.exchanges = 0     #trocas
        self.permutations = 0  #permutacoes
        self.transactions = [] #transacoes
