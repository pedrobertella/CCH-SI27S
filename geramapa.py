import random
import numpy

mapXSize = 21
mapYSize = 32

# P = parede, C = caixa, B = barreira, E = pedra, O = poste, A = agua, N = cone;
obstaculos = ["P", "C", "B", "E", "O", "A", "N"]
livre = "0"

map = []
for x in range(mapXSize):
    line = []

    for y in range(mapYSize):
        n = random.randint(0,1)
        if n == 0:
            line.append(livre)
        else:
            line.append(obstaculos[random.randint(0,6)])

    map.append(line)

for x in map:
    for y in x:
        print(y, end="")
    print("")