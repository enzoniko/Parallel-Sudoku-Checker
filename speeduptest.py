from random import randint
from paralela import leitura_arquivo, main
from sequencial import main_sequencial
from time import perf_counter
import matplotlib.pyplot as plt
if __name__ == '__main__':
    dict_solucoes = leitura_arquivo("input-sample.txt")
    num_solucoes = len(dict_solucoes)
    # Executar o programa sequencial
    tempo_inicio = perf_counter()
    main_sequencial(dict_solucoes)
    tempo_fim = perf_counter()
    tempo_sequencial = tempo_fim - tempo_inicio
    conjunto_processos = [1, 2, 4, 8, 12]
    # Fazer as combinações (processos, threads) em que os processos vão de 1 até 12 e as threads de 1 até 9
    combinacoes_processos_e_threads = [(processos, threads) for processos in conjunto_processos for threads in range(1, 10)]

    # Para cada combinação, executar o programa e salvar o tempo de execução
    tempos_execucao = []
    for combinacao in combinacoes_processos_e_threads:
        processos, threads = combinacao
        tempo_inicio = perf_counter()
        main(processos, threads, dict_solucoes)
        tempo_fim = perf_counter()
        tempos_execucao.append((processos, threads, tempo_fim - tempo_inicio))

    # Plotar o gráfico do tempo de execução em função do número de threads
    # Eixo y vai ser o tempo de execução
    # Eixo x vai ser o número de threads
    # Cada linha vai ser um número de processos diferente
    # Cada ponto vai ser uma combinação de processos e threads

    # Calcular os tempos de execução para cada número de processos
    tempos_execucao_por_processos = []
    for processos in conjunto_processos:
        tempos_execucao_por_processos.append([tempos_execucao[i][2] for i in range(len(tempos_execucao)) if tempos_execucao[i][0] == processos])
    
    # Plotar o gráfico
    thickness = 1
    for conjunto in range(len(conjunto_processos)):
        plt.plot([tempos_execucao_por_processos[conjunto][i] for i in range(len(tempos_execucao_por_processos[conjunto]))], linewidth = thickness, label=f"{conjunto_processos[conjunto]} processos")
        thickness += 0.15
    # Plotar a linha do tempo sequencial
    plt.plot([tempo_sequencial for i in range(len(tempos_execucao_por_processos[0]))], linewidth = thickness, label="Sequencial")
    plt.title(f"Tempo de execução em função do número de threads para {num_solucoes} soluções")
    plt.ylabel("Tempo de execução (s)")
    plt.xlabel("Número de threads")
    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(f"Graphs/Time{num_solucoes}sol.png", dpi=200)
    #plt.show()

    # Limpar o gráfico
    plt.clf()

    # Calcular os speedups de cada combinação
    speedups = []
    for i in range(len(tempos_execucao)):
        processos, threads, tempo_execucao = tempos_execucao[i]
        speedups.append((processos, threads, tempo_sequencial / tempo_execucao))
    
    # Calcular os speedups para cada número de processos
    speedups_por_processos = []
    for processos in conjunto_processos:
        speedups_por_processos.append([speedups[i][2] for i in range(len(speedups)) if speedups[i][0] == processos])
    
    # Plotar o gráfico
    thickness = 1
    for conjunto in range(len(conjunto_processos)):
        plt.plot([speedups_por_processos[conjunto][i] for i in range(len(speedups_por_processos[conjunto]))], linewidth = thickness, label=f"{conjunto_processos[conjunto]} processos")
        thickness += 0.15
    
    # Plotar a linha do speedup ideal
    plt.plot([i for i in range(1, 10, 1)], linewidth = thickness, label="Speedup ideal")
    plt.title(f"Speedup em função do número de threads para {num_solucoes} soluções")
    plt.ylabel("Speedup")
    plt.xlabel("Número de threads")
    plt.legend()
    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig(f"Graphs/Speedup{num_solucoes}sol.png", dpi=200)
    plt.show()
