from builtins import print

import ete3

# x = ete3.Tree("((A,B),C);")
# print(x)

# t = ete3.Tree()
# t.populate(20, ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], random_branches=True, reuse_names=True)
# t.write(outfile="example_tree_1.printed9.txt", format=9)
# print("Print Tree: ",t)
# print("t.is_root? ",t.is_root())
# print("t.is_leaf? ",t.is_leaf())

# children = t.get_children()
# child1, child2 = t.get_children()
# lenChildren = len(t.get_children())
# print("len children: ", lenChildren)
# print("children: ", child1.get_children()[0])
# print("children: ", child2.get_children()[1])
#
# for x in range(lenChildren):
#     print("children: n° ",x," ", children[x])


# http://etetoolkit.org/docs/2.3/tutorial/tutorial_drawing.html#overview
# http://evomicsorg.wpengine.netdna-cdn.com/wp-content/uploads/2019/01/ete_tutorial.pdf

# tx = ete3.Tree()
# print(tx)
# # tx = tx.add_child(name = "Root")
# # print(tx)
# tx.populate(10, ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"], random_branches=True, reuse_names=True)
# print(tx)
# leaf = tx.get_leaves_by_name("J")[0]
# print(leaf.up)

# aggiungere figli ad un nodo dato il suo nome
# cambiare colore del nome del nodo dato il suo nome

from ete3 import TreeStyle, Tree

t = Tree()
t.populate(30)
ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"
ts.arc_start = -180 # 0 degrees = 3 o'clock
ts.arc_span = 180
t.show(tree_style=ts)