import tkinter as tk
import os

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

x = 300
y = 479

posX = (SCREEN_WIDTH / 2) - 794
posY = (SCREEN_HEIGHT / 2) - 260

windTitle = 'Guide'


def showSidePanel(root, titolo, tipoDescrizione):
    """
    This function creates a side panel in which it is printed the name and the description of the IA currently running
    :param root: an object of the Tk class,responsible for the creation of the side panel
    :param titolo: a string containing the name of the IA
    :param tipoDescrizione: a string containing the descrpition of the IA
    :return: None
    """
    root.title(windTitle)
    label = tk.Label(root, bg='black', fg='white')
    label['text'] = titolo
    label.config(font=('freesansbold', 43))
    label.pack(padx=4, pady=4)

    T = tk.Text(root, width=50, height=29)
    T.configure(font='freesansbold 13')
    T.insert(tk.END, tipoDescrizione)
    T.config(bg='black', fg='white')
    T.pack(padx=2, pady=2)

    # decommentando la riga 40 e commentando la riga 41 è possibile cambiare la posizione di spawn del sidepanel
    # root.geometry("+{}+{}".format(int(posX), int(posY)))
    root.geometry("+{}+{}".format(int(0), int(0)))
    root.update()


titoloDFS = 'DFS Guide'
descrizioneDFS = 'descrizione dfs'

titoloSDGQL = 'SDGQL Guide'
descrizioneSDGQL = 'kkkkk'

titoloGen = 'Genetic Guide'
descrizioneGen = 'zzzzz'

titoloMCTS = 'MCTS Guide'
descrizioneMCTS = 'yyyyy'

titoloRB = 'Rule Based Guide'
descrizioneRB = 'xxxxxx'

if __name__ == "__main__":
    root = tk.Tk()
    print("prova1")
    showSidePanel(root, titoloDFS, descrizioneDFS)
    print("prova2")
    #root.destroy()
