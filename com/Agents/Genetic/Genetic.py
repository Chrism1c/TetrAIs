import numpy as np
import sys
import copy
from abc import ABC
from operator import itemgetter
from com.Core.BaseGame import *
from com.Utils.Utils import *
from com.Utils.fileManager import chromToStr, getPerfectChromosome


class Genetic(BaseGame, ABC):
    """
        Main class for Genetic algorithm (one object = one move), it implements abstract move() function of BaseGame
        Attributes
        ----------
                        None
        Methods
        -------
        get_expected_score(test_board)
            Calculate score of test_board
        get_move()
            Execute
        getGeneticMove(board, piece, NextPiece)
            Execute the main move of the AI
        getScore(board)
            Calculate score of board
        get_expected_score(test_board)
            Calculate score of test_board
        calculateWScore(board)
            Calculate weighted score of board
    """

    def __init__(self, r_p, chromosome, timeKiller=False):
        """
            Parameters
            ----------
            r_p : str
                type of piece used ('r' = random, 'p' = pi)
            chromosome : list
                list of weights used to identify and alterates the score function
            timeKiller : bool
                useful to stop a very good random Chromosome
        """
        super().__init__(r_p)
        self.timeKiller = timeKiller
        self.chromosome = chromosome

    def get_move(self):
        """
            Return the main function to use (getGeneticMove)
        """
        return self.getGeneticMove(self.board, self.falling_piece, self.next_piece)

    def getGeneticMove(self, board, piece, NextPiece):
        """
            Main Scanning function Deep LV2 based on DFS
            Parameters
            ----------
            board : str
                Matrix (lists of lists) of strings
            piece : Object
                conteining 'shape', 'rotation', 'x', 'y', 'color'
            NextPiece : Object
                conteining 'shape', 'rotation', 'x', 'y', 'color'
        """
        best_rot = 0
        best_sideways = 0
        best_score = - 99
        NextScore = (0, 0, -99)  # rot,sideways, score

        # rot =  1-'O':    2-'I': 2-'Z':    4-'J': 4-'L': 4-'T'
        for rot in range(0, len(PIECES[piece['shape']])):  # per le rotazioni possibili su lpezzo corrente
            for sideways in range(-5, 6):  # per i drop possibili sulla board
                move = [rot, sideways]  # salvo la coppia corrente
                test_board = copy.deepcopy(board)  # duplico la board corrente
                test_piece = copy.deepcopy(piece)  # duplico il pezzo corrente
                test_board = simulate_board(test_board, test_piece, move)  # simulo il pezzo e la mossa sulla board test
                # Check NEXT
                if test_board is not None:  # se la simulazione è andata a buon fine
                    # Chose the best after next,  effettuo il calcolo con il pezzo successivo
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

        return [best_rot, best_sideways]

    # restituisce il vettore con le metriche calcolate
    def getScore(self, board):
        """
            Calculate score of board
            # serve per calcolare lo score del tetramino che si sta piazzando in base ai valori assegnati al cromosoma
            # restituisce il vettore con le metriche calcolate
            Parameters
            ----------
                  board : Matrix (lists of lists) of strings
        """
        fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol = get_parameters(
            board)
        score = [fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol]
        return score

    def get_expected_score(self, test_board):
        """
            Calculate score of test_board with fixed weights
            # serve per calcolare lo score del tetramino che si sta piazzando in base ai valori assegnati al cromosoma
            Parameters
            ----------
                  test_board : Matrix (lists of lists) of strings
        """
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * self.chromosome[0]) - (vHoles * self.chromosome[1]) - (vBlocks * self.chromosome[2]) -
            (maxHeight * self.chromosome[3]) - (stdDY * self.chromosome[4]) - (absDy * self.chromosome[5]) -
            (maxDy * self.chromosome[6]))
        return test_score, fullLines

    def calculateWScore(self, board):
        """
            Calculate weighted score of board
            # Funzione che calcola lo score pesato relativo alla board corrente
            Parameters
            ----------
                  board : Matrix (lists of lists) of strings
        """
        score = self.getScore(board)
        wscore = 0
        for x in range(len(score)):
            # molto probabilmente è da riformulare, possibili somme e moltiplicazioni per i valori del cromosoma
            wscore -= score[x] * self.chromosome[x]
        print("Wscore = ", wscore)
        return wscore


def perfectRun(pieceType):
    """
        Execute run of the Perfect Chromosome
        Parameters
        ----------
        pieceType : str
            type of piece used ('r' = random, 'p' = pi)
    """
    perfectChromosome = getPerfectChromosome()  # import del chromosoma perfetto da file
    r_p = pieceType
    if perfectChromosome is not None:
        gen = Genetic(r_p, perfectChromosome)
        newScore, _ = gen.run()
        print("Game achieved a score of: ", newScore)
        menu.main()
    else:
        print("Needs to be Trained!")
        exit(0)


if __name__ == "__main__":
    perfectRun(sys.argv[1])
