import matplotlib.pyplot as plt
import math
import time
import random
import tracemalloc
import gc
import json
import sys
import os

from p import algoritmo_p
from t import algoritm_t_online, algoritm_t_offline
from tracker import AlgorithmTracker

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

algoritms = {"T online": algoritm_t_online, "T offline": algoritm_t_offline}

def print_tabelas_finais(n_list, all_data):
    """
    Imprime as tabelas formatadas no terminal a partir dos dados consolidados nos JSONs.
    Responde à provocação do professor sobre 'Setup vs Uso'.
    """
    # Identifica os algoritmos presentes nos dados (ex: T online, T offline, P)
    alg_names = all_data[n_list[0]].keys()

    for name in alg_names:
        print(f"\n\n\t\t*** Relatório Consolidado: {name} ***")
        header_line = "-" * 165
        print(header_line)
        
        # Cabeçalho com separação clara de métricas
        print(f"{'n':<4} | {'n!':<10} | {'Comparacoes':<12} | {'Atrib. (Local)':<18} | {'Atrib. (Vetor)':<18} | {'Trocas':<8} | {'Memória (kb)':<15} | {'Setup (ms)':<15} | {'Uso Real (ms)':<15}")
        print(header_line)

        for n in n_list:
            if name in all_data[n]:
                res = all_data[n][name]
                
                # Cálculo dos tempos baseado na estrutura do JSON que definimos
                setup_time = res.get("Setup_ms", 0.0)
                total_time = res.get("Total_ms", 0.0)
                # O Uso Real é o que sobra quando retiramos o tempo de construção
                uso_real = total_time - setup_time
                
                print(f"{n:<4} | "
                      f"{res['n!']:<10} | "
                      f"{res['Comparações']:<12} | "
                      f"{res['Atribuições Local']:<18} | "
                      f"{res['Atribuições V']:<18} | "
                      f"{res['Trocas']:<8} | "
                      f"{res['Memoria']:<15.2f} | "
                      f"{setup_time:<15.4f} | "
                      f"{uso_real:<15.4f}")
        
        print(header_line)
        
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
        plt.savefig(f'{RESULTS_DIR}/{alg}.png')
        #plt.show()

def plot_comparativo_recursos(n_list, metrics):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    for alg_name, data in metrics.items():
        ax1.plot(n_list, data["Tempo"], label=f"{alg_name} (Uso)", marker='o')
        
        if "offline" in alg_name.lower():
            ax1.plot(n_list, data["Temp. Tab."], label=f"{alg_name} (Setup)", 
                     linestyle='--', alpha=0.7, marker='x')
        
        ax2.plot(n_list, data["Memoria"], label=alg_name, marker='s')

    # Configurações do gráfico de Tempo
    ax1.set_yscale('log')
    ax1.set_xlabel('n (Tamanho da entrada)')
    ax1.set_ylabel('Tempo (ms) - Escala Log')
    ax1.set_title('Comparativo de Tempo: Setup vs Uso')
    ax1.legend()
    ax1.grid(True, which="both", ls="-", alpha=0.5)

    # Configurações do gráfico de Memória
    ax2.set_yscale('log')
    ax2.set_xlabel('n (Tamanho da entrada)')
    ax2.set_ylabel('Pico de Memória (KB) - Escala Log')
    ax2.set_title('Consumo de Memória (Pico)')
    ax2.legend()
    ax2.grid(True, which="both", ls="-", alpha=0.5)

    plt.tight_layout()
    plt.savefig('results/recursos.png')
    #plt.show()

def save_n_results(n, results):
    filename = os.path.join(RESULTS_DIR, f"data_n_{n}.json")
    # Se já existir, carregamos para adicionar o novo algoritmo
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = {}
    
    existing_data.update(results)
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)

def load_all_results():
    all_data = {}
    files = [f for f in os.listdir(RESULTS_DIR) if f.startswith("data_n_") and f.endswith(".json")]
    
    for file in sorted(files, key=lambda x: int(x.split('_')[2].split('.')[0])):
        n = int(file.split('_')[2].split('.')[0])
        with open(os.path.join(RESULTS_DIR, file), 'r') as f:
            all_data[n] = json.load(f)
    return all_data

def run_benchmark(n):
    vetor = list(range(1, n + 1))
    #random.shuffle(vetor)
    
    results_for_n = {}
    
    for name, func in algoritms.items():
        gc.collect()
        tracemalloc.start()
        
        tracker = AlgorithmTracker()
        tracker.start_time = time.perf_counter()
        func(vetor, tracker)
        tracker.end_time = time.perf_counter()
        
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Guardamos os dados brutos
        results_for_n[name] = {
            "n!": math.factorial(n),
            "Comparações": tracker.comparisons,
            "Atribuições Local": tracker.att_local,
            "Atribuições V": tracker.att_vector,
            "Trocas": tracker.exchanges,
            "Memoria": peak / 1024,
            "Setup_ms": tracker.duration_build_table_ms(),
            "Total_ms": tracker.duration_ms()
        }
    
    save_n_results(n, results_for_n)
    print(f"Resultados para n={n} salvos com sucesso.")

def generate_reports():
    data = load_all_results()
    if not data:
        print("Nenhum dado encontrado em /results.")
        return

    n_list = sorted(data.keys())
    
    # Reorganiza para o formato que as suas funções de plot já usam
    formatted_metrics = {}
    for name in algoritms.keys():
        formatted_metrics[name] = {
            "Comparações": [], "Atribuições Local": [], "Atribuições V": [],
            "Trocas": [], "Memoria": [], "Temp. Tab.": [], "Tempo": []
        }

    for n in n_list:
        for name in algoritms.keys():
            res = data[n][name]
            formatted_metrics[name]["Comparações"].append(res["Comparações"])
            formatted_metrics[name]["Atribuições Local"].append(res["Atribuições Local"])
            formatted_metrics[name]["Atribuições V"].append(res["Atribuições V"])
            formatted_metrics[name]["Trocas"].append(res["Trocas"])
            formatted_metrics[name]["Memoria"].append(res["Memoria"])
            formatted_metrics[name]["Temp. Tab."].append(res["Setup_ms"])
            # Tempo puro de uso
            formatted_metrics[name]["Tempo"].append(res["Total_ms"] - res["Setup_ms"])

    # Chama suas funções de plot e print existentes
    # (Ajuste suas funções print_tabela para receber esses dados)
    print_tabelas_finais(n_list, data) 
    plot_results(n_list, formatted_metrics)
    plot_comparativo_recursos(n_list, formatted_metrics)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "report":
            generate_reports()
        else:
            try:
                n_val = int(sys.argv[1])
                run_benchmark(n_val)
            except ValueError:
                print("Uso: python main.py [n] OU python main.py report")
    else:
        print("Informe um valor de n ou 'report'.")

