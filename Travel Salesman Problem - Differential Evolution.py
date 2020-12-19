# -*- coding: utf-8 -*-
"""TSP-DifferentialEvolution

"""

# from google.colab import drive
# drive.mount('/content/gdrive')

populationSize = 50
nodeCount = 34 #problemSize
weightingFactor = 0.8
crossoverRate = 0.2
iterationCount = 10

filePath = '/content/gdrive/My Drive/Colab Notebooks/'
"""
fileReader = open(filePath + 'ftv33.txt')
fileLines = fileReader.readlines()
fileMergedLines = " ".join(fileLines).split()
fileValues = list(map(int, fileMergedLines))
fileReader.close()
"""
with open(filePath + 'ftv33.txt') as fileReader:
  fileLines = fileReader.readlines()
  fileMergedLines = " ".join(fileLines).split()
  fileValues = list(map(int, fileMergedLines))

import numpy as np
from random import randint, shuffle, choice, random
distanceMatrix = np.reshape(fileValues, (nodeCount, nodeCount)).tolist()

def CreateMember():
  member = list(range(nodeCount))
  shuffle(member)
  return member

def GreedyMember(startPoint):
  member = [startPoint]
  for _ in range(nodeCount-1):
    curPoint = member[-1]
    nearestPoint = None
    for i in range(nodeCount):
      if i in member: continue
      if nearestPoint is None: nearestPoint = i
      if distanceMatrix[curPoint][i] < distanceMatrix[curPoint][nearestPoint]:
        nearestPoint = i
    member.append(nearestPoint)
  return member

def InitializePopulation():
  return [CreateMember() for _ in range(populationSize)]
  #return [GreedyMember(i) for i in range(populationSize)]

def EvaluateMember(member):
  """
  top = 0
  for curIndex in range(nodeCount):
    top += distanceMatrix[member[curIndex]][member[(curIndex+1)%nodeCount]]
  return top
  """
  return sum([distanceMatrix[member[curIndex]][member[(curIndex+1) % nodeCount]] for curIndex in range(nodeCount)])

def EvaluatePopulation(population):
  return [EvaluateMember(member) for member in population]

def UniqueChoice(members, population):
  randomMember = choice(population)
  while randomMember in members:
    randomMember = choice(population)
  return randomMember

def NewSample(member0, population):
  member1 = UniqueChoice([member0], population)
  member2 = UniqueChoice([member0, member1], population)
  member3 = UniqueChoice([member0, member1, member2], population)
  cutPoint = randint(0, nodeCount)
  newMember = []
  for i in range(nodeCount):
    if i == cutPoint and random() < crossoverRate:
      newMember.append(member3[i] + weightingFactor * (member1[i] - member2[i]))
    else:
      newMember.append(member0[i])
  newMember = [city + random()/100000 for city in newMember]
  sortedMembers = sorted(newMember.copy())
  return [sortedMembers.index(city) for city in newMember]

def IsFeasible(member):
  return len(set(member)) == nodeCount and min(member) == 0 and max(member) == nodeCount-1

def argmin(listOfItems):
  minItem = min(listOfItems)
  return listOfItems.index(minItem)

population = InitializePopulation()
print(population)
bestMember = population[0]
curIter = 0
evaluationHistory = []
bestMemberHistory = []
infeasibleHistory = []
while curIter < iterationCount:
  inFeasibleCount = 0
  newPopulation = []
  for member in population:
    newMember = NewSample(member, population)
    if not IsFeasible(newMember):
      inFeasibleCount += 1
    if IsFeasible(newMember) and EvaluateMember(newMember) <= EvaluateMember(member):
      newPopulation.append(newMember)
    else:
      newPopulation.append(member)
  evaluations = EvaluatePopulation(newPopulation)
  bestOfPopulation = newPopulation[argmin(evaluations)]
  evaluationHistory.append(EvaluateMember(bestOfPopulation))
  if EvaluateMember(bestOfPopulation) < EvaluateMember(bestMember):
    bestMember = bestOfPopulation
  bestMemberHistory.append(EvaluateMember(bestMember))
  infeasibleHistory.append(inFeasibleCount*100/(populationSize*crossoverRate))
  curIter += 1
  if curIter % 100 == 0:
    print('Iteration #{} = {} [Infeasible Count: {}]'.format(curIter, EvaluateMember(bestMember), inFeasibleCount*100/(populationSize*crossoverRate)))

print(bestMember)