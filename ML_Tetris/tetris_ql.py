from mpmath import mp
from ML_Tetris.tetris_utils import *

alpha = 0.01
gamma = 0.9
#explore_change = 0.5

PIeces = ""
explore_change = 0.75
weights = [-1, -1, -1, -30]  # Initial weight vector


def set_PIece(num):
    global PIeces
    mp.dps = num
    PIeces = str(mp.pi).translate({ord(i): None for i in '.897'})

# Riceve il prossimo pezzo dalla seguenza del Pigreo
def get_next_PIece():
    global PIeces

    if len(PIeces) < 50:
        set_PIece(100)  # 200

    listx = list(PIECES.keys())
    shape = listx[int(PIeces[0])]
    new_piece = {'shape': shape, 'rotation': 0,  # random.randint(0,len(PIECES[shape]) - 1),
                 'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                 'y': -2,  # start it above the board (i.e. less than 0)
                 'color': random.randint(1, len(COLORS) - 1)
                 }
    PIeces = PIeces[1:]

    return new_piece


def remove_complete_lines(board):

    # Remove any completed lines on the board, move everything above them down, and return the number of complete lines.
    lines_removed = 0
    y = BOARDHEIGHT - 1  # start y at the bottom of the board
    while y >= 0:
        if is_complete_line(board, y):
            # Remove the line and pull boxes down by one line.
            for pull_down_y in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pull_down_y] = board[x][pull_down_y - 1]
            # Set very top line to blank.
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            lines_removed += 1
            # Note on the next iteration of the loop, y is the same.
            # This is so that if the line that was pulled down is also
            # complete, it will be removed.
        else:
            y -= 1  # move on to check next row up
    return lines_removed, board


def get_parameters(board):
    # This function will calculate different parameters of the current board

    # Initialize some stuff
    heights = [0] * BOARDWIDTH
    diffs = [0] * (BOARDWIDTH - 1)
    holes = 0
    diff_sum = 0

    # Calculate the maximum height of each column
    for i in range(0, BOARDWIDTH):  # Select a column
        for j in range(0, BOARDHEIGHT):  # Search down starting from the top of the board
            if int(board[i][j]) > 0:  # Is the cell occupied?
                heights[i] = BOARDHEIGHT - j  # Store the height value
                break

    # Calculate the difference in heights
    for i in range(0, len(diffs)):
        diffs[i] = heights[i + 1] - heights[i]

    # Calculate the maximum height
    max_height = max(heights)

    # Count the number of holes
    for i in range(0, BOARDWIDTH):
        occupied = 0  # Set the 'Occupied' flag to 0 for each new column
        for j in range(0, BOARDHEIGHT):  # Scan from top to bottom
            if int(board[i][j]) > 0:
                occupied = 1  # If a block is found, set the 'Occupied' flag to 1
            if int(board[i][j]) == 0 and occupied == 1:
                holes += 1  # If a hole is found, add one to the count

    height_sum = sum(heights)
    for i in diffs:
        diff_sum += abs(i)
    return height_sum, diff_sum, max_height, holes


def get_expected_score_QL_P(test_board, weights):
    # This function calculates the score of a given board state, given weights and the number of lines previously cleared.
    height_sum, diff_sum, max_height, holes = get_parameters(test_board)
    A = weights[0]
    B = weights[1]
    C = weights[2]
    D = weights[3]
    test_score = float(A * height_sum + B * diff_sum + C * max_height + D * holes)
    return test_score


def simulate_board(test_board, test_piece, move):
    # This function simulates placing the current falling piece onto the
    # board, specified by 'move,' an array with two elements, 'rot' and 'sideways'.
    # 'rot' gives the number of times the piece is to be rotated ranging in [0:3]
    # 'sideways' gives the horizontal movement from the piece's current position, in [-9:9]
    # It removes complete lines and gives returns the next board state as well as the number
    # of lines cleared.

    rot = move[0]
    sideways = move[1]
    test_lines_removed = 0
    reference_height = get_parameters(test_board)[0]
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
        test_lines_removed, test_board = remove_complete_lines(test_board)

    height_sum, diff_sum, max_height, holes = get_parameters(test_board)
    one_step_reward = 5 * (test_lines_removed * test_lines_removed) - (height_sum - reference_height)
    return test_board, one_step_reward


def find_best_move(board, piece, weights, explore_change):
    move_list = []
    score_list = []
    for rot in range(0, len(PIECES[piece['shape']])):
        for sideways in range(-5, 6):
            move = [rot, sideways]
            test_board = copy.deepcopy(board)
            test_piece = copy.deepcopy(piece)
            test_board = simulate_board(test_board, test_piece, move)
            if test_board is not None:
                move_list.append(move)
                test_score = get_expected_score_QL_P(test_board[0], weights)
                score_list.append(test_score)
    best_score = max(score_list)
    best_move = move_list[score_list.index(best_score)]

    if random.random() < explore_change:
        move = move_list[random.randint(0, len(move_list) - 1)]
    else:
        move = best_move
    return move


def QL_P(board, piece):
    global weights, explore_change
    move = find_best_move(board, piece, weights, explore_change)
    old_params = get_parameters(board)
    test_board = copy.deepcopy(board)
    test_piece = copy.deepcopy(piece)
    test_board = simulate_board(test_board, test_piece, move)
    if test_board is not None:
        new_params = get_parameters(test_board[0])
        one_step_reward = test_board[1]
    for i in range(0, len(weights)):
        weights[i] = weights[i] + alpha * weights[i] * (
                one_step_reward - old_params[i] + gamma * new_params[i])
    regularization_term = abs(sum(weights))
    for i in range(0, len(weights)):
        weights[i] = 100 * weights[i] / regularization_term
        weights[i] = math.floor(1e4 * weights[i]) / 1e4  # Rounds the weights

    if explore_change > 0.001:
        explore_change = explore_change * 0.99
    else:
        explore_change = 0

    return move
