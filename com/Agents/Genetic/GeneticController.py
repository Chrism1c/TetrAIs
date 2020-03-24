from com.Agents.Genetic.Genetic import Genetic
from com.Utils.fileManager import *
from com.Menu import menu
import numpy as np
import random
import time
from operator import itemgetter
from com.Utils.NetworkX import *
from com.Utils.Plot import plot_learning_curve

GeneticTreePlot = TreePlot()

class GeneticController:
    global GeneticTreePlot
    """
        Main class for Genetic Algorithm on Training mode
        Attributes
        ----------
                        None
        Methods
        -------
        get_expected_score(test_board)
            Calculate score of test_board
        get_move()
            Execute
        getGeneticMove(board, piece, NextPiece)
            Execute the main move of the AI
        getScore(board)
            Calculate score of board
        get_expected_score(test_board)
            Calculate score of test_board
        calculateWScore(board)
            Calculate weighted score of board
    """

    def __init__(self, r_p, numGen, treePlot):
        """
        :param r_p:  type of piece used ('r' = random, 'p' = pi)
        :param numGen:  number of Generation to create for Training
        """
        self.r_p = r_p
        self.numGen = int(numGen)
        self.numRun = 1
        self.dimChromomsome = 7
        self.generation = list()
        self.population = list()
        self.treePlot = treePlot
        # self.bello = np.array([1.8, 1, 0.5, 1.5, 0.01, 0.2, 0.3])

    def workGenetic(self):
        """
            Main work function dor Genetic Training
            Parameters
            ----------
                None
        """
        print("start creation gen:0")
        # numGen0 = 2 ** self.numGen
        self.numGen0 = 4
        self.generation = self.createGen0(self.numGen0)
        # self.generation = self.createGen01(numGen0)
        game_index_array = []
        scoreArray = list()
        gene0Array = list()
        gene1Array = list()
        gene2Array = list()
        gene3Array = list()
        gene4Array = list()
        gene5Array = list()
        gene6Array = list()
        print("end creation gen0")
        i = 0
        n_run = 0
        while True:
            n_run += 1
            print("start gen:", i)
            population = list()
            for x in range(len(self.generation)):
                avgScoreChromosome = self.AVGfitnesingSing(self.generation[x])
                scoreArray.append(avgScoreChromosome)
                population.append((self.generation[x], avgScoreChromosome))
                gene0Array.append(self.generation[x][0])
                gene1Array.append(self.generation[x][1])
                gene2Array.append(self.generation[x][2])
                gene3Array.append(self.generation[x][3])
                gene4Array.append(self.generation[x][4])
                gene5Array.append(self.generation[x][5])
                gene6Array.append(self.generation[x][6])
                game_index_array.append(n_run)
                print("Gen ", i, " Run ", x, " AvgScore ", str(avgScoreChromosome))
            # k = round(len(self.generation)/2)
            k = len(self.generation)
            print("Full Generation = ", self.generation)
            print("end gen:", i)
            i += 1
            # self.generation = self.crossingFixedPopulation(self.bestChromosomeSearch(population, k), k, i)
            self.generation = self.crossingFixedPopulation(self.generation, i)
            # save
            for x in range(len(population)):
                self.population.append(population[x])
            print(len(self.generation))
            if len(self.generation) == 1:
                break
            else:
                continue
        destroy(fileName)
        saveOnFile(fileName, self.generation)
        if self.treePlot == 'yes':
            GeneticTreePlot.plot()
            GeneticTreePlot.Graph.clear()
        plot_learning_curve(scoreArray, game_index_array,
                            [gene0Array, gene1Array, gene2Array, gene3Array, gene4Array, gene5Array, gene6Array],
                            'gen')(self.numGen, self.numRun, self.numGen0)
        print('end training')


    def fitnessFunction(self, numTetraminoes, score):
        """
            Alternative fitness function that use numTetraminoes to alterate the score value
            # funzione fitness alternativa, che tiene conto del numero di tetramini piazzati ma anche dello score finale
            Parameters
            ----------
            numTetraminoes : int
                number of tetraminoes dropped in the game
            score : float
                pre calculated score
        """
        Newscore = (score + numTetraminoes) * 0.1
        # print("***************************************** fitnessFunctionAlt = ", Newscore)
        return Newscore


    def AVGfitnesingSing(self, chromosome):
        """
            Average of fitness scores by a chromosome
            # somma i valori contenuti nel vettore vFitness, che sostanzialmente contiene i valori fitness
            # delle varie partite fatte con lo stesso cromosoma, e ne fa la media
            Parameters
            ----------
            chromosome : list
                list of weights
        """
        avgFitness = 0
        for i in range(self.numRun):
            g = Genetic(self.r_p, chromosome, True)
            start = time.time()
            score, _, _, _, _, _ = g.run()
            finish = time.time()
            tempo = round(finish - start)
            avgFitness += (score + tempo)
            print(' - Match ' + str(i) + ' Score ' + str(score + tempo), " Chromosome = ", chromosome)
        return avgFitness / self.numRun

    def getNewChromosome(self):
        """
        crate a new random list of int (Chromosome)
        :return: new list
        """
        Chromosome = list()
        for x in range(7):
            Chromosome.append(round(random.uniform(0.0, 1.0), 3))
        return Chromosome
        # return np.random.uniform(low=0.0, high=1.0, size=7)

    # Create Gen0
    def createGen0(self, num):
        """
        Create the first generation where the magic start
        :param num:
            num of chromosome in gen0
        :return: gen0
        """
        gen0 = list()
        self.num = num

        for i in range(num):
            newChromo = self.getNewChromosome()
            gen0.append(newChromo)
            GeneticTreePlot.addedge("ROOT", str(newChromo))
        if self.treePlot == 'yes':
            GeneticTreePlot.plot()
        return gen0

    # Serch top k best Chromosome (based on score)
    def bestChromosomeSearch(self, population, k):
        """
        Search firs "k" Chromosome with best scores
        :param population: population of Chromosome
        :param k: number of Chromosome to search
        :return: the best k Chromosome
        """
        bestK = list()
        orderedChromosome = sorted(population, key=itemgetter(1), reverse=True)

        for x in range(k):
            chromosome, _ = orderedChromosome[x]
            bestK.append(chromosome)
            print(" - BestK - ", chromToStr(chromosome, self.dimChromomsome) + " --- WScore Of: ", str(_))
        return bestK

    def mutation(self, a):
        """
        function to mutate the values of a chromosome
        :param a:
        :return: probability of mutation
        """
        if random.randint(1, 10) == 10:  # 10% of mutation
            if 4.5 <= a <= 5.0:
                return -0.1 * random.randint(1, 5)
            else:
                return 0.1 * random.randint(1, 5)
        else:
            return 0  # 90% of not mutation

        # Crossing Chromosoma function

    def crossingchromosome(self, a, b):
        """
        Cross Chromosome by 2 Chromosome parents
        :param a: daddy Chromosome
        :param b: mummy Chromosome
        :return: Crossed Chromosome
        """
        newchromosome = [0] * self.dimChromomsome  # new empty crhomosome
        for x in range(self.dimChromomsome):
            if random.randint(0, 9) == 1:  # 10% chromosome from parent 1
                newchromosome[x] = a[x]
                # print("Gene from Parent_1 =",a[x])
            elif random.randint(0, 9) == 2:  # 10% chromosome from parent 2
                newchromosome[x] = b[x]
                # print("Gene from Parent_2 =",b[x])
            else:
                # 80% to avarage 2 Chromosome parents values
                newchromosome[x] = (a[x] + b[x]) / 2
                # print("Gene from Merged genes =",newchromosome[x])
            newchromosome[x] += self.mutation(newchromosome[x])
        # print("newchromosome = ",newchromosome)
        GeneticTreePlot.addedge(str(a), str(newchromosome))
        GeneticTreePlot.addedge(str(b), str(newchromosome))
        return newchromosome

    def crossingTournmentPopulation(self, population, k):
        """
         Cross Chromosome in tournament mode
        :param population:
        :param k:
        :return: newPopulation
        """
        newPopulation = list()
        if len(population) == 2:
            newPopulation.append(population[0])
        else:
            for x in range(0, int(k), 2):
                newPopulation.append(self.crossingchromosome(population[x], population[x + 1]))
        return newPopulation


    def crossingFixedPopulation(self, population, numGen):
        """
        # fixed number of Chromosomes
        # 1/2 best + 1/4 crossed of best + 1/4 new
        :param population:
        :param numGen:
        :return: newPopulation
        """
        newPopulation = list()
        orderedPopulation = sorted(population, key=itemgetter(1), reverse=True)
        if numGen == self.numGen:
            newPopulation.append(orderedPopulation[0])
        else:
            cross = self.crossingTournmentPopulation(orderedPopulation, round((len(orderedPopulation)) / 2))
            for x in range(round(len(orderedPopulation) / 2)):  # 1/2 best
                newPopulation.append(orderedPopulation[x])
            for x in range(round(len(cross))):                  # 1/4 crossed
                newPopulation.append(cross[x])
            new = round(len(population) - len(newPopulation))
            for x in range(new):                                # 1/4 new
                newPopulation.append(self.getNewChromosome())
        return newPopulation


