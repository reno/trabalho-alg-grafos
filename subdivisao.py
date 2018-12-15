'''
GCC2018 Algoritmos em Grafos - Trabalho final
kcluster.py

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
    return G.nodes[v].get('volume') * G.nodes[v].get('valor')


def obter_vertice(G, nao_alocados, matrizes_ordenadas, r):
    proximo = next(iter(nao_alocados))
    for v in nao_alocados:
        #print('{} {} {} {}'.format(v, calcula_distancia(G, r, v), proximo, calcula_distancia(G, r, proximo)))
        if (calcula_distancia(G, r, v) < calcula_distancia(G, r, proximo)):
            proximo = v
    #print ("vertice obtido: ", proximo)
    return proximo


def subdivisao(G, k):
    """ """
    lista_regioes = [{centro} for centro in range(k)]
    # calcula distancia dos vertices para cada um dos centros
    matriz_distancias = {}  # {regiao:[distancias]}
    for v in range(k, G.order()):
        distancias = [calcula_distancia(G, centro, v) for centro in range(k)]
        matriz_distancias[v] = distancias
    # ordena matriz_distancias para cada centro, salva resultados numa lista
    matrizes_ordenadas = [sorted(matriz_distancias.items(), 
                          key=lambda v: v[1][r]) for r in range(k)]


    # inicializa variáveis 
    nao_alocados = {v for v in G.nodes() if v >= k}
    demandas = [0 for r in range(k)]

    while nao_alocados:
        # encontra região com menor demanda
        r = demandas.index(min(demandas))
        # obtem vértice mais próximo do centro de r
        v = obter_vertice(G, nao_alocados, matrizes_ordenadas, r)
        print('Alocando {} em {}'.format(v, r))
        # soma demanda do vértice a demanda da região
        demandas[r] += demanda_vertice(G, v)
        # aloca vertice na regiao r e remove dos não alocados
        lista_regioes[r].add(v)
        G.nodes()[v]['regiao'] = r
        nao_alocados -= {v}

    demanda_ideal = sum(demandas) / k
    desvios = [stdev([demandas[r], demanda_ideal]) for r in range(k)]

    print('Demandas: {}'.format(demandas))   
    print('Demanda ideal: {}'.format(demanda_ideal))
    print('Desvios: {}'.format(desvios))
    print('Soma dos desvios: {}'.format(sum(desvios)))
 
    