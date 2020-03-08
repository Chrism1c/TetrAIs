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

    def getGeneticMove(self, board, piece, NextPiece):
        ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
        # start = time.perf_counter()  # salvo il tempo di partenza

        best_rot = 0
        best_sideways = 0
        best_score = - 99

        NextScore = (0, 0, -99)  # rot,sideways, score
        bestLines = -1
        nextLines = -1

        # rot =  1-'O':    2-'I': 2-'Z':    4-'J': 4-'L': 4-'T'

        for rot in range(0, len(PIECES[piece['shape']])):  # per le rotazioni possibili su lpezzo corrente
            for sideways in range(-5, 6):  # per i drop possibili sulla board
                move = [rot, sideways]  # salvo la coppia corrente
                test_board = copy.deepcopy(board)  # duplico la board corrente
                test_piece = copy.deepcopy(piece)  # duplico il pezzo corrente
                test_board = simulate_board(test_board, test_piece, move)  # simulo il pezzo e la mossa sulla board test
                # Check NEXT
                if test_board is not None:  # se la simulazione è andata a buon fine
                    ## Chose the best after next                                # effettuo il calcolo con il pezzo successivo
                    for rot2 in range(0, len(PIECES[NextPiece['shape']])):
                        for sideways2 in range(-5, 6):
                            move2 = [rot2, sideways2]
                            test_board2 = copy.deepcopy(test_board)
                            test_piece2 = copy.deepcopy(NextPiece)
                            test_board2 = simulate_board(test_board2, test_piece2, move2)
                            if test_board2 is not None:
                                test_score2, nextLines = self.get_expected_score(test_board2)
                                if NextScore[2] < test_score2:
                                    NextScore = [rot2, sideways2, test_score2]  # aggiorno il best local score (LV2)
                    if best_score < NextScore[2]:  # confronto
                        best_score = NextScore[2]  # aggiorno il best local score (LV1+LV2)
                        best_sideways = sideways  # aggiorno il best sideway (LV1)
                        best_rot = rot  # aggiorno il best rot (LV1)

        # finish = time.perf_counter()
        # print(f'Finished in {round(finish - start, 2)} second(s) with full')

        return [best_rot, best_sideways]

        # crea un nuovo cromooma con geni random

    # restituisce il vettore con le metriche calcolate
    def getScore(self, board):
        fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol = get_parameters(
            board)
        score = [fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol]
        return score

    # serve per calcolare lo score del tetramino che si sta piazzando in base ai valori assegnati al cromosoma

    def get_expected_score(self, test_board):
        ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 2 * self.chromosome[0]) - (vHoles * self.chromosome[1]) - (vBlocks * self.chromosome[2]) -
            ((maxHeight ** 1.5) * self.chromosome[3]) - (stdDY * self.chromosome[4]) - (absDy * self.chromosome[5]) -
            (maxDy * self.chromosome[6]))
        return test_score, fullLines

    # Funzione che calcola lo score pesato relativo alla board corrente

    def calculateWScore(self, board):
        score = self.getScore(board)
        wscore = 0
        for x in range(len(score)):
            # molto probabilmente è da riformulare, possibili somme e moltiplicazioni per i valori del cromosoma
            wscore -= score[x] * self.chromosome[x]
        print("Wscore = ", wscore)
        return wscore

def perfectRun(pieceType):
    perfectChromosome = getPerfectChromosome()     #import del chromosoma perfetto da file
    r_p = pieceType
    if perfectChromosome is not None:
        gen = Genetic(r_p, perfectChromosome)
        newScore, _ = gen.run()
        print("Game achieved a score of: ", newScore)
    else:
        print("Needs to be Trained!")
        exit(0)

if __name__ == "__main__":
    perfectRun(sys.argv[1])