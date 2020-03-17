from com.Core.BaseGame import BaseGame
from abc import ABC
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES
import sys,time

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

    def __init__(self, r_p):
        """
        :param r_p: str
                type of piece used ('r' = random, 'p' = pi)
        """
        super().__init__(r_p)

    def get_move(self):
        """
        Return the main function to use (find_best_moveLS)
        :return:
        """
        return self.find_best_moveLS(self.board, self.falling_piece, self.next_piece)


    def find_best_moveLS(self, board, piece,NextPiece):
        """
         It finds the best move to do according to the passed weights

        :param board:  Matrix (lists of lists) of strings
        :param piece:  Object containing: 'shape', 'rotation', 'x', 'y', 'color'
        :param NextPiece: Object containing: 'shape', 'rotation', 'x', 'y', 'color'
        :return:strategy2: a list that contains rot and sideway
        """
        ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi

        #print("-----------------------------------------------------------------------------")
        #print("******************************* ",piece['shape'],"   *********************************")
        ### Cerco il max locale LV1
        strategy = (0,0,-999)
        best_board = None
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)
                if test_board is not None:
                    test_score, fullLines = self.get_expected_score(test_board)
                    #print(move," -- ",strategy[2],"<", test_score)
                    if not strategy or strategy[2] < test_score:
                        #print("update = new max LV1")
                        strategy = (rot, sideways, test_score)
                        best_board = test_board

        #print("LV1 Winner is: ",strategy)
        #time.sleep(2)
        #print("******************************* ", NextPiece['shape'], "   *********************************")
        ### Cerco il Max Locale LV2
        strategy2 = (0,0,-999)
        for rot in range(0, len(PIECES[NextPiece['shape']])):
            for sideways in range(-5, 6):
                move2 = [rot, sideways]
                test_board2 = copy.deepcopy(best_board)
                test_piece2 = copy.deepcopy(NextPiece)
                test_board2 = simulate_board(test_board2, test_piece2, move2)
                if test_board2 is not None:
                    test_score2, fullLines2 = self.get_expected_score(test_board2)
                    #print(move2," -- ", strategy2[2], "<", test_score2)
                    if not strategy2 or strategy2[2] < test_score2:
                        #print("update = new max LV2")
                        strategy2 = (rot, sideways, test_score2)

        #print("LV2 Winner is: ", strategy2)
        #finish = time.perf_counter()
        #print(f'Finished in {round(finish - start, 2)} second(s) with LV1Only')

        return [strategy2[0], strategy2[1]]


    def get_expected_score(self, test_board):
        """
        It calculates the score on the test board
        :param test_board: Matrix (lists of lists) of strings
        :return: test_score: it contains the score of the passed test_board
                 fullLines: an int variable containing the number of cleared lines
        """
        ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.002) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines


if __name__ == "__main__":
    #  get arguments when AI file is executed by the menu
    r_p = sys.argv[1]
    numOfRun = int(sys.argv[2])
    #  loop to run  the game with AI for numOfRun executions
    for x in range(numOfRun):
        ls = LocalSearch(r_p)
        newScore, weights = ls.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)
