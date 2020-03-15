# -*- coding: utf-8 -*-
from pyswip import Prolog
from random import randint
import time

from com.Core.BaseGame import BaseGame
from abc import ABC
from com.Core.Model import PIECES
from itertools import cycle
import sys


class ansi:
    END = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    GRAY = '\033[30;1m'
    CLEAR = '\033[2J'

    @staticmethod
    def POS(_x=0, _y=0):
        return '\033[' + str(_x) + ';' + str(_y) + 'H'


prolog = Prolog()
prolog.consult("com/Agents/tetris.pl");


def show(x, y, stone, field):
    newfield = []
    out = ""
    # print x,y
    a = 0
    i = 0
    n = "   "
    for b in range(0, 11):
        n += ("%01d " % b)
    out += n + "\n"
    for row in field:
        out += ("%02d" % a)
        newrow = []
        printrow = []
        if i < len(stone) and y == 0:
            # print x,y,row[0:x],stone[i],row[x+len(stone[i]):]
            l = row[0:x] + stone[i] + row[x + len(stone[i]):]
            # print l
            # print row
            i += 1
            for p, q in zip(row, l):
                if p == 2:
                    newrow.append(2)
                    printrow.append(2)
                elif p == 1:
                    newrow.append(1)
                    printrow.append(1)
                elif q == 1:
                    newrow.append(1)
                    printrow.append(3)
                else:
                    newrow.append(0)
                    printrow.append(0)
        else:
            y -= 1
            for p in row:
                if p == 2:
                    newrow.append(2)
                    printrow.append(2)
                elif p == 1:
                    newrow.append(1)
                    printrow.append(1)
                elif p == 0:
                    newrow.append(0)
                    printrow.append(0)

        if ([2] + [1] * (len(row) - 2) + [2]) == newrow:
            newfield.reverse()
            newfield.append([2] + [0] * (len(row) - 2) + [2])
            newfield.reverse()
            for p in printrow:
                if p == 2:
                    out += ansi.GRAY + '▉ ' + ansi.END
                elif p == 3:
                    out += ansi.MAGENTA + '▉ ' + ansi.END
                else:
                    out += ansi.YELLOW + '▉ ' + ansi.END
        else:
            newfield.append(newrow)
            for p in printrow:
                if p == 3:
                    out += ansi.BLUE + '▉ ' + ansi.END
                if p == 2:
                    out += ansi.GRAY + '▉ ' + ansi.END
                elif p == 1:
                    out += ansi.RED + '▉ ' + ansi.END
                elif p == 0:
                    out += '▉ '

        out += "\n"
        a += 1
    return newfield, out


