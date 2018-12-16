
'''
GCC2018 Algoritmos em Grafos - Trabalho final
roteirizacao.py

Alunos: 
Heuller Silva, João Pedro Andolpho, Luiz Carlos Conde,
Gabriel Amorim, Renan Modenese e Victor Landin

Neste arquivo contem 3 classes que se interagem para criar a roterizacao de cada regiao: Veiculo, Entrega, Roterizacao.
De modo que a roterizacao contem varias entregas(rota), cada entrega contem um veiculo.
'''


import networkx as nx
from networkx import MultiGraph
import random
from statistics import mean, stdev
from pprint import pprint
from subdivisao import calcula_distancia

'''classe veiculo'''
class Veiculo:
    def __init__(self, V, P, Nv, vf, vd, tc, td, ph, pkm, pf, tipo):
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
        self.tipo = tipo

    def custo_dia(self, horas_dia=7, n_entregas=10): 
        """Calcula o custo total diario do veiculo"""
        tempo_parado = n_entregas * (self.tempo_descarga + self.tempo_carga)
        #print(tempo_parado)
        deslocamento_km = (horas_dia - tempo_parado) * self.velocidade
        #print(deslocamento_km)
        custo_dia = self.custo_fixo + (self.custo_hora * horas_dia) + (self.custo_km * deslocamento_km)
        return custo_dia
'''classe entrega'''
class Entrega:
    def __init__(self, carga_horaria):
        self.tempo_restante = carga_horaria
        self.pacotes = 0
        self.volume = 0
        self.valor = 0
        self.tipo_veiculo = ''
        self.veiculo = None
        self.rota = []
        self.km = 0


    def prossegue(self, Gr, matriz, u, v, r, entrega, veiculo):
        tempo =(matriz[u][v] / veiculo.velocidade + matriz[v][r] / veiculo.velocidade_centro + Gr.node[v].get('quantidade')*(veiculo.tempo_carga + veiculo.tempo_descarga))
        if entrega.tempo_restante - tempo > 0:
            if entrega.volume + Gr.node[v].get('volume') < veiculo.volume_max and entrega.valor + Gr.node[v].get('valor') < veiculo.valor_max:
                return True
        return False



'''
notas:
custo fixo do veiculo representa mais da metade do custo total diario,
minimizar numero de veiculos!
''' 


