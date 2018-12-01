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

def calcula_demanda(G, k=1):
    """Calcula a demanda total dos vértices de G e divide por k regiões."""
    demandas = [G.nodes[v].get('volume') * G.nodes[v].get('valor')
                for v in G.nodes()]
    demanda_total = sum(demandas)
    demanda_ideal = demanda_total / k
    return demanda_ideal


def calcula_distancia(G, u, v, x='x', y='y'):
    """Calcula a distância euclideana entre os vértices u,v de G."""
    return sqrt((G.nodes[u][x] - G.nodes[v][x])**2 +
                (G.nodes[u][y] - G.nodes[v][y])**2)


def calcula_raio(G, centro, regiao):
    """Calcula o raio a partir das distancias dos vértices contidos na região."""
    distancias = set(regiao.values()) - {regiao[centro]}
    raio = mean(distancias)
    return raio


def esta_contido(G, v, centro, regiao):
    """Retorna True se o vértice v está dentro do alcance do raio da região."""
    distancias_regiao = set(regiao.values()) - {regiao[centro]}
    raio = mean(distancias_regiao)
    distancia_vc = calcula_distancia(G, v, centro)
    if distancia_vc < raio:
        return True
    else:
        return False


def arvore_adjacencia(G, k):
    """Retorna a AGM para os centros do grafo G com base na distância."""
    centros = [c for c in range(k)]
    G_centros = G.subgraph(centros).copy()
    for u in range(k):
       for v in range(u, k):
            if u != v:
                distancia = calcula_distancia(G_centros, u, v)
                G_centros.add_edge(u, v, distancia=distancia)
    G_adj = nx.minimum_spanning_tree(G_centros, weight='distancia')
    return G_adj


def kcluster(G, k):
    """Heurística baseada na K-medoids, adaptada para atender as
    características do problema proposto.

    Divide inicialmente os vértices conforme a distância entre os centros.
    Melhora solução considerando a distância para o centro e a demanda
    por região.

    args:
        G: grafo não direcionado (nx.MultiGraph)
        k: número de regiões desejadas

    returns:
        regioes: lista contendo um dict para cada região
                 dicts possuem número do vertice como chave
                 e distância para o centro como valor
    """

    # inicializa as regiões
    matriz_distancias = [] # distância entre cada vértice e os todos os centros
    regioes = []
    for centro in range(k):
        regioes.append({centro:0})
    # faz distribuição inicial dos vértices de acordo com o centro mais próximo
    for v in range(k, G.order()):
        distancias = []
        for centro in range(k):
            distancia = calcula_distancia(G, centro, v)
            distancias.append(distancia)
        menor_distancia = (min(distancias))
        regiao = distancias.index(menor_distancia)
        regioes[regiao][v] = menor_distancia
        matriz_distancias.append(distancias)
    #pprint(matriz_distancias)
    #pprint(regioes)

    # cria dicionario em ordem decrescente de distancia (teste)
    regioes_ordenado = []
    for r in range(k):
        regioes_ordenado.append(OrderedDict(sorted(regioes[r].items(),
                                                   key=itemgetter(1),
                                                   reverse=True)))
    #pprint(regioes_ordenado)

    # calcula demandas das regiões (e os desvios para a demanda ideal)
    demanda_ideal = calcula_demanda(G, k)
    demanda_regiao = {}
    desvios = {} # para debug, não precisa ser armazenado na versão final
    for r in range(k):
        Gr = G.subgraph(regioes[r].keys())
        demanda = calcula_demanda(Gr)
        demanda_regiao[r] = demanda
        desvios[r] = stdev((demanda_ideal, demanda))
    #pprint(demanda_regiao)
    #pprint(desvios)
    #print(max(desvios.values()))
    
    # escreve as regiões definitivas nos vértices (para plotar)
    for r in range(k):
        for v in regioes[r]:
            G.nodes()[v]['regiao'] = r

    return regioes

