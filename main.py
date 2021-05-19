from selector import RankedSelector
from mapa import Mapa
import random
import datetime
from exportacao import Export
from exportacao import ExportTime
import time
import numpy as np

TAMANHO_DA_POPULACAO = 50
NUMERO_DE_GERACOES = 20
TAXA_DE_MUTACAO = 0.05

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

    populacao.sort(key = lambda elem : elem.aptidao.aptidao, reverse=True)

def criterio_de_parada():
    return geracao > NUMERO_DE_GERACOES

def aplicar_cruzamento():
    global populacao, geracao
    rankedSelector = RankedSelector( populacao, CHANCE_DE_REPRODUCAO_MIN, CHANCE_DE_REPRODUCAO_MAX )
    nova_populacao = []

    while( len(nova_populacao) < TAMANHO_DA_POPULACAO ):
        indA = rankedSelector.selecionar_individuo()
        indB = rankedSelector.selecionar_individuo()
        
        filho1 = indA.cruzar( indB )
        if(filho1.calcular_menor_caminho() > 0):
            nova_populacao.append(filho1 ) 

        if( len(nova_populacao) < TAMANHO_DA_POPULACAO ):
            filho2 = indB.cruzar( indA )
            if(filho2.calcular_menor_caminho() > 0):
                nova_populacao.append( filho2)
    
    populacao.clear()
    populacao += nova_populacao
    geracao += 1

def aplicar_mutacao():
    limite = np.floor(TAMANHO_DA_POPULACAO * TAXA_DE_MUTACAO)
    individuos_mutados = []

    while( len(individuos_mutados) <= limite ):
        index = random.randint(0, TAMANHO_DA_POPULACAO-1)
        if(not index in individuos_mutados):
            individuos_mutados.append(index)
            populacao[index].aplicar_mutacao()

if __name__ == '__main__':
    start = time.time()

    iniciar_populacao()
    while( not criterio_de_parada() ):
        avaliar_populacao()
        best = populacao[0]
        print("1 -\\/")
        best.calcular_aptidao()
        Export(geracao, best.aptidao)
        aplicar_cruzamento()
        aplicar_mutacao()
    best.calcular_menor_caminho(isDebug = True)
    best.printar_mapa_expandido()
    print("2 -\\/")
    best.calcular_aptidao()
    end = time.time()
    print(str(datetime.timedelta(seconds=end - start)))
    ExportTime(datetime.timedelta(seconds=end - start))
