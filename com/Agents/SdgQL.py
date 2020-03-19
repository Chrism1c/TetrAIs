from com.Core.BaseGame import BaseGame
from abc import ABC
import copy
from com.Core.Model import PIECES, BOARDWIDTH, BOARDHEIGHT, is_valid_position, add_to_board, \
    remove_complete_lines
import sys
import random
import math
from com.Menu import menu
from com.Utils.Plot import plot_learning_curve

wx = [-1, -1, -1, -30]  # Initial weight vector
explore_change = 0


class SDG_QL(BaseGame, ABC):
    """
        Main class for SDG_QL reinforcement learning algorithm (one object = one move), it implements abstarct move() function of BaseGame
        Attributes
        ----------
                        None

        Methods
        -------
        get_move(board, piece)
            Execute sdg to get the move

        get_parameters_x(board)
            It calculates some parameters useful to the algorithm, in order to make it work correctly

        get_expected_score_x(test_board)
            This function calculates the score of a given board state, given weights and the number of lines previously
            cleared.

        simulate_board_x(test_board, test_piece, move)
            This function simulate placing the current falling piece onto the board.

        find_best_move(board, piece)
            It finds the best fitting on the board for a tetramino

        sdg(board, piece)
            This function uses previous functions in order to get the best move according to weights given by previous
            tetramino
    """

    def __init__(self, r_p):
        """
               Parameters
               ----------
               r_p : str
                   type of piece used ('r' = random, 'p' = pi)

               alpha : float
                   constant used in the formula to get the score in sdg

               gamma : float
                    constant used in the formula to get the score in sdg
        """

        super().__init__(r_p)
        self.alpha = 0.01
        self.gamma = 0.9

    def get_move(self):
        """
            Returns sdg to get the move

            Parameters
            ----------
                        None
            Returns
            -------
            Returns the call to the sdg method

        """
        return self.sdg(self.board, self.falling_piece)

    def get_parameters_x(self, board):
        """
            It calculates some parameters useful to the algorithm, in order to make it work correctly
            Parameters
            ----------
                  board : Matrix (lists of lists) of strings
            Returns
            -------
            height_sum
                an int variable representing the sum of the heights of the various pieces

            diff_sum
                an int variable representing the sum of the difference of consecutive heights

            max_height
                an int variable representing the max height in the board

            holes
                an int variable representing the number of holes made by the tetraminoes in the board
        """
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

    def get_expected_score_x(self, test_board):
        """
            This function calculates the score of a given board state, given weights and the number of lines previously
            cleared.

            Parameters
            ----------
                 test_board : Matrix (lists of lists) of strings
            Returns
            -------

            test_score
                a float variable representing the score obtained with the test_board
        """
        global wx
        # This function calculates the score of a given board state, given weights and the number of lines previously
        # cleared.
        height_sum, diff_sum, max_height, holes = self.get_parameters_x(test_board)
        A = wx[0]
        B = wx[1]
        C = wx[2]
        D = wx[3]
        test_score = float(A * height_sum + B * diff_sum + C * max_height + D * holes)
        return test_score

    def simulate_board_x(self, test_board, test_piece, move):
        """
            This function simulate placing the current falling piece onto the board.

            Parameters
            ----------
                 test_board : Matrix (lists of lists) of strings
                 test_piece : Object containing: 'shape', 'rotation', 'x', 'y', 'color'
                 move: List containing: 'rot' and 'sideways'
            Returns
            -------

            test_score
                a float variable representing the score obtained with the test_board
        """

        # This function simulates placing the current falling piece onto the
        # board, specified by 'move,' an array with two elements, 'rot' and 'sideways'.
        # 'rot' gives the number of times the piece is to be rotated ranging in [0:3]
        # 'sideways' gives the horizontal movement from the piece's current position, in [-9:9]
        # It removes complete lines and gives returns the next board state as well as the number
        # of lines cleared.

        rot = move[0]
        sideways = move[1]
        test_lines_removed = 0
        reference_height = self.get_parameters_x(test_board)[0]
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

        height_sum, diff_sum, max_height, holes = self.get_parameters_x(test_board)
        one_step_reward = 5 * (test_lines_removed * test_lines_removed) - (height_sum - reference_height)
        # print("one_step_reward: ",one_step_reward)
        return test_board, one_step_reward

    def find_best_move(self, board, piece):
        global explore_change
        """
            It finds the best fitting on the board for a tetramino
            Parameters
            ----------
                 board : Matrix (lists of lists) of strings

                 piece : Object containing: 'shape', 'rotation', 'x', 'y', 'color'
            Returns
            -------

            move
                it is a list containing which rotation and sideway the tetramino must have to make a play

        """

        move_list = []
        score_list = []
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = self.simulate_board_x(test_board, test_piece, move)
                if test_board is not None:
                    move_list.append(move)
                    test_score = self.get_expected_score_x(test_board[0])
                    score_list.append(test_score)
        best_score = max(score_list)
        best_move = move_list[score_list.index(best_score)]

        if random.random() < explore_change:
            move = move_list[random.randint(0, len(move_list) - 1)]
        else:
            move = best_move
        return move

    def sdg(self, board, piece):
        """
        This function uses previous functions in order to get the best move according to weights given by previous
        tetramino

        Parameters
        ----------
            board : Matrix (lists of lists) of strings

            piece : Object containing: 'shape', 'rotation', 'x', 'y', 'color'
        Returns
        -------

        move
            it is a list containing which rotation and sideway the tetramino must have to make a play

    """

        global wx, explore_change
        move = self.find_best_move(board, piece)
        old_params = self.get_parameters_x(board)
        test_board = copy.deepcopy(board)
        test_piece = copy.deepcopy(piece)
        test_board = self.simulate_board_x(test_board, test_piece, move)
        if test_board is not None:
            new_params = self.get_parameters_x(test_board[0])
            one_step_reward = test_board[1]
        for i in range(0, len(wx)):
            wx[i] = wx[i] + self.alpha * wx[i] * (one_step_reward - old_params[i] + self.gamma * new_params[i])
        regularization_term = abs(sum(wx))
        for i in range(0, len(wx)):
            wx[i] = 100 * wx[i] / regularization_term
            wx[i] = math.floor(1e4 * wx[i]) / 1e4  # Rounds the weights
        print("-- Updated wx: ", wx)
        if explore_change > 0.001:
            explore_change = explore_change * 0.99
        else:
            explore_change = 0
        print("-- explore_change wx: ", explore_change)
        return move


