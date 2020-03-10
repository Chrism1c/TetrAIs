from com.Utils.KnowledgeBaseScheme import *
from collections import namedtuple

#codifica le regole semplici
# differenza tra il pezzo corrente e il pezzo precedente
differences_ = {
    -2: 'jump_down',
    -1: 'down',
    0: 'flat',
    1: 'up',
    2: 'jump_up',
}

differences = {
    'jump_down': -2,
    'down': -1,
    'flat': 0,
    'up': 1,
    'jump_up': 2,
}

#codifica le regole composte

#grandezza 4
flat_4 = ('flat', 'flat', 'flat', 'flat')

#grandezza 3
flat_3 = ('flat', 'flat', 'flat')



#grandezza 2



