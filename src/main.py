import matplotlib.pyplot as plt
import math
import time
import json
import tracemalloc
import gc
import json
import sys
import os

from p import algoritmo_p
from t import algoritm_t_online, algoritm_t_offline
from tracker import AlgorithmTracker

N = 'n'
N_FAT = 'n!'
SUF_TAB = '- Tab.'
COMP = 'Comparações'
COMP_TAB = COMP + ' ' + SUF_TAB
ATTR_LOCAL = 'Atrib. (Local)'
ATTR_LOCAL_TAB = ATTR_LOCAL + ' ' + SUF_TAB
ATTR_VECTOR = 'Atrib. (Vetor)'
ATTR_VECTOR_TAB = ATTR_VECTOR + ' ' + SUF_TAB
EXCHANGES = 'Trocas'
EXCHANGES_TAB = EXCHANGES + ' ' + SUF_TAB
MEMORY = 'Memória (kb)'    
TIME_SETUP = 'Setup (ms)'
TIME_OPERATION = 'Operation (ms)'
 
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

algoritms = {"P": algoritmo_p, "T online": algoritm_t_online, "T offline": algoritm_t_offline}

def print_tabelas_finais(n_list, all_data):
    alg_names = all_data[n_list[0]].keys()

    for name in alg_names:
        print(f"\n\n\t\t*** Relatório Consolidado: {name} ***")
        header_line = "-" * 165
        print(header_line)
        
        # Cabeçalho com separação clara de métricas
        print(f"{N:<4} | {N_FAT:<10} | {COMP:<12} | {ATTR_LOCAL:<18} | {ATTR_VECTOR:<18} | {EXCHANGES:<8} | {MEMORY:<15} | {TIME_SETUP:<15} | {TIME_OPERATION:<15}")
        print(header_line)

        for n in n_list:
            if name in all_data[n]:
                res = all_data[n][name]
                
                setup_time = res.get(TIME_SETUP, 0.0)
                total_time = res.get(TIME_OPERATION, 0.0)
                op_time = total_time - setup_time
                
                print(f"{n:<4} | "
                      f"{res[N_FAT]:<10} | "
                      f"{res[COMP]:<12} | "
                      f"{res[ATTR_LOCAL]:<18} | "
                      f"{res[ATTR_VECTOR]:<18} | "
                      f"{res[EXCHANGES]:<8} | "
                      f"{res[MEMORY]:<15.2f} | "
                      f"{setup_time:<15.4f} | "
                      f"{op_time:<15.4f}")
        
        print(header_line)
        
def plot_results(n_list, metrics):
    
    for alg, data in metrics.items():
        plt.figure(figsize=(10, 6))
        
        plt.plot(n_list, data[COMP], label=COMP, marker='o')
        if data[COMP_TAB][0] > 0:
            plt.plot(n_list, data[COMP_TAB], label=COMP_TAB, marker='o')
        
        plt.plot(n_list, data[ATTR_LOCAL], label=ATTR_LOCAL, marker='s')
        if data[ATTR_LOCAL_TAB][0] > 0:
            plt.plot(n_list, data[ATTR_LOCAL_TAB], label=ATTR_LOCAL_TAB, marker='s')
        
        plt.plot(n_list, data[ATTR_VECTOR], label=ATTR_VECTOR, marker='s')
        if data[ATTR_VECTOR_TAB][0] > 0:
            plt.plot(n_list, data[ATTR_VECTOR_TAB], label=ATTR_VECTOR_TAB, marker='s')

        plt.plot(n_list, data[EXCHANGES], label=EXCHANGES, marker='x')
        if data[EXCHANGES_TAB][0] > 0:
            plt.plot(n_list, data[EXCHANGES_TAB], label=EXCHANGES_TAB, marker='>')

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
        d = data[TIME_OPERATION]
        #if "offline" in alg_name.lower():
        #    d = data[TIME_SETUP]
            
        ax1.plot(n_list, d, label=f"{alg_name}", marker='o')
        ax2.plot(n_list, data[MEMORY], label=alg_name, marker='s')

    # Configurações do gráfico de Tempo
    ax1.set_yscale('log')
    ax1.set_xlabel('n (Tamanho da entrada)')
    ax1.set_ylabel('Tempo (ms)')
    ax1.set_title('Comparativo de Tempo')
    ax1.legend()
    ax1.grid(True, which="both", ls="-", alpha=0.5)

    # Configurações do gráfico de Memória
    ax2.set_yscale('log')
    ax2.set_xlabel('n (Tamanho da entrada)')
    ax2.set_ylabel('Pico de Memória (KB)')
    ax2.set_title('Consumo de Memória')
    ax2.legend()
    ax2.grid(True, which="both", ls="-", alpha=0.5)

    plt.tight_layout()
    plt.savefig('results/recursos.png')
    #plt.show()

def export_to_web_report(all_data, filename="results"):
    import json
    # Estrutura compatível com o index.html anterior
    web_data = {
        "algorithm": "Comparativo P vs T",
        "rows": []
    }
    
    # Ordena os n para garantir que o gráfico fique correto
    for n in sorted(all_data.keys()):
        res = all_data[n]
        web_data["rows"].append({
            "n": n,
            "p": {
                "total": {
                    "time_ms": res["P"]["Operation (ms)"],
                    "comparisons": res["P"]["Comparações"],
                    "local_assignments": res["P"]["Atrib. (Local)"],
                    "vector_assignments": res["P"]["Atrib. (Vetor)"]
                }
            },
            "t_online": {
                "total": {
                    "time_ms": res["T online"]["Operation (ms)"],
                    "comparisons": res["T online"]["Comparações"],
                    "local_assignments": res["T online"]["Atrib. (Local)"],
                    "vector_assignments": res["T online"]["Atrib. (Vetor)"]
                }
            }
        })

    # 2. Salva o arquivo .json
    json_path = f"{filename}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(web_data, f, indent=2)
    print(f"Arquivo {json_path} gerado com sucesso.")

    # 3. Salva o arquivo .js (Payload para o navegador)
    js_path = f"{filename}.js"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(f"window.__ALGO_T_RESULTS__ = {json.dumps(web_data, indent=2)};")
    print(f"Arquivo {js_path} gerado com sucesso.")

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
        
        results_for_n[name] = {
            N_FAT: math.factorial(n),
            COMP: tracker.comparisons,
            COMP_TAB: tracker.tab_comparisons,
            ATTR_LOCAL: tracker.att_local,
            ATTR_LOCAL_TAB: tracker.tab_att_local,
            ATTR_VECTOR: tracker.att_vector,
            ATTR_VECTOR_TAB: tracker.tab_att_vector,
            EXCHANGES: tracker.exchanges,
            EXCHANGES_TAB: tracker.tab_exchanges,
            MEMORY: peak / 1024,
            TIME_SETUP: tracker.duration_build_table_ms(),
            TIME_OPERATION: tracker.duration_ms()
        }
    
    save_n_results(n, results_for_n)
    print(f"Resultados para n={n} salvos com sucesso.")

def generate_reports():
    data = load_all_results()
    if not data:
        print("Nenhum dado encontrado em /results.")
        return

    n_list = sorted(data.keys())
        
    formatted_metrics = {}
    for name in algoritms.keys():
        formatted_metrics[name] = {
            COMP: [], COMP_TAB: [], 
            ATTR_LOCAL: [], ATTR_LOCAL_TAB: [], ATTR_VECTOR: [], ATTR_VECTOR_TAB: [],
            EXCHANGES: [], EXCHANGES_TAB: [], MEMORY: [], TIME_SETUP: [], TIME_OPERATION: []
        }

    for n in n_list:
        for name in algoritms.keys():
            res = data[n][name]
            formatted_metrics[name][COMP].append(res[COMP])
            formatted_metrics[name][COMP_TAB].append(res[COMP_TAB])
            formatted_metrics[name][ATTR_LOCAL].append(res[ATTR_LOCAL])
            formatted_metrics[name][ATTR_LOCAL_TAB].append(res[ATTR_LOCAL_TAB])
            formatted_metrics[name][ATTR_VECTOR].append(res[ATTR_VECTOR])
            formatted_metrics[name][ATTR_VECTOR_TAB].append(res[ATTR_VECTOR_TAB])
            formatted_metrics[name][EXCHANGES].append(res[EXCHANGES])
            formatted_metrics[name][EXCHANGES_TAB].append(res[EXCHANGES_TAB])
            formatted_metrics[name][MEMORY].append(res[MEMORY])
            formatted_metrics[name][TIME_SETUP].append(res[TIME_SETUP])
            formatted_metrics[name][TIME_OPERATION].append(res[TIME_OPERATION])

    print_tabelas_finais(n_list, data) 
    plot_results(n_list, formatted_metrics)
    plot_comparativo_recursos(n_list, formatted_metrics)
    export_to_web_report(data)

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

