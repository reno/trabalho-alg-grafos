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
from kcluster import *

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


    # chamadas de função aqui :)
    regioes = kcluster(G, numero_regioes)
    G_adj = arvore_adjacencia(G, numero_regioes)


    # desenho do grafo:
    tamanho_imagem = (5,5) # deve ter proporção 1:1
    resolucao = 150
    plt.figure(figsize=tamanho_imagem, dpi=resolucao)
    # gera dicionario com tupla de coordenadas para cada vértice
    posicao = {}
    for v in G.nodes():
        posicao[v] = tuple(G.nodes.data()[v][k] for k in ('x', 'y'))
    # gera lista de cores de acordo com a região dos vértices
    cores = ('c', 'm', 'y', 'r', 'g')
    lista_cores = [cores[G.nodes.data()[v]['regiao']] if v > 4
                   else 'k' for v in G.nodes()]
    # desenho de G        
    nx.draw(G, pos=posicao, with_labels=True, font_size=8, font_color='w',
            font_weight='bold', node_size=100, node_color=lista_cores)
    # desenho de G_adj
    nx.draw(G_adj, pos=posicao, with_labels=True, font_size=8, font_color='w',
            font_weight='bold', node_size=100, node_color=lista_cores)
    # calcula circulos representando regiões
    circulos = {'centros':[], 'diametros':[]}
    for n, regiao in enumerate(regioes):
        #print(regiao)
        diametro = 2 * calcula_raio(G, n, regiao) * tamanho_imagem[0] * resolucao
        circulos['diametros'].append(diametro)
        centro = tuple(G.nodes.data()[n][k] for k in ('x', 'y'))
        circulos['centros'].append(centro)
    regioes = [k for k in range(numero_regioes)]
    # desenha circulos
    nx.draw(G, nodelist=regioes, pos=circulos['centros'],
            node_size=circulos['diametros'], node_color=cores, alpha=0.2)
    # salva imagem
    plt.savefig('{}.jpg'.format(arg.arquivo[:-4]))


if __name__ == '__main__':
    main()
