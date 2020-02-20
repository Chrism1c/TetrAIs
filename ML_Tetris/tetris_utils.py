#contiene funzioni utili per l'implementazione delle AI

from tetris_model import *



def simulate_board(test_board, test_piece, move):
    ### Simula la board di test piazzando il tetramino di test e la mossa scelta 

    # This function simulates placing the current falling piece onto the
    # board, specified by 'move,' an array with two elements, 'rot' and 'sideways'.
    # 'rot' gives the number of times the piece is to be rotated ranging in [0:3]
    # 'sideways' gives the horizontal movement from the piece's current position, in [-9:9]
    # It removes complete lines and gives returns the next board state as well as the number
    # of lines cleared.

    rot = move[0]
    sideways = move[1]
    test_lines_removed = 0
    ##print("simulating reference_height")
    #reference_height = get_parameters(test_board)[3]
    if test_piece is None:
        return None

    # Rotate test_piece to match the desired move
    for i in range(0, rot):
        test_piece['rotation'] = (test_piece['rotation'] + 1) % len(PIECES[test_piece['shape']])

    # Test for move validity!
    if not is_valid_position(test_board, test_piece, adj_x=sideways, adj_y=0):
        # The move itself is not valid!
        return None

    # Move the test_piece to collide on the board
    test_piece['x'] += sideways
    for i in range(0, BOARDHEIGHT):
        if is_valid_position(test_board, test_piece, adj_x=0, adj_y=1):
            test_piece['y'] = i

    # Place the piece on the virtual board
    if is_valid_position(test_board, test_piece, adj_x=0, adj_y=0):
        add_to_board(test_board, test_piece)
        #test_lines_removed, test_board = remove_complete_lines(test_board)

    #fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
    
    return test_board



def get_expected_score(test_board):
    ### Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica 
    fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
    #A = weights[0]
    #B = weights[1]
    #C = weights[2]
    #D = weights[3]
    #E = weights[4]
    #F = weights[5]
    #G = weights[6]

    #test_score = float(A * height_sum + B * diff_sum + C * max_height + D * holes)
    #test_score = float((fullLines * A) - (vHoles * B) - (vBlocks * C) - ((maxHeight ** 1.5) * 0.02) - (stdDY * E) - (absDy * F) - (maxDy * G))
    test_score = float((fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5)*0.002) - (stdDY * 0.01) - (absDy * 0.2) - (maxDy * 0.3))
    #test_score = float((fullLines) - ((maxHeight ** 2)))
    
    # score = fullLines * 1.8 - vHoles * 1.0 - vBlocks * 0.5 - maxHeight ** 1.5 * 0.02 - stdY * 0.0 - stdDY * 0.01 - absDy * 0.2 - maxDy * 0.3

    return test_score, fullLines



###################################### METRICS FUNCTIONS ###################################################


#def get_parametersOld(board):
#    ### Calcola le metriche sulla board corrente
#    # This function will calculate different parameters of the current board

#    # Initialize some stuff
#    heights = [0]*BOARDWIDTH
#    diffs = [0]*(BOARDWIDTH-1)
#    holes = 0
#    diff_sum = 0
#    numTetraminoes = 0
#    standardDvHeights = 0
#    abs_diffCol = 0
#    max_diffCol = 0

#    # Calculate the maximum height of each column
#    for i in range(0, BOARDWIDTH):  # Select a column
#        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
#            #print((i,j))
#            if int(board[i][j]) > 0:  # Is the cell occupied?
#                heights[i] = BOARDHEIGHT - j  # Store the height value
#                break

#    # Calculate the difference in heights
#    for i in range(0, len(diffs)):
#        diffs[i] = heights[i + 1] - heights[i]
#    #print("diffs ",diffs)

#    # Calculate the maximum height
#    max_height = max(heights)

#    # Count the number of holes
#    for i in range(0, BOARDWIDTH):
#        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
#        for j in range(0, BOARDHEIGHT):  # Scan from top to bottom
#            if int(board[i][j]) > 0:
#                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
#            if int(board[i][j]) == 0 and occupied == 1:
#                holes += 1  # If a hole is found, add one to the count

