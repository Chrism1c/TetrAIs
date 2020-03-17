from com.Core.BaseGame import BaseGame
from com.Utils.KnowledgeBase import *
from com.Core.Model import BOARDHEIGHT, BOARDWIDTH, is_on_board
import sys
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES

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


    def get_move_by_rule(self, piece):

        def rule_S():
            query = list()
            query.append('bestFit(s0, X0);')
            query.append('bestFit(s1, X1);')
            for q in query:
                results = list(prolog.query(q))
                while True:
                    result = results.pop(len(results) - 1)
                    try:
                        posX0 = result['X0']
                    except:
                        posX1 = result['X1']

            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        def rule_Z():
            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        def rule_J():
            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        def rule_L():
            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        def rule_I():
            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        def rule_O():
            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        def rule_T():
            # return [self.get_rot(best_rotation), self.get_sideway(best_sideway)]
            pass

        if piece['shape'] == 'S':
            return rule_S
        if piece['shape'] == 'Z':
            return rule_Z
        if piece['shape'] == 'J':
            return rule_J
        if piece['shape'] == 'L':
            return rule_L
        if piece['shape'] == 'I':
            return rule_I
        if piece['shape'] == 'O':
            return rule_O
        if piece['shape'] == 'T':
            return rule_T


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



