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

def k_regioes(G, k, tolerancia=1):
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

    
    def olha_ao_redor(v, r_v, alcance=20):
        """ """
        # obtem as coordenadas de v
        x, y = (G.nodes[v]['x'], G.nodes[v]['y'])
        # itera u mais distantes de regioes vizinhas, em sentido randômico
        regioes = list(range(k))
        regioes.remove(r_v)
        ordem = choice((regioes, reversed(regioes)))
        for r_u in ordem:
            if r_u != r_v:
                for u, d in reversed(matrizes_ordenadas[r_u]):
                    # se u está proximo de v, retorna u e sua região
                    x_u, y_u = (G.nodes[u]['x'], G.nodes[u]['y'])
                    if abs(x - x_u) < alcance and abs(y - y_u) < alcance:
                        print('Encontrado {} na regiao {}'.format(u, r_u))
                        return (u, r_u)
        return (None, None)


    def troca_vertice(v, r_atual, r_destino):
        """ """
        print('Removendo v{} de r{} a adiconando a r{}'.format(v, r_atual, r_destino))
        del lista_regioes[r_atual][v]
        lista_regioes[r_destino] = v
        





    # inicializa as regiões com seus centros
    lista_regioes = [{centro: 0} for centro in range(k)]

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
                lista_regioes[r][v] = matrizes_ordenadas[r][i][1][r]
                nao_alocados -= {v}
                #print('não alocados =', nao_alocados)
        i += 1
    #print(i, 'iteracoes')

    #print(lista_regioes)

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

    polaridade = lambda x: 1 if demandas[x] > demanda_ideal else -1

    #print(desvios_decrescente)
    #print(r_por_desvio)

    for r in r_por_desvio:
        desvio_atual = desvios[r]
        desvio_anterior = 0
        print('Iniciando trocas para regiao {}'.format(r))
        #while(desvio_atual - desvio_anterior > 1):  
        for i in range(10):
            for u, d in reversed(matrizes_ordenadas[r]):
                print('Procurando v proximo de u{} em {}'.format(u, r))
                v, r_vizinha = olha_ao_redor(u, r)
                if r_vizinha == None or polaridade(r) == polaridade(r_vizinha):
                    print('Não encontrado')
                    break
                elif polaridade(r) > polaridade(r_vizinha):
                    troca_vertice(u, r, r_vizinha)
                    print('Trocando {} de {} para {}'.format(u, r, r_vizinha))
                else:
                    troca_vertice(v, r_vizinha, r)
                    print('Trocando {} de {} para {}'.format(u, r, r_vizinha))
                desvio_anterior = desvio_atual
                print('Desvio anterior: {}'.format(desvio_anterior))
                desvio_atual = calcula_desvio(r)
                print('Novo desvio: {}'.format(desvios[r]))

    desvios = {r: calcula_desvio(r) for r in range(k)}
    print('demandas =', demandas)
    print('desvios =', desvios)
    print('soma desvios =', sum(desvios.values()))

    # escreve as regiões definitivas nos vértices (para plotar)
    for r in range(k):
        for v in lista_regioes[r]:
            G.nodes()[v]['regiao'] = r

    return lista_regioes

