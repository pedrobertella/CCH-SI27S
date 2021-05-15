import random
import numpy as np

W = 21
H = 32
halfH = np.floor(H/2)

objetos = {
    'vazio': 0,
    'parede': 1,
    'agua': 2,
    'vegetacao': 3,
}

mapa = np.zeros( (H, W), dtype=np.uintc )

def calcularVizinhanca( y,x ):
    objCount= np.zeros( len(objetos), dtype=np.uintc ) 

    for i in [-1,0,1]:
        for j in [-1,0,1]:

            if( (i == 0 or j == 0) 
            and not (i == 0 and j == 0) 
            and 0 <= y+i < H 
            and 0 <= x+j < W ):
                objCount[ mapa[ y+i, x+j ] ] += 1

    return objCount

#posicionando objetos no mapa
qtdObjetos = {
    'agua': 3,
    'parede': 5,
    'vegetacao':3,
}

for k in qtdObjetos:
    for count in range(qtdObjetos[k]):

        while( True ):
            y,x = (random.randint(0,halfH-1), random.randint(0,W-1))

            if( mapa[y,x] == objetos['vazio']):
                mapa[y,x] = objetos[k]
                break

#espelhando metade de cima para baixo
for y in range(len(mapa)):
    for x in range(len(mapa[y])):
        if( y < (len(mapa)/2) ):
            continue

        te = (16)-(y-(16))
        mapa[y,x] = mapa [te,x]

#expandindo os objetos
for i in range(2):
    novoMapa = mapa.copy()
    
    for y in range(len(mapa)):
        for x in range(len(mapa[y])):

            if( mapa[y,x] == objetos['vazio'] ): 
                vizinhanca = calcularVizinhanca(y,x)
                
                for k in objetos:
                    if( k != 'vazio' and vizinhanca[objetos[k]] > 0 ):
                        novoMapa[y,x] = objetos[k]

    mapa = novoMapa
                
#print do mapa
objetosSprintes = {
    objetos['vazio']: ' ' ,
    objetos['agua']: '~', 
    objetos['parede']: '#', 
    objetos['vegetacao']: '´', 
}

for i in range(H+2): 
    print("#" , end="")
print("")

for x in mapa:
    print("#", end="")
    for cell in x:
        print(objetosSprintes[cell], end="")
    print("#")

for i in range(H+2): 
    print("#" , end="")
print("")

