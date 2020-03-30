from abc import ABC
from com.Core.BaseGame import BaseGame
from com.Menu import menu
import tkinter as tk
import pygame
import time


class Player(BaseGame):
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
        super().__init__(r_p, gdSidePanel='no', title=None, description=None)
        self.player = True

    def get_move(self):
        time.sleep(0.5)


def pl_main(r_p, numOfRun):
    #  get arguments when AI file is executed by the menu
    caption = "Game {game}".format(game=1)
    pygame.display.set_caption(caption)
    numOfRun = int(numOfRun)
    AVG_runs = 0
    #  loop to run  the game with AI for numOfRun executions
    for x in range(numOfRun):
        p = Player(r_p)
        newScore, weights, tot_time, n_tetr, avg_move_time, tetr_s = p.run()
        AVG_runs = AVG_runs + newScore
        print("Game achieved a score of: ", newScore)
        print("tot run time: ", tot_time)
        print("#moves:  ", n_tetr)
        print("avg time per move: ", avg_move_time)
        print("moves/sec:  ", tetr_s)
    AVG_runs = AVG_runs / numOfRun
    if numOfRun > 1:
        print("AVGScore after ", numOfRun, " Runs : ", AVG_runs)


if __name__ == "__main__":
    pl_main('r', 1)
