#!/usr/bin/python3
# -*- coding: utf-8 -*-

#import classe model
from tetris_model import BOARD_DATA, Shape
from tetris_utils import *
import math
from datetime import datetime
import numpy as np

#Classe che gestisce l'AI (Default)
class TetrisAI(object):
    
    # Funzione Cuore dell' AI che definisce la prossima mossa (Strategy) da
    # svolgere basandosi sul miglior score ottenibile
    # con il pezzo corrente e quello successivo
    def nextMove(self):
        t1 = datetime.now()         #Mi salvo la data corrente nella variabile t1
        if BOARD_DATA.currentShape == Shape.shapeNone:  #Se la forma corrente è ShapeNone (Nulla)
            return None

        currentDirection = BOARD_DATA.currentDirection
        currentY = BOARD_DATA.currentY
        _, _, minY, _ = BOARD_DATA.nextShape.getBoundingOffsets(0)  #Direction 0
        nextY = -minY
        
            #in base alla forma corrente definisco il range di direction
            #(d0Range) consentite
        strategy = None    
        if BOARD_DATA.currentShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            d0Range = (0, 1)
        elif BOARD_DATA.currentShape.shape == Shape.shapeO:
            d0Range = (0,)
        else:
            d0Range = (0, 1, 2, 3)

            #in base alla forma successiva definisco il range di direction
            #(d1Range) consentite
        if BOARD_DATA.nextShape.shape in (Shape.shapeI, Shape.shapeZ, Shape.shapeS):
            d1Range = (0, 1)
        elif BOARD_DATA.nextShape.shape == Shape.shapeO:
            d1Range = (0,)
        else:
            d1Range = (0, 1, 2, 3)
        
        for d0 in d0Range:     # Su ogni direction concessa dall forma corrente presente in d0Range,
            minX, maxX, _, _ = BOARD_DATA.currentShape.getBoundingOffsets(d0)   #prelevo le coordniate di limite sx e dx del tetramino
            for x0 in range(-minX, BOARD_DATA.width - maxX):        # Su ogni step tra -minX e la borad - maxX
                board = self.calcStep1Board(d0, x0)          #Simulo il drop del tetramino su una board copia
                for d1 in d1Range:
                    minX, maxX, _, _ = BOARD_DATA.nextShape.getBoundingOffsets(d1)
                    dropDist = self.calcNextDropDist(board, d1, range(-minX, BOARD_DATA.width - maxX))  #calcNextDropDist()
                    for x1 in range(-minX, BOARD_DATA.width - maxX):
                        score = self.calculateScore(np.copy(board), d1, x1, dropDist)   #Calcolo lo score della scelta in test
                        if not strategy or strategy[2] < score: #Se non ho strategy o lo score dello strategy corrente è minore dello score
                                                                #appena calcolato,
                            strategy = (d0, x0, score)          #assegno la nuova strategia a strategy, fornendo la direction (d0) la
                                                                #coordinata (x0) e lo score di tale strategia
        print("===", datetime.now() - t1)           #stampo a video quanto tempo ci ha impiegato per scegliere la mossa
        return strategy     #restituisco la strategia vincente e che verrà intrapresa

    #Funzione che calcola la distanza del prossimo drop (?)
    def calcNextDropDist(self, data, d0, xRange):
        res = {}
        for x0 in xRange:
            if x0 not in res:
                res[x0] = BOARD_DATA.height - 1
            for x, y in BOARD_DATA.nextShape.getCoords(d0, x0, 0):
                yy = 0
                while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):
                    yy += 1
                yy -= 1
                if yy < res[x0]:
                    res[x0] = yy
        return res

    #Funzione che restituisce una board sulla quale viene eseguito il dropdown
    #del tetramino su direction (d0) e coordinata (x0)
    def calcStep1Board(self, d0, x0):   #Fornisco in imput la direction d0 e la coordinata x0 che indica la
                                        #posizione possibile nel range [-minX, Board.width -maxX]
        board = np.array(BOARD_DATA.getData()).reshape((BOARD_DATA.height, BOARD_DATA.width))   #genera un array dai dati della BOARD e poi lo rende una matrice alta
                                                                                                #BOARD_DATA.height, e larga BOARD_DATA.width
        self.dropDown(board, BOARD_DATA.currentShape, d0, x0) #esegue il dropDown (di test) del tetramino corrente con la direction e la
                                                              #coordinata in prova
        return board #restituisce la matrice (di test) con il tetramino droppato usando da
                     #direction (d0) e la coordinata (x0) in input

    # Funzione madre che esegue il dropdown sulla board (data) con il tetramino
    # (shape) con direction (direction) e coordinta (x0)
    def dropDown(self, data, shape, direction, x0):
        dy = BOARD_DATA.height - 1
        for x, y in shape.getCoords(direction, x0, 0):
            yy = 0
            while yy + y < BOARD_DATA.height and (yy + y < 0 or data[(y + yy), x] == Shape.shapeNone):  #raggiungo il limite di drop (cresta dei tetramini)
                yy += 1
            yy -= 1
            if yy < dy:   
                dy = yy #assegno a dy (distanza) il valore appena decrementato "yy"
        # print("dropDown: shape {0}, direction {1}, x0 {2}, dy
                               # {3}".format(shape.shape, direction, x0, dy))
        self.dropDownByDist(data, shape, direction, x0, dy) #effettuo il dropdown vero e propio incollando una copia del tetramino sulla
                                                            #cresta dei tetramini
    
    #Funzione cuore che esegue il dropdown
    def dropDownByDist(self, data, shape, direction, x0, dist):
        for x, y in shape.getCoords(direction, x0, 0):                  #per ogni x, y
            data[y + dist, x] = shape.shape                             #copio il tetramino corrente nella board (data)
                                                                        #La board è rappresentata come una matrice avente in ogni cella un
                                                                        #numero indicante il tetramino a cui appartiene (?)

    #Funzione che calcola lo score relativo alla board corrente (step1Board)
    def calculateScore(self, step1Board, d1, x1, dropDist):
        # print("calculateScore")
        t1 = datetime.now()             # mi salvo il datetime in t1
        width = BOARD_DATA.width
        height = BOARD_DATA.height

        self.dropDownByDist(step1Board, BOARD_DATA.nextShape, d1, x1, dropDist[x1])     #Simula il dropdown sulla board di test (step1Board) con il tetramino
                                                                                        #successivo
        # print(datetime.now() - t1)

        # Term 1: lines to be removed
        fullLines, nearFullLines = 0, 0
        roofY = [0] * width                 #creo un vettore di width (10) zeri
        holeCandidates = [0] * width        #creo un vettore di width (10) zeri
        holeConfirm = [0] * width           #creo un vettore di width (10) zeri
        vHoles, vBlocks = 0, 0
        for y in range(height - 1, -1, -1):     #verifico le linee complete che andranno rimosse
            hasHole = False
            hasBlock = False
            for x in range(width):                          #per ogni celletta sull'intera riga a partire da
                                                            #sotto,
                if step1Board[y, x] == Shape.shapeNone:     #se la cella della board è una shapeNone, quindi ha valore 0,
                    hasHole = True                          #fleggo a true la variabile che indica che c'è un
                                                            #buco
                    holeCandidates[x] += 1                  #incremento la cella associata nel vettore holeCandidates
                else:
                    hasBlock = True                         #altrimente pongo il flag opposto a true e
                    roofY[x] = height - y                   # riempio roofY con l'altezza - y
                    if holeCandidates[x] > 0:               # Se holeCandidates > 0 lo travaso in holeConfirm e ripulisco
                                                            # holeCandidates
                        holeConfirm[x] += holeCandidates[x]
                        holeCandidates[x] = 0
                    if holeConfirm[x] > 0:                  #Incremento vBlocks se il buco è stato confermato
                        vBlocks += 1
            if not hasBlock:                                #Se non sono stati trovati blocchi esco dal
                                                            #ciclo di ricerca
                break
            if not hasHole and hasBlock:                    #Se non ci sono buchi e ci sono blocchi incremento
                                                            #fullLines di 1
                fullLines += 1
        vHoles = sum([x ** .7 for x in holeConfirm])
        maxHeight = max(roofY) - fullLines                  #Altezza massima del tetto - il numero di linee piene (da
                                                            #rimuovere) [altezza palazzo tetramini]
        # print(datetime.now() - t1)
            #Calcolo le metriche utili al confronto degli score delle scelte
                                                      #effettuabili
        roofDy = [roofY[i] - roofY[i + 1] for i in range(len(roofY) - 1)]     # ?

        if len(roofY) <= 0:         #Se la dimensione del tettoY è <= 0
            stdY = 0
        else:
            stdY = math.sqrt(sum([y ** 2 for y in roofY]) / len(roofY) - (sum(roofY) / len(roofY)) ** 2) # calcolo dello scarto quadratico medio delle altezze della cresta
        if len(roofDy) <= 0:        # Se la dimensione del tettoDy <= 0
            stdDY = 0
        else:
            stdDY = math.sqrt(sum([y ** 2 for y in roofDy]) / len(roofDy) - (sum(roofDy) / len(roofDy)) ** 2) # calcolo scarto quadratico medio relativa

        absDy = sum([abs(x) for x in roofDy])
        maxDy = max(roofY) - min(roofY)
        # print(datetime.now() - t1)
            # Determino lo score risultante da utilizzare ai fini del confronto
            # concatenando le metriche calcolate in precedenza
        score = fullLines * 1.8 - vHoles * 1.0 - vBlocks * 0.5 - maxHeight ** 1.5 * 0.02 - stdY * 0.0 - stdDY * 0.01 - absDy * 0.2 - maxDy * 0.3
        # print(score, fullLines, vHoles, vBlocks, maxHeight, stdY, stdDY,
        # absDy, roofY, d0, x0, d1, x1)
        return score
