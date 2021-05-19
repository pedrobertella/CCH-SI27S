import csv
from aptidao import Aptidao
from datetime import date

class Export(object):
    def __init__(self, generation, aptidao: Aptidao):
        strCSV = "logBook"
        with open(strCSV + '.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile,
                                        delimiter=',',
                                        quotechar='|',
                                        quoting=csv.QUOTE_MINIMAL)
            if(generation == 0):
                 spamwriter.writerow(["Generation", "Aptidao", "Aptidao Caminhos","Média Caminhos", "Melhor Caminho", "Aptidao Espacial"])
            spamwriter.writerow([generation, aptidao.aptidao, aptidao.caminhos,aptidao.media, aptidao.melhor_caminho, aptidao.aptidao_espacial])

class ExportTime(object):
    def __init__(self, tempo_execucao):
        strCSV = "logBook"
        with open(strCSV + '.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile,
                                        delimiter=',',
                                        quotechar='|',
                                        quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["Tempo de execução",tempo_execucao])