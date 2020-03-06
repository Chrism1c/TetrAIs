import sys
from com.Agents.Genetic.Genetic import perfectRun
from com.Agents.Genetic.GeneticController import GeneticController

r_p = sys.argv[1]
mode = sys.argv[2]
numGen = sys.argv[3]


#r_p = 'r'
#mode = 'train'
#numGen = 4

if mode == 'Training':

    train = GeneticController(r_p, numGen)
    train.workGenetic()

else:
    perfectRun(r_p)
