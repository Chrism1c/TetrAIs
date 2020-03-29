import tkinter as tk
import os

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

        T = tk.Text(self.root, width=51, height=29)
        T.configure(font='freesansbold 13')
        T.insert(tk.END, self.description)
        T.config(bg='black', fg='white')
        T.pack(padx=2, pady=2)

        self.root.geometry("+{}+{}".format(int(0), int(0)))
        self.root.update()

    def destroyPanel(self):
        self.root.destroy()


titleDFS = 'DFS Guide'
descriptionDFS = 'A generic search algorithm is independent of any search ' \
                 '\nstrategy. The idea is that given a graph, the paths are ' \
                 '\nincrementally explored starting from the starting nodes and' \
                 '\nthen reaching the target nodes.' \
                 '\n\nDFS is an uninformed search algorithm on graphs, in which the ' \
                 'system reasons on a model of the world made of states, in the ' \
                 'absence of uncertainty and with purposes to be achieved:' \
                 '\n\t- A flat representation of the domain;' \
                 '\n\t- In the state space, a way is sought to go from the ' \
                 '\n\t  current state to a goal.\n\n' \
                 'In in-depth research (DFS), the border is organized as a stack ' \
                 '\n(LIFO) in which the elements are added one at a time and the ' \
                 'one selected and taken will be the last added.'

titleLS = 'LS Guide'
descriptionLS = 'Local search is a heuristic method for solving computationally ' \
                'hard optimization problems. ' \
                '\n\nLocal search can be used on problems that can be formulated ' \
                'as finding a solution maximizing a criterion among a number ' \
                '\nof candidate solutions. ' \
                '\n\nLocal search algorithms move from solution to solution in the ' \
                'space of candidate solutions (the search space) by applying ' \
                '\nlocal changes, until a solution deemed optimal is found or a ' \
                '\ntime bound is elapsed.'

titleSDGQL = 'SDGQL Guide'
descriptionSDQL = 'The SDG_QL algorithm is based on the Stochastic Gradient ' \
                  '\nAscent algorithm as an optimization of Q-Learning.' \
                  '\nIt uses a "weights vector" representing the importance that ' \
                  '\neach metric has within the score calculation function. It ' \
                  '\nchooses the best move to play given a game scheme (State), ' \
                  '\nthe algorithm compares the possible moves (Action)' \
                  '\nconcerning only the current tetramino simulating a "drop ” of ' \
                  '\nthe tetramino on the board.​The AI calculates the Reward ' \
                  '\nrelating to the Action on the current State.' \
                  '\n\nThe Reward = 5 * (linesRemvd * lineRemvd)-(Hsum - oldHsum)' \
                  '\n\nThe TD-Update rule of the Q-learning algorithm returns the ' \
                  '\n"Q-value" as well as the new weight in the vector :​' \
                  '\n\nwx[i]=wx[i]+alpha*wx[i]*(Reward-oldPar[i]+gamma*newPar[i])​' \
                  '\n\nThe policy is probability of extracting the not highest Q-value' \
                  '\nmove. The proposed AI update its weights and converge ' \
                  '\ntowards values sufficient to obtain very high scores in ' \
                  '\nrelatively few “training runs”.​'

titleGen = 'Genetic Guide'
descriptionGen = 'Mashup:​' \
                 '\n\t- Reproductive trait of Genetic' \
                 '\n\t- ​Efficiency of Beam Search' \
                 '\n\nEach gene represents the weight of one of the heuristics used ' \
                 '\nby the system.' \
                 '\n\nNew generation composed of:' \
                 '\n\t- ½ better chromosomes of the previous generation​' \
                 '\n\t- ½ one point crossing between the best ' \
                 '\n\t  chromosomes of the previous generation​' \
                 '\n\nIn the crossing phase we select two of the best chromosomes' \
                 '\nand we couple them. For each chromosome gene that is the ' \
                 '\nchild of two parent chromosomes:' \
                 '\n\t- 20% chance that the gene is from one of the two ' \
                 '\n\t  parents​' \
                 '\n\t- 80% chance that the gene is an average of the two ' \
                 '\n\t  parents respective genes​' \
                 '\nAt this stage there is also a 10% chance of a slight gene ' \
                 '\nmutation.'

titleMCTS = 'MCTS Guide'
descriptionMCTS = 'MCTS (Monte Carlo Tree Search) is a heuristic search strategy ' \
                  '\nadopted in some types of decision-making processes, such as ' \
                  '\nthose decision-making processes that are typically adopted in ' \
                  'games. Markov Chain Monte Carlo (MCMC) methods are ' \
                  '\napplied to generate samples.' \
                  '\n\n​The goal of the MCTS is to analyze the most promising ' \
                  '\nplayouts, expanding the search tree, which is based on a ' \
                  '\nrandom sampling of the search space.' \
                  '\nThe final result of each playout is used to weigh the nodes of ' \
                  '\nthe search tree, so that the best nodes subsequently have ' \
                  '\nmore chances to be chosen for future playouts. ' \
                  '\n\nEach round of the choice of move in the MCTS consists of four steps:​' \
                  '\n\t- Selection​' \
                  '\n\t- Expansion​' \
                  '\n\t- Simulation​' \
                  '\n\t- Backpropagation​'

titleRB = 'Rule Based Guide'
descriptionRB = 'For "Rule Based" Agent, we mean an Ai who uses a knowledge ' \
                'base to find the best move with a tetromino, in an instance of ' \
                'the board.​' \
                '\n\nCoding all the possibilities present in the sheet, as well as ' \
                '\nbeing expensive, made it an unintelligent agent, since when it ' \
                'talks about AI it is only necessary to describe the solution to ' \
                '\nthe problem, not how to reach it.​' \
                '\n\nSo we took into consideration the "shadows" of the ' \
                '\ntetramines: each tetromino, in every rotation, casts a different' \
                ' shadow on the crest of the card.​'

if __name__ == '__main__':
    sd = SidePanel(titleLS, descriptionRB)
    sd.showSidePanel()
