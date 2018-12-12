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
                
