import matplotlib
import networkx as nx
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class TreePlot:
    """
    Class useful to create an object of type networkx and plot decisional TreePlot of Ais
    """

    def __init__(self):
        self.Graph = nx.Graph()
        self.ROOTZERO = "ROOT"

    def addedge(self, a, b):
        """
        wrapper for add_edge function for Graph object
        :param a: label of first node
        :param b: label of second node
        :return: None
        """
        self.Graph.add_edge(a, b)

    def plot(self):
        """
        function to plot the Graph
        :return: None
        """

        options = {
            'with_labels': True,
            'node_color': 'lightblue',  # blue
            'node_size': 1000,
            'node_shape': 's',  # 'd', '^', 'o',  '^',
            'font_size': 20,
            'font_weight': 'bold'
        }

        type_of_draw = 'kamada_kawai'
        # DRAW IN DIFFERENT LAYOUT
        if type_of_draw == 'planar':
            nx.draw_planar(self.Graph, **options)
        elif type_of_draw == 'spectral':
            nx.draw_spectral(self.Graph, **options)
        elif type_of_draw == 'kamada_kawai':
            nx.draw_kamada_kawai(self.Graph, **options)
        elif type_of_draw == 'spring':
            nx.draw_spring(self.Graph, **options)

        print("Plotting 4 You...")
        plt.draw()
        plt.show()
        # plt.savefig("saved_Plot4You.png")
        plt.clf()


# example to test
if __name__ == "__main__":
    tp = TreePlot()
    tp.addedge(0, 1)
    tp.addedge(0, 2)
    tp.addedge(0, 3)
    tp.addedge(0, 4)

    tp.addedge(4, 8)
    tp.addedge(4, 9)
    tp.plot()
