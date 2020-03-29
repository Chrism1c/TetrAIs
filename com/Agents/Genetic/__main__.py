import sys
from com.Agents.Genetic.Genetic import perfectRun
from com.Agents.Genetic.GeneticController import GeneticController
from com.Utils.logger import Logger
from com.Menu import menu

"""
    __main__.py useful to choose run modality of Genetic Algorithm
"""


def gen_main(r_p, mode, numGen, treePlot, gdSidePanel):
    sys.stdout = Logger()
    numGen = int(numGen)
    if mode == 'Training':
        train = GeneticController(r_p, numGen, treePlot, gdSidePanel)
        train.workGenetic()
    else:
        for i in range(numGen):
            perfectRun(r_p, gdSidePanel, i)

# #  get arguments when AI file is executed by the menu
# r_p = sys.argv[1]
# mode = sys.argv[2]
# numGen = sys.argv[3]
#
# # log object to store console output inside a .log file (com.Utils.log)
# sys.stdout = Logger()
#
# # Switch to choose the execution mode of Genetic Algorithm (Training or PerfectRun)
# if mode == 'Training':
#     train = GeneticController(r_p, numGen)
#     train.workGenetic()
# else:
#     perfectRun(r_p)
