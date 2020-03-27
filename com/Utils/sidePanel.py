import tkinter as tk
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

x = 300
y = 479

posX = (SCREEN_WIDTH / 2) - 794
posY = (SCREEN_HEIGHT / 2) - 260

windTitle = 'Guide'


class SidePanel:
    def __init__(self, title, description):
        self.root = tk.Tk()
        self.title = title
        self.description = description

    def showSidePanel(self):
        """
        This function creates a side panel in which it is printed the name and the description of the IA currently running
        :param root: an object of the Tk class,responsible for the creation of the side panel
        :param titolo: a string containing the name of the IA
        :param tipoDescrizione: a string containing the descrpition of the IA
        :return: None
        """
        self.root.title(windTitle)
        label = tk.Label(self.root, bg='black', fg='white')
        label['text'] = self.title
        label.config(font=('freesansbold', 43))
        label.pack(padx=4, pady=4)

        T = tk.Text(self.root, width=50, height=29)
        T.configure(font='freesansbold 13')
        T.insert(tk.END, self.description)
        T.config(bg='black', fg='white')
        T.pack(padx=2, pady=2)

        self.root.geometry("+{}+{}".format(int(0), int(0)))
        self.root.update()

    def destroyPanel(self):
        self.root.destroy()


titleDFS = 'DFS Guide'
descriptionDFS = 'descrizione dfs'

titleLS = 'LS Guide'
descriptionLS = 'nvidsnvosdnvo'

titleSDGQL = 'SDGQL Guide'
descriptionSDQL = 'kkkkk'

titleGen = 'Genetic Guide'
descriptionGen = 'zzzzz'

titleMCTS = 'MCTS Guide'
descriptionMCTS = 'yyyyy'

titleRB = 'Rule Based Guide'
descriptionRB = 'xxxxxx'
