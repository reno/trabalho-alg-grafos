'''
GCC2018 Algoritmos em Grafos - Trabalho final
teste.py

Alunos: 
Heuller Silva, João Pedro Andolpho, Luiz Carlos Conde,
Gabriel Amorim, Renan Modenese e Victor Landin

Chama gerador_instancias.py e passa arquivo resultante para main.py,
repetindo o processo n vezes. 

exemplo de uso: python3 teste.py n
'''

from argparse import ArgumentParser
import os
import os.path

def main():
    # processa os argumentos de entrada
    parser = ArgumentParser() 
    parser.add_argument('n', type=int, nargs='?',
                        help='Número de instâncias',
                        default=1)
    parser.add_argument('--pasta', type=str, nargs='?',
                        help='Pasta de destino',
                        default='Instancias')
    arg = parser.parse_args()

    for i in range(1, arg.n+1):
        nome_arquivo = 'Instancia_{:03d}.txt'.format(i)
        caminho_destino = os.path.join(arg.pasta, nome_arquivo)
        os.system('python3 gerador_instancias.py {}'.format(caminho_destino))
        os.system('python3 main.py {}'.format(caminho_destino))

if __name__ == '__main__':
    main()
