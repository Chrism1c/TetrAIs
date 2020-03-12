import matplotlib as mplb
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
import time

mplb.use('TkAgg')

class TreePlot():
    def __init__(self, *args, **kwargs):
        self.Graph = nx.Graph()

    def addedge(self, a, b):
        self.Graph.add_edge(a, b)


    def plot(self):
        # print("Hello")
        options = {
            'with_labels': True,
            'node_color': 'lightblue',  # blue
            'node_size': 1000,
            'node_shape': 's',  # 'd', '^', 'o',  '^',
            'font_size': 20,
            'font_weight': 'bold'
        }

        type = 'kamada_kawai'
        # DRAW IN DIFFERENT LAYOUT
        if type == 'planar':
            nx.draw_planar(self.Graph, **options)
        elif type == 'spectral':
            nx.draw_spectral(self.Graph, **options)
        elif type == 'kamada_kawai':
            nx.draw_kamada_kawai(self.Graph, **options)
        elif type == 'spring':
            nx.draw_spring(self.Graph, **options)

        plt.draw()
        plt.show()
        # plt.savefig("filename2.png")
        plt.clf()
        # print("ByBy")


# if __name__ == "__main__":
#     tp = TreePlot()
#     tp.addedge(0, 1)
#     tp.addedge(0, 2)
#     tp.addedge(0, 3)
#     tp.addedge(0, 4)
#
#     tp.addedge(4, 8)
#     tp.addedge(4, 9)
#     tp.plot('spring')
