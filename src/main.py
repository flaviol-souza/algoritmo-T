import matplotlib.pyplot as plt
import math
import time
import random
import tracemalloc
import gc

from p import algoritmo_p
from t import algoritm_t_online, algoritm_t_offline
from tracker import AlgorithmTracker

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

def plot_comparativo_recursos(n_list, metrics):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    for alg_name, data in metrics.items():
        # Gráfico de Tempo
        ax1.plot(n_list, data["Tempo"], label=f"{alg_name}", marker='o')
        # Gráfico de Memória
        ax2.plot(n_list, data["Memoria"], label=f"{alg_name}", marker='s')

    # Configurações do Gráfico de Tempo
    ax1.set_yscale('log')
    ax1.set_xlabel('n (Tamanho da entrada)')
    ax1.set_ylabel('Tempo (ms) - Escala Log')
    ax1.set_title('Comparação de Tempo de Execução')
    ax1.legend()
    ax1.grid(True, which="both", ls="-", alpha=0.5)

    # Configurações do Gráfico de Memória
    ax2.set_yscale('log')
    ax2.set_xlabel('n (Tamanho da entrada)')
    ax2.set_ylabel('Memória (KB) - Escala Log')
    ax2.set_title('Comparação de Consumo de Memória (Pico)')
    ax2.legend()
    ax2.grid(True, which="both", ls="-", alpha=0.5)

    plt.tight_layout()
    plt.savefig('results/recursos.png')
    #plt.show()

algoritms = {"T online": algoritm_t_online, "T offline": algoritm_t_offline}
values_n = list(range(3, 11))

dict_vector = {}
for n in values_n:
    vetor = list(range(1, n + 1))
    #random.shuffle(vetor) 
    dict_vector[n] = vetor

metrics = {}
for name in algoritms:
    metrics[name] = {"Comparações": [], "Atribuições Local": [], "Atribuições V": [], "Trocas": [], "Memoria": [], "Tempo": [] }

    print(f"\n\n\t\t*** Algoritm: {name} ***")
    print("-" * 140)
    print(f"{'n':<4} | {'n!':<10} | {'Comparacoes':<12} | {'Atribuicoes (local vars)':<25} | {'Atribuicoes (to/from  V)':<23} | {'Trocas':<8} | {'Memoria (kb)':<15} |  {'Tempo (ms)':<8}")
    print("-" * 140)    

    for n, vector in dict_vector.items():
        gc.collect()
        tracemalloc.start()

        tracker = AlgorithmTracker()

        tracker.start_time = time.perf_counter()
        algoritms[name](vector, tracker)
        tracker.end_time = time.perf_counter()

        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        tracker.memory_peak_kb = peak / 1024

        metrics[name]["Comparações"].append(tracker.comparisons)
        metrics[name]["Atribuições Local"].append(tracker.att_local)
        metrics[name]["Atribuições V"].append(tracker.att_vector)
        metrics[name]["Trocas"].append(tracker.exchanges)
        metrics[name]["Memoria"].append(tracker.memory_peak_kb)
        metrics[name]["Tempo"].append(tracker.duration_ms())
        
        print(f"{n:<4} | {math.factorial(n):<10} | {tracker.comparisons:<12} | {tracker.att_local:<25} | {tracker.att_vector:<23}  | {tracker.exchanges:<8} | {tracker.memory_peak_kb:<15.2f} | {tracker.duration_ms():<8.4f} ")

plot_results(values_n, metrics)
plot_comparativo_recursos(values_n, metrics)