"""
Plot result function
"""

import matplotlib.pyplot as plt

def plot_results(scoreArray, game_index_array, w0, w1, w2, w3):
    plt.figure(1)
    plt.subplot(211)
    plt.plot(game_index_array, scoreArray, 'k-')
    plt.xlabel('Game Number')
    plt.ylabel('Game Score')
    plt.title('Learning Curve')
    plt.xlim(1, max(game_index_array))
    plt.ylim(0, max(scoreArray) * 1.1)

    # Plot the weights over time
    plt.subplot(212)
    plt.xlabel('Game Number')
    plt.ylabel('Weights')
    plt.title('Learning Curve')
    ax = plt.gca()
    ax.set_yscale('log')
    plt.plot(game_index_array, w0, label="Aggregate Height")
    plt.plot(game_index_array, w1, label="Unevenness")
    plt.plot(game_index_array, w2, label="Maximum Height")
    plt.plot(game_index_array, w3, label="Number of Holes")
    plt.legend(loc='lower left')
    plt.xlim(0, max(game_index_array))
    plt.ylim(0.0001, 100)
    plt.show()