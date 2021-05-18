from selector import RankedSelector
from mapa import Mapa
import random

TAMANHO_DA_POPULACAO = 20
TAXA_DE_REPRODUCAO = 0.3
TAXA_DE_MUTACAO = 0.3

CHANCE_DE_REPRODUCAO_MIN = 1
CHANCE_DE_REPRODUCAO_MAX = 100

populacao = []
geracao = 0

def iniciar_populacao():
    for i in range( TAMANHO_DA_POPULACAO ):
        mapa = Mapa()
        mapa.posicionar_objetos()
        mapa.printar_mapa_expandido()
        populacao.append(mapa)

def avaliar_populacao():
    for individuo in populacao:
        individuo.calcular_aptidao()

    populacao.sort(key = lambda elem : elem.aptidao, reverse=True)

def criterio_de_parada():
    return geracao > 10

def aplicar_cruzamento():
    global populacao, geracao
    rankedSelector = RankedSelector( populacao, CHANCE_DE_REPRODUCAO_MIN, CHANCE_DE_REPRODUCAO_MAX )
    nova_populacao = []

    while( len(nova_populacao) < TAMANHO_DA_POPULACAO ):
        indA = rankedSelector.selecionar_individuo()
        indB = rankedSelector.selecionar_individuo()

        nova_populacao.append( indA.cruzar( indB )) 
        nova_populacao.append( indB.cruzar( indA ))
    
    populacao.clear()
    populacao += nova_populacao
    print( populacao )
    geracao += 1


if __name__ == '__main__':
    iniciar_populacao()
    while( not criterio_de_parada() ):
        avaliar_populacao()
        aplicar_cruzamento()
    avaliar_populacao()
    populacao[0].printar_mapa_expandido()