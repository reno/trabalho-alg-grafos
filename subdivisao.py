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
from statistics import stdev
from pprint import pprint
from operator import itemgetter
#from collections import OrderedDict
from random import choice
#from copy import deepcopy

def calcula_distancia(G, u, v):
        """Calcula a distância euclideana entre os vértices u,v de G."""
        distancia = sqrt((G.nodes[u]['x'] - G.nodes[v]['x'])**2 +
                         (G.nodes[u]['y'] - G.nodes[v]['y'])**2)
        return distancia

def k_regioes(G, k):
    """Heurística ...
    Faz distribuição inicial dos vértices de maneira uniforme entre as
    regiões.

    args:
        G: grafo não direcionado onde os k primeiros vértices são centros
        k: número de regiões desejadas

    returns:
        None
    """

    # declaração de funções auxiliares

    def calcula_demanda(G, k=1):  
        """Calcula a demanda total dos vértices de G e divide por k regiões."""
        demandas = [G.nodes[v].get('volume') * G.nodes[v].get('valor')
                    for v in G.nodes()]
        demanda_total = sum(demandas)
        demanda_ideal = demanda_total / k
        return demanda_ideal


    def calcula_desvio(r):
        """ """
        Gr = G.subgraph(lista_regioes[r]) # .keys()
        demanda = calcula_demanda(Gr)
        desvio = stdev([demanda, demanda_ideal])
        return desvio

    
    def olha_ao_redor(v, r_v, alcance=10):
        """ """
        # obtem as coordenadas de v
        x, y = (G.nodes[v]['x'], G.nodes[v]['y'])
        # itera u mais distantes de regioes vizinhas, em sentido randômico
        regioes = list(range(k))
        regioes.remove(r_v)
        ordem = choice((regioes, reversed(regioes)))
        for r_u in ordem:
            if r_u != r_v:
                for u in reversed([t[0] for t in matrizes_ordenadas[r_u]]):
                    if u in lista_regioes[r_u]:
                        # se u está proximo de v, retorna u e sua região
                        x_u, y_u = (G.nodes[u]['x'], G.nodes[u]['y'])
                        if abs(x - x_u) < alcance and abs(y - y_u) < alcance:
                            print('Encontrado {} na regiao {}'.format(u, r_u))
                            return (u, r_u)
        return (None, None)


    def troca_vertice(v, r_atual, r_destino):
        """ """
        print('Removendo v{} de r{} a adiconando a r{}'.format(v, r_atual, r_destino))
        lista_regioes[r_atual] -= {v}
        lista_regioes[r_destino].add(v)
        



    # inicializa as regiões com seus centros
    lista_regioes = [{centro} for centro in range(k)]

    # calcula distancia dos vertices para cada um dos centros
    matriz_distancias = {}  # {regiao:[distancias]}
    for v in range(k, G.order()):
        distancias = [calcula_distancia(G, centro, v) for centro in range(k)]
        matriz_distancias[v] = distancias

    # ordena matriz_distancias para cada centro, salva resultados numa lista
    matrizes_ordenadas = [sorted(matriz_distancias.items(), 
                          key=lambda v: v[1][r]) for r in range(k)]
    
    nao_alocados = {v for v in G.nodes() if v >= k}
    i = 0
    # adiciona vértices não alocados nas regiões, de forma alternada
    while nao_alocados:
        for r in range(k):
            # escolhe o i-ésimo vertice mais próximo do centro de r
            v = matrizes_ordenadas[r][i][0]
            if v in nao_alocados:
                # adiciona v a regiao r 
                lista_regioes[r].add(v)
                nao_alocados -= {v}
        i += 1

    # calcula demandas e desvios das regioes
    demandas = {r: calcula_demanda(G.subgraph(lista_regioes[r])) for r in range(k)}
    demanda_ideal = calcula_demanda(G, k)
    desvios = {r: calcula_desvio(r) for r in range(k)}
    print('demanda ideal:', demanda_ideal)
    print('demandas =', demandas)
    print('desvios =', desvios)
    print('soma desvios =', sum(desvios.values()))

    # obtem lista de r (int) ordenada conforme demandas
    desvios_decrescente = sorted(desvios.items(), key=itemgetter(1),
                                 reverse=True)
    r_por_desvio = [desvios_decrescente[r][0] for r in range(k)]
    polaridade = lambda r: 1 if demandas[r] > demanda_ideal else -1

    desvio_atual = desvios[r]
    desvio_anterior = float('inf')
    #while(desvio_anterior - desvio_atual > 2): 
    #for i in range(10):
    trocados = set()
    r_por_desvio = [desvios_decrescente[r][0] for r in range(k)]
    for r in r_por_desvio:            
        print('Iniciando trocas para regiao {}'.format(r))
        vertices_ordenados = [t[0] for t in matrizes_ordenadas[r]]
        vertices_regiao = [v for v in vertices_ordenados if v in lista_regioes[r]]
        n = len(vertices_regiao) // 2
        v_regiao_dec = list(reversed(vertices_regiao))
        vertices_distantes = v_regiao_dec[:n]
        print('vertices_distantes: {}'.format(vertices_distantes))
        for u in vertices_distantes:
            print('Procurando v proximo de u{} em {}'.format(u, r))
            v, r_vizinha = olha_ao_redor(u, r)
            if r_vizinha == None or polaridade(r) == polaridade(r_vizinha):
                print('Não encontrado ou mesma polaridade')
                break
            elif polaridade(r) > polaridade(r_vizinha) and u not in trocados:
                troca_vertice(u, r, r_vizinha)
                trocados.add(u)
            elif v not in trocados:
                troca_vertice(v, r_vizinha, r)
                trocados.add(v)
            demandas[r] = calcula_demanda(G.subgraph(lista_regioes[r]))
            desvio_anterior = desvio_atual
            print('Desvio anterior: {}'.format(desvio_anterior))
            desvio_atual = calcula_desvio(r)
            print('Novo desvio: {}'.format(desvios[r]))

    demandas = {r: calcula_demanda(G.subgraph(lista_regioes[r])) for r in range(k)}
    desvios = {r: calcula_desvio(r) for r in range(k)}
    print('demandas =', demandas)
    print('desvios =', desvios)
    print('soma desvios =', sum(desvios.values()))
    print('-'*20)

    
    # escreve as regiões definitivas nos vértices (para plotar)
    for r in range(k):
        for v in lista_regioes[r]:
            G.nodes()[v]['regiao'] = r
    
    return lista_regioes

