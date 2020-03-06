from com.Agents.Genetic.Genetic import Genetic
from com.Utils.fileManager import *
import numpy as np
import random
import time
from operator import itemgetter

class GeneticController:

    def __init__(self, r_p, numGen):
        self.r_p = r_p
        self.numGen = int(numGen)
        self.numRun = 5
        self.dimChromomsome = 7
        self.generation = list()
        self.population = list()
        #self.bello = np.array([1.8, 1, 0.5, 1.5, 0.01, 0.2, 0.3])

    def workGenetic(self):
        print("start creation gen:0")
        numGen0 = 2**self.numGen
        self.generation = self.createGen0(numGen0)
        #self.generation = self.createGen01(numGen0)
        print("end creation gen0")
        i = 0
        while True:
            print("start gen:", i)
            population = list()
            for x in range(len(self.generation)):
                avgScoreChromosome = self.AVGfitnesingSing(self.generation[x])
                population.append((self.generation[x], avgScoreChromosome))
                print("Gen ", i, " Run ", x, " AvgScore ", str(avgScoreChromosome))
            #k = round(len(self.generation)/2)
            k = len(self.generation)
            self.generation = self.crossingPopulation(self.bestChromosomeSearch(population, k), k)
            print("end gen:", i)
            i += 1
            #save
            for x in range(len(population)):
                self.population.append(population[x])
            print(len(self.generation))
            if len(self.generation) == 1:
                break
            else:
                continue
        saveOnFile(fileName, self.generation)
        print('end training')

    # funzione fitness alternativa, che tiene conto del numero di tetramini piazzati ma anche dello score finale

    def fitnessFunction(self, numTetraminoes, score):
        Newscore = (score + numTetraminoes) * 0.1
        print("***************************************** fitnessFunctionAlt = ", Newscore)
        return Newscore

    # somma i valori contenuti nel vettore vFitness, che sostanzialmente contiene i valori fitness delle varie partite
    # fatte con lo stesso cromosoma, e ne fa la media

    def AVGfitnesingSing(self, chromosome):
        # global TETRIS_AI_GENETIC
        # TETRIS_AI_GENETIC = TetrisAIGenetic(chromosome)
        #strChromosome = chromToStr(chromosome, self.dimChromomsome)
        avgFitness = 0
        for i in range(self.numRun):
            g = Genetic(self.r_p, chromosome, True)
            start = time.time()
            score, weights = g.run()
            finish = time.time()
            tempo = round(finish - start)
            avgFitness += (score + tempo)
            print(' - Match ' + str(i) + ' Score ' + str(score + tempo))
        return avgFitness / self.numRun

    def avgFitness(self, vFitness):
        mFitness = 0
        for x in vFitness:
            mFitness += vFitness[x]
        return mFitness / len(vFitness)

    def getNewChromosome(self):
        return np.random.uniform(low=0.0, high=1.0, size=7)

    # Create Gen0

    def createGen0(self, num):
        gen0 = list()
        self.num = num

        for i in range(num):
            gen0.append(self.getNewChromosome())

        return gen0

    # Serch top k best Chromosome (based on score)

    def bestChromosomeSearch(self, population, k):
        bestK = list()
        orderedChromosome = sorted(population, key=itemgetter(1), reverse=True)

        # for x in range(len(orederedChromosome)):
        #    print(chromoListToChromoStr_Scored(orederedChromosome[x])+" - Print
        #    orederedChromosomes - ")
        for x in range(k):
            chromosome, _ = orderedChromosome[x]
            bestK.append(chromosome)
            print(chromToStr(chromosome, self.dimChromomsome) + " - Print bestK - ")
        return bestK

    def kChoice(self, populationWScore):

        orderedPopulation = sorted(populationWScore, key=itemgetter(6), reverse=True)
        lenP = len(orderedPopulation)
        avgScore = 0
        k = 0
        pow2 = [2 ** x for x in range(0, 7)]
        for x in range(lenP):
            avgScore += orderedPopulation[x][6]
        avgScore /= lenP
        print(avgScore)
        for x in range(lenP):
            if orderedPopulation[x][6] >= avgScore:
                k += 1
        print(k)
        pow2.append(k)
        pow2.sort()
        indexK = pow2.index(k)
        k = pow2[indexK + 1]
        print(k)
        return k

    def mutation(self, a):
        if random.randint(1, 10) == 10:  # 10% di possibilità di mutazione
            if a >= 4.5 and a <= 5.0:
                return -0.1 * random.randint(1, 5)
            else:
                return 0.1 * random.randint(1, 5)
        else:
            return 0  # 90% di possibilità di non mutazione

        # Crossing Chromosoma function

    def crossingchromosome(self, a, b):

        # print("crossingfunction ")
        # print("a = ",a)
        # print("b = ",b)
        newchromosome = [0] * self.dimChromomsome  # nuovo cromosoma vuoto
        # print("newchromosome = ",newchromosome)
        for x in range(self.dimChromomsome):
            if random.randint(0, 9) == 1:  # 10% di possibilità di prelevare il cromosoma dal Genitore 1
                newchromosome[x] = a[x]
                # print("Gene from Parent_1 =",a[x])
            elif random.randint(0, 9) == 2:  # 10% di possibilità di prelevare il cromosoma dal Genitore 2
                newchromosome[x] = b[x]
                # print("Gene from Parent_2 =",b[x])
            else:
                # 80% di possibilità di prelevare il cromosoma dalla Media dei 2 Genitori
                newchromosome[x] = (a[x] + b[x]) / 2
                # print("Gene from Merged genes =",newchromosome[x])
            newchromosome[x] += self.mutation(newchromosome[x])
        # print("newchromosome = ",newchromosome)
        return newchromosome

    def crossingPopulation(self, population, k):
        newPopulation = list()
        for x in range(0, int(k - 1), 2):
            newPopulation.append(self.crossingchromosome(population[x], population[x - 1]))
        return newPopulation

    def createGen01(self, num):
        gen0 = list()
        self.num = num
        for i in range(num):
            gen0.append(self.bello)
        return gen0


