from geramapa2 import Mapa

TAMANHO_DA_POPULACAO = 100
TAXA_DE_REPRODUCAO = 0.3
TAXA_DE_MUTACAO = 0.3

populacao = List<Mapa>
geracao = 0

def iniciar_populacao():
    for i in range( TAMANHO_DA_POPULACAO ):
        mapa = Mapa()
        mapa.posicionar_objetos()
        mapa.printar_mapa()
        populacao.append(mapa)

def avaliar_populacao():
    for individuo in populacao:
        mapa_reduzido = individuo.mapa
        individuo.expandir_objetos(2)
        individuo.calcular_aptidao()
        individuo.mapa = mapa_reduzido

def criterio_de_parada():
    return geracao > 10

def selecionar_individuos():
    populacao.sort(key = lambda elem : elem.aptidao)
    populacao_reproducao = int(TAMANHO_DA_POPULACAO * TAXA_DE_REPRODUCAO)
   
    if(populacao_reproducao % 2 != 0): 
        populacao_reproducao += 1
    
    return populacao[:populacao_reproducao]

def cruzar( a,b ):
    pass

# minimo = 16

iniciar_populacao()
avaliar_populacao()
selecionar_individuos()