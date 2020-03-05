from abc import ABC
from com.Core.BaseGame import BaseGame
import pygame


class Player(BaseGame, ABC):

    def __init__(self, r_p):
        super().__init__(r_p)
        self.player = True

    def get_move(self):
        pass


if __name__ == "__main__":
    caption = "Game {game}".format(game=1)
    pygame.display.set_caption(caption)
    # q = Square(4)

    p = Player('r')
    newScore, weights = p.run()
    print("Game achieved a score of: ", newScore)
    print("weights ", weights)