#### Deprecated code ####

    def avgFitness(self, vFitness):
        mFitness = 0
        for x in vFitness:
            mFitness += vFitness[x]
        return mFitness / len(vFitness)

    def crossingPopulation_OLD(self, population, k):
        newPopulation = list()
        for x in range(0, int(k - 1), 2):
            newPopulation.append(self.crossingchromosome(population[x], population[x - 1]))
        return newPopulation

    # numero fisso di chromosomi
    # metà migliori e metà incrocio dei migliori
    def crossingFixedPopulation_OLD(self, population, numGen):
        newPopulation = list()
        orderedPopulation = sorted(population, key=itemgetter(1), reverse=True)
        if numGen == self.numGen:
            newPopulation.append(orderedPopulation[0])
        else:
            aux = self.crossingTournmentPopulation(orderedPopulation, len(orderedPopulation))
            for x in range(round(len(orderedPopulation) / 2)):  # metà migliori
                newPopulation.append(orderedPopulation[x])
            for x in range(round(len(orderedPopulation) / 2), len(orderedPopulation), 1):  # metà incroci
                newPopulation.append(aux[x])
        return newPopulation

    def crossingFullPopulation(self, population, k, numGen):
        pass

    def createGen01(self, num):
        gen0 = list()
        self.num = num
        for i in range(num):
            gen0.append(self.bello)
        return gen0