def sdgql_main(r_p, mode, numOfRun):
    global explore_change
    explore_change = float(mode)
    numOfRun = int(numOfRun)
    print("First wx: ", wx)
    games_completed = 0
    scoreArray = list()
    weightsMatrix = list()
    weight0Array = list()
    weight1Array = list()
    weight2Array = list()
    weight3Array = list()
    game_index_array = []
    # loop to run  the game with AI for numOfRun executions
    for x in range(numOfRun):
        games_completed += 1
        weight0Array.append(-wx[0])
        weight1Array.append(-wx[1])
        weight2Array.append(-wx[2])
        weight3Array.append(-wx[3])
        SdgQL = SDG_QL(r_p)
        newScore, _, tot_time, n_tetr, avg_move_time, tetr_s = SdgQL.run()
        game_index_array.append(games_completed)
        print("Game achieved a score of: ", newScore)
        print("weights: ", wx)
        print("tot run time: ", tot_time)
        print("#moves:  ", n_tetr)
        print("avg time per move: ", avg_move_time)
        print("moves/sec:  ", tetr_s)
        scoreArray.append(newScore)
    weightsMatrix.append(weight0Array)
    weightsMatrix.append(weight1Array)
    weightsMatrix.append(weight2Array)
    weightsMatrix.append(weight3Array)
    # plot_ql(scoreArray, game_index_array, weightsMatrix, 0.01, 0.9, 0.5)
    plot_learning_curve(scoreArray, game_index_array, weightsMatrix, 'ql')(SdgQL.alpha, SdgQL.gamma, float(mode))
    menu.main()


if __name__ == "__main__":
    sdgql_main('r', '0.5', 1)
