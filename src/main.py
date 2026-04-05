import matplotlib.pyplot as plt
import math

from p import algoritmo_p
from t import algoritm_t_online, algoritm_t_offline

def plot_results(n_list, metrics):
    
    for alg, data in metrics.items():
        plt.figure(figsize=(10, 6))
        plt.plot(n_list, data["Comparações"], label="Comparações", marker='o')
        plt.plot(n_list, data["Atribuições Local"], label="Atribuições Locais", marker='s')
        plt.plot(n_list, data["Atribuições V"], label="Atribuições Vetor", marker='s')
        plt.plot(n_list, data["Trocas"], label="Trocas", marker='x')

        plt.yscale('log') 
        plt.xlabel('n (Tamanho da entrada)')
        plt.ylabel('Contagem (Escala Log)')
        plt.title(f'Complexidade de Geração de Permutações ({alg})')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.5)
        plt.savefig(f'results/{alg}.png')
        #plt.show()

algoritms = {"T online": algoritm_t_online, "T offline": algoritm_t_offline}
values_n = list(range(3, 11))

metrics = {}
for name in algoritms:
    metrics[name] = {"Comparações": [], "Atribuições Local": [], "Atribuições V": [], "Trocas": []}

    print(f"\n\n\t\t*** Algoritm: {name} ***")
    print("-" * 97)
    print(f"{'n':<4} | {'n!':<10} | {'Comparacoes':<12} | {'Atribuicoes (local vars)':<25} | {'Atribuicoes (to/from  V)':<23} | {'Trocas':<8}")
    print("-" * 97)

    for n in values_n:
        tracker = algoritms[name](n)
        metrics[name]["Comparações"].append(tracker.comparisons)
        metrics[name]["Atribuições Local"].append(tracker.att_local)
        metrics[name]["Atribuições V"].append(tracker.att_vector)
        metrics[name]["Trocas"].append(tracker.exchanges)
        
        print(f"{n:<4} | {math.factorial(n):<10} | {tracker.comparisons:<12} | {tracker.att_local:<25} | {tracker.att_vector:<23}  | {tracker.exchanges:<8} ")

plot_results(values_n, metrics)    
