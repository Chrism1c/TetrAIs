import time
import math
import random
import copy
import numpy as np
import operator
from abc import ABC

from com.Core.BaseGame import *
from com.Core.Model import *
from com.Utils.Utils import *
from com.Core.Plot import *

PSEUDO_INFINITY = 1000000000000.0


def shallowMaxSearch(root):
    future_states = root.getFutureStates()
    best_state = random.choice(future_states)
    max_val = - PSEUDO_INFINITY

    for i, state in enumerate(future_states):
        if max_val < state.heuristic:
            max_val = state.heuristic
            best_state = state

    return best_state


def DeepMaxSearch(root):
    future_states = root.getFutureStates()
    best_state = random.choice(future_states)
    max_val = - PSEUDO_INFINITY

    for i, state in enumerate(future_states):
        val = state.heuristic + shallowMaxSearch(state).heuristic
        if max_val < val:
            max_val = val
            best_state = state

    return best_state


class MonteCarlo(BaseGame, ABC):
    def __init__(self, r_p, board, parent=None, action=None, depth=0):
        super().__init__(r_p)
        self.hashtable = [0] * self.hash_length  # tavola hash per evitare children duplicati
        self.board = board  # contiene la copia del gioco corrente
        self.action = action  # la mossa che ci ha portato a questo stato
        self.parent = parent  # riferimento al nodo genitore
        self.depth = depth
        self.visitedStates = []
        self.futureStates = []
        self.wins = 0
        self.plays = 0
        self.UCB = 0
        self.metrics = getParametersMC(self.board)

    def get_move(self):
        return self.getMCMove(self.board, self.falling_piece, self.next_piece)

    def getMCMove(self):
        move = 0
        return move
