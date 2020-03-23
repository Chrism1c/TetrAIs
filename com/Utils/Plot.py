"""
Plot result function
"""

import matplotlib.pyplot as plt


# plot_learning_curve(...)(...)

def plot_learning_curve(scoreArray, game_index_array, weights, type_='def'):
    """
    Print a plot in a new window
    :param scoreArray: the array of scores of dim=n_run
    :param game_index_array: the number of runs
    :param weights: the list of arrays containing the weights
    :param type_: can be 'gen', 'ql' or 'def'
    :return: None
    """
    def __init_plot():
        """
        The common plot startup procedure
        :return: None
        """
        plt.figure(1)
        plt.subplot(211)
        plt.plot(game_index_array, scoreArray, 'k-')
        plt.xlabel('Game Number')
        plt.ylabel('Game Score')
        plt.title('Curve')
        plt.xlim(1, max(game_index_array))
        plt.ylim(0, max(scoreArray) * 1.1)

    def plot_default():
        """
        plot the score curve
        :return: None
        """
        __init_plot()
        plt.show()

    def plot_genetic(numGen: int, n_run_x_chromosome: int, n_gen0: int):
        """
        plot function suited for genetic training phase that creates the learning curve.
        visualizing also the variation in weights per chromosome.
        :param numGen: number of generation in the genetic training
        :param n_run_x_chromosome: number of run for training a chromosome
        :param n_gen0: number of chromosomes in the first generation
        :return: None
        """
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        title = str('Genetic Learning Curve: numGen=' + str(numGen) + 'n run per chromosoma=' + str(n_run_x_chromosome) +
                  ' n_gen0='+ str(n_gen0))
        plt.title(title)
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label='fullLines')
        plt.plot(game_index_array, weights[1], label='vHoles')
        plt.plot(game_index_array, weights[2], label='vBlocks')
        plt.plot(game_index_array, weights[3], label='maxHeight')
        plt.plot(game_index_array, weights[4], label='stdDY')
        plt.plot(game_index_array, weights[5], label='absDy')
        plt.plot(game_index_array, weights[6], label='maxDy')
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_ql(alpha: float, gamma: float, explore_change: float):
        """
        plot function suited for Qlearning training phase that creates the learning curve.
        visualizing also the variation in weights per run.
        :param alpha: constant used in the formula to get the score in sdg
        :param gamma: constant used in the formula to get the score in sdg
        :param explore_change: the way the algorithm find the next move
        :return: None
        """
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        title = str('QLearning Curve: alpha=' + str(round(alpha, 2)) + ' gamma=' + str(round(gamma, 2)) +
                    ' explore_change=' + str(round(explore_change, 2)))
        plt.title(title)
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label='height_sum')
        plt.plot(game_index_array, weights[1], label='diff_sum')
        plt.plot(game_index_array, weights[2], label='max_height')
        plt.plot(game_index_array, weights[3], label='holes')
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    # chosing which plot function will be returned
    if type_ == 'gen':
        return plot_genetic
    elif type_ == 'ql':
        return plot_ql
    else:
        return plot_default

# def plot_ql(scoreArray, game_index_array, weightsMatrix, alpha, gamma, explore_change):
#     plt.subplot(211)
#     plt.plot(game_index_array, scoreArray, 'k-')
#     plt.xlabel('Game Number')
#     plt.ylabel('Game Score')
#     plt.title('Curve')
#     plt.xlim(1, max(game_index_array))
#     plt.ylim(0, max(scoreArray) * 1.1)
#
#     # Plot the weights over time
#     plt.subplot(212)
#     plt.xlabel('Game Number')
#     plt.ylabel('Weights')
#     title = str('QLearning Curve: alpha=' + str(round(alpha, 2)) + ' gamma=' + str(round(gamma, 2)) +
#                 ' explore_change=' + str(round(explore_change, 2)))
#     plt.title(title)
#     ax = plt.gca()
#     ax.set_yscale('log')
#     plt.plot(game_index_array, weightsMatrix[0], label='height_sum')
#     plt.plot(game_index_array, weightsMatrix[1], label='diff_sum')
#     plt.plot(game_index_array, weightsMatrix[2], label='max_height')
#     plt.plot(game_index_array, weightsMatrix[3], label='holes')
#     plt.legend(loc='lower left')
#     plt.xlim(0, max(game_index_array))
#     plt.ylim(0.0001, 100)
#     plt.show()


