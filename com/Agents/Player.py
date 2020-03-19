from abc import ABC
from com.Core.BaseGame import BaseGame
from com.Menu import menu
import pygame
import sys


class Player(BaseGame, ABC):
    """
        Main class for simple run of a new Game played by an Human
        Methods
        -------
        get_move()
            Execute the move given by the player
    """

    def __init__(self, r_p):
        """
        :param r_p: type of piece used ('r' = random, 'p' = pi)
        """
        super().__init__(r_p)
        self.player = True

    def get_move(self):
        pass


def pl_main(r_p, numOfRun):
    #  get arguments when AI file is executed by the menu
    caption = "Game {game}".format(game=1)
    pygame.display.set_caption(caption)
    numOfRun = int(numOfRun)
    #  loop to run  the game with AI for numOfRun executions
    for x in range(numOfRun):
        p = Player(r_p)
        newScore, weights, tot_time, n_moves, avg_move_time, moves_s = p.run()
        print("Game achieved a score of: ", newScore)
        print("weights: ", weights)
        print("tot run time: ", tot_time)
        print("#moves:  ", n_moves)
        print("avg time per move: ", avg_move_time)
        print("moves/sec:  ", moves_s)
    menu.main()

if __name__ == "__main__":
    pl_main('r', 1)
