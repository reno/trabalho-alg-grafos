'''
GCC2018 Algoritmos em Grafos - Trabalho final
main.py

Alunos: 
Heuller Silva, João Pedro Andolpho, Luiz Carlos Conde,
Gabriel Amorim, Renan Modenese e Victor Landin
'''

import networkx as nx
from networkx import MultiGraph
import matplotlib.pyplot as plt
from pprint import pprint
from argparse import ArgumentParser
from subdivisao import *
from roteirizacao import *

def main():
    # Processa argumentos fornecidos na execução
    parser = ArgumentParser() 
    parser.add_argument('arquivo', type=str, nargs='?',
                        help='Arquivo com instância do grafo',
                        default="InstanciaTeste.txt")
    arg = parser.parse_args()
    # Instancia grafo e faz leitura do arquivo
    G = nx.MultiGraph()
    with open(arg.arquivo) as arquivo:
        # le o arquivo, linha a linha
        numero_clientes = int(arquivo.readline())
        numero_regioes = int(arquivo.readline())
        tipo_veiculos = int(arquivo.readline())
        carga_horaria = int(arquivo.readline())
        # 5 primeiros vértices são centros de distribuição
        for i in range(numero_regioes):
            centro_dist = arquivo.readline()
            dados_centro = centro_dist.split()
            x, y = [float(valor) for valor in dados_centro[:2]]
            G.add_node(i, x=x, y=y, volume=0, valor=0)
        # demais vértices são clientes
        for i in range(numero_regioes, numero_clientes):
            cliente = arquivo.readline()
            dados_cliente = cliente.split()
            x, y, v = [float(valor) for valor in dados_cliente[:3]]
            p, n = [int(valor) for valor in dados_cliente[3:]]
            G.add_node(i, x=x, y=y, volume=v, valor=p, quantidade=n)
        # instancia e lê os dados dos veiculos
        veiculos = {}
        for tipo in ('van', 'minivan', 'carro', 'moto', 'terceirizado'):
            veiculo = arquivo.readline()
            dados_veiculo = veiculo.split()
            V = float(dados_veiculo[0])
            P, Nv, vf, vd = [int(valor) for valor in dados_veiculo[1:5]] 
            tc, td = [float(valor) for valor in dados_veiculo[5:7]]
            ph, pkm, pf = [int(valor) for valor in dados_veiculo[7:]]
            veiculos[tipo] = Veiculo(V, P, Nv, vf, vd, tc, td, ph, pkm, pf)
    # fim do arquivo

    # 1a etapa: divide G em regiões
    regioes = k_regioes(G, numero_regioes)
    #print(G.nodes.data())

    # 2a etapa: em andamento...
    #custos = [veiculos[tipo].custo_dia(horas_dia=carga_horaria) for tipo in veiculos.keys()]
    #print('custos', custos)

    #roteiro(G, regioes, 0, veiculos['van'])

    # desenho do grafo:
    tamanho_imagem = (5, 5)  # em polegadas, deve ter proporção 1:1
    resolucao = 150
    plt.figure(figsize=tamanho_imagem, dpi=resolucao)
    # gera dicionario com tupla de coordenadas para cada vértice
    posicao = {}
    for v in G.nodes():
        posicao[v] = tuple(G.nodes.data()[v][k] for k in ('x', 'y'))
    # gera lista de cores de acordo com a região dos vértices
    cores = ('c', 'm', 'y', 'r', 'g', '#767b7e')
    lista_cores = [cores[G.nodes.data()[v]['regiao']] if v > 4
                   else 'k' for v in G.nodes()]
    # desenho de G
    nx.draw(G, pos=posicao, with_labels=True, font_size=8, font_color='w',
            font_weight='bold', node_size=100, node_color=lista_cores)
    # salva imagem com mesmo nome do arquivo de entrada
    plt.savefig('{}.jpg'.format(arg.arquivo[:-4]))


if __name__ == '__main__':
    main()
