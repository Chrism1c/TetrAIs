import tkinter as tk
import os

fileName = 'testo.txt'

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

x = 300
y = 479

posX = (SCREEN_WIDTH / 2) - 794
posY = (SCREEN_HEIGHT / 2) - 260

windTitle = 'Guide'


def sidePanel(titolo, tipoDescrizione):
    """
    This function makes a side panel. It shows the description of the algorithm executed

    :param titolo: a string that contains the name of the IA
    :param tipoDescrizione: a string that contains the description of the IA
    """
    # titolo = "Questo è un titolo"
    root = tk.Tk()
    root.title(windTitle)
    label = tk.Label(root, bg='black', fg='white')
    label['text'] = titolo
    label.config(font=('freesansbold', 43))
    label.pack(padx=4, pady=4)

    T = tk.Text(root, width=50, height=29)
    T.configure(font='freesansbold 13')
    # test = loadTextFromFile(fileName)
    T.insert(tk.END, tipoDescrizione)
    T.config(bg='black', fg='white')
    T.pack(padx=2, pady=2)

    root.geometry("+{}+{}".format(int(posX), int(posY)))
    root.update()


# strings that contain the text that must be shown during execution

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
