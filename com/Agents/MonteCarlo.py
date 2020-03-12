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


class GameNode(object):
    def __init__(self, board, parent=None, move=None, depth=0):
        self.hashtable = [0] * self.hash_length  # tavola hash per evitare children duplicati
        self.board = board  # contiene la copia del gioco corrente
        self.move = move  # la mossa che ci ha portato a questo stato
        self.parent = parent  # riferimento al nodo genitore
        self.depth = depth
        self.visitedStates = []
        self.futureStates = []
        self.wins = 0
        self.plays = 0
        self.UCB = 0
        self.metrics = getParametersMC(self.board)

    # una specie di simulate_board, devo passargli il pezzo quando richiamo questo metodo
    def getFutureStates(self, falling_piece):
        if len(self.futureStates) == 0:
            depth_children = self.depth + 1

            for sideways in range(-5, 6, 1):
                for rotation in range(0, 4, 1):  # numero di rotazioni
                    action_child = rotation, sideways  # sarebbe la move
                    # simula il gioco facendo rotazioni e traslazioni in modo da ottenere il nuovo stato (per ogni mossa)
                    new_state = simulate_board(self.board, falling_piece, move)

                    child = GameNode(new_state, self, action_child, depth_children)

                    # hashing preprocess
                    child_grid_string = child.griToString()
                    hash_value = abs(hash(child_grid_string))

                    # se questo child non è stato ancora aggiunto, si fa un append alla children list
                    if (self.hashtable[hash_value % self.hash_length] == 0):
                        self.hashtable[hash_value % self.hash_length] = 1
                        self.future_states.append(child)

        return self.future_states

    # restituisce una copia della board
    def getBoard(self):
        board = [[0 for i in range(BOARDWIDTH)]
                 for i in range(BOARDHEIGHT)]
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                board[y][x] = self.board[x][y]
        return board

    # parte da controllare potrebbe essere necessario cancellare tutto, eventualmente aggiungere lo score a riga 109 e 113
    # trasforma la board in stringa
    def boardToString(self):
        state_string = ""
        board = [[0 for i in range(BOARDWIDTH)]
                 for i in range(BOARDHEIGHT)]
        for x in range(BOARDWIDTH):
            for y in range(BOARDHEIGHT):
                board[y][x] = self.board[x][y]

        for row in state:
            state_string += str(row)
            state_string += "\n"
        return state_string

    def __str__(self):
        if self.parent is None:
            return ("ROOT" + "\nBoard\n" + str(self.boardToString()) + "Depth: " + str(self.depth) + "\nPlays: " + str(
                self.plays) + "\nWins: " + str(self.wins) + "\nMetrics: " + str(self.metrics))
        else:
            return ("State:\n" + str(self.gridToStringPretty()) + "Action: " + str(self.action) + "\nDepth: " + str(
                self.depth) + "\nPlays: " + str(self.plays) + "\nWins: " + str(self.wins) + "\nMetrics: " + str(
                self.metrics))