field = [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
         [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

stones = [
    [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],  # 0 # J capovolta
    [[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],  # 1 # L capovolta
    [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],  # 2 # L dritta
    [[0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],  # 3 # J dritta
    [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],  # 4 # L testa a sinistra
    [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],  # 5 # J testa a destra
    [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]],  # 6 # J testa a sinistra
    [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]],  # 7 # L testa a destra
    [[0, 0, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 0, 0]],  # 8 # I dritta
    [[0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0]],  # 9 # I sdraiata
    [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]],  # 10 # S dritta
    [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]],  # 11 # Z dritta
    [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],  # 12 # T capovolta
    [[0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]],  # 13 # T dritta
    [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],  # 14 # Z verticale
    [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],  # 15 # S varticale
    [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],  # 16 # T testa a destra
    [[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],  # 17 # T testa a sinistra
    [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]  # 18 # O
]

rot = [
    ['00000', '00110', '00100', '00100', '00000'],  # J capovolta
    ['00000', '01100', '00100', '00100', '00000'],  # L capovolta
    ['00000', '00100', '00100', '00110', '00000'],  # L dritta
    ['00000', '00100', '00100', '01100', '00000'],  # J dritta
    ['00000', '00010', '01110', '00000', '00000'],  # L testa a sinistra
    ['00000', '01000', '01110', '00000', '00000'],  # J testa a destra
    ['00000', '00000', '01110', '00010', '00000'],  # J testa a sinistra
    ['00000', '00000', '01110', '01000', '00000'],  # L testa a destra
    ['00100', '00100', '00100', '00100', '00000'],  # I dritta
    ['00000', '00000', '11110', '00000', '00000'],  # I sdraiata
    ['00000', '00000', '00110', '01100', '00000'],  # S dritta
    ['00000', '00000', '01100', '00110', '00000'],  # Z dritta
    ['00000', '00100', '01110', '00000', '00000'],  # T capovolta
    ['00000', '00000', '01110', '00100', '00000'],  # T dritta
    ['00000', '00100', '01100', '01000', '00000'],  # Z verticale
    ['00000', '00100', '00110', '00010', '00000'],  # S varticale
    ['00000', '00100', '01100', '00100', '00000'],  # T testa a destra
    ['00000', '00100', '00110', '00100', '00000'],  # T testa a sinistra
    ['00000', '00000', '01100', '01100', '00000']  # O
]


class RuleBased(BaseGame, ABC):
    def __init__(self, r_p):
        super().__init__(r_p)
        self.first = True

    def get_move(self):
        return self.RuleBased_move(self.board, self.falling_piece)

    def PieceToStone(self, piece):
        global rot, stones
        backupRot = rot
        for i in range(len(rot)):
            # print('rot[i] == piece:', rot[i], " == ", piece)
            if str(rot[i]) == piece:
                # print('YES ', stones[i])
                return stones[i]

    def StoneToRotIndex(self, stone):
        global rot, stones
        find = None

        # print("len(rot) ****** ", len(rot))
        for k in range(len(rot)):
            # print("if: ", stones[k], " == ", stone)
            if str(stones[k]) == str(stone):
                # print("OK: --> ", stones[k], " == ", stone)
                # print("k :", k)
                find = str(rot[k])
                # print("find: ", str(find))
                return find, k

    def getNumberOfRot(self, newRotPiece, piece):

        rotxx = PIECES[piece['shape']]
        pool = cycle(rotxx)
        countRotation = 0
        Checked = False

        for item in pool:

            if str(item) == str(PIECES[piece['shape']][piece['rotation']]):
                # print("START Counting... ")
                Checked = True
            if Checked and newRotPiece == str(item):
                # print("==== countRotation ------ : ", countRotation)
                return item, countRotation
            if Checked:
                # print("increment counting...")
                countRotation = countRotation + 1
            # else:
            # print("not increment counting...")

    def check_first(self, board):
        if self.first:
            board = self.get_blank_board()
            # print("board : ", board)
            self.first = False
            print("self.first : ", self.first)

    def get_offeset(self, indexInRot):
        offset = None
        if indexInRot in [0, 2, 8, 15, 17]:
            # print("Offset = -5")
            offset = -5
        elif indexInRot in [1, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 16, 18]:
            # print("Offset = -4")
            offset = -4
        elif indexInRot == 9:
            # print("Offset = -3")
            offset = -3
        else:
            # print("Not Found")
            offset = -99
        return offset

    def console_gui_pt1(self, stone, pos):
        out = ansi.CLEAR
        # draw old stone
        out += show(0, 0, stone,
                    [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]])[1]
        out += "\n"
        # draw rotated stone
        out += show(0, 0, pos['Stone'],
                    [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0]])[1]
        out += "\n"
        # draw game field
        return out

    def console_gui_pt2(self, out, asd):
        out += asd
        out += "\n"
        print(out)
        # if pos['XPos'] == -1 and pos['YPos'] == -1:
        #     s = 'exit'
        #     print("******************* EXIT *************************")

    # Main function
    def RuleBased_move(self, board, piece):
        global field, stones

        # clear board to remove first drop
        self.check_first(board)

        # RotToStone()
        pieceLikeList = PIECES[piece['shape']][piece['rotation']]
        strippedPiece = str(pieceLikeList)
        stone = self.PieceToStone(strippedPiece)

        q = "my_best_position(%s,%s,XPos,YPos,Stone)." % (str(field), str(stone))
        pos = list(prolog.query(q))[0]

        # StoneToRot()
        OldrotPiece, indexInRot = self.StoneToRotIndex(pos['Stone'])
        newrotPiece, countRotation = self.getNumberOfRot(OldrotPiece, piece)
        # XPos_To_Sydeway()
        x_sideway = pos['XPos'] + self.get_offeset(indexInRot)  # 4

        # non necessaria (GUI Console)
        out = self.console_gui_pt1(stone, pos)

        # draw and update game field
        field, asd = show(pos['XPos'], pos['YPos'], pos['Stone'], field)

        # non necessaria (GUI Console)
        self.console_gui_pt2(out, asd)

        return countRotation, x_sideway  # rot and sideways


if __name__ == "__main__":
    r_p = 'r'  # sys.argv[1]
    numOfRun = 1  # int(sys.argv[2])

    for x in range(numOfRun):
        rulBas = RuleBased(r_p)
        newScore, _ = rulBas.run()
        print("Game achieved a score of: ", newScore)
