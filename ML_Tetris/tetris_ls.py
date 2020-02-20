from tetris_utils import *

### LV1 only analysis
def find_best_moveLS_LV1only(board, piece):
    ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
    start = time.perf_counter()

    strategy = None
    for rot in range(0, len(PIECES[piece['shape']])):
        for sideways in range(-5, 6):
            move = [rot, sideways]
            test_board = copy.deepcopy(board)
            test_piece = copy.deepcopy(piece)
            test_board = simulate_board(test_board, test_piece, move)
            if test_board is not None:
                test_score = get_expected_score(test_board)
                if not strategy or strategy[2] < test_score:
                    strategy = (rot, sideways, test_score)

    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s) with LV1Only')

    return [strategy[0],strategy[1]]

### LV1
def find_best_moveLS_step1(board, piece, NextPiece):
    ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
    start = time.perf_counter()

    strategy = None #(0,0,-99999)
    for rot in range(0, len(PIECES[piece['shape']])):
        for sideways in range(-5, 6):
            move = [rot, sideways]
            test_board = copy.deepcopy(board)
            test_piece = copy.deepcopy(piece)
            test_board = simulate_board(test_board, test_piece, move)
            # Check NEXT
            if test_board is not None:
                NextScore = find_best_moveLS_step2(test_board, NextPiece)
                ## Chose the best after next
                #test_score = get_expected_score(test_board)

                #print("if",test_score,">",strategy[2],end = '')
                if not strategy or strategy[2] < NextScore:
                    #print(" yes")
                    strategy = (rot,sideways,NextScore)
                #else:
                #    print(" no")
    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')

    return [strategy[0],strategy[1]]


### LV2 afetr LV1
def find_best_moveLS_step2(board, piece):
    ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
    strategy = None
    for rot in range(0, len(PIECES[piece['shape']])):
        for sideways in range(-5, 6):
            move = [rot, sideways]
            test_board = copy.deepcopy(board)
            test_piece = copy.deepcopy(piece)
            test_board = simulate_board(test_board, test_piece, move)
            if test_board is not None:
                test_score = get_expected_score(test_board)
                #print("if",test_score,">>>",local_best)
                if not strategy or strategy[2] < test_score:
                    strategy = (rot, sideways, test_score)
    return strategy[2]


### FULL LV1+LV2 choise
def find_best_moveLS_full(board, piece, NextPiece):
    ### Cerca la mossa migliore da effettuare sulla board, passando il vettore dei pesi
    start = time.perf_counter() # salvo il tempo di partenza

    best_rot = 0
    best_sideways = 0
    best_score = - 99

    NextScore = (0,0, -99) # rot,sideways, score
    bestLines = -1
    nextLines = -1

    # rot =  1-'O':    2-'I': 2-'Z':    4-'J': 4-'L': 4-'T'

    for rot in range(0, len(PIECES[piece['shape']])):                       # per le rotazioni possibili su lpezzo corrente
        for sideways in range(-5, 6):                                       # per i drop possibili sulla board
            move = [rot, sideways]                                          # salvo la coppia corrente
            test_board = copy.deepcopy(board)                               # duplico la board corrente
            test_piece = copy.deepcopy(piece)                               # duplico il pezzo corrente
            test_board = simulate_board(test_board, test_piece, move)       # simulo il pezzo e la mossa sulla board test
            # Check NEXT
            if test_board is not None:                                      # se la simulazione è andata a buon fine
                ## Chose the best after next                                # effettuo il calcolo con il pezzo successivo
                for rot2 in range(0, len(PIECES[NextPiece['shape']])):  
                    for sideways2 in range(-5, 6):
                        move2 = [rot2, sideways2]
                        test_board2 = copy.deepcopy(test_board)
                        test_piece2 = copy.deepcopy(NextPiece)
                        test_board2 = simulate_board(test_board2, test_piece2, move2)
                        if test_board2 is not None:
                            test_score2, nextLines = get_expected_score(test_board2)
                            #print("if", '{:05.2f}'.format(NextScore[2])," < ",'{:05.2f}'.format(test_score2)," rot=",rot," sideways=",sideways," rot2=",rot2," sideways2=",sideways2," scoreLV1=", '{:05.2f}'.format(best_score)," scoreLV2=",'{:05.2f}'.format(test_score2), end="")
                            #print("if", '{:05.2f}'.format(NextScore[2])," < ",'{:05.2f}'.format(test_score2)," sideways=",sideways," sideways2=",sideways2," scoreLV1=", '{:05.2f}'.format(best_score)," scoreLV2=",'{:05.2f}'.format(test_score2), end="")
                            if NextScore[2] < test_score2:
                                NextScore = [rot2, sideways2, test_score2]  # aggiorno il best local score (LV2)
                            #else:
                            #    print(" no")
                            #print(get_parameters(test_board2))
                # Confront LV2 Scores
                #print("if", '{:05.2f}'.format(best_score)," < ",'{:05.2f}'.format(NextScore[2]), end="")
                if best_score < NextScore[2]:         # confronto 
                    best_score = NextScore[2]         # aggiorno il best local score (LV1+LV2)
                    best_sideways = sideways          # aggiorno il best sideway (LV1)
                    best_rot = rot                     # aggiorno il best rot (LV1)

    finish = time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s) with full')

    return [best_rot,best_sideways]


def LS(board, piece, NextPiece):
    ### Funzione algoritmo AI Local Search

    mH = maxHeight(board)
    print("maxHeight -- ",mH)

    #if mH>=15:
    move = find_best_moveLS_full(board, piece, NextPiece)                  ### Trova la mossa migliore da effettuare
    #else:
       # move = find_best_moveLS_LV1only(board, piece)                  ### Trova la mossa migliore da effettuare
    
    #stampa delle metriche sulla mossa scelta
    fulllines, vholes, vblocks, maxheight, stddy, absdy, maxdy = get_parameters(board)
    #print("================== 7 metrics ==================")
    #print("fulllines ",fulllines)
    #print("holes ",vholes)
    #print("numtetraminoes ",vblocks)
    #print("max_height ",maxheight)
    #print("standarddvheights ",stddy)
    #print("abs_diffcol ",absdy)
    #print("max_diffcol ",maxdy)

    # Slow down to help debug alaysis
    #time.sleep(2)

    return move                                           ### Restituisce la mossa scelta
