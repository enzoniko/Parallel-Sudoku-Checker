import time
import os
def black_box_leitura_arquivo(nome_arquivo):

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
    #print("Leitura do arquivo concluída. Soluções encontradas:")
    #pprint.pprint(dict_solucoes)
    return dict_solucoes


# Primeira alternativa de implementação:
def f1(lista):

    # Transforma a lista em um set para eliminar os elementos repetidos
    lista = set(lista)

    # Se o tamanho do set for diferente de 9, então a lista não é válida
    if len(lista) != 9:
        return False
    return True


# Segunda alternativa de implementação:
def f2(lista):

    # Transforma a lista em um set para eliminar os elementos repetidos
    lista = set(lista)

    # Se a soma dos elementos do set for igual a 45, então a lista é válida
    return sum(lista) == 45 


# Terceira alternativa de implementação:
def f3(lista):
    aim = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # Ordena a lista
    lista.sort()

    # Se a lista ordenada for igual a lista objetivo, então a lista é válida
    return lista == aim


# Quarta alternativa de implementação:
def f4(lista):
    aux = []

    for i in lista:
        if i not in aux:
            aux.append(i)
        else:
            return False
        
    return True


dict_solucoes = black_box_leitura_arquivo('input-sample.txt')

def testf1(n):
    y = []
    for i in n:
        start = time.perf_counter()
        for _ in range(i):
            for solucao in dict_solucoes.values():
                for linha in solucao:
                    f1(linha)
        end = time.perf_counter()
        y.append(end - start)
    return y
def testf2(n):
    y = []
    for i in n:
        start = time.perf_counter()
        for _ in range(i):
            for solucao in dict_solucoes.values():
                for linha in solucao:
                    f2(linha)
        end = time.perf_counter()
        y.append(end - start)
    return y

def testf3(n):
    y = []
    for i in n:
        start = time.perf_counter()
        for _ in range(i):
            for solucao in dict_solucoes.values():
                for linha in solucao:
                    f3(linha)
        end = time.perf_counter()
        y.append(end - start)
    return y

def testf4(n):
    y = []
    for i in n:
        start = time.perf_counter()
        for _ in range(i):
            for solucao in dict_solucoes.values():
                for linha in solucao:
                    f4(linha)
        end = time.perf_counter()
        y.append(end - start)
    return y

# Plot the results in a graph for comparison
import matplotlib.pyplot as plt
import numpy as np

# For each function plot a line from n = 1 to n = 1000
n = np.arange(1, 100)

# Plot the results
plt.plot(n, testf1(n), label='f1')
plt.plot(n, testf2(n), label='f2')
plt.plot(n, testf3(n), label='f3')
plt.plot(n, testf4(n), label='f4')

# Add a legend
plt.legend()

# Plot
plt.xlabel('n')
plt.ylabel('time')
plt.show()


