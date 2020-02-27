"""
l'idea alla base di questa ia probabilistica è quella di cercare di predire quale sarà la sequenza di tetramini che cadranno
così da cercare di massimizzare il punteggio organizzando la board di conseguenza

per capire qual è la probabilità di base della scelta dei pezzi, si potrebbe o controllare con quale probabilità la funzione
random decide quale dei 7 pezzi prendere, oppure solo quando viene deciso di utilizzare questa ia si può decidere di utilizzare
una funzione ad hoc, in modo da essere certi che i tetramini vengano decisi con un criterio.

teoricamente random.choice dovrebbe assegnare a ognuno degli elementi della lista uguali probabilità (quindi ogni tetramino
avrà una probabilità pari a 1/7 di essere scelto

un modo per calcolare la probabilità di indovinare quale tetramino sarà scelto è quello di utilizzare il modello di bernoulli
(poichè nell'esempio più semplice esso riguarda l'estrazione consecutiva con rimessa di palline che possono essere o nere o bianche
quindi cerca di calcolare la probabilità con cui alla j-esima estrazione si tratti di una pallina bianca)

a tale scopo è possibile utilizzare il coefficiente binomiale per il calcolo della probabilità (da controllare se esso è
applicabile a più di due elementi distinti)

ho assodato che la probabilità con cui un pezzo venga scelto è uguale per tutti e 7, quello che potrei fare è magari capire
se posso applicare la scelta ad un n numero di tetramini

"""

from tetris_utils import *
from tetris_game_test import *
import random


# nuova funzione per la scelta del tetramino, serve dare in input un numero, che alla prima chiamata può essere zero ma
# a chiamate successive ha bisogno di avere in input il numero generato precedentemente (regole basate sulla standard
# edition
def randProbChoice(n):
    i = int(random.randint(1, 7))
    if i == n:
        randProbChoice(n)
    else:
        return i


if __name__ == '__main__':
    randProbChoice()
