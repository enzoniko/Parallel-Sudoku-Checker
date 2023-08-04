# Importar bibliotecas necessárias
import os
import sys
import pprint
from time import perf_counter, sleep
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

def black_box_parametros_entrada():
    # Recebe os parâmetros de entrada do programa, e os valida.

    # Logica para limitar as threads 
    # numero de solucoesxQTD_COISAS / numero de processos
    nome_arquivo = str(sys.argv[1])
    # processos = int(sys.argv[2])
    # threads = int(sys.argv[3])
    max_processos = cpu_count()

    # Ler arquivo de entrada e criar dicionário de soluções usando a seguinte função:
    dict_solucoes = black_box_leitura_arquivo(nome_arquivo)
    solucoes = len(dict_solucoes)

    if len(sys.argv) != 2:

        print("Entrata inválida digita: nome_do_programa nome_doarquivo" )
        exit()

    # os retornando logo em seguida ou encerrando o programa caso algum parâmetro seja inválido (explicar por que foi inválido).
    return dict_solucoes

def black_box_leitura_arquivo(nome_arquivo):

    # Obtem o caminho completo para o arquivo
    caminho_arquivo = os.path.join(os.path.dirname(__file__), nome_arquivo)
    
    # Abre o arquivo para leitura
    with open(caminho_arquivo, 'r') as arquivo:
        # Lê todo o conteúdo do arquivo
        conteudo = arquivo.read()
    
    # Divide o conteúdo em partes separadas pelo separador '\n\n'
    partes = conteudo.strip().split('\n\n')
    
    # Cria um dicionário para armazenar as soluções
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

def avaliar_solucoes(dict_solucoes):
    aim = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    for quebra_cabeca in dict_solucoes:
        solucao = dict_solucoes[quebra_cabeca]
        dict_erros = {'L': [], 'C': [], 'R': []}
        
        # Verifica erros nas linhas
        for i in range(len(solucao)):
            linha = solucao[i][:]
            linha.sort()
            if linha != aim:
                dict_erros['L'].append(i + 1)
        # Verifica erros nas colunas
        for j in range(9):
            coluna = [solucao[row][j] for row in range(9)]
            coluna.sort()
            if coluna != aim:
                dict_erros['C'].append(j + 1)
        # Verifica erros nas regiões
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                regiao = [
                    solucao[row][col] for row in range(i, i + 3) for col in range(j, j + 3)
                ]
                regiao.sort()
                if regiao != aim:
                    dict_erros['R'].append((i // 3 + 1) * 3 + j // 3 + 1)
        if dict_erros:
            erros = []
            for tipo, locais in dict_erros.items():
                for local in locais:
                    erros.append(f"{tipo}{local}")

            print(f"Quebra_cabeca {quebra_cabeca}:{len(erros)} erros encontrados ({', '.join(erros)})")
        else:
            #pass
            print(f"Quebra_cabeca {quebra_cabeca}: 0 erros encontrados")

def main_sequencial(dict_solucoes):

    avaliar_solucoes(dict_solucoes)
  
if __name__ == '__main__':
    # Receber os parâmetros de entrada do programa, e os validar usando a seguinte função:
    dict_solucoes = black_box_parametros_entrada()
    main_sequencial(dict_solucoes)