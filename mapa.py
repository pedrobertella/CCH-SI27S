import random
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from aptidao import Aptidao

W = 21
H = 32
PLAYER_POS_Y = np.floor(W/2).astype(int)
PLAYER_POS_X = 0
OBJECTIVE_POS_Y = np.floor(W/2).astype(int)
OBJECTIVE_POS_X = np.floor(H/2).astype(int)
HALF_H = np.floor(H/2).astype(int)

TAXA_DE_CAMPOS_LIVRES_MIN = 0.30
TAXA_DE_CAMPOS_LIVRES_MAX = 0.60

DISTANCIA_MEDIA_DOS_CAMINHOS_MIN = HALF_H + 5
DISTANCIA_MEDIA_DOS_CAMINHOS_MAX = HALF_H + 20

DISTANCIA_MENOR_CAMINHO_MIN = HALF_H + 5
DISTANCIA_MENOR_CAMINHO_MAX = HALF_H + 10

QTD_CAMINHOS_MIN = 3
QTD_CAMINHOS_MAX = 5

class Mapa:
    objetos = {
        'vazio': 0,
        'parede': 1,
        'agua': 2,
        'vegetacao': 3,
    }
    
    objetosSprites = {
        objetos['vazio']: '  ' ,
        objetos['agua']: '~~', 
        objetos['parede']: '[]', 
        objetos['vegetacao']: '`´', 
    }

    _default_qtd_objetos = { 
        'agua': 3,
        'parede': 5,
        'vegetacao':3,
    }

    _objetos_livres = [
        [objetos['vazio']],
        [objetos['vegetacao']]
    ]

    fator_de_expancao = 2

    def __init__(self):
        self.mapa = np.zeros( (H, W), dtype=np.uintc )
        self.aptidao = Aptidao()

    def cruzar( self, outro ):
        pontos_de_corte = [ (H/4), (H/4) * 3]
        filho = self.mapa.copy()
        
        is_corte = False
        for i in range( len(filho) ):
            if( i in pontos_de_corte ):
                is_corte = not is_corte

            if( is_corte ):
                filho[i] = outro.mapa[i]

        resultado = Mapa()
        resultado.mapa = filho
        
        return resultado

    def calcular_vizinhanca(self,mapa, y,x ):
        objCount= np.zeros( len(self.objetos), dtype=np.uintc ) 

        for i in [-1,0,1]:
            for j in [-1,0,1]:

                if( (i == 0 or j == 0) 
                and not (i == 0 and j == 0) 
                and 0 <= y+i < H 
                and 0 <= x+j < W ):
                    objCount[ mapa[ y+i, x+j ] ] += 1

        return objCount


    def posicionar_objetos(self, qtdObjetos = _default_qtd_objetos ):
        
        for k in qtdObjetos:
            for count in range(qtdObjetos[k]):

                while( True ):
                    y,x = (random.randint(0,HALF_H-1), random.randint(0,W-1))

                    if( self.mapa[y,x] == self.objetos['vazio']):
                        self.mapa[y,x] = self.objetos[k]
                        break

        #espelhando metade de cima para baixo
        for y in range(len(self.mapa)):
            for x in range(len(self.mapa[y])):
                self.mapa[H-1-y,W-1-x] = self.mapa[y,x]

    def expandir_objetos(self, iteracoes = fator_de_expancao ):
        resultado = self.mapa.copy()
        
        for i in range(iteracoes):
            novo_mapa = resultado.copy()

            for y in range(len(resultado)):
                for x in range(len(resultado[y])):

                    if( self.mapa[y,x] == self.objetos['vazio'] ): 
                        vizinhanca = self.calcular_vizinhanca(resultado,y,x)
                        
                        for k in self.objetos:
                            if( k != 'vazio' and vizinhanca[self.objetos[k]] > 0 ):
                                novo_mapa[y,x] = self.objetos[k]
            resultado = novo_mapa

        return resultado

    def calcular_menor_caminho(self, isDebug = False):         
        return len(self.calcular_caminho(self.expandir_objetos(), isDebug))

    def calcular_caminho(self, mapa_expandido, isDebug = False):         
        grid = Grid(matrix=self.converter_mapa_to_grid_alternativo(mapa_expandido))
        start = grid.node(PLAYER_POS_Y, PLAYER_POS_X)
        end = grid.node(OBJECTIVE_POS_Y, OBJECTIVE_POS_X)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        
        Grid.cleanup
        if(isDebug):
            print('operations:', runs, 'path length:', len(path))
            print(grid.grid_str(path=path, start=start, end=end))
        return path

    def calcular_caminhos_alternativos(self):
        count_caminhos = 0
        sum_caminhos = 0
        mapa_expandido = self.expandir_objetos()
        while(True):
            caminho = self.calcular_caminho(mapa_expandido)
            
            if( len(caminho) == 0 ):
                break
            
            count_caminhos +=1
            sum_caminhos += len(caminho)
            mapa_expandido = self.bloqueia_caminho(mapa_expandido, caminho)   

        return count_caminhos ,sum_caminhos/count_caminhos if count_caminhos > 0 else 0
        
    def bloqueia_caminho(self, mapa_expandido, path):
        for val in path[3:-3]:
            mapa_expandido[val[1]][val[0]] = self.objetos["parede"]
        return mapa_expandido

    def converter_mapa_to_grid_alternativo(self, mapa_expandido):
        matriz = []
        for linha in mapa_expandido:
            matriz_linha = []
            for item in linha:
                matriz_linha.append(1 if item == self.objetos['vazio'] or item == self.objetos['vegetacao'] else 0)
            matriz.append(matriz_linha) 
        return matriz    

    def converter_mapa_to_grid(self):
        mapa_expandido = self.expandir_objetos()

        matriz = []
        for linha in mapa_expandido:
            matriz_linha = []
            for item in linha:
                matriz_linha.append(1 if item == self.objetos['vazio'] or item == self.objetos['vegetacao'] else 0)
            matriz.append(matriz_linha) 
        return matriz
            
    def printar_mapa_expandido( self ):
        self._printar_mapa( self.expandir_objetos() )

    def printar_mapa_reduzido( self ):
        self._printar_mapa( self.mapa )

    def _printar_mapa(self, mapa):
        for i in range((W*2)+2): 
            print("#" , end="")
        print("")

        for x in mapa:
            print("#", end="")
            for cell in x:
                print(self.objetosSprites[cell], end="")
            print("#")

        for i in range((W*2)+2): 
            print("#" , end="")
        print("")

    def count_campos_by_type(self, types ):
        count = 0
        for y in self.mapa:
            for x in y:
                if x in types:
                    count = count + 1
        return count

    def calcular_aptidao_por_espaco_livre(self):
        count_livre = self.count_campos_by_type( self._objetos_livres )

        total = H*W
        qtd_livre_min = np.floor(total * TAXA_DE_CAMPOS_LIVRES_MIN)
        qtd_livre_max = np.floor(total * TAXA_DE_CAMPOS_LIVRES_MAX)
        
        return self.calcular_desvio_padrao( count_livre, qtd_livre_min, qtd_livre_max )

    def calcular_aptidao_por_menor_caminho(self):
        return self.calcular_desvio_padrao(self.calcular_menor_caminho(), DISTANCIA_MENOR_CAMINHO_MIN, DISTANCIA_MENOR_CAMINHO_MAX)

    def calcular_aptidao_por_caminhos_alternativos(self):
        qtd_caminhos, distancia_media = self.calcular_caminhos_alternativos()
        aptidao_qtd_caminhos = self.calcular_desvio_padrao ( qtd_caminhos, QTD_CAMINHOS_MIN, QTD_CAMINHOS_MAX)
        aptidao_distancia_media = self.calcular_desvio_padrao ( distancia_media, DISTANCIA_MEDIA_DOS_CAMINHOS_MIN, DISTANCIA_MEDIA_DOS_CAMINHOS_MAX)
        return aptidao_qtd_caminhos,aptidao_distancia_media

    def calcular_desvio_padrao( self, valor, minimo, maximo ):
        valores_possiveis = maximo - minimo + 1 
        resultado = 0
        if( valor < minimo ):
            resultado = minimo - valor
        elif ( valor > maximo ):
            resultado = valor - maximo
        else:
            resultado = 0        
        return 100 * (resultado/valores_possiveis)

    def calcular_aptidao( self ): 
        aptidao_qtd_caminhos, aptidao_distancia_media = self.calcular_aptidao_por_caminhos_alternativos()
        aptidao_espaco_livre = self.calcular_aptidao_por_espaco_livre()
        aptidao_menor_caminho = self.calcular_aptidao_por_menor_caminho()
        aptidao = aptidao_qtd_caminhos + aptidao_distancia_media + aptidao_espaco_livre + aptidao_menor_caminho
        self.aptidao = Aptidao( aptidao_distancia_media, aptidao_qtd_caminhos, aptidao_menor_caminho, aptidao_espaco_livre, aptidao)
        print(
            "aptidao_qtd_caminhos={}\naptidao_distancia_media={}\n aptidao_espaco_livre={}\naptidao_menor_caminho={}"
            .format(aptidao_qtd_caminhos,aptidao_distancia_media,aptidao_espaco_livre,aptidao_menor_caminho)
        )        
        
    def aplicar_mutacao(self):
        listaObjetos = []
        for y in range(HALF_H):
            for x in range(W):
                if( self.mapa[y,x] != self.objetos['vazio'] ):
                    listaObjetos.append((y,x))
        
        is_remove = random.randint(0,1)
        if ( is_remove ):
            y,x = listaObjetos[ random.randint(0,(len(listaObjetos)-1)) ]
            self.mapa[y,x] = self.objetos['vazio'] 
            self.mapa[H-y-1, W-x-1] = self.objetos['vazio']
        else:
            while(True):
                y,x = random.randint(0,HALF_H-1), random.randint(0,W-1)
                if( (y,x) not in listaObjetos ):
                    break
            objeto = random.randint( 1, len(self.objetos) - 1 )
            self.mapa[y,x] = objeto 
            self.mapa[H-y-1, W-x-1] = objeto 
