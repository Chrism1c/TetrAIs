from com.Core.BaseGame import BaseGame
from abc import ABC
import copy
from com.Utils.Utils import simulate_board, get_parameters
from com.Core.Model import PIECES, BOARDWIDTH, BOARDHEIGHT, PIECES_COLORS, TEMPLATEWIDTH
import random
import time
from operator import itemgetter
import sys
from com.Utils.NetworkX import TreePlot

MonteCarloPlot = TreePlot()
ROOTZERO = "ROOT"

class MonteCarlo(BaseGame, ABC):
    global MonteCarloPlot
    def __init__(self, r_p, mode, treePlot):
        super().__init__(r_p)
        self.mode = mode
        self.action = ""
        self.deepLimit = 2
        self.treePlot = treePlot

    def get_move(self):
        return self.MonteCarlo_MCTS(self.board, self.falling_piece, self.next_piece)

    def get_expected_score(self, test_board):
        # Calcola lo score sulla board di test passando il vettore dei pesi di ogni metrica
        fullLines, vHoles, vBlocks, maxHeight, stdDY, absDy, maxDy = get_parameters(test_board)
        test_score = float(
            (fullLines * 1.8) - (vHoles) - (vBlocks * 0.5) - ((maxHeight ** 1.5) * 0.002) - (stdDY * 0.01) - (
                    absDy * 0.2) - (maxDy * 0.3))
        return test_score, fullLines

    # MonteCarlo Step 1 (DFS BASED)
    def MonteCarlo_MCTS(self, board, piece, NextPiece):
        # Main Step1 Branch Analyser
        deep = 1
        numIter = 0
        # print("Branch Deep :", deep, " Real piece: ", piece['shape'])
        self.action = str(piece['shape'])
        topStrategies = list()
        strategy = None
        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in range(-5, 6):
                numIter = numIter + 1
                # print("<<<<<<<<<< Enter into branch n° ", numIter)
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)

                fatherName = str(piece['shape'] + ":" + str(sideways) + ":" + str(0))
                MonteCarloPlot.addedge(ROOTZERO, fatherName)
                # print("ROOTZERO X fatherName ===== ", fatherName)

                if test_board is not None:
                    test_score, fullLines = self.get_expected_score(test_board)
                    NextScore = 0
                    selfAction = ""

                    if self.deepLimit > 1:
                        NextScore, selfAction = self.MonteCarlo_MCTS_stepx(board, deep + 1, NextPiece, fatherName)
                    else:
                        # print("EXECPTION = self.action : ", self.action)
                        selfAction = self.action
                        self.action = str(piece['shape'])
                    NextScore = NextScore + test_score

                    if not strategy or strategy[2] < NextScore:
                        strategy = (rot, sideways, NextScore, selfAction)
                        topStrategies.append(strategy)

        if self.treePlot and self.deepLimit < 3:
            MonteCarloPlot.plot()
        MonteCarloPlot.Graph.clear()

        print("--->> TOP STRATEGIES <<---")
        topStrategies = sorted(topStrategies, key=itemgetter(2), reverse=True)
        for x in range(len(topStrategies)):
            print(topStrategies[x])

        # print("---X>> Winner STRATEGY <<X---",topStrategies[0])

        return [topStrategies[0][0], topStrategies[0][1]]

    def MonteCarlo_MCTS_stepx(self, board, deep, piece, fatherName):
        # Recursive Scanning of Virtual Branches on Deep >2
        # print("deep, :", deep, " piece: ", piece['shape'])
        inizio = -5
        fine = 6
        self.action = self.action + "-" +piece['shape']
        strategy = None

        sidewaysIndex = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5] #11 Sideways

        if self.mode == 'random':
            if deep > 2:
                # print("Random DeathSelection")
                toRemove = random.randint(0, 8)
                print("------------------- daRimuovere ",toRemove)
                for z in range(toRemove):
                    deathindex = random.randint(0, len(sidewaysIndex) - 1)
                    #print("*** deathindex: ",deathindex-1)
                    sidewaysIndex.pop(deathindex)
                lenindex = len(sidewaysIndex)
                # print('@@@ sidewaysIndex : ',sidewaysIndex," W len of :",lenindex)
                # inizio = random.randint(-5, 0)
                # fine = random.randint(1, 6)

        for rot in range(0, len(PIECES[piece['shape']])):
            for sideways in sidewaysIndex: #range(inizio, fine):
                # print("sideways and rot",sideways, " ",rot)
                move = [rot, sideways]
                test_board = copy.deepcopy(board)
                test_piece = copy.deepcopy(piece)
                test_board = simulate_board(test_board, test_piece, move)

                NameNode = str(piece['shape'] + ":" + str(sideways) +  ":" + str(deep))
                MonteCarloPlot.addedge(fatherName, fatherName + "_" + NameNode)
                # print("fatherName === ", fatherName, " NodeNameX === ", fatherName + "_" + NameNode)

                if test_board is not None:
                    test_score, fullLines = self.get_expected_score(test_board)
                    # print("STEPX: test_score: ",test_score)

                    # print("yyyy: ", deep, " ",self.deepLimit)
                    if deep < self.deepLimit:
                        # print("dxxxxx: ", deep)
                        RandPiece = self.__random()
                        deepScore, pieceType = self.MonteCarlo_MCTS_stepx(board, deep+1, RandPiece, fatherName+"_"+NameNode)
                        test_score = test_score + deepScore

                    if not strategy or strategy[2] < test_score:
                        strategy = (rot, sideways, test_score)
        return strategy[2], self.action

    def __random(self):
        # return a random new piece
        shape = random.choice(list(PIECES.keys()))
        new_piece = {
            'shape': shape,
            'rotation': random.randint(0, len(PIECES[shape]) - 1),
            'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
            'y': -2,  # start it above the board (i.e. less than 0)
            # 'color': random.randint(1,len(COLORS) - 1)
            'color': PIECES_COLORS[shape]
        }
        return new_piece

