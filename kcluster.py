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


def kcluster(G, k, tolerancia=0.5):
    """Heurística ...

    args:
        G: grafo não direcionado onde os k primeiros vértices são centros
        k: número de regiões desejadas

    returns:
        ...
    """

    # inicializa as regiões com seus centros
    lista_regioes = []
    for centro in range(k):
        lista_regioes.append({centro: 0})
    # calcula distancia dos vertices para cada um dos centros
    matriz_distancias = {}  # dict de listas, distância entre v e cada centro
    for v in range(k, G.order()):
        distancias = []
        for centro in range(k):
            distancia = calcula_distancia(G, centro, v)
            distancias.append(distancia)
        matriz_distancias[v] = distancias
    # calcula demandas
    demanda_regioes = {r: 0 for r in range(k)}
    demanda_ideal = calcula_demanda(G, k)
    print('demanda ideal:', demanda_ideal)     
    # inicializa matriz com v em ordem de proximidade para cada regiao
    vertices_proximos = []   
    vertices_proximos += [sorted(matriz_distancias.items(),
                          key=lambda v: v[1][r]) for r in range(k)]
    # inicializa conjunto com v nao alocados
    nao_alocados = {v for v in G.nodes() if v >= k}
    # inicializa outras variaveis
    i = 0
    desvios = [0 for r in range(k)]
    # adiciona v nao alocados as regioes de forma alternada
    while nao_alocados: #and i < G.order():
        for r in range(k):
            #if demanda_regioes[r] < demanda_ideal:
                print('demanda da regiao', r, '=', demanda_regioes[r])
                # escolhe o i-esimo vertice mais próximo do centro de r
                v = vertices_proximos[r][i][0]
                if v in nao_alocados:
                    # adiciona v a regiao r e recalcula a demanda da regiao
                    lista_regioes[r][v] = vertices_proximos[r][i][1][r]
                    nao_alocados -= {v}
                    print('não alocados =', nao_alocados)
                    Gr = G.subgraph(lista_regioes[r].keys())
                    demanda_regioes[r] = calcula_demanda(Gr)
                    # atualiza os desvios
                    desvios[r] = stdev([demanda_ideal, demanda_regioes[r]])
        i += 1
        print('soma desvios =', sum(desvios))
        #print('soma desvios anteriores =', sum(desvios_anteriores))
    print('desvios:', desvios)
    print(i, 'iteracoes')

    '''
    # garante que todos vertices foram alocados
    # apenas se loop não alocar todos os vertices
    # necessário alterar linha 136 para range(k+1)
    vertices_alocados = []
    vertices_alocados = [v for regiao in lista_regioes for v in regiao]
    for v in G.nodes():
        if v not in vertices_alocados:
            if len(lista_regioes) == k:
                lista_regioes.append ({v: float('inf')})
            lista_regioes[k][v] = float('inf')
            #print(v)
            #menor_distancia = min(matriz_distancias[v])
            #r = matriz_distancias[v].index(menor_distancia)
            #lista_regioes[r][v] = menor_distancia
    #pprint(lista_regioes)
    '''


    
    '''
    #teste
    # lista de dicts com v em ordem decrescente de distancia 
    vertices_distantes = []
    for r in range(k):
        vertices_distantes.append(OrderedDict(sorted(regioes[r].items(),
                                              key=itemgetter(1),
                                              reverse=True)))
    #pprint(vertices_distantes)
    '''

    # desvios_anteriores = [float('inf') for r in range(k)]
    #desvios_anteriores[r] = desvios[r]

    # while abs(sum(desvios) - sum(desvios_anteriores)) > tolerancia:
    # tenta troca de v para regiao do 2o centro mais proximo


    # escreve as regiões definitivas nos vértices (para plotar)
    for r in range(k):
        for v in lista_regioes[r]:
            G.nodes()[v]['regiao'] = r

    #return lista_regioes

