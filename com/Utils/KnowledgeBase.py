from collections import namedtuple

#codifica le regole semplici



#shadows_S = {
#    [0, 0, 1]: 1,
#    [0, -1]: 2,
#}



#codifica le regole composte

#crea dizionario con le regole
#grandezza 4
f_4 = (0, 0, 0, 0)


#grandezza 3
f_3 = (0, 0, 0)
f_d_u = (0, -1, 0)
f_f_u = (0, 0, 1)
f_d_f = (0, -1, -1)
f_u_f = (0, 1, 1)
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

a = [0, 0, -1, 0, 1, 1, 0, 0, 0, 2]         #cresta


Pa = list()                                 #insieme delle parti della cresta

#non utilizziamo il riferimento assolumo ma quello relativo per definire la cresta
#c[x] = b[x] - b[x-1]

for x in range(int(len(a))):                #1
    Pa.append((x, [0]))

for x in range(int(len(a) - 1)):            #2
    Pa.append((x, [0, a[x+1] - a[x]]))

for x in range(int(len(a) - 2)):            #3
    Pa.append((x, [0, a[x+1] - a[x], a[x+2] - a[x+1]]))

for x in range(int(len(a) - 3)):            #4
    Pa.append((x, [0, a[x+1] - a[x], a[x+2] - a[x+1], a[x+3] - a[x+2]]))

b = [0, 1, 0] #ombra del pezzo

c = [0]*10
for x in range(-5, 6):
    c[x] =[x, b]

print('ombra b')
print(b)

print('Insieme delle parti')
print(Pa)

print('possibili posizioni di b')
print(c)


for pax in Pa:
    start, seq = pax
    if seq == b:
        print('yes, start: ', str(start))


Shadow = namedtuple('Shadow', [
    'shape',
    'rotation',
    'sequence',
    'priority'
])

shadows = (
    Shadow('S', 0, [0, 0, 1], 1),
    Shadow('S', 1, [0, -1], 0),
    Shadow('Z', 0, [0, -1, 0], 1),
    Shadow('Z', 1, [0, 1], 0),
    Shadow('I', 0, [0, 0, 0, 0], 0),
    Shadow('I', 1, [0], 0),
    Shadow('O', 0, [0, 0], 0),
    Shadow('J', 0, [0, 0, 0], 1),
    Shadow('J', 1, [0, 2], 2),
    Shadow('J', 2, [0, 0, -1], 3),
    Shadow('J', 3, [0, 0], 0),
    Shadow('L', 0, [0, 0, 0], 1),
    Shadow('L', 1, [0, -2], 2),
    Shadow('L', 2, [0, 1, 0], 3),
    Shadow('L', 3, [0, 0], 0),
    Shadow('T', 0, [0, 0, 0], 0),
    Shadow('T', 1, [0, 1], 1),
    Shadow('T', 2, [0, -1, 1], 3),
    Shadow('T', 3, [0, -1], 2),
)

