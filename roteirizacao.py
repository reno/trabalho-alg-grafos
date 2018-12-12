import random

class Veiculo:
    def __init__(self, V, P, Nv, vf, vd, tc, td, ph, pkm, pf):
        self.volume = V
        self.valor = P
        self.quantidade = Nv
        self.velocidade_inicial = random.randint(vf - 5, vf + 5)
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

'''
notas:
custo fixo do veiculo representa mais da metade do custo total diario,
minimizar numero de veiculos!
''' 



