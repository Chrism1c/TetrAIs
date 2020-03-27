from com.Core.BaseGame import BaseGame
from abc import ABC
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Utils.NetworkX import *
from com.Core.Model import PIECES
from com.Menu import menu
from com.Utils.sidePanel import *
import sys

#  Create a new istance of TreePlot
DFSTreePlot = TreePlot()

class DeepFirstSearch(BaseGame, ABC):
    global DFSTreePlot
    """
        Main class for DFS search algorithm (one object = one move), it implements abstarct move() function of BaseGame
        Attributes
        ----------
                        None
        Methods
        -------
        get_move(board, piece, NextPiece)
            Execute DFS_full or  DFS_LV1Only
        DFS_full()
            Execute DFS at level 2 of depth
        DFS_LV1Only(board, piece)
            Execute DFS at level 1 of depth
        get_expected_score(test_board)
            Calculate score of test_board
    """

    def __init__(self, r_p, gdSidePanel, lv, treePlot):
        """
            Parameters
            ----------
            r_p : str
                type of piece used ('r' = random, 'p' = pi)
            lv : str
                type of function to use (LV1 or LV2)
            treePlot : TreePlot
                instance of TreePlot object to print Tree Graphs
        """
        super().__init__(r_p, gdSidePanel, title=titleDFS, description=descriptionDFS)
        self.lv = lv
        self.treePlot = treePlot

    def get_move(self):
        """
            Return the function to use (DFS Lv1 or DFS Lv2)
            Parameters
            ----------
                        None
        """
        if self.lv == 'LV1':
            return self.DFS_LV1Only(self.board, self.falling_piece)
        else:
            return self.DFS_full(self.board, self.falling_piece, self.next_piece)


    def DFS_full(self, board, piece, NextPiece):
        """
            Execute DFS at level 2 of depth
            Parameters
            ----------
                  board : Matrix (lists of lists) of strings
                  piece : Object conteining: 'shape', 'rotation', 'x', 'y', 'color'
                  NextPiece : Object conteining: 'shape', 'rotation', 'x', 'y', 'color'
        """
        best_rot = 0
        best_sideways = 0
        best_score = - 99
        NextScore = (0, 0, -99)  # rot, sideways, score
        # rot =  1-'O':    2-'I': 2-'Z':    4-'J': 4-'L': 4-'T'
        print("Shape: ", piece['shape'])
        for rot in range(0, len(PIECES[piece['shape']])):  # per le rotazioni possibili su lpezzo corrente
            for sideways in range(-5, 6):  # per i drop possibili sulla board
                move = [rot, sideways]  # salvo la coppia corrente
                test_board = copy.deepcopy(board)  # duplico la board corrente
                test_piece = copy.deepcopy(piece)  # duplico il pezzo corrente
                test_board = simulate_board(test_board, test_piece, move)  # simulo il pezzo e la mossa sulla board test
                # Check NEXT

                fatherName = str(piece['shape'] + ":" + str(sideways) + ":" + str(0))
                DFSTreePlot.addedge(DFSTreePlot.ROOTZERO, fatherName)

                if test_board is not None:
                    for rot2 in range(0, len(PIECES[NextPiece['shape']])):
                        for sideways2 in range(-5, 6):
                            move2 = [rot2, sideways2]
                            test_board2 = copy.deepcopy(test_board)
                            test_piece2 = copy.deepcopy(NextPiece)
                            test_board2 = simulate_board(test_board2, test_piece2, move2)
                            NameNode = str(NextPiece['shape'] + ":" + str(sideways2) + ":" + str(1))
                            DFSTreePlot.addedge(fatherName, fatherName + "_" + NameNode)
                            if test_board2 is not None:
                                test_score2, nextLines = self.get_expected_score(test_board2)
                                print("Tested branch : LV1[ rot= ", rot, "/sideway=", sideways, "] : LV2[ rot2= ",
                                      rot2, "/sideway2=", sideways2, "] : scored = ",
                                      round(test_score2,3))
                                if NextScore[2] < test_score2:
                                    NextScore = [rot2, sideways2, test_score2]  # aggiorno il best local score (LV2)
                    if best_score < NextScore[2]:  # confronto
                        best_score = NextScore[2]  # aggiorno il best local score (LV1+LV2)
                        best_sideways = sideways  # aggiorno il best sideway (LV1)
                        best_rot = rot  # aggiorno il best rot (LV1)

        if self.treePlot == 'yes':
            DFSTreePlot.plot()
            DFSTreePlot.Graph.clear()

        print("-- Winner Strategy = <", best_rot, "/", best_sideways, ">\n")
        return [best_rot, best_sideways]


    def DFS_LV1Only(self, board, piece):
        """
            Execute DFS at level 1 of depth
            Parameters
            ----------
                  board : Matrix (lists of lists) of strings
                  piece : Object containing: 'shape', 'rotation', 'x', 'y', 'color'
        """
        print("Shape: ",piece['shape'])
        strategy = None
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)
                DFSTreePlot.addedge(DFSTreePlot.ROOTZERO, str(piece['shape'] + ":" + str(sideways) + ":" + str(0)))
                if test_board is not None:
                    test_score, _ = self.get_expected_score(test_board)
                    print("Tested branch : [ rot= ",rot ,"/sideway=",sideways,"] : scored = ",round(test_score,3))
                    if not strategy or strategy[2] < test_score:
                        strategy = (rot, sideways, test_score)

        if self.treePlot == 'yes':
            DFSTreePlot.plot()
            DFSTreePlot.Graph.clear()

        print("-- Winner Strategy = <", strategy[0], "/", strategy[1], ">\n")
        return [strategy[0], strategy[1]]

    def get_expected_score(self, test_board):
        """
            Calculate score of test_board
            Parameters
            ----------
                  test_board : Matrix (lists of lists) of strings
        """
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.002) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines


def dfs_main(r_p, lv, numOfRun, treePlot, gdSidePanel):
    #  loop to run  the game with AI for numOfRun executions
    numOfRun = int(numOfRun)
    for x in range(numOfRun):
        dfs = DeepFirstSearch(r_p, gdSidePanel, lv, treePlot)
        newScore, weights, tot_time, n_tetr, avg_move_time, tetr_s = dfs.run()
        print("Game achieved a score of: ", newScore)
        print("weights: ", weights)
        print("tot run time: ", tot_time)
        print("#moves:  ", n_tetr)
        print("avg time per move: ", avg_move_time)
        print("moves/sec:  ", tetr_s)



if __name__ == "__main__":
    dfs_main('r', 'LV1', 1, 'no')
