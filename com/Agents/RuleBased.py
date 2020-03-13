from com.Core.BaseGame import BaseGame
from com.Utils.KnowledgeBase import *
from com.Core.Model import BOARDHEIGHT, BOARDWIDTH, is_on_board

class RuleBased(BaseGame):
    def __init__(self, r_p):
        super().__init__(r_p)
        self.crest = [0]*BOARDWIDTH                 #cresta relativa

    def get_move(self):
        #self.update_crest(self.get_heights())
        self.crest = self.get_heights()
        return self.get_move_by_rule(self.falling_piece, self.get_Pcrest())

    def get_move_by_rule(self, piece, Pa_):
        current_start = 0
        current_rot = 1
        current_priority = 0
        for shadow in shadows:
            shape, rot, seq_s, priority = shadow
            if shape == piece['shape']:
                for scenario in Pa_:
                    start_, seq_x = scenario
                    if seq_s == seq_x and (current_priority < priority or self.crest[start] < self.crest[current_start]):
                        current_start = start_
                        current_rot = rot
        return [current_rot, current_start - 5]


    def get_move_by_rule_old(self, piece, Pa):

        def rule_S():
            current_start = 0
            current_rot = 1
            current_priority = 0
            for shadow in shadows:
                shape, rot, seq_s, priority = shadow
                if shape == piece['shape']:
                    for pax in Pa:
                        start, seq_x = pax
                        if seq_s == seq_x and current_priority < priority:
                            current_start = start
                            current_rot = rot
            return current_rot, current_start

        def rule_Z():
            pass
        def rule_J():
            pass
        def rule_L():
            pass
        def rule_I():
            pass
        def rule_O():
            pass
        def rule_T():
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


    def update_crest(self, heights):
        self.crest = 0
        for x in range(BOARDWIDTH):
            self.crest[x] = heights[x] - heights[x-1]

    def get_Pcrest(self): #MODIFICA
        Pcrest = list()
        for x in range(int(len(self.crest))):  # 1
            Pcrest.append((x, [0]))
        for x in range(int(len(self.crest) - 1)):  # 2
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x]]))
        for x in range(int(len(self.crest) - 2)):  # 3
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x], self.crest[x + 2] - self.crest[x + 1]]))
        for x in range(int(len(self.crest) - 3)):  # 4
            Pcrest.append((x, [0, self.crest[x + 1] - self.crest[x], self.crest[x + 2] - self.crest[x + 1], self.crest[x + 3] - self.crest[x + 2]]))
        return Pcrest

    def get_heights(self):
        heights = [0]*BOARDWIDTH
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if is_on_board(x, y):
                    heights[x] = y
        return heights