def plot_results(scoreArray, game_index_array, weights):
    """
    Print a different plot in a new window based on the number of weights.
    :param scoreArray: the array of scores of dim=n_run
    :param game_index_array: the number of runs
    :param weights: the list of arrays containing the weights
    :return: None
    """
    # initializing the plot figure
    def __init_plot():
        plt.figure(1)
        plt.subplot(211)
        plt.plot(game_index_array, scoreArray, 'k-')
        plt.xlabel('Game Number')
        plt.ylabel('Game Score')
        plt.title('Learning Curve')
        plt.xlim(1, max(game_index_array))
        plt.ylim(0, max(scoreArray) * 1.1)

    # define function per number of weights
    def plot_result_0():
        __init_plot()
        plt.show()

    def plot_result_1(label_0):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_result_2(label_0, label_1):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.plot(game_index_array, weights[1], label=label_1)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_result_3(label_0, label_1, label_2):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.plot(game_index_array, weights[1], label=label_1)
        plt.plot(game_index_array, weights[2], label=label_2)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    def plot_result_4(label_0, label_1, label_2, label_3):
        __init_plot()

        # Plot the weights over time
        plt.subplot(212)
        plt.xlabel('Game Number')
        plt.ylabel('Weights')
        plt.title('Learning Curve')
        ax = plt.gca()
        ax.set_yscale('log')
        plt.plot(game_index_array, weights[0], label=label_0)
        plt.plot(game_index_array, weights[1], label=label_1)
        plt.plot(game_index_array, weights[2], label=label_2)
        plt.plot(game_index_array, weights[3], label=label_3)
        plt.legend(loc='lower left')
        plt.xlim(0, max(game_index_array))
        plt.ylim(0.0001, 100)
        plt.show()

    # chosing which plot function will be returned
    if len(weights) == 0:
        return plot_result_0
    elif len(weights) == 1:
        return plot_result_1
    elif len(weights) == 2:
        return plot_result_2
    elif len(weights) == 3:
        return plot_result_3
    elif len(weights) == 4:
        return plot_result_4
    else:
        return lambda: print("Too much weights!")

# def plot_results(scoreArray, game_index_array, w0, w1, w2, w3):
#     plt.figure(1)
#     plt.subplot(211)
#     plt.plot(game_index_array, scoreArray, 'k-')
#     plt.xlabel('Game Number')
#     plt.ylabel('Game Score')
#     plt.title('Learning Curve')
#     plt.xlim(1, max(game_index_array))
#     plt.ylim(0, max(scoreArray) * 1.1)

#     # Plot the weights over time
#     plt.subplot(212)
#     plt.xlabel('Game Number')
#     plt.ylabel('Weights')
#     plt.title('Learning Curve')
#     ax = plt.gca()
#     ax.set_yscale('log')
#     plt.plot(game_index_array, w0, label="Aggregate Height")
#     plt.plot(game_index_array, w1, label="Unevenness")
#     plt.plot(game_index_array, w2, label="Maximum Height")
#     plt.plot(game_index_array, w3, label="Number of Holes")
#     plt.legend(loc='lower left')
#     plt.xlim(0, max(game_index_array))
#     plt.ylim(0.0001, 100)
#     plt.show()

# def plot_results(scoreArray, game_index_array):
#     plt.figure(1)
#     plt.subplot(211)
#     plt.plot(game_index_array, scoreArray, 'k-')
#     plt.xlabel('Game Number')
#     plt.ylabel('Game Score')
#     plt.title('Learning Curve')
#     plt.xlim(1, max(game_index_array))
#     plt.ylim(0, max(scoreArray) * 1.1)
#     plt.show()