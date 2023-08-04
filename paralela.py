# Importar bibliotecas necessárias
import os
import sys
from multiprocessing import Process, cpu_count
import threading 
from queue import Queue

# Configurações da execução do programa:
# Tamanho do tabuleiro
N = 9
PRINT = True

# Constantes que serão usadas no programa:

# Tamanho do quadrante
Q = int(N**0.5)
# Quantidade de coisas (linhas + colunas + regiões) em um tabuleiro
QTD_COISAS = 3*N
# Balde de coisas
BALDE = [("linhas", i) for i in range(N)] + [("colunas", i) for i in range(N)] + [("regioes", i) for i in range(N)]
# Vetor ordenado de 1 a N que será usado para verificar se uma solução é válida
AIM = [i for i in range(1, N+1)]

# Configure PRINT == False para não ter prints no programa (para não atrapalhar a medição de tempo)
if not PRINT:
    sys.stdout = open(os.devnull, 'w')

def parametros_entrada():
    # Recebe os parâmetros de entrada do programa, e os valida,

    # Valida a linha de comando
    entradas = len(sys.argv)

    if entradas != 4:
        print("Você precisa informar (nessa ordem) o nome do arquivo que deseja avaliar, a quantidade de processos e a quantidade de threads em cada processo.")
        exit()

    # Logica para limitar as threads 
    # numero de solucoesx27 / numero de processos
    nome_arquivo = str(sys.argv[1])
    processos = int(sys.argv[2])
    threads = int(sys.argv[3])
    max_processos =  cpu_count()

    # Ler arquivo de entrada e criar dicionário de soluções usando a seguinte função:
    dict_solucoes = leitura_arquivo(nome_arquivo)
    solucoes = len(dict_solucoes)

    # Valida a quantidade de processos 
    if processos > max_processos or processos < 1:

        print("Você não tem essa quantidade de cores no seu computador ou o número de processos é invalido, escolha uma quantidade de 1 até", max_processos)
        exit()

    #valida a quantidade de threads 
    elif threads > round((solucoes*QTD_COISAS/processos)+0.5) or threads < 1:
        print("O número de threads não está disponivel, para a entrada de", solucoes , "soluções e", processos , "processos, escolha uma quantidade de 1 até", round((solucoes*QTD_COISAS/processos)+0.5), "threads.")
        exit()

    # os retornando logo em seguida ou encerrando o programa caso algum parâmetro seja inválido (explicar por que foi inválido).
    return processos, threads, dict_solucoes

def leitura_arquivo(nome_arquivo):

    # Obtem o caminho completo para o arquivo
    caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    
    # Abre o arquivo para leitura
    with open(caminho_arquivo, 'r') as arquivo:
        # Lê todo o conteúdo do arquivo
        conteudo = arquivo.read()
    
    # Divide o conteúdo em partes separadas pelo separador '\n\n'
    partes = conteudo.strip().split('\n\n')
    
    # Crie um dicionário para armazenar as soluções
    dict_solucoes = {}

    # Percorre as partes do conteúdo
    for i, parte in enumerate(partes):
        # Divide cada parte em linhas separadas pelo separador '\n'
        linhas = parte.strip().split('\n')
        
        # Crie uma matriz vazia para armazenar os valores
        matriz = []
        
        # Percorre as linhas
        for linha in linhas:
            # Converte a linha em uma string separada por espaço
            linha = ' '.join(str(valor) for valor in linha)
            
            # Divide a linha em valores individuais
            valores = linha.strip().split()
            
            # Converte os valores em inteiros e adiciona à matriz
            matriz.append([int(valor) for valor in valores])
        
        # Armazena a matriz no dicionário de soluções
        dict_solucoes[i] = matriz
    
    # Retorna o dicionário de soluções
    return dict_solucoes

