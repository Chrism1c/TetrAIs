from abc import ABC
from com.Core.BaseGame import BaseGame
import pygame
import sys


class Player(BaseGame, ABC):

    def __init__(self, r_p):
        super().__init__(r_p)
        self.player = True

    def get_move(self):
        pass


if __name__ == "__main__":
    caption = "Game {game}".format(game=1)
    pygame.display.set_caption(caption)
    r_p = sys.argv[1]
    numOfRun = int(sys.argv[2])
    for x in range(numOfRun):
        p = Player(r_p)
        newScore, weights = p.run()
        print("Game achieved a score of: ", newScore)
        print("weights ", weights)
