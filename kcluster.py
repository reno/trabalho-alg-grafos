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


def kcluster(G, k, tolerancia=1):
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
    # faz uma copia da matriz_distancias ordenada para cada regiao
    vertices_proximos = []   
    vertices_proximos += [sorted(matriz_distancias.items(),
                          key=lambda v: v[1][r]) for r in range(k)]
    # inicializa conjunto com v nao alocados
    nao_alocados = {v for v in G.nodes() if v >= k}
    # inicializa outras variaveis
    i = 0

    # adiciona v nao alocados as regioes de forma alternada
    while nao_alocados: #and i < G.order():
        for r in range(k):
            # escolhe o i-esimo vertice mais próximo do centro de r
            v = vertices_proximos[r][i][0]
            if v in nao_alocados:
                # adiciona v a regiao r 
                lista_regioes[r][v] = vertices_proximos[r][i][1][r]
                nao_alocados -= {v}
                #print('não alocados =', nao_alocados)
        i += 1
    print(i, 'iteracoes')

    demanda_regioes = {r: 0 for r in range(k)}
    demanda_ideal = calcula_demanda(G, k)
    desvios = [0 for r in range(k)]

    for r in range(k):
        Gr = G.subgraph(lista_regioes[r].keys())
        demanda_regioes[r] = calcula_demanda(Gr)
        desvios[r] = stdev([demanda_ideal, demanda_regioes[r]])

    print('soma desvios =', sum(desvios))
    print('desvios =', desvios)
    print('demanda ideal:', demanda_ideal)   
    print('demandas =', demanda_regioes)

    #print(lista_regioes)

    # gera lista das regioes em ordem decrescente de demanda
    demandas_ordem = sorted(demanda_regioes.items(),
                            key=itemgetter(1), reverse=True)
    regioes_demanda = [demandas_ordem[r][0] for r in range(k)]

    #menor_distancia = min(matriz_distancias[v])
    #r = matriz_distancias[v].index(menor_distancia)
    #lista_regioes[r][v] = menor_distancia

    
    #teste
    # lista de dicts com v em ordem decrescente de distancia 
    #vertices_distantes = []
    for r in range(k):
        vertices_distantes = [sorted(lista_regioes[r].items(), reverse=True,
                               key=lambda v: v[1]) for r in range(k)]
    
    #pprint(vertices_distantes)

    # trocar v para 2a regiao mais proxima nao funciona bem
    #tentar trocar v para regiao mais proxima caso não esteja nela

    '''
    i = 0
    desvios_anteriores = [float('inf') for r in range(k)]
    #while abs(sum(desvios) - sum(desvios_anteriores)) > tolerancia:
    for n in range(10):
        # itera regioes partindo da maior demanda
        for r in regioes_demanda:
            # i-esimo v mais distante de r
            v = vertices_distantes[r][i][0]
            # encontra o 2a regiao mais proxima de v 
            distancia = min(matriz_distancias[v][d] for d in range(k) if d != r)
            r_proxima = matriz_distancias[v].index(distancia)
            print(r, v, r_proxima, distancia)
            # troca v de regiao
            del lista_regioes[r][v]
            lista_regioes[r_proxima][v] = distancia
            # recalcula demanda e desvio
            Gr = G.subgraph(lista_regioes[r].keys())
            demanda_regioes[r] = calcula_demanda(Gr)
            desvios_anteriores[r] = desvios[r]
            desvios[r] = stdev([demanda_ideal, demanda_regioes[r]])
        i += 1

    print('soma desvios =', sum(desvios))
    print('desvios:', desvios)
    print('demandas', demanda_regioes)
    print(i, 'iterações')
    '''

    # escreve as regiões definitivas nos vértices (para plotar)
    for r in range(k):
        for v in lista_regioes[r]:
            G.nodes()[v]['regiao'] = r

    #return lista_regioes

