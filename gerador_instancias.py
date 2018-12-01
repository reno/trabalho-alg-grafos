'''
GCC2018 Algoritmos em Grafos - Trabalho final
gerador_instancias.py

Fornecido pelo Prof. Mayron O. Moreira
'''
import random
from argparse import ArgumentParser

class Vertices:
    def __init__(self, v, p, n):
        self.v = v
        self.p = p
        self.n = n
        self.x = random.uniform(0,100)
        self.y = random.uniform(0,100)

    def __str__(self):
        return str(self.v) + " " + str(self.p) + " " + str(self.n) + "\n"


class Veiculo:
    def __init__(self, V, P, Nv, vf, vd, tc, td, ph, pkm, pf):
        self.V = V
        self.P = P
        self.Nv = Nv
        self.vf = random.randint(vf - 5, vf + 5)
        self.vd = random.randint(vd - 5, vd + 5)
        self.tc = random.uniform(tc, 3*tc)
        self.td = td
        self.ph = ph
        self.pkm = pkm
        self.pf = pf


def main():
    # Processa argumentos fornecidos na execução
    parser = ArgumentParser() 
    parser.add_argument('arquivo', type=str, nargs='?',
                        help='Nome do arquivo de saída',
                        default="InstanciaTeste.txt")
    arg = parser.parse_args()
    N = 100
    R = 5
    K = 5
    H = 7
    # Lista de clientes
    vertices = [Vertices(random.uniform(0.001, 0.01), 
      random.randint(10,1001), random.randint(1,11)) 
      for i in range(0,N)]  
    # Os 5 primeiros clientes são centros de distribuição
    for i in range(5):
        vertices[i].v = vertices[i].p = vertices[i].n = 0
    # Lista de informações sobre os veículos
    veiculos = [Veiculo(0, 0, 0, 25, 30, 0.01, 0, 0, 0, 0) for i in range(5)]
    # Tipo 0: Van
    veiculos[0].V = random.randint(8,16)
    veiculos[0].P = random.randint(70000,75000)
    veiculos[0].Nv = random.randint(10,20)
    veiculos[0].td = random.uniform(0.04, 0.08)
    veiculos[0].ph = random.randint(30,60)
    veiculos[0].pkm = random.randint(2,4)
    veiculos[0].pf = random.randint(100,200)  
    # Tipo 1: Mini-Van
    veiculos[1].V = random.randint(2,4)
    veiculos[1].P = random.randint(70000,75000)
    veiculos[1].Nv = random.randint(10,20)
    veiculos[1].td = random.uniform(0.02, 0.04)
    veiculos[1].ph = random.randint(30,60)
    veiculos[1].pkm = random.randint(2,4)
    veiculos[1].pf = random.randint(90,180)  
    # Tipo 2: Comum
    veiculos[2].V = random.uniform(0.7,1.4)
    veiculos[2].P = random.randint(30000,35000)
    veiculos[2].Nv = random.randint(20,30)
    veiculos[2].td = random.uniform(0.02, 0.04)
    veiculos[2].ph = random.randint(30,60)
    veiculos[2].pkm = random.randint(1,2)
    veiculos[2].pf = random.randint(60,120)  
    # Tipo 3: Motocicleta
    veiculos[3].V = random.uniform(0.02,0.04)
    veiculos[3].P = random.randint(1000,5000)
    veiculos[3].Nv = random.randint(20,30)
    veiculos[3].td = random.uniform(0.02, 0.04)
    veiculos[3].ph = random.randint(30,60)
    veiculos[3].pkm = random.randint(1,2)
    veiculos[3].pf = random.randint(40,80)  
    # Tipo 4: Van terceirizada
    veiculos[4].V = random.uniform(0.08,0.16)
    veiculos[4].P = random.randint(75000,80000)
    veiculos[4].Nv = N
    veiculos[4].td = random.uniform(0.04, 0.08)
    veiculos[4].ph = 0
    veiculos[4].pkm = random.randint(2,4)
    veiculos[4].pf = 0

    file = open(arg.arquivo, "w") # Abrindo o arquivo
    file.write(str(N) + "\n") # Número de clientes
    file.write(str(R) + "\n") # Número de sub-regiões
    file.write(str(K) + "\n") # Tipos de veículos
    file.write(str(H) + "\n") # Carga horária diária

    # Informações sobre os vértices
    for v in vertices:
        file.write(str(v.x) + " " + str(v.y) + " " + str(v.v) + 
                   " " + str(v.p) + " " + str(v.n) + "\n")
    # Informações sobre os veículos
    for u in veiculos:
        file.write(str(u.V) + " " + str(u.P) + " " + str(u.Nv) + 
                   " " + str(u.vf) + " " + str(u.vd) + " " +
                   str(u.tc) + " " + str(u.td) + " " +
                   str(u.ph) + " " + str(u.pkm) + " " +
                   str(u.pf) + "\n")
    file.close()


if __name__ == '__main__':
    main()

