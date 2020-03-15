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


def loadTextFromFile(fileName):
    file = open(fileName, 'r', encoding="utf8")
    if file.mode == 'r':
        text = file.read()

    return text


def sidePanel(titolo, tipoDescrizione):
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
    tk.mainloop()


titoloDFS = 'DFS Guide'
descrizioneDFS = 'descrizione dfs'

titoloSDGQL = 'SDGQL Guide'
descrizioneSDGQL = 'nidsabfdhfi'

titoloGen = 'Genetic Guide'
descrizioneGen = 'nowdhvds'

titoloMCTS = 'MCTS Guide'
descrizioneMCTS = 'chidshvodh'
