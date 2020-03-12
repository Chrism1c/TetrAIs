from com.Core.BaseGame import BaseGame
from abc import ABC
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES
import sys


class DeepFirstSearch(BaseGame, ABC):
    def __init__(self, r_p, lv):
        super().__init__(r_p)
        self.lv = lv

    def get_move(self):
        if self.lv == 'LV1':
            return self.DFS_LV1Only(self.board, self.falling_piece)
        else:
            return self.DFS_full(self.board, self.falling_piece, self.next_piece)

    def DFS_full(self, board, piece, NextPiece):
        ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
        # start = time.perf_counter()  # salvo il tempo di partenza

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


    def DFS_LV1Only(self, board, piece):
        ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
        # start = time.perf_counter()

        strategy = None
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)
                if test_board is not None:
                    test_score = self.get_expected_score(test_board)
                    if not strategy or strategy[2] < test_score:
                        strategy = (rot, sideways, test_score)

        # finish = time.perf_counter()
        # print(f'Finished in {round(finish - start, 2)} second(s) with LV1Only')

        return [strategy[0], strategy[1]]

    def get_expected_score(self, test_board):
        ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.002) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines


if __name__ == "__main__":
    r_p = sys.argv[1]
    lv = sys.argv[2]
    numOfRun = int(sys.argv[3])
    for x in range(numOfRun):
        dfs = DeepFirstSearch(r_p,lv)
        newScore, weights = dfs.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)