#    height_sum = sum(heights)
#    for i in diffs:
#        diff_sum += abs(i)


#    #numero di tetramini piazzati
#    countTetra = 0
#    for i in range(0, BOARDWIDTH):
#        for j in range(0, BOARDHEIGHT):
#            if board[i][j] != '0':
#                countTetra += 1


#    roofRY = roofRelativeY(heights)

#    #holes
#    numTetraminoes = countTetra // 4
#    #max_height
#    standardDvHeights = standard_deviation_heights(heights)
#    abs_diffCol = sum([abs(x) for x in roofRY])
#    max_diffCol = roofRY[len(roofRY) - 1]

#    return fullLines, holes, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol

def get_parameters(board):
    global DeepLines
    ### Calcola le metriche sulla board corrente

    # Initialize some stuff
    heights = [0]*BOARDWIDTH
    diffs = [0]*(BOARDWIDTH-1)
    holes = 0
    diff_sum = 0
    numTetraminoes = 0
    standardDvHeights = 0
    abs_diffCol = 0
    max_diffCol = 0

    DeepLines = count_full_lines(board)

    # Calculate all tougether to optimize calculation
    countTetra = 0
    max_height = 0
    height_sum = 0
    for i in range(0, BOARDWIDTH):  # Select a column
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        Hflag = False
        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
            if int(board[i][j]) > 0:  # Is the cell occupied?
                countTetra+=1
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
                if not Hflag:
                    heights[i] = BOARDHEIGHT - j  # Store the height value
                    height_sum += heights[i]
                    if max_height < heights[i]:
                        max_height = heights[i]
                    Hflag = True
            if int(board[i][j]) == 0 and occupied == 1:
                holes += 1  # If a hole is found, add one to the count         

    # Calculate the difference in heights
    for i in range(0, len(diffs)):
        diffs[i] = heights[i + 1] - heights[i]

    for i in diffs:
        diff_sum += abs(i)
    roofRY = roofRelativeY(heights)

    fullLines = DeepLines
    #holes
    numTetraminoes = countTetra // 4
    #max_height
    standardDvHeights = standard_deviation_heights(heights)
    abs_diffCol = sum([abs(x) for x in roofRY])
    max_diffCol = roofRY[len(roofRY) - 1]

    return fullLines, holes, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol



#numero di tetramini piazzati, dato che conta il numero di blocchi presenti
#ho diviso per 4 il totale in modo da avere il vero numero di tetramini
def numTetraminoes(board):
    countTetra = 0
    for i in range(0, BOARDWIDTH):
        for j in range(0, BOARDHEIGHT):
            if board[i][j] != '0':
                countTetra += 1
    return int(countTetra / 4)



#calcola la differenza fra colonne consecutive e prende quella con il valore maggiore
def max_diffCol(roofRelativeY):
    return roofRelativeY[len(roofRelativeY) - 1]



def abs_diffCol(roofRelativeY):   
    absh = sum([abs(x) for x in roofRelativeY])
    return absh



def roofRelativeY(heights):
        return [heights[i] - heights[i + 1] for i in range(len(heights) - 1)]



#calcola la deviazione standard dell'altezza di ogni colonna
def standard_deviation_heights(heights):
    if len(heights) <= 0:         
        return 0
    else:
        return math.sqrt(sum([y ** 2 for y in heights]) / len(heights) - (sum(heights) / len(heights)) ** 2)



def count_full_lines(board):
    # Count the number of lines
    count = 0
    for i in range(0, BOARDHEIGHT):
        check = True
        for j in range(0, BOARDWIDTH):
            if board[j][i] == '0':
                #print("Find hole in = ",(i+1,j+1))
                check = False
                break
            #else:
            #    print("Cot Find hole in = ",(i+1,j+1))
        if check:
            count+=1
    return count



def maxHeight(board):
    max = 0
    heights = [0]*BOARDWIDTH
    # Calculate the maximum height of each column
    for i in range(0, BOARDWIDTH):  # Select a column
        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
            if int(board[i][j]) > 0:  # Is the cell occupied?
                heights[i] = BOARDHEIGHT - j  # Store the height value
                if max < heights[i]:
                    max = heights[i]
                break
    return max