def divisao_trabalho(processo, num_solucoes, processos, threads):
    
    # Pegar o número de soluções que cada processo vai avaliar:
    num_solucoes_por_processo = num_solucoes // processos

    # Pegar o resto de soluções que cada processo vai avaliar:
    resto_solucoes_por_processo = num_solucoes % processos

    # Cria a lista da parcela do processo
    parcela_processo = []

    # Determinar quais soluções o processo vai avaliar.
    # Isso é um dicionário onde as chaves são as soluções e os valores uma lista contendo as linhas, colunas e regiões que o processo vai avaliar.
    solucoes_para_avaliar = {i:BALDE[:] for i in range(num_solucoes - resto_solucoes_por_processo) if i//num_solucoes_por_processo == processo - 1}
    
    # Índices das soluções que faltaram
    solucoes_que_faltaram = [i for i in range(num_solucoes)][-resto_solucoes_por_processo:] if resto_solucoes_por_processo != 0 else []

    # Calcula quantas coisas cada processo vai avaliar dessas soluções que faltaram   
    coisas_por_processo = (len(solucoes_que_faltaram)*QTD_COISAS)//processos

    # Calcula o resto de coisas que cada processo vai avaliar dessas soluções que faltaram
    resto_coisas_por_processo = (len(solucoes_que_faltaram)*QTD_COISAS)%processos

    # Imagine uma lista com todas as coisas de todas as soluções que faltaram, em ordem, podemos dividir essa lista em partes para cada processo.
    # Pegamos o índice do primeiro elemento da parte dessa lista que o processo vai avaliar e o chamamos de start
    start = (processo - 1)*coisas_por_processo + (processo - (1 + processos - resto_coisas_por_processo)) if processo >= 1 + processos - resto_coisas_por_processo else (processo - 1)*coisas_por_processo
    
    # Percorremos essa parte imaginária, indo índice por índice, do start até o start + coisas_por_processo
    for indice in range(start, (start + coisas_por_processo + 1) if processo >= 1 + processos - resto_coisas_por_processo else (start + coisas_por_processo)):

        # Determina qual a solução (das soluções que faltaram) que esse índice pertence
        solucao = solucoes_que_faltaram[indice//QTD_COISAS]

        # Se a chave dessa solução ainda não está nas solucoes_para_avaliar do processo
        if not solucao in solucoes_para_avaliar:

            # Adiciona a chave e cria uma lista vazia para essa solução
            solucoes_para_avaliar[solucao] = []

        # Adiciona na lista dessa solução as coisas a serem avaliadas
        solucoes_para_avaliar[solucao].append(BALDE[indice%QTD_COISAS])


    # Guarda o total de coisas a serem avaliadas pelo processo
    total_de_coisas = sum([len(solucoes_para_avaliar[i]) for i in solucoes_para_avaliar])

    # Para cada thread
    for thread in range(threads):

        # Cria um dicionário
        parcela_processo.append({})

        # Pega o número de coisas que cada thread vai avaliar
        coisas_por_thread = total_de_coisas // threads

        # Pega o resto do número de coisas que cada thread vai avaliar
        resto_coisas_por_thread = total_de_coisas % threads

        # Adiciona cada solução a ser avaliada como uma chave do dicionário onde os valores vão ser dicionários contendo as coisas a serem avaliadas dessa solução por esse processo
        for solucao in solucoes_para_avaliar:
            parcela_processo[thread][solucao] = {
                "linhas": [],
                "colunas": [],
                "regioes": []
            }

        # Caso forem as resto_coisas_por_thread últimas threads, elas vão avaliar uma coisa a mais
        if thread >= threads - resto_coisas_por_thread:
            coisas_por_thread+=1

        # A thread vai avaliar coisas_por_thread coisas, então para cada coisa
        for _ in range(coisas_por_thread):
            
            # Percorremos solucoes_para_avaliar em ordem, portanto pegamos a primeira solução
            solucao = list(solucoes_para_avaliar.keys())[0]

            # E retiramos uma coisa da lista dessa solução
            coisa = solucoes_para_avaliar[solucao].pop()

            # Adicionando essa coisa no lugar correto da parcela_processo
            parcela_processo[thread][solucao][coisa[0]].append(coisa[1])

            # Caso acabem as coisas a serem avaliadas dessa solução
            if solucoes_para_avaliar[solucao] == []:
                
                # Remove essa solução das soluções a avaliar
                solucoes_para_avaliar.pop(solucao)

    # Retorna a parcela do processo
    return parcela_processo 
    
def transforma_indices_em_estruturas(dict_solucoes, parcela_do_processo):
    # Função que recebe a parcela de um processo e transforma os índices das linhas, colunas e regiões em estruturas de fato, a fim de avaliarmos se elas estão válidas
  
    # Para cada thread do processo
    for thread in parcela_do_processo:

        # Para cada solução
        for solucao in thread:

            # Transforma os índices das linhas em um dicionário com as linhas como chaves e os valores sendo as linhas da matriz
            thread[solucao]["linhas"] = {
                thread[solucao]["linhas"][i]: # A chave do dicionário vai ser o índice da linha
                dict_solucoes[solucao][thread[solucao]["linhas"][i]] for i in range(len(thread[solucao]["linhas"])) # E o valor vai ser um vetor com os valores da linha
            }
            
            # Transforma os índices das colunas em um dicionário com as colunas como chaves e os valores sendo as colunas da matriz em forma de vetor
            thread[solucao]["colunas"] = {
                thread[solucao]["colunas"][j]: # A chave do dicionário vai ser o índice da coluna
                [dict_solucoes[solucao][i][thread[solucao]["colunas"][j]] for i in range(N)] # E o valor vai ser um vetor com os valores da coluna
                for j in range(len(thread[solucao]["colunas"])) # Para cada uma das colunas dessa solução que essa thread vai avaliar.
            }
            
            # Transforma os índices das regiões em um dicionário com as regiões como chaves e os valores sendo as regiões da matriz em forma de vetor
            thread[solucao]["regioes"] = {
                thread[solucao]["regioes"][x]: # A chave do dicionário vai ser o índice da região
                [ # E o valor vai ser um vetor com os valores da região
                    dict_solucoes[solucao][i][j] 
                    for i in range((thread[solucao]["regioes"][x]//Q)*Q,  (thread[solucao]["regioes"][x]//Q)*Q + Q)
                    for j in range((thread[solucao]["regioes"][x]%Q)*Q, ((thread[solucao]["regioes"][x]%Q)+1)*Q) 
                ] # Para cada uma das regiões dessa solução que essa thread vai avaliar.
                for x in range(len(thread[solucao]["regioes"]))
            }

    return parcela_do_processo

# Função que avalia se uma solução é válida, escolhida com base numa análise do tempo de execução dos arquivos complexitytest.py e complexitytest2.py
def avaliar_solucao(lista):

    # Ordena a lista
    lista.sort()
    # Se a lista ordenada for igual a lista objetivo, então a lista é válida
    return lista == AIM

def funcao_thread(num_thread, parcela_da_thread, resultado_queue):
    erros = {i:{num_thread: []} for i in parcela_da_thread}
     
    for solucao in parcela_da_thread: 
        errosThreadLinhas = []
        errosThreadColunas = []
        errosThreadRegioes = []
        for chave in parcela_da_thread[solucao]: 
            for indice in parcela_da_thread[solucao][chave]:
                if not avaliar_solucao(parcela_da_thread[solucao][chave][indice]):
                    if chave=='linhas':
                        errosThreadLinhas.append(f"L{indice + 1}")
                    elif chave=='colunas':
                        errosThreadColunas.append(f"C{indice + 1}")
                    elif chave=='regioes':
                        errosThreadRegioes.append(f"R{indice + 1}")
        
        errosThreadLinhas.sort()
        errosThreadColunas.sort()
        errosThreadRegioes.sort()
        erros[solucao][num_thread] = [errosThreadLinhas, errosThreadColunas, errosThreadRegioes]

    resultado_queue.put(erros)

def funcao_processo(num_processo, dict_solucoes, processos, threads):

    # Faz o processo calcular qual é sua parcela (por fazer isso paralelamente melhora a performance)
    parcela_do_processo = divisao_trabalho(num_processo, len(dict_solucoes), processos, threads)

    # Para cada solução que o processo for avaliar printa que o processo num_processo está resolvendo o quebra-cabeças num_solucao.
    for num_solucao in parcela_do_processo[0]:  
        print(f"Processo {num_processo}: resolvendo o quebra-cabeças {num_solucao + 1}")
    
    # Para enviar as parcelas das threads para as threads precisamos converter os índices das linhas, colunas e regiões 
    # para as estruturas de fato, a fim de avaliarmos se elas estão válidas.

    # Portanto é necessário uma função que receba os índices das linhas, colunas e regiões e devolva as estruturas de fato.
    # Usamos a seguinte função para isso, que devolve a parcela do processo transformada:
    parcela_do_processo_transformada = transforma_indices_em_estruturas(dict_solucoes, parcela_do_processo)

    # Lista de threads
    threads_lista = []

    # Cria uma fila de resultados
    resultado_queue = Queue()
   
    # Para cada thread do processo
    for thread in range(len(parcela_do_processo_transformada)):
        
        # Cria a thread passando a função que ela vai executar, os argumentos da função e a fila de resultados
        t = threading.Thread(target = funcao_thread, args=(thread, parcela_do_processo_transformada[thread], resultado_queue))

        # Adiciona a thread na lista de threads
        threads_lista.append(t)
        
        # Inicia a thread 
        t.start()
        
    # Aguarda a conclusão das threads
    for t in threads_lista:
        t.join()
    
    # Processa os resultados, juntando-os para cada solução que o processo avaliou
    resultados = {num_solucao: {} for num_solucao in parcela_do_processo[0]}
    while not resultado_queue.empty():
        resultado = resultado_queue.get()
        for num_solucao in resultado:
            resultados[num_solucao].update(resultado[num_solucao])

    # Para cada solução
    for solucao in resultados:

        # Contador do total de erros encontrados na solução pelo processo
        total_de_erros_da_solucao = 0

        # String que vai conter a posição dos erros encontrados por cada thread, no formato requisitado
        erros_da_solucao = ''

        # Para cada thread
        for thread in resultados[solucao]:

            # Lista que vai guardar a posição dos erros encontrados pela thread
            erros_da_thread = []

            # Para cada conjunto de erros encontrados pela thread nessa solução (erros em linhas, colunas e regiões)
            for erros in resultados[solucao][thread]:

                # Extende nos erros da thread
                erros_da_thread.extend(erros)

            # Incrementa o total de erros
            total_de_erros_da_solucao += len(erros_da_thread)

            # Se essa thread encontrou algum erro nessa solução
            if len(erros_da_thread) > 0:

                # Escrevemos os erros na string
                erros_da_solucao += f"T{thread + 1}: {', '.join(erros_da_thread)}; "
        # Tira os últimos dois caractéres (";" e " ")
        erros_da_solucao = erros_da_solucao[:-2]

        # Se não foram encontrados erros nessa solução, printa isso.
        if total_de_erros_da_solucao == 0:
            print(f"Processo {num_processo}: {total_de_erros_da_solucao} erros encontrados no quebra-cabeças {solucao + 1}")
        
        # Se foram encontrados erros nessa solução os printa.
        else:
            print(f"Processo {num_processo}: {total_de_erros_da_solucao} erros encontrados no quebra-cabeças {solucao + 1} ({erros_da_solucao})")
            
def main(processos, threads, dict_solucoes):

    # Cria uma lista para armazenar os processos 
    processos_lista = []
  
    # Cria cada processo e faz ele decidir qual sua parcela.
    for processo in range(1, processos +1):

        # Cria um processo e o adiciona à lista de processos 
        p = Process(target=funcao_processo, args=(processo, dict_solucoes, processos, threads))
        processos_lista.append(p)

        # Inicia o processo
        p.start()

    # Aguarda a conclusão dos processos 
    for p in processos_lista:
        p.join()

if __name__ == '__main__':

    # Recebe os parâmetros de entrada do programa, e os valida usando a seguinte função:
    processos, threads, dict_solucoes = parametros_entrada()

    # Chama a função main passando todos os parâmetros. (separamos assim para facilitar os testes de tempo)
    main(processos, threads, dict_solucoes)