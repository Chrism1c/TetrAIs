import numpy as np
import sys
import copy
from abc import ABC
from operator import itemgetter
from com.Core.BaseGame import *
from com.Utils.Utils import *
from com.Utils.fileManager import chromToStr, getPerfectChromosome




class Genetic(BaseGame, ABC):

    def __init__(self, r_p, chromosome, timeKiller = False):
        super().__init__(r_p)
        self.timeKiller = timeKiller
        #print('creazione cromosoma')
        # self.chromosome = self.createGen0(numChrom)
        # self.chromosome = self.getNewChromosome()
        self.chromosome = chromosome
        #print('stampa cromosoma')
        #print(self.chromosome)


    def get_move(self):
        return self.getGeneticMove(self.board, self.falling_piece, self.next_piece)

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
                                testScore2, nextLine = self.calTestScore(testBoard2)
                                if nextScore[2] < testScore2:
                                    nextScore = [rotation2, sideway2, testScore2]
                    if bestScore < nextScore[2]:
                        bestScore = nextScore[2]
                        bestSide = sideway
                        bestRot = rotation

        finish = time.perf_counter()
        #print(f'Finito in {round(finish - start, 2)} secondi')

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
            (score[0] * self.chromosome[0]) - (score[1] * self.chromosome[1]) - (score[2] * self.chromosome[2]) - (
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

def perfectRun():
    perfectChromosome = getPerfectChromosome()     #import del chromosoma perfetto da file
    #r_p = sys.argv[1]
    r_p = 'r'
    if perfectChromosome is not None:
        gen = Genetic(r_p, perfectChromosome)
        newScore, _ = gen.run()
        print("Game achieved a score of: ", newScore)
    else:
        print("Needs to be Trained!")
        exit(0)

if __name__ == "__main__":
    perfectRun()