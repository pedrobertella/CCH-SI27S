import random
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

W = 21
H = 32
PLAYER_POS_Y = np.floor(W/2).astype(int)
PLAYER_POS_X = 0
OBJECTIVE_POS_Y = np.floor(W/2).astype(int)
OBJECTIVE_POS_X = np.floor(H/2).astype(int)
halfH = np.floor(H/2)

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

    fator_de_expancao = 2

    def __init__(self):
        self.mapa = np.zeros( (H, W), dtype=np.uintc )
        self.aptidao = 0

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
                    y,x = (random.randint(0,halfH-1), random.randint(0,W-1))

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

    def calcular_menor_caminho(self):         
        grid = Grid(matrix=self.converter_mapa_to_grid())

        start = grid.node(PLAYER_POS_Y, PLAYER_POS_X)
        end = grid.node(OBJECTIVE_POS_Y, OBJECTIVE_POS_X)

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        
        Grid.cleanup
        print('operations:', runs, 'path length:', len(path))
        print(grid.grid_str(path=path, start=start, end=end))
        return len(path)

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
        for i in range(H+2): 
            print("#" , end="")
        print("")

        for x in mapa:
            print("#", end="")
            for cell in x:
                print(self.objetosSprites[cell], end="")
            print("#")

        for i in range(H+2): 
            print("#" , end="")
        print("")

    def calcular_aptidao( self ):
        self.aptidao = abs(25 - self.calcular_menor_caminho())
        