'''classe roteiro'''
class roteiro:
    def __init__(self, G, regiao, r, veiculos, carga_horaria):
        #criar o subGrafo da regiao
        self.Gr = G.subgraph(regiao).copy()
        self.completa()
        self.centro = r
        
        #lista de entregas
        self.rotas = []
        
        #calcular menor caminho de todos para todos
        self.matriz = self.caminhoMinimo(self.Gr)

        #lista de veiculos
        self.veiculos = []
        self.quantVeiculos = []
        self.quantVeiculosUsados = []
        self.CustoPorKm = 0
        self.CustoPorHora = 0
        self.CustoFixo = 0
        self.CustoTotal = 0
        '''
        dividir veiculos
        '''
        for tipo in veiculos.keys():
            self.veiculos.append(Veiculo(veiculos[tipo].volume_max, veiculos[tipo].valor_max, veiculos[tipo].quantidade/5, veiculos[tipo].velocidade_centro, veiculos[tipo].velocidade, veiculos[tipo].tempo_carga, veiculos[tipo].tempo_descarga, veiculos[tipo].custo_hora, veiculos[tipo].custo_km, veiculos[tipo].custo_fixo, tipo))
            self.quantVeiculos.append(veiculos[tipo].quantidade/5)
            self.quantVeiculosUsados.append(0)
        '''chama a funcao roterizar'''
        self.roteirizar(r, carga_horaria)

    #funcao chamada automaticamente
    #responsavel por criar as todas
    def roteirizar(self,r, carga_horaria):
        #a lista recebe todos os vertices contidos na regiao
        clientes_nao_atendidos = []
        for i in self.matriz:
            clientes_nao_atendidos.append(i)
        #enquanto nao atendemos todos os vertices na regiao, rodamos o loop
        #se sobrar apenas o centro, atendemos todos os vertices da regiao
        while clientes_nao_atendidos != [r]:
            #entregas
            entregas = []
            
            #cria uma entrega com a carga horaria maxima
            entrega = Entrega(carga_horaria)
            
            #encontra-se um veiculo disponivel para atender a rota
            veiculo = self.veiculoDisponivel()
            
            #adicionamos o veiculo a entrega
            entrega.veiculo = veiculo
            #adiciona centro
            u = r
            entrega.rota.append(u)

            #ordena os vizinhos de u de forma crescente por distancia 
            Adj = self.listOrdCres(self.matriz[u], clientes_nao_atendidos, u, r)
            #encontra o primeiro cliente
            encontrou = False
            for v in Adj:
                #verifica se v é um vertice seguro
                encontrou = entrega.prossegue(self.Gr, self.matriz, u, v, r, entrega, veiculo)
                #se encontrou um vertice segura, adiciona-o na entrega e atualiza o somatorios da entrega
                if encontrou:
                    entrega.rota.append(v)
                    entrega.km += self.matriz[u][v]
                    entrega.tempo_restante -= self.matriz[u][v] / veiculo.velocidade_centro + self.Gr.nodes[v].get('quantidade') * (veiculo.tempo_carga + veiculo.tempo_descarga)
                    entrega.volume += self.Gr.nodes[v].get('volume')
                    entrega.valor += self.Gr.nodes[v].get('valor')
                    u = v
                    break
            
            #percorre a regiao para adicionar os clientes intermediarios na rota,
            nao_encontrou = False
            while not nao_encontrou:
                #booleano para verificar se no loop abaixo encontrou-se algum cliente para adicionar na rota
                nao_encontrou = True
                encontrou = False
                Adj = self.listOrdCres(self.matriz[u],clientes_nao_atendidos, u, r)
                for v in Adj:
                    if v not in entrega.rota:
                        encontrou = entrega.prossegue(self.Gr, self.matriz, u, v, r, entrega, veiculo)
                        if encontrou:
                            entrega.rota.append(v)
                            entrega.km += self.matriz[u][v]
                            entrega.tempo_restante -= self.matriz[u][v] / veiculo.velocidade_centro + self.Gr.nodes[v].get('quantidade') * (veiculo.tempo_carga + veiculo.tempo_descarga)
                            entrega.volume += self.Gr.nodes[v].get('volume')
                            entrega.valor += self.Gr.nodes[v].get('valor')
                            u = v
                            nao_encontrou = False
                            break
            #retorno para o centro
            entrega.rota.append(r)
            entrega.km += self.matriz[r][u]
            entrega.tempo_restante -= self.matriz[r][u] / veiculo.velocidade_centro
            self.rotas.append(entrega)
            clientes_nao_atendidos.append(r)
        #calcular o somatorio de custos da regiao
        self.calcularCustos()

    def calcularCustos(self):
        #custo fixo
        indice = 0
        #custoPorHora e por km
        for entrega in self.rotas:
            self.CustoFixo += entrega.veiculo.custo_fixo
            self.CustoPorHora += entrega.veiculo.custo_hora * (7 - entrega.tempo_restante)
            self.CustoPorKm += entrega.veiculo.custo_km * entrega.km
            self.CustoTotal += self.CustoFixo + self.CustoPorHora + self.CustoPorKm
    #prenche o dicionario com a distancia direta entre os vertices - grafo kn
    def caminhoMinimo(self, Gr):
        distancias = {}
        for i in Gr:
            dicionario = {}
            for j in Gr:
                dicionario[j] = 0
            distancias[i] = dicionario
        for u in Gr:
            for v in Gr:
                distancia = ((Gr.nodes[u].get('x') - Gr.nodes[v].get('x'))**2 + (Gr.nodes[u].get('y') - Gr.nodes[v].get('y'))**2)**(1/2)
                distancias[u][v] = distancia
        return distancias
    #ordena a lista de chaves pela distancia para o vertice u
    def listOrdCres(self, matriz, keys, u, r):
        if u in keys:
            keys.remove(u)
        if u != r and r in keys:
            keys.remove(r)
        
        listOrdCres = []
        #adiciona as chaves em outra lista
        for i in keys:
            listOrdCres.append(i)
        n = len(keys)
        #ordena a lista de saida pela distancia
        for i in range(0, n):
            for j in range(i+1, n):
                if matriz[listOrdCres[i]] > matriz[listOrdCres[j]]:
                    aux = listOrdCres[i]
                    listOrdCres[i] = listOrdCres[j]
                    listOrdCres[j] = aux
        return listOrdCres
    #retorna um veiculo disponivel e atualiza os valores referentes a ele
    def veiculoDisponivel(self):
        indice = 0
        for v in self.veiculos:
            if self.quantVeiculos[indice] > 0:
                self.quantVeiculos[indice] -= 1
                self.quantVeiculosUsados[indice] +=1
                return v
            indice += 1
    #completa o subgrafo Gr com as arestas entre os vertices representando a distancia
    def completa(self):
        for u in self.Gr.nodes():
            for v in self.Gr.nodes():
                if u != v:
                    distancia = calcula_distancia(self.Gr,u, v)
                    self.Gr.add_edge(u, v, distancia=distancia)
    #imprime os dados das rotas
    def imprimir(self):
        print('Rotas da regiao ' + str(self.centro))
        for rota in self.rotas:
            print('rota: ', rota.rota, 'veiculo:', rota.veiculo.tipo)
        print('Custo por KM = ', self.CustoPorKm)
        print('Custo por Hora = ', self.CustoPorHora)
        print('Custo Fixo = ', self.CustoFixo)
        print('Somatório de Custos = ', self.CustoTotal)
        
