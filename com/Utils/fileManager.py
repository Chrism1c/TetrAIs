import ast

fileName = "Population.txt"
fileNameScoreMatch = "MatchScore.txt"
filePerfect = "LastChromosome.txt"


def countLines(fileName):
    """
    function to count the number of lines in a file (NOT USED IN THE APPLICATION)
    :param fileName:
    :return: count of lines as int value
    """
    count = 0
    with open(fileName, 'r') as f:
        for line in f:
            count += 1
    print("Total number of lines is:", count)
    return count


def chromToStr(c, dim):
    """
    function to convert a Chromosome as list into a Chromosome as string
    :param c: Chromosome as list to convert
    :param dim: size of the chromosome (7 in all AIs, 4 in SDG Q-L)
    :return: _str string of converted Chromosome
    """
    _str = "["
    for i in range(dim):
        _str += str((c[i]))
        if i < dim - 1:
            _str += ","
    _str += "]"
    return _str


def saveOnFile(fileName, population):
    """
    function to save on file a population
    # funzione che salva su file una popolazione di cromosomi
    :param fileName: str of the file name
    :param population: list of chromosome to save on file
    :return: None
    """
    file = open(fileName, "a+")
    y = 0
    for x in range(1, len(population) + 1, 1):
        writethis = str(chromToStr(population[y], len(population[y]))) + "\n"
        y += 1
        file.write(writethis)
    file.close()


def destroy(fileName):
    """
    Clear the file
    # Distrugge l'intera population
    :param fileName: str of the file name
    :return: None
    """
    file = open(fileName, "w")
    file.close()


def loadFromFile(fileName):
    """
    Load from file the population
    # Carica da file la popolazione di cromosomi
    :param fileName:
    :return: None
    """
    population = list()
    File = open(fileName, "r")
    for line in File:
        chromosome = ast.literal_eval(line)
        print(chromosome)
        population.append(chromosome)
    File.close()
    return population


def getPerfectChromosome():
    """
    Save get the perfect chromosome from "fileName" file
    # salva il chromosoma perfetto in un altro file dedicato
    :return: None
    """
    population = loadFromFile(filePerfect)
    if len(population) == 1:
        return population[0]
    else:
        return None
