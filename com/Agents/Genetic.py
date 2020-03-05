from abc import ABC
import pygame
import numpy as np

from com.Core.BaseGame import *
from com.Core.Model import *
from com.Core.Utils import *

numChrom = 7


class Genetic(BaseGame, ABC):

    def __init__(self, r_p):
        super().__init__(r_p)
        print('creazione cromosoma')
        #self.chromosome = self.createGen0(numChrom)
        self.chromosome = self.getNewChromosome()

        print('stampa cromosoma')
        print(self.chromosome)

    def get_move(self):
        return self.getGeneticMove(self.board, self.piece, self.nextPiece)

    def getGeneticMove(self, board, piece, nextPiece):

        start = time.perf_counter()

        bestRot = 0
        bestSide = 0
        bestScore = -99

        nextScore = (0, 0, -99)  # rotazione, sideway, score
        bestLine = -1
        nextLine = -1

        for rotation in range(0, len(PIECES[piece['shape']])):
            for sideway in range(-5, 6):
                move = [rotation, sideway]
                testBoard = copy.deepcopy(board)
                testPiece = copy.deepcopy(piece)
                testBoard = simulate_board(testBoard, testPiece, move)

                if testBoard is not None:
                    # sceglie la mossa migliore in combo con il pezzo successivo
                    for rotation2 in range(0, len(PIECES[piece['shape']])):
                        for sideway2 in range(-5, 6):
                            move2 = [rotation2, sideway2]
                            testBoard2 = copy.deepcopy(board)
                            testPiece2 = copy.deepcopy(nextPiece)
                            testBoard2 = simulate_board(testBoard, testPiece, move)
                            if testBoard2 is not None:
                                testScore2, nextLine = self.calTestScore(self.chromosome, testBoard2)
                                if nextScore[2] < testScore2:
                                    nextScore = [rotation2, sideway2, testScore2]
                    if bestScore < nextScore[2]:
                        bestScore = nextScore[2]
                        bestSide = sideway
                        bestRot = rotation

        finish = time.perf_counter()
        print(f'Finito in {round(finish - start, 2)} secondi')

        return [bestRot, bestSide]

        # crea un nuovo cromooma con geni random

    # restituisce il vettore con le metriche calcolate
    def getScore(self, board):
        fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol = get_parameters(
            board)
        score = [fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol]
        return score

    # serve per calcolare lo score del tetramino che si sta piazzando in base ai valori assegnati al cromosoma

    def calTestScore(self, board):
        # così mi calcolo le metriche di cui ho bisogno per l'algoritmo genetico
        score = self.getScore(board)

        testScore = float(
            (score[0] * self.chromosome[0]) - (score[1] * self.chromosome[1]) - (
                        score[2] * self.chromosome[2]) - (
                    (score[3] ** 1.5) * self.chromosome[3]) - (score[4] * self.chromosome[4]) - (
                    score[5] * self.chromosome[5]) - (score[6] * self.chromosome[6]))

        return testScore, score[0]

    # Funzione che calcola lo score pesato relativo alla board corrente

    def calculateWScore(self, board):
        score = self.getScore(board)
        wscore = 0
        for x in range(len(score)):
            # molto probabilmente è da riformulare, possibili somme e moltiplicazioni per i valori del cromosoma
            wscore -= score[x] * self.chromosome[x]
        print("Wscore = ", wscore)
        return wscore

    # funzione fitness alternativa, che tiene conto del numero di tetramini piazzati ma anche dello score finale

    def fitnessFunction(self, numTetraminoes, score):
        Newscore = (score + numTetraminoes) * 0.1
        print("***************************************** fitnessFunctionAlt = ", Newscore)
        return Newscore

    # somma i valori contenuti nel vettore vFitness, che sostanzialmente contiene i valori fitness delle varie partite
    # fatte con lo stesso cromosoma, e ne fa la media

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

    def bestChromosomeSearch(self, populationWScore, k):
        bestK = list()
        orderedChromosome = sorted(populationWScore, key=itemgetter(6), reverse=True)

        # for x in range(len(orederedChromosome)):
        #    print(chromoListToChromoStr_Scored(orederedChromosome[x])+" - Print
        #    orederedChromosomes - ")
        for x in range(k):
            orderedChromosome[x].pop(len(orderedChromosome[x]) - 1)
            bestK.append(orderedChromosome[x])
            print(chromoListToChromoStr(orderedChromosome[x]) + " - Print bestK - ")

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
        newchromosome = [0] * 6  # nuovo cromosoma vuoto
        # print("newchromosome = ",newchromosome)
        for x in range(6):
            if random.randint(0, 9) == 1:  # 10% di possibilità di prelevare il cromosoma dal Genitore 1
                newchromosome[x] = a[x]
                # print("Gene from Parent_1 =",a[x])
            elif random.randint(0, 9) == 2:  # 10% di possibilità di prelevare il cromosoma dal Genitore 2
                newchromosome[x] = b[x]
                # print("Gene from Parent_2 =",b[x])
            else:
                newchromosome[x] = (a[x] + b[
                    x]) / 2  # 80% di possibilità di prelevare il cromosoma dalla Media dei 2 Genitori
                # print("Gene from Merged genes =",newchromosome[x])
            newchromosome[x] += mutation(newchromosome[x])
        # print("newchromosome = ",newchromosome)
        return newchromosome


if __name__ == "__main__":
    caption = "Game {game}".format(game=1)
    pygame.display.set_caption(caption)

    p = Genetic('r')
    print("fuori")

    newScore, weights = p.run()
    print("Game achieved a score of: ", newScore)
    print("weights ", weights)
