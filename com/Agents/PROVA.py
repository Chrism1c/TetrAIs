from com.Core.BaseGame import BaseGame
from com.Utils.KnowledgeBase import *
from com.Core.Model import BOARDHEIGHT, BOARDWIDTH, is_on_board
import sys
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES
import random
from pyswip import Prolog
prolog = Prolog()
prolog.consult("com/Utils/Kb.pl");



class RuleBased(BaseGame):
    def __init__(self, r_p):
        super().__init__(r_p)
        self.crest = [0]*BOARDWIDTH                 #cresta relativa

    def get_move(self):
        #self.update_crest(self.get_heights(self.board))
        self.crest = self.get_heights(self.board)
        self.writePCrest(self.get_Pcrest())
        #return self.align(self.get_move_by_rule(self.falling_piece, self.get_Pcrest()), self.falling_piece)
        return self.get_move_by_rule()()

    def simulate_move(self, move, piece):
        test_board = copy.deepcopy(self.board)
        test_piece = copy.deepcopy(piece)
        test_board = simulate_board(test_board, test_piece, move)
        if test_board is not None:
            test_score, _ = self.get_expected_score(test_board)
            return test_score
        else:
            return -99

    def align(self, move, piece):
        rot = move[0]
        sideway = move[1]
        if piece['shape'] == 'S' or piece['shape'] == 'Z' or piece['shape'] == 'I':
            new_rot = abs(rot - piece['rotation'])
        elif piece['shape'] == 'J' or piece['shape'] == 'L' or piece['shape'] == 'T':
            if piece['rotation'] == 3:
                if rot == 3:
                    new_rot = 0
                elif rot == 2:
                    new_rot = 3
                elif rot == 1:
                    new_rot = 2
                else:
                    new_rot = 1
            if piece['rotation'] == 2:
                if rot == 3:
                    new_rot = 1
                elif rot == 2:
                    new_rot = 0
                elif rot == 1:
                    new_rot = 3
                else:
                    new_rot = 2
            if piece['rotation'] == 1:
                if rot == 3:
                    new_rot = 2
                elif rot == 2:
                    new_rot = 3
                elif rot == 1:
                    new_rot = 0
                else:
                    new_rot = 1
            else:
                new_rot = rot
        else:
            new_rot = 0

        new_sideway = sideway - 5
        return[new_rot, new_sideway]


    def get_move_by_rule(self, piece):
        query = list()
        if piece['shape'] == 'S':
            query.append('bestFit(s0, X0)')
            query.append('bestFit(s1, X1)')
        elif piece['shape'] == 'Z':
            query.append('bestFit(z0, X0)')
            query.append('bestFit(z1, X1)')
        elif piece['shape'] == 'J':
            query.append('bestFit(j0, X0)')
            query.append('bestFit(j1, X1)')
            query.append('bestFit(j2, X2)')
            query.append('bestFit(j3, X3)')
        elif piece['shape'] == 'L':
            query.append('bestFit(l0, X0)')
            query.append('bestFit(l1, X1)')
            query.append('bestFit(l2, X2)')
            query.append('bestFit(l3, X3)')
        elif piece['shape'] == 'I':
            query.append('bestFit(i0, X0)')
            query.append('bestFit(i1, X1)')
        elif piece['shape'] == 'O':
            query.append('bestFit(o0, X0)')
        elif piece['shape'] == 'T':
            query.append('bestFit(t0, X0)')
            query.append('bestFit(t1, X1)')
            query.append('bestFit(t2, X2)')
            query.append('bestFit(t3, X3)')

        scores = list()
        for q in query:
            results = list(prolog.query(q))
            while len(results) > 0:
                posX0 = False
                posX1 = False
                posX2 = False
                posX3 = False
                result = results.pop(len(results) - 1)

                try:
                    posX0 = result['X0']
                except:
                    pass

                try:
                    posX1 = result['X1']
                except:
                    pass

                try:
                    posX2 = result['X2']
                except:
                    pass

                try:
                    posX3 = result['X3']
                except:
                    pass

                if posX0:
                    #simula con X0 e salva il risultato
                    move = self.align([0, posX0], piece)
                    scores.append((move, self.simulate_move(move, piece)))
                elif posX1:
                    #simula con X1
                    move = self.align([1, posX1], piece)
                    scores.append((move, self.simulate_move(move, piece)))
                elif posX2:
                    #simula con X2
                    move = self.align([2, posX2], piece)
                    scores.append((move, self.simulate_move(move, piece)))
                elif posX3:
                    #simula con X3
                    move = self.align([3, posX3], piece)
                    scores.append((move, self.simulate_move(move, piece)))

        if len(scores) == 0:
            return [random.randint(0, 1), random.randint(-5, 5)]        #mossa casuale
        else:
            maxScore = -99
            for x in scores:
                move, score = x
                if score > maxScore:
                    bestMove = move
            return bestMove


    def get_heights(self, board):
        heights = [0] * BOARDWIDTH
        # Calculate all tougether to optimize calculation
        for i in range(0, BOARDWIDTH):  # Select a column
            Hflag = False
            for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
                if int(board[i][j]) > 0:  # Is the cell occupied?
                    if not Hflag:
                        heights[i] = BOARDHEIGHT - j  # Store the height value
                        Hflag = True
        return heights

    def get_Pcrest(self):
        Pcrest = list()
        for x in range(int(len(self.crest))):  # 1
            Pcrest.append((x, [0]))
        for x in range(int(len(self.crest) - 1)):  # 2
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x]]))
        for x in range(int(len(self.crest) - 2)):  # 3
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x], self.crest[x + 2] - self.crest[x]]))
        for x in range(int(len(self.crest) - 3)):  # 4
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x], self.crest[x + 2] - self.crest[x],
                               self.crest[x + 3] - self.crest[x]]))
        return Pcrest

    #get the aligned rotation
    def get_rot(self, rotation):
        pass

    #get the aligned sideway
    def get_sideway(self, x):
        pass

    #write assert on Kb for the crest encoding
    def writePCrest(self, Pcrest):
        self.deletePCrest()
        for elem in Pcrest:
            position, window = elem
            pre ="inCrest(crest, "
            sequence = self.encodeShadow(window)
            if sequence:            #memorizziamo solo le shadow che si possono incastrare con i pezzi
                assertion = pre + sequence + "," + str(position)
                prolog.assertz(assertion)

    def encodeShadow(self, window):
        str_ = 's'  #in prolog le variabili cominciano per lettera maiuscola o per underscore
        for x in range(len(window)):
            if window[x] == 0:
                str_ += '_0'
            elif window[x] == 1:
                str_ += '_1'
            elif window[x] == 2:
                str_ += '_2'
            elif window[x] == -1:
                str_ += '_m1'
            elif window[x] == -2:
                str_ += '_m2'
            else:
                return False
        return str_

    def decodeShadow(self):
        pass

    #delete the previus crest
    def deletePCrest(self):
        prolog.retractall('inCrest(crest, S, X)')





if __name__ == "__main__":
    r_p = sys.argv[1]
    numOfRun = int(sys.argv[2])
    for x in range(numOfRun):
        rb = RuleBased(r_p)
        newScore, weights = rb.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)



