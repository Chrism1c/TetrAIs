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

#crea dizionario con le regole

#grandezza 4
f_4 = ('flat', 'flat', 'flat', 'flat')


#grandezza 3
f_3 = ('flat', 'flat', 'flat')
f_d_u = ('flat', 'down', 'up')
f_f_u = ('flat', 'flat', 'up')
f_d_f = ('flat', 'down', 'flat')
f_u_f = ('flat', 'up', 'flat')
f_f_d = ('flat', 'flat', 'down')


#grandezza 2
f_2 = ('flat', 'flat')
f_d = ('flat', 'down')
f_u = ('flat', 'up')
f_jd = ('flat', 'jump_down')
f_ju = ('flat', 'jump_up')


#grandezza 1
f_1 = ('flat')

shadows_S = {
    f_f_u: 1,
    f_d: 2
}

shadows_Z = {
    f_d_f: 1,
    f_u: 2
}


shadows_J = {
    f_f_d: 1,
    f_ju: 2,
    f_3: 3,
    f_2: 4
}


shadows_L = {
    f_u_f: 1,
    f_jd: 2,
    f_3: 3,
    f_2: 4
}


shadows_I = {
    f_1: 1,
    f_4: 2,
}

shadows_O = {
    f_2: 1
}

shadows_T = {
    f_d_u: 1,
    f_d: 2,
    f_u: 3,
    f_3: 4,
}
