
'''
GCC2018 Algoritmos em Grafos - Trabalho final
roteirizacao.py

Alunos: 
Heuller Silva, João Pedro Andolpho, Luiz Carlos Conde,
Gabriel Amorim, Renan Modenese e Victor Landin
'''

import networkx as nx
from networkx import MultiGraph
import random
from statistics import mean, stdev
from pprint import pprint
from subdivisao import calcula_distancia

class Veiculo:
    def __init__(self, V, P, Nv, vf, vd, tc, td, ph, pkm, pf):
        self.volume_max = V
        self.valor_max = P
        self.quantidade = Nv
        self.velocidade_centro = random.randint(vf - 5, vf + 5)
        self.velocidade = random.randint(vd - 5, vd + 5)
        self.tempo_carga = random.uniform(tc, 3*tc)
        self.tempo_descarga = td
        self.custo_hora = ph
        self.custo_km = pkm
        self.custo_fixo = pf

    def custo_dia(self, horas_dia=7, n_entregas=10): 
        """Calcula o custo total diario do veiculo"""
        tempo_parado = n_entregas * (self.tempo_descarga + self.tempo_carga)
        #print(tempo_parado)
        deslocamento_km = (horas_dia - tempo_parado) * self.velocidade
        #print(deslocamento_km)
        custo_dia = self.custo_fixo + (self.custo_hora * horas_dia) + (self.custo_km * deslocamento_km)
        return custo_dia

class Entrega:
    def __init__(self, carga_horaria):
        self.tempo_restante = carga_horaria
        self.pacotes = 0
        self.volume = 0
        self.valor = 0
        self.tipo_veiculo = ''

    #def prossegue(self, Gr, u, v):
        """Retorna True se for viável percorrer trajeto u,v e retornar ao centro"""
        '''
        tempo_centro = (distancia_centro / vel_centro)
        tempo_uv = (distancia_uv / velocidade)

        if (tempo_uv + tempo_centro) < tempo_restante :
                return True
        '''

def completa(G):
    for u in G.nodes():
        for v in G.nodes():
            if u != v:
                distancia = calcula_distancia(G, u, v)
                G.add_edge(u, v, distancia=distancia)

'''
notas:
custo fixo do veiculo representa mais da metade do custo total diario,
minimizar numero de veiculos!
''' 

def roteiro(G, lista_regioes, r, veiculo):
    Gr = G.subgraph(lista_regioes[r].keys()).copy()
    completa(Gr)
    matriz_distancias = nx.floyd_warshall(Gr, weight='distancia')
    pprint(matriz_distancias)

    '''
    trajeto = {}  # vertices percorridos#

    '''