if __name__ == "__main__":
    r_p =  sys.argv[1]              # 'r' # 'p'
    mode =  sys.argv[2]               # 'full' # 'random'
    numOfRun = int(sys.argv[3])    # 1

    for x in range(numOfRun):
        mc = MonteCarlo(r_p, mode)
        newScore, _ = mc.run()
        print("Game achieved a score of: ", newScore)


"""
** Implementazione **
Inizialmente abbiamo tentato di utilizzare una variante di Monte Carlo Tree Search chiamata
Blind-Bandit MCTS. Blind Bandit MCTS cerca in profondità, usando una politica casuale, 
nel tentativo di trovare una condizione "vincente". Dal momento che non puoi mai "vincere"
a Tetris, stabiliamo la condizione di vittoria se le funzioni euristiche dovesse essere all'interno
di un certo valore. Pertanto, l'albero esplorerebbe fino a quando non dovesse trovasse una condizione di vittoria,
e sposta il pezzo corrente per trovare questa determinata condizione.
Il vantaggio dell'approccio Blind-Bandit è che la ricerca può essere
accelerata rapidamente usando una tabella hash [5]. Dato che stai cercando in profondità, la
tabella hash salva i risultati e migliora la velocità che il gioco impiega ad esplorare
un albero. Man mano che il gioco procede, la tabella hash si espande, il che a sua volta libera
più tempo per consentire la ricerca.

Il problema con questo approccio è che i pezzi futuri sono casuali e non precedentemente determinati. 
Pertanto, i pezzi si sposteranno in una posizione difficile che dipende da un pezzo futuro. 
Quando quel pezzo non arriva, il precedente pezzo rimane nella stessa "povera" posizione.
Abbiamo comunque mantenuto una tabella hash locale per ogni nodo, per evitare di rivisitare gli stati.
Ad esempio, il pezzo quadrato non può essere ruotato, quindi non ha senso cercare attraverso tutte le possibili rotazioni di esso.
Di conseguenza, invece dell'approccio Blind-Bandit, abbiamo valutato l'euristica
su ciascun nodo. Inizialmente abbiamo basato la validità di un'azione basata sull' ultima euristica di ciascun ramo. 
Tuttavia, ciò significava che qualsiasi percorso con le gocce del pezzo ideale saranno favorite e finiremo 
con lo stesso problema dell'approccio Blind-Bandit.

Invece di prendere l'ultimo nodo come valore euristico, abbiamo sommato il
euristica da ciascun nodo figlio e normalizzata dal numero di nodi. 
Come tale, invece di valutare il miglior percorso possibile, stiamo invece valutando la robustezza della posizione del pezzo per ciascun nodo figlio. 
Se un'azione dà una buona euristica, sappiamo che si tratta di bambini casuali e dei loro casuali
tutti i bambini hanno una buona euristica. 
Questo si oppone all'azione un percorso in cui il nodo finale è l'ideale, ma la deviazione dal percorso causerà 
un errore nel posizionamento dei pezzi.
Nel nostro ultimo tentativo di risolvere il problema, abbiamo convalidato le situazioni "vincenti" di
condizionamento sull'altezza e il numero di fori della radice dell'albero (la corrente
stato), la foglia (la scelta più immediata) e l'ultimo playout (il futuro)
raggiunto nella simulazione. Questo ci ha dato i migliori risultati, ma è stato comunque
non in grado di competere con le prestazioni del semplice Breadth-First-Search.
Va detto che a causa dei limiti delle prestazioni nel motore di gioco, noi
non abbiamo tentato simulazioni con una profondità superiore a 3, né abbiamo esplorato
più di 30 nodi. A causa delle limitazioni delle prestazioni, non abbiamo lavorato nel migliorare le prestazioni del motore, 
che avrebbe potuto permetterci di funzionare più iterazioni di MCTS in meno tempo, aumentando quindi le nostre informazioni
guadagnare durante la pianificazione.

** 5 Riepilogo e conclusioni **
In questo articolo, abbiamo sviluppato un'intelligenza artificiale in grado di riprodurre Tetris con una ragionevole competenza 
utilizzando Monte Carlo Tree Search (MCTS) basato su banditi. MCTS esplora le possibilità casuali a una profondità più profonda 
del possibile con la prima ricerca dell'albero (BFS). L'intelligenza artificiale è stata in grado di cancellare 27 linee senza intervento umano.
Sebbene questi numeri non siano enormi, mostra che MCTS può funzionare come AI competente per giochi discreti non deterministici. 
Probabilmente potremmo migliorare i risultati implementando algoritmi genetici per migliorare i nostri pesi e perfezionare le funzioni euristiche. 
Allo stesso modo, potremmo salvare i risultati di hashing tra i giochi, il che farebbe migliorare MCTS con più giochi giocati. 
La nostra attuale implementazione è ancora piuttosto rudimentale e ha ampi margini di miglioramento.
Sorprendentemente, BFS ha superato MCTS. Riteniamo che MCTS sia distorto avendo percorsi casuali con cadute di pezzi ideali, 
che poi sposteranno il pezzo corrente in una posizione sbagliata in previsione di quei pezzi futuri.
Dal momento che il gioco è stocastico, i pezzi non arrivano mai e MCTS rimane in peggiore stato di gioco. 
Prevediamo che MCTS sarà l'ideale in scenari in cui vi è un chiaro vantaggio nell'esplorazione in profondità, 
piuttosto che in profondità. Sono preferibili situazioni con poche azioni e quelle in cui è possibile annullare le azioni. 
Ad esempio, spostare un personaggio attraverso una griglia (come in Pac-Man) sarebbe uno scenario ideale.
Tuttavia, con Tetris, MCTS non offre alcun chiaro vantaggio.

"""