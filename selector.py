import random

class RankedSelector:
    def __init__(self, populacao, min, max):
        self.populacao = populacao
        self.min = min
        self.max = max

    def expVal(self, i):
        return (self.min + ((self.max - self.min) * ((i-1)/(len(self.populacao) -1))))

    def selecionar_individuo(self):
        total = (self.min + self.max) * ((len(self.populacao))/2)
        numeroSelecionado = random.randint(self.min, total)
        
        soma = 0
        for i in range(len(self.populacao)):
            soma += self.expVal(i+1)
            if (numeroSelecionado <= soma):
                return self.populacao[i]
