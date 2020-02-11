#!/usr/bin/python/
import ast
import re
import numpy as np

fileName = "Population.txt"
#fileNameScore = "PopulationScore.txt"
fileNameScoreMatch = "MatchScore.txt"

### Funzione che conta le linee del file
def countLines(fileName):
    count = 0
    with open(fileName, 'r') as f:
        for line in f:
            count += 1
    print("Total number of lines is:", count)
    return count

### Trasforma La lista chromosoma in una stringa 
def chromToStr(c,dim):
    _str = "["
    for i in range(dim):
        _str += str((c[i]))
        if i < dim-1:
            _str += ","
    _str += "]"
    return _str

### funzione che salva su file una popolazione di cromosomi
def saveOnFile(fileName,population):
    file = open(fileName,"a+")
    y = 0
    for x in range(1,len(population) + 1,1):
        #writethis = "BOT-" + str(start) + " = " + population[y] + "\n"
        writethis = str(chromToStr(population[y],len(population[y]))) + "\n"
        y+=1
        #start+=1
        file.write(writethis)
    file.close()

### Salva sul MatchScore lo score corrente
def saveScore(fN, score):
    file = open(fN,"w")
    file.write(str(score))
    file.close()

### Carica lo score da MatchScore
def loadScore(fN):
    file = open(fN,"r")
    score = file.read()
    file.close()
    return int(score)

### Distrugge l'intera population
def destroy(fileName):
    file = open(fileName,"w")
    file.close()

### Carica da file la popolazione di cromosomi
def loadFromFile(fileName): 
    population = list()
    File = open(fileName,"r")
    for line in File:
        chromosome = ast.literal_eval(line)
        print(chromosome)
        population.append(chromosome)
    File.close()
    return population

### Aggiunge lo score al vettore de chromosma
def addChromosomeScore(fileName,chromosome,score):
    f = open(fileName,'a+')
    chromoStr = chromToStr((population[x]),len(population[x]))[:-1]+","+str(score)+"]"+ "\n"
    print(chromoStr)
    f.write(chromoStr)
    f.close()

### Convert population of list into poulation of strings
def populationAsListofStr(population):
    populationOfStr = list()
    for x in range(len(population)):
        populationOfStr.append(chromToStr((population[x]),len(population[x])))
    return populationOfStr




################   TEST FUNCTIONS  #################################################################################################

#populationStr = ["[1,2,31,4,51,6]","[1,20,3,4,53,6]","[1,2,10,4,5,6]","[1,2,8,4,5,6]","[0,9,3,9,5,60,250]"]
#population = [[1,2,31,4,51,6],[1,20,3,4,53,6],[1,2,10,4,5,6],[1,2,8,4,5,6],[0,9,3,9,5,60,250]]

#destroy(fileName)
#START = saveOnFile(fileName,population)
#START = loadFromFile(fileName)

#addChromosomeScore(fileNameScore,[1,2,3,4,5,6],50)

#START = removeDuplicates(fileName)

#population, scoreVector = loadFromFileWScore(fileNameScore)
#populationScored = loadFromFileWScoreV2(fileNameScore)

#for x in range(len(populationScored)):
#    print(chromToStr((populationScored[x]),len(population[x]))+" - TEST - ")
