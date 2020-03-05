"""
 considerare come metriche:
 + numero di linee rimosse con quella mossa (fatto)
 - gaps (fatto)
 - numTetraminoes (fatto)
 - max_high**1.5 (fatto)
 - standard_deviation_heights (fatto)
 - abs_diffCol (fatto)
 - max_diffCol(fatto)
"""

from tetris_utils import *
from tetris_game_test import *
import numpy as np

gen0FileName = "gen0FileName.txt"


# crea un nuovo cromooma con geni random
def getNewChromosome():
    return np.random.uniform(low=0.0, high=1.0, size=7)


# funzione che restituisce il vettore che contiene le metriche calcolate
def getScore(board):
    fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol = get_parameters(
        board)
    score = [fullLines, gaps, numTetraminoes, max_height, standardDvHeights, abs_diffCol, max_diffCol]
    return score


# serve per calcolare lo score del tetramino che si sta piazzando in base ai valori assegnati al cromosoma
def calTestScore(chromosome, board):
    # così mi calcolo le metriche di cui ho bisogno per l'algoritmo genetico
    score = getScore(board)

    testScore = float(
        (score[0] * chromosome[0]) - (score[1] * chromosome[1]) - (score[2] * chromosome[2]) - (
                (score[3] ** 1.5) * chromosome[3]) - (score[4] * chromosome[4]) - (
                score[5] * chromosome[5]) - (score[6] * chromosome[6]))

    return testScore, score[0]


# Funzione che calcola lo score pesato relativo alla board corrente
def calculateWScore(chromosome, board):
    score = getScore(board)
    wscore = 0
    for x in range(len(score)):
        # molto probabilmente è da riformulare, possibili somme e moltiplicazioni per i valori del cromosoma
        wscore -= score[x] * chromosome[x]
    print("Wscore = ", wscore)
    return wscore


"""
funzione che calcola la mossa da effettuare in base ai valori dei cromosomi, lo score è calcolato usando la funzione calTestScore
simula il piazzamento di due tetramini (attuale e successivo) e vede in quale posizione ottiene uno score migliore e piazza il tetramino
nella posizione ritenuta migliore
"""


def getMove(board, piece, nextPiece, chromosome):
    # bisogna fare una prova in cui posiziono il pezzo in tutti i modi possibili su una board di prova
    # e ogni volta calcolo lo score

    start = time.perf_counter()

    bestRot = 0
    bestSide = 0
    bestScore = -99

    nextScore = (0, 0, -99)  # rotazione, sideway, score
    bestLine = -1
    nextLine = -1

    for rotation in range(0, len(PIECES[piece['shape']])):
        for sideway in range(-5, 6):
            move = [rotation, sideway]
            testBoard = copy.deepcopy(board)
            testPiece = copy.deepcopy(piece)
            testBoard = simulate_board(testBoard, testPiece, move)

            if testBoard is not None:
                # sceglie la mossa migliore in combo con il pezzo successivo
                for rotation2 in range(0, len(PIECES[piece['shape']])):
                    for sideway2 in range(-5, 6):
                        move2 = [rotation2, sideway2]
                        testBoard2 = copy.deepcopy(board)
                        testPiece2 = copy.deepcopy(nextPiece)
                        testBoard2 = simulate_board(testBoard, testPiece, move)
                        if testBoard2 is not None:
                            testScore2, nextLine = calTestScore(chromosome, testBoard2)
                            if nextScore[2] < testScore2:
                                nextScore = [rotation2, sideway2, testScore2]
                if bestScore < nextScore[2]:
                    bestScore = nextScore[2]
                    bestSide = sideway
                    bestRot = rotation

    finish = time.perf_counter()
    print(f'Finito in {round(finish - start, 2)} secondi')

    return [bestRot, bestSide]

# Create Gen0
def createGen0(num):
    gen0 = list()
    for i in range(num):
        gen0.append(getNewChromosome())

    return gen0


# Crossing Chromosoma function
def crossingchromosome(a, b):
    # print("crossingfunction ")
    # print("a = ",a)
    # print("b = ",b)
    newchromosome = [0] * 6  # nuovo cromosoma vuoto
    # print("newchromosome = ",newchromosome)
    for x in range(6):
        if random.randint(0, 9) == 1:  # 10% di possibilità di prelevare il cromosoma dal Genitore 1
            newchromosome[x] = a[x]
            # print("Gene from Parent_1 =",a[x])
        elif random.randint(0, 9) == 2:  # 10% di possibilità di prelevare il cromosoma dal Genitore 2
            newchromosome[x] = b[x]
            # print("Gene from Parent_2 =",b[x])
        else:
            newchromosome[x] = (a[x] + b[
                x]) / 2  # 80% di possibilità di prelevare il cromosoma dalla Media dei 2 Genitori
            # print("Gene from Merged genes =",newchromosome[x])
        newchromosome[x] += mutation(newchromosome[x])
    # print("newchromosome = ",newchromosome)
    return newchromosome


# funzione fitness alternativa, che tiene conto del numero di tetramini piazzati
# ma anche dello score finale
def fitnessFunction(numTetraminoes, score):
    Newscore = (score + numTetraminoes) * 0.1
    print("***************************************** fitnessFunctionAlt = ", Newscore)
    return Newscore


# somma i valori contenuti nel vettore vFitness,
# che sostanzialmente contiene i valori fitness
# delle varie partite fatte con lo stesso cromosoma, e ne fa la media
def avgFitness(vFitness):
    mFitness = 0
    for x in vFitness:
        mFitness += vFitness[x]
    return mFitness / len(vFitness)


def mutation(a):
    if random.randint(1, 10) == 10:  # 10% di possibilità di mutazione
        if a >= 4.5 and a <= 5.0:
            return -0.1 * random.randint(1, 5)
        else:
            return 0.1 * random.randint(1, 5)
    else:
        return 0  # 90% di possibilità di non mutazione


# Serch top k best Chromosome (based on score)
def bestChromosomeSearch(populationWScore, k):
    bestK = list()
    orderedChromosome = sorted(populationWScore, key=itemgetter(6), reverse=True)
    # for x in range(len(orederedChromosome)):
    #    print(chromoListToChromoStr_Scored(orederedChromosome[x])+" - Print
    #    orederedChromosomes - ")
    for x in range(k):
        orderedChromosome[x].pop(len(orderedChromosome[x]) - 1)
        bestK.append(orderedChromosome[x])
        print(chromoListToChromoStr(orderedChromosome[x]) + " - Print bestK - ")
    return bestK


def kChoice(populationWScore):
    orderedPopulation = sorted(populationWScore, key=itemgetter(6), reverse=True)
    lenP = len(orderedPopulation)
    avgScore = 0
    k = 0
    pow2 = [2 ** x for x in range(0, 7)]
    for x in range(lenP):
        avgScore += orderedPopulation[x][6]
    avgScore /= lenP
    print(avgScore)
    for x in range(lenP):
        if orderedPopulation[x][6] >= avgScore:
            k += 1
    print(k)
    pow2.append(k)
    pow2.sort()
    indexK = pow2.index(k)
    k = pow2[indexK + 1]
    print(k)
    return k


"""
if __name__ == '__main__':
    gen0 = list()
    gen0 = createGen0(2)

    chrom1 = gen0[0]

    print(gen0)
    print("stampa primo cromosoma")
    print(chrom1)

# FUNZIONI REIMPLEMENTATE

# Create Gen0
def createGen0(num):
    file = open(fileName, "w")
    file.close
    gen0 = list()
    for i in range(num):
        gen0.append(getNewChromosome())
    saveOnFile(populationFileName, gen0)
"""
