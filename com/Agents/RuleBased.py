from com.Core.BaseGame import BaseGame
from com.Utils.KnowledgeBase import *
from com.Core.Model import BOARDHEIGHT, BOARDWIDTH, is_on_board
import sys
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES

class RuleBased(BaseGame):
    def __init__(self, r_p):
        super().__init__(r_p)
        self.crest = [0]*BOARDWIDTH                 #cresta relativa

    def get_move(self):
        #self.update_crest(self.get_heights(self.board))
        self.crest = self.get_heights(self.board)
        #return self.align(self.get_move_by_rule(self.falling_piece, self.get_Pcrest()), self.falling_piece)
        return self.get_move_by_rule(self.falling_piece, self.get_Pcrest())

    def update_crest(self, heights):
        self.crest[0] = 0
        for x in range(1, len(heights)):
            self.crest[x] = heights[x] - heights[x - 1]

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

    def get_expected_score(self, test_board):
        ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.002) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines


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


    def get_move_by_rule(self, piece, Pa_):
        current_start = 0
        current_rot = 1
        current_priority = 0
        best_rot = 0
        best_sideways = 0
        best_score = - 99
        NextScore = [best_rot, best_sideways, best_score]
        for shadow in shadows:
            shape, rot, seq_s, priority = shadow
            if shape == piece['shape']:
                for scenario in Pa_:
                    start_, seq_x = scenario
                    if seq_s == seq_x :
                        current_start = start_
                        current_rot = rot
                        #move = self.align([current_rot, current_start], piece)
                        move = [current_rot, current_start - 5]
                        test_board = copy.deepcopy(self.board)
                        test_piece = copy.deepcopy(piece)
                        test_board = simulate_board(test_board, test_piece, move)
                        if test_board is not None:
                            test_score, _ = self.get_expected_score(test_board)
                            if NextScore[2] < test_score:
                                NextScore = [move[0], move[1], test_score]  # aggiorno il best local score (LV2)
                    if best_score < NextScore[2]:  # confronto
                        best_score = NextScore[2]  # aggiorno il best local score (LV1+LV2)
                        best_sideways = NextScore[1]  # aggiorno il best sideway (LV1)
                        best_rot = NextScore[0]  # aggiorno il best rot (LV1)
        if self.too_much_difference():
            dfs_rot, dfs_sideways, dfs_score = self.get_DFS_move()
            if best_score <= dfs_score:
                best_rot = dfs_rot
                best_sideways = dfs_sideways
                print('uso dfs')
            else:
                print('uso rule')
        else:
            print('uso rule con diff < 2')
        return [best_rot, best_sideways]

    def too_much_difference(self):
        flag = False
        for x in range(1, len(self.crest)):
            if abs(self.crest[x-1] - self.crest[x]) > 2:
                flag = True
                break
        return flag

    def get_DFS_move(self):
        best_rot = 0
        best_sideways = 0
        best_score = - 99

        NextScore = (0, 0, -99)  # rot,sideways, score

        # rot =  1-'O':    2-'I': 2-'Z':    4-'J': 4-'L': 4-'T'

        for rot in range(0, len(PIECES[self.falling_piece['shape']])):  # per le rotazioni possibili su lpezzo corrente
            for sideways in range(-5, 6):  # per i drop possibili sulla board
                move = [rot, sideways]  # salvo la coppia corrente
                test_board = copy.deepcopy(self.board)  # duplico la board corrente
                test_piece = copy.deepcopy(self.falling_piece)  # duplico il pezzo corrente
                test_board = simulate_board(test_board, test_piece, move)  # simulo il pezzo e la mossa sulla board test
                # Check NEXT
                if test_board is not None:  # se la simulazione è andata a buon fine
                    ## Chose the best after next                                # effettuo il calcolo con il pezzo successivo
                    for rot2 in range(0, len(PIECES[self.next_piece['shape']])):
                        for sideways2 in range(-5, 6):
                            move2 = [rot2, sideways2]
                            test_board2 = copy.deepcopy(test_board)
                            test_piece2 = copy.deepcopy(self.next_piece)
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

        return best_rot, best_sideways, best_score


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


    def get_Pcrest(self):
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


    def get_heights_old(self):
        heights = [0]*BOARDWIDTH
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                if is_on_board(x, y):
                    heights[x] = y
                else:
                    print('no')
        #print(heights)
        return heights



if __name__ == "__main__":
    r_p = sys.argv[1]
    numOfRun = int(sys.argv[2])
    for x in range(numOfRun):
        rb = RuleBased(r_p)
        newScore, weights = rb.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)



