import random
import numpy

mapXSize = 32
mapXHalfSize = 16
mapYSize = 21

# P = parede, C = caixa, B = barreira, E = pedra, O = post_, N = cone;
obstaculos = ["P", "C", "B", "E", "O", "N"]
agua = "~"
livre = " "

map = []

#gerando metade do mapa aleatoria
for x in range(0, mapXHalfSize, 1):
    line = []
    for y in range(0, mapYSize, 1):
        n = random.randint(0,1)
        if n == 0:#0=livre 1=obstaculo/agua 
            line.append(livre)
        else: 
            if(random.randint(1,7)<2):#verificar se vai ser água ou obstaculo
                line.append(agua)
            else:
                line.append(obstaculos[random.randint(0,5)])

    map.append(line)

#espelhando metade de cima para baixo
for x in range(mapXHalfSize-1, -1, -1):
    line = []
    for y in map[x]:
        line.append(y)

    map.append(line)

#print do mapa
for i in range(mapYSize+2): 
    print("#" , end="")
print("")

for x in map:
    print("#", end="")
    for y in x:
        print(y, end="")
    print("#")

for i in range(mapYSize+2): 
    print("#" , end="")
print("")

