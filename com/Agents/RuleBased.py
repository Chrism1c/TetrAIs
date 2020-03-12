from com.Core.BaseGame import BaseGame
from com.Utils.KnowledgeBase import *
from com.Core.Model import BOARDHEIGHT, BOARDWIDTH, is_on_board

class RuleBased(BaseGame):
    def __init__(self, r_p):
        super().__init__(r_p)

    def get_move(self):
        crest = self.get_crest()
        rule = self.get_rule_by_crest(self.falling_piece)
        return self.align(rule(crest))

    #non utilizzata
    def bin_matrix_board(self):
        bin_matrix_board_ = list()
        for y in range(BOARDHEIGHT):
            line = [0] * BOARDWIDTH
            for x in range(BOARDWIDTH):
                if is_on_board(x, y):
                    line[x] = 1
            bin_matrix_board_.append(line)
        return bin_matrix_board_

    def get_crest(self):
        crest = [0] * BOARDWIDTH
        for x in range(BOARDWIDTH):  # per ogni colonna
            maxH = 0
            for y in range(BOARDHEIGHT):  # per ogni riga
                if is_on_board(x, y):
                    if maxH < y:
                        maxH = y
            crest[x] = maxH
        return crest

    #ricontrollare i pezzi
    def get_rule_by_crest(self, piece):

        def rule_S(crest):
            # 2 flat 1 up altimenti 1 flat 1 down
            y_flat = crest[0]
            count_flat = 1
            pos1 = -1
            pos2 = -1
            for x in range(1, len(crest)):
                if count_flat == 2 and crest[x] == y_flat + 1:
                    pos1 = x - 1
                elif crest[x] == y_flat - 1:
                    pos2 = x
                elif y_flat == crest[x]:
                    count_flat += 1
                else:
                    y_flat = crest[x]
                    count_flat = 1
                    flat = x
            if pos1 != -1:
                # metti il pezzo in pos1
                pass
            elif pos2 != -1:
                # metti il pezzo in pos2
                pass
            elif count_flat > 2:
                # metti il pezzo nella posizione 1 a partire da flat
                pass
            else:
                # metti il pezzo in min(crest[x]) o random
                pass

        def rule_Z(crest):
            # 1 flat 1 up altimenti 1 flat 1 down 1 flat
            y_flat = crest[0]
            count_flat_1 = 1
            count_flat_2 = 0
            pos1 = -1
            pos2 = -1
            for x in range(1, len(crest)):
                if count_flat_1 == 1 and crest[x] == y_flat + 1:
                    pos1 = x - 1
                    y_flat = crest[x]
                    count_flat_1 = 1
                elif crest[x] == y_flat - 1:
                    count_flat_2 = 1
                    y_flat = crest[x]
                    count_flat_1 = 1
                elif y_flat == crest[x]:
                    count_flat_1 += 1
                elif y_flat == crest[x] and count_flat_2 == 1:
                    pos2_x = x - 2
                else:
                    y_flat = crest[x]
                    count_flat_1 = 1
                    flat = x
            if pos1 != -1:
                # metti il pezzo in pos1
                pass
            elif pos2 != -1:
                # metti il pezzo in pos2
                pass
            elif count_flat_1 > 2:
                # metti il pezzo nella posizione 1 a partire da flat
                pass
            else:
                # metti il pezzo in min(crest[x]) o random
                pass

        def rule_J(crest):
            y_flat = crest[0]
            count_flat = 1
            pos1 = -1  # 2 flat 1 down
            pos2 = -1  # 1 flat 1 jump
            pos3 = -1  # 3 flat
            pos4 = -1  # 2 flat
            for x in range(1, len(crest)):
                if crest[x] == y_flat:
                    count_flat += 1
                else:
                    if crest[x] == y_flat - 1 and count_flat == 2:
                        pos1 = x - 2
                    elif crest[x] == y_flat + 2:
                        pos2 = x - 1
                    y_flat = crest[x]
                    count_flat = 1
                if count_flat == 3:
                    pos3 = x - 2
                if count_flat == 2:
                    pos4 == x - 1

            if pos1 != -1:
                pass
            elif pos2 != -1:
                pass
            elif pos3 != -1:
                pass
            elif pos4 != -1:
                pass
            else:
                # random
                pass

        def rule_L(crest):
            y_flat = crest[0]
            count_flat = 1
            up = 0
            pos1 = -1  # 1 flat 2 up
            pos2 = -1  # 1 flat 1 jump down
            pos3 = -1  # 3 flat
            pos4 = -1  # 2 flat
            for x in range(1, len(crest)):
                if crest[x] == y_flat:
                    count_flat += 1
                    if up == 1:
                        pos1 = x - 2
                        up = 0
                else:
                    if crest[x] == y_flat + 1:
                        up = 1
                    elif crest[x] == y_flat + 2:
                        pos2 = x - 1
                    y_flat = crest[x]
                    count_flat = 1
                if count_flat == 3:
                    pos3 == x - 2
                if count_flat == 2:
                    pos4 = x - 1

            if pos1 != -1:
                pass
            elif pos2 != -1:
                pass
            elif pos3 != -1:
                pass
            elif pos4 != -1:
                pass
            else:
                # random
                pass

        def rule_I(crest):
            current_flat = crest[0]
            current_Column = 0
            flat = 1
            for x in range(1, len(crest)):
                if crest[x] == current_flat:
                    flat += 1
                else:
                    current_flat = crest[x]
                    current_Column = x
                    flat = 1

                if flat == 4:
                    x_flat = current_Column

                # if crest[x] <= current_L:
                #     low_x = x
                #     current_L = crest[x]
            if flat >= 4:
                # posiziona il pezzo in orrizontale a partire da current_Column
                # return current_Column, current_flat,
                pass
            else:
                current_L = max(crest)
                low_x = 0
                for x in range(1, len(crest)):
                    if crest[x] <= current_L:
                        low_x = x
                        current_L = crest[x]
                pass  # posiziona il pezzo in verticale nel punto più basso (current_L), quindi nel punto low_x

        def rule_O(crest):
            # posiziona il pezzo nel punto più basso possibile
            current_flat = crest[0]
            current_L = max(crest)
            low_x = 0
            current_Column = 0
            flat = 1
            for x in range(1, len(crest)):
                if crest[x] == current_flat:
                    flat += 1
                else:
                    current_flat = crest[x]
                    current_Column = x
                    flat = 1
                if crest[x] <= current_L:
                    low_x = x
                    current_L = crest[x]
                if flat == 2:
                    x_flat = current_Column
            if flat >= 2:
                # posiziona il pezzo a partire da current_Column
                pass
            else:
                # posiziona il pezzo nel punto più basso
                pass

        def rule_T(crest):  # 4 possivili rotazioni: punta a sx, dx, alto e in basso
            # analizzo la crest
            current_flat = crest[0]
            current_L = max(crest)
            low_x = 0
            current_Column_flat = 0
            count_flat = 1
            x_up_stair = 0
            x_down_stair = 0
            x_down = 0
            up_stair = crest[0] + 1
            down_stair = crest[0] - 1

            for x in range(1, len(crest)):
                if crest[x] == current_flat:  # controllo se flat
                    count_flat += 1
                else:
                    if crest[x] == up_stair and (not x_down_stair or (
                            x_down_stair and x_down_stair != x - 1)):  # caso up_stair (controllo se non siamo finiti nel caso con la punta verso il basso)
                        x_up_stair = x - 1
                    elif crest[x] == up_stair and x_down_stair and x_down_stair == x - 1:  # caso down
                        x_down = x
                    elif crest[x] == down_stair:  # caso down_stair
                        x_down_stair = x

                    current_flat = crest[x]
                    current_Column = x
                    count_flat = 1
                    if not x_up_stair:
                        up_stair = crest[x] + 1
                    if not x_down_stair:
                        down_stair = crest[x] - 1

                if x_down:
                    # posiziona il pezzo con la punta nel punto x_down
                    pass
                elif x_down_stair:
                    # posiziona il pezzo in piedi con la punta più in basso in x_down_stair e ruotato a sx
                    pass
                elif x_up_stair:
                    # posiziona il pezzo in piedi con la punta più in basso in x_up_stair e ruotato a dx
                    pass
                elif count_flat >= 3:
                    # posiziona il pezzo sdraiato con il margine sinistro in current_column_flat
                    pass
                else:
                    # posiziona il pezzo random
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

#restituisce una cresta con offset sullo start



