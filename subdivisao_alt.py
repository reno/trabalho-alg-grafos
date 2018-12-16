'''
GCC2018 Algoritmos em Grafos - Trabalho final
subdivisao_alt.py

Alunos: 
Heuller Silva, João Pedro Andolpho, Luiz Carlos Conde,
Gabriel Amorim, Renan Modenese e Victor Landin
'''

import networkx as nx
from networkx import MultiGraph
from math import sqrt
from statistics import mean, stdev
from pprint import pprint
from operator import itemgetter
from collections import OrderedDict

def calcula_distancia(G, u, v, x='x', y='y'):
    """Calcula a distância euclideana entre os vértices u,v de G."""
    return sqrt((G.nodes[u][x] - G.nodes[v][x])**2 +
                (G.nodes[u][y] - G.nodes[v][y])**2)


def demanda_vertice(G, v): 
    """Calcula a demanda de um cliente, considerando volume e valor do pedido"""
    return G.nodes[v].get('volume') * G.nodes[v].get('valor')


def obter_vertice_alt(G, k, matrizes_ordenadas, nao_alocados, r):
    """Retorna o vértice não alocado mais próximo do centro da região R"""
    matriz_distancias = matrizes_ordenadas[r]
    for u in range(G.order() - k):
        v = matriz_distancias[u][0]
        if v in nao_alocados:
            return v


def subdivisao_alt(G, k):
    """Heurística para distribuição dos vértices em regiões, priorizando
    as regiões com menor demanda, modificada para minimizar a ocorrência de 
    vértices isolados.

    args:
        G: grafo não direcionado onde os k primeiros vértices são centros
        k: número de regiões desejadas

    returns:
        regioes: lista de conjuntos contendo os vértices de cada região
    """
    
    # inicializa as regiões com seus centros
    regioes = [{centro} for centro in range(k)]
    
    # calcula distancia dos vértices para cada um dos centros
    matriz_distancias = {}  
    for v in range(k, G.order()):
        distancias = [calcula_distancia(G, centro, v) for centro in range(k)]
        matriz_distancias[v] = distancias

    # ordena matriz_distancias para cada região, salvando resultados numa lista
    matrizes_ordenadas = [sorted(matriz_distancias.items(), 
                          key=lambda v: v[1][r]) for r in range(k)]

    # inicializa variáveis 
    nao_alocados = {v for v in G.nodes() if v >= k}
    demandas = [0 for r in range(k)]
    # os n últimos vértices são distribuídos separadamente
    n = len(nao_alocados) / 10  

    while len(nao_alocados) > n:
        # encontra região com menor demanda
        r = demandas.index(min(demandas))
        # obtem vértice mais próximo do centro de r
        v = obter_vertice_alt(G, k, matrizes_ordenadas, nao_alocados, r)
        # soma demanda do vértice a demanda da região
        demandas[r] += demanda_vertice(G, v)
        # aloca vertice na regiao r e remove dos não alocados
        regioes[r].add(v)
        G.nodes()[v]['regiao'] = r
        nao_alocados -= {v}

    # distribui os vértices restantes considerando apenas o centro mais próximo
    while nao_alocados:
        for v in list(nao_alocados):
            r = matriz_distancias[v].index(min(matriz_distancias[v]))
            demandas[r] += demanda_vertice(G, v)
            regioes[r].add(v) 
            G.nodes()[v]['regiao'] = r
            nao_alocados -= {v}

    # Calcula a demanda média e os desvios        
    demanda_ideal = sum(demandas) / k
    desvios = [stdev([demandas[r], demanda_ideal]) for r in range(k)]

    # Imprime os resultados obtidos
    print('Demandas: {}'.format(demandas))   
    print('Demanda ideal: {}'.format(demanda_ideal))
    print('Desvios: {}'.format(desvios))
    print('Soma dos desvios: {}'.format(sum(desvios)))
    
    return regioes
 
    