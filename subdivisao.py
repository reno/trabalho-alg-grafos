'''
GCC2018 Algoritmos em Grafos - Trabalho final
subdivisao.py

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

def calcula_distancia(G, u, v):
    """Calcula a distância euclideana entre os vértices u,v de G."""
    distancia = sqrt((G.nodes[u]['x'] - G.nodes[v]['x'])**2 +
                     (G.nodes[u]['y'] - G.nodes[v]['y'])**2)
    return distancia
    

def demanda_vertice(G, v): 
    """Calcula a demanda de um cliente, considerando volume e valor do pedido"""
    return G.nodes[v].get('volume') * G.nodes[v].get('valor')


def obter_vertice(G, nao_alocados, r):
    """Retorna o vértice não alocado mais próximo do centro da região R"""
    proximo = next(iter(nao_alocados))
    for v in nao_alocados:
        if (calcula_distancia(G, r, v) < calcula_distancia(G, r, proximo)):
            proximo = v
    return proximo


def subdivisao(G, k):
    """Heurística para distribuição dos vértices em regiões, priorizando
    as regiões com menor demanda. 

    args:
        G: grafo não direcionado onde os k primeiros vértices são centros
        k: número de regiões desejadas

    returns:
        regioes: lista de conjuntos contendo os vértices de cada região
    """
    
    # inicializa as regiões com seus centros
    regioes = [{centro} for centro in range(k)]
    
    # inicializa variáveis 
    nao_alocados = {v for v in G.nodes() if v >= k}
    demandas = [0 for r in range(k)]

    # distribuição inicial
    while nao_alocados:
        # encontra região com menor demanda
        r = demandas.index(min(demandas))
        # obtem vértice mais próximo do centro de r
        v = obter_vertice(G, nao_alocados, r)
        # soma demanda do vértice a demanda da região
        demandas[r] += demanda_vertice(G, v)
        # aloca vertice na regiao r e remove dos não alocados
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


