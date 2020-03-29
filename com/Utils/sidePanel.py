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

        T = tk.Text(self.root, width=59, height=29)
        T.configure(font='freesansbold 13')
        T.insert(tk.END, self.description)
        T.config(bg='black', fg='white')
        T.pack(padx=2, pady=2)

        self.root.geometry("+{}+{}".format(int(0), int(0)))
        self.root.update()


    def destroyPanel(self):
        self.root.destroy()


titleDFS = 'DFS Guide'
descriptionDFS = 'A generic search algorithm is independent of any search strategy. The ' \
                 '\nidea is that given a graph, the paths are incrementally explored starting ' \
                 'from the starting nodes and then reaching the target nodes.' \
                 '\n\nDFS is an uninformed search algorithm on graphs, in which the system ' \
                 '\nreasons on a model of the world made of states, in the absence of ' \
                 '\nuncertainty and with purposes to be achieved:' \
                 '\n\t- A flat representation of the domain;' \
                 '\n\t- In the state space, a way is sought to go from the ' \
                 '\n\t current state to a goal.\n\n' \
                 'In in-depth research (DFS), the border is organized as a stack (LIFO) in ' \
                 '\nwhich the elements are added one at a time and the one selected and ' \
                 '\ntaken will be the last added.'

titleLS = 'LS Guide'
descriptionLS = 'Local search is a heuristic method for solving computationally hard ' \
                '\noptimization problems. ' \
                '\n\nLocal search can be used on problems that can be formulated as finding ' \
                'a solution maximizing a criterion among a number of candidate ' \
                '\nsolutions. ' \
                '\n\nLocal search algorithms move from solution to solution in the space of ' \
                '\ncandidate solutions (the search space) by applying local changes, until a' \
                'solution deemed optimal is found or a time bound is elapsed.'

titleSDGQL = 'SDGQL Guide'
descriptionSDQL = 'The SDG_QL algorithm is based on the Stochastic Gradient Ascent ' \
                  '\nalgorithm as an optimization of Q-Learning. It uses a "weights vector"' \
                  '\nrepresenting the importance that each metric has within the score ' \
                  '\ncalculation function. It chooses the best move to play given a game ' \
                  '\nscheme (State), the algorithm compares the possible moves (Action)' \
                  '\nconcerning only the current tetramino simulating a "drop ” of the ' \
                  '\ntetramino on the board.​The AI calculates the Reward relating to the ' \
                  '\nAction on the current State.' \
                  '\n\nThe Reward = 5 * (linesRemvd * lineRemvd) - (Hsum - oldHsum)' \
                  '\n\nThe TD-Update rule of the Q-learning algorithm returns the ' \
                  '\n"Q-value" as well as the new weight in the vector :​' \
                  '\n\nwx[i] = wx[i] + alpha * wx[i] * (Reward - oldPar[i] + gamma * newPar[i])​' \
                  '\n\nThe policy is probability of extracting the not highest Q-value move.' \
                  '\nThe proposed AI update its weights and converge towards values' \
                  '\nsufficient to obtain very high scores in relatively few “training runs”.​'

titleGen = 'Genetic Guide'
descriptionGen = 'Mashup:​' \
                 '\n\t- Reproductive trait of Genetic' \
                 '\n\t- ​Efficiency of Beam Search' \
                 '\n\nEach gene represents the weight of one of the heuristics used by the' \
                 '\nsystem.' \
                 '\n\nNew generation composed of:' \
                 '\n\t- ½ better chromosomes of the previous generation​' \
                 '\n\t- ½ one point crossing between the best chromosomes of the ' \
                 '\n\t  previous generation​' \
                 '\n\nIn the crossing phase we select two of the best chromosomes and we ' \
                 '\ncouple them. For each chromosome gene that is the child of two parent ' \
                 'chromosomes:' \
                 '\n\t- 20% chance that the gene is from one of the two parents​' \
                 '\n\t- 80% chance that the gene is an average of the two parents ' \
                 '\n\t respective genes​' \
                 '\nAt this stage there is also a 10% chance of a slight gene mutation.'

titleMCTS = 'MCTS Guide'
descriptionMCTS = 'MCTS (Monte Carlo Tree Search) is a heuristic search strategy adopted ' \
                  '\nin some types of decision-making processes, such as those ' \
                  '\ndecision-making processes that are typically adopted in games. Markov ' \
                  '\nChain Monte Carlo (MCMC) methods are applied to generate samples.' \
                  '\n\n​The goal of the MCTS is to analyze the most promising playouts, ' \
                  '\nexpanding the search tree, which is based on a random sampling of the ' \
                  'search space.' \
                  '\nThe final result of each playout is used to weigh the nodes of the search ' \
                  'tree, so that the best nodes subsequently have more chances to be ' \
                  '\nchosen for future playouts. ' \
                  '\n\nEach round of the choice of move in the MCTS consists of four steps:​' \
                  '\n\t- Selection​' \
                  '\n\t- Expansion​' \
                  '\n\t- Simulation​' \
                  '\n\t- Backpropagation​'

titleRB = 'Rule Based Guide'
descriptionRB = 'For "Rule Based" Agent, we mean an Ai who uses a knowledge base to' \
                '\nfind the best move with a tetromino, in an instance of the board.​' \
                '\n\nCoding all the possibilities present in the sheet, as well as being ' \
                '\nexpensive, made it an unintelligent agent, since when it talks about AI it ' \
                'is only necessary to describe the solution to the problem, not how to ' \
                '\nreach it.​' \
                '\n\nSo we took into consideration the "shadows" of the tetramines: each ' \
                '\ntetromino, in every rotation, casts a different shadow on the crest of the ' \
                'card.​'

if __name__ == '__main__':
    sd = SidePanel(titleLS, descriptionLS)
    sd.showSidePanel()
