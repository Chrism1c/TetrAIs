from com.Core.BaseGame import BaseGame
from abc import ABC
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES
from com.Menu import menu
from com.Utils.sidePanel import *
import sys


class LocalSearch(BaseGame, ABC):
    """
        Main class for LS search algorithm (one object = one move), it implements abstarct move() function of BaseGame
        Attributes
        ----------
                        None
        Methods
        -------
        get_move(board, piece, NextPiece)
            Execute the main method to get the move according to the LS AI
        find_best_moveLS(board, piece,NextPiece)
            It finds the best move to do according to the passed weights
        get_expected_score(test_board)
            It calculates the score on the test board
    """

    def __init__(self, r_p, gdSidePanel):
        """
        :param r_p: str
                type of piece used ('r' = random, 'p' = pi)
        """
        super().__init__(r_p, gdSidePanel, title=titleLS, description=descriptionLS)

    def get_move(self):
        """
        Return the main function to use (find_best_moveLS)
        :return:
        """
        return self.find_best_moveLS(self.board, self.falling_piece, self.next_piece)

    def find_best_moveLS(self, board, piece, NextPiece):
        """
         It finds the best move to do according to the passed weights

        :param board:  Matrix (lists of lists) of strings
        :param piece:  Object containing: 'shape', 'rotation', 'x', 'y', 'color'
        :param NextPiece: Object containing: 'shape', 'rotation', 'x', 'y', 'color'
        :return:strategy2: a list that contains rot and sideway
        """
        print("Current Piece: ", piece['shape'])
        strategy = (0, 0, -999)
        best_board = None
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)
                if test_board is not None:
                    test_score, fullLines = self.get_expected_score(test_board)
                    print("Tested branch : LV1 [ rot= ", rot, "/sideway=", sideways, "] : scored = ",
                          round(test_score, 3))
                    if not strategy or strategy[2] < test_score:
                        print("updated new max LV1")
                        strategy = (rot, sideways, test_score)
                        best_board = test_board
        print("--> LV1 Winner is: ", strategy)

        print(" Next Piece : ", NextPiece['shape'])
        strategy2 = (0, 0, -999)
        for rot in range(0, len(PIECES[NextPiece['shape']])):
            for sideways in range(-5, 6):
                move2 = [rot, sideways]
                test_board2 = copy.deepcopy(best_board)
                test_piece2 = copy.deepcopy(NextPiece)
                test_board2 = simulate_board(test_board2, test_piece2, move2)
                if test_board2 is not None:
                    test_score2, fullLines2 = self.get_expected_score(test_board2)
                    print("Tested branch : LV2 [ rot= ", rot, "/sideway=", sideways, "] : scored = ",
                          round(test_score2, 3))
                    if not strategy2 or strategy2[2] < test_score2:
                        print("updated = new max LV2")
                        strategy2 = (rot, sideways, test_score2)
        print("----> LV2 Winner is: ", strategy2, "\n")

        return [strategy2[0], strategy2[1]]

    def get_expected_score(self, test_board):
        """
        It calculates the score on the test board
        :param test_board: Matrix (lists of lists) of strings
        :return: test_score: it contains the score of the passed test_board
                 fullLines: an int variable containing the number of cleared lines
        """
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.002) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines


def ls_main(r_p, numOfRun, gdSidePanel):
    #  loop to run  the game with AI for numOfRun executions
    numOfRun = int(numOfRun)
    AVG_runs = 0
    for x in range(numOfRun):
        ls = LocalSearch(r_p, gdSidePanel)
        newScore, weights, tot_time, n_tetr, avg_move_time, tetr_s = ls.run()
        AVG_runs = AVG_runs + newScore
        print("Game achieved a score of: ", newScore)
        print("weights: ", weights)
        print("tot run time: ", tot_time)
        print("#moves:  ", n_tetr)
        print("avg time per move: ", avg_move_time)
        print("moves/sec:  ", tetr_s)
    AVG_runs = AVG_runs / numOfRun
    if numOfRun > 1:
        print("AVGScore after ", numOfRun, " Runs : ", AVG_runs)


if __name__ == "__main__":
    ls_main('r', 1)
