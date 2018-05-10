#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

import random
import time
import string
import heapq

#create ASCII versions of images with pillow

random.seed(time.time())
allChars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ,.:;!@#$%^&*()-_=+<>/?[]}{|~')
targetString = input("Target string?\n")
targetList = list(targetString)

class GenderMismatch(Exception):
	pass

class Generation():
	def __init__(self,size=None,prevGeneration=None):
		self.individualsDict = {}
		if size != None and prevGeneration == None:
			for i in range(size):
				if not any(indv.gender == 'Male' for indv in self.individualsDict.values()):
					print("first male")
					self.individualsDict[i] = Individual(forcedGender='Male')
				elif not any(indv.gender == 'Female' for indv in self.individualsDict.values()):
					print("first female")
					self.individualsDict[i] = Individual(forcedGender='Female')
				else:
					self.individualsDict[i] = Individual()
		elif size == None and prevGeneration != None:
			toBreedCount = len(prevGeneration.individualsDict)//4#(len(prevGeneration.individualsDict)+firstGenScore//prevGeneration.bestIndividuals(1)[0].score)
			toBreed = {'Male':[],'Female':[]}
			for gender in toBreed:
				toBreed[gender] = prevGeneration.bestIndividuals(toBreedCount,gender)
			self.breed(toBreed,len(prevGeneration.individualsDict)+firstGenScore//prevGeneration.bestIndividuals(1)[0].score)

	def breed(self,specimensByGender,popSize):
		while len(self.individualsDict) < popSize:
			if not any(indv.gender == 'Male' for indv in self.individualsDict.values()):
				self.individualsDict[len(self.individualsDict)] = Individual(random.choice(specimensByGender['Male']),random.choice(specimensByGender['Female']),forcedGender='Male')
			elif not any(indv.gender == 'Female' for indv in self.individualsDict.values()):
				self.individualsDict[len(self.individualsDict)] = Individual(random.choice(specimensByGender['Male']),random.choice(specimensByGender['Female']),forcedGender='Female')
			else:
				self.individualsDict[len(self.individualsDict)] = Individual(random.choice(specimensByGender['Male']),random.choice(specimensByGender['Female']))
		return

	def bestIndividuals(self,count,gender=None):
		if gender != None:
			return heapq.nsmallest(count,(indv for indv in self.individualsDict.values() if indv.gender == gender),key=lambda indv:indv.score)
		if gender == None:
			return heapq.nsmallest(count,(indv for indv in self.individualsDict.values()),key=lambda indv:indv.score)

	def worstIndividuals(self,count,gender=None):
		if gender != None:
			return heapq.nlargest(count,(indv for indv in self.individualsDict.values() if indv.gender == gender),key=lambda indv:indv.score)
		if gender == None:
			return heapq.nlargest(count,(indv for indv in self.individualsDict.values()),key=lambda indv:indv.score)

class Individual():
	def __init__(self,Individual1=None,Individual2=None,forcedGender=None):
		if Individual1 == None and Individual2 == None:
			self.currentDNA = [random.choice(allChars) for i in range(len(targetString))]
			self.genes = DNA2Genes(self.currentDNA)

		elif Individual1 != None and Individual2 != None and Individual1.gender != Individual2.gender:
			self.genes = [random.choice([Individual1.genes[count],Individual2.genes[count]]) for count in range(len(Individual1.genes))]
			self.currentDNA = list(genepart for gene in self.genes for genepart in gene)
			if random.randrange(0,100) > 10:
				self.currentDNA = mutate(self.currentDNA)
				self.genes = DNA2Genes(self.currentDNA)

		else:
			if Individual1.gender == Individual2.gender:
				raise GenderMismatch("Mismatched individual genders!")
			raise NotImplementedError("only one individual passed to Individual constructor!")

		if forcedGender != None:
			self.gender = forcedGender
		elif forcedGender == None:
			self.gender = random.choice(['Male','Female'])

		self.score = scoreIndividual(self.currentDNA,targetList)

	def printGenes(self):
		print("\ncurrent DNA: %s" % self.currentDNA)
		print("gender: %s" % self.gender)
		print("genes: %s" % self.genes)
		return

def DNA2Genes(currentDNA):
	genes = [currentDNA[:len(currentDNA)//4],currentDNA[len(currentDNA)//4:len(currentDNA)//2],currentDNA[len(currentDNA)//2:-len(currentDNA)//4],currentDNA[-len(currentDNA)//4:]]
	return genes

def scoreIndividual(currentGenes,targetGenes):
	score = 0
	for i in range(len(targetGenes)):
		multiplier = ord(currentGenes[i])-ord(targetGenes[i])
		score += multiplier*multiplier
	return score

def mutate(oldGenList):
	currentGenList = list(oldGenList)
	for count in range(random.randrange(len(oldGenList))):
		chance = random.randrange(0,7)
		char = random.randrange(len(currentGenList))

		if chance == 0:
			pass
		if chance == 1:
			try:
				currentGenList[char] = currentGenList[char+1]
			except IndexError:
				pass
		if chance == 2:
			try:
				currentGenList[char] = currentGenList[char-1]
			except IndexError:
				pass
		if chance == 3:
			try:
				currentGenList[char] = currentGenList[char+2]
			except IndexError:
				pass
		if chance == 4:
			try:
				currentGenList[char] = currentGenList[char-2]
			except IndexError:
				pass
		if chance == 5:
			try:
				currentGenList[char] = chr(ord(currentGenList[char])+1)
			except IndexError:
				pass
		if chance == 6:
			try:
				currentGenList[char] = chr(ord(currentGenList[char])-1)
			except IndexError:
				pass
	return currentGenList

def nextGen(oldGeneration):
	newGeneration = Generation(oldGeneration)
	return newGeneration

genCount = 0
lastscore=10000
bestscore=99999
lastprintgen = 0
initialGenSize = random.randrange(100,150)*2
currentGen = Generation(size=initialGenSize)
firstGenScore = currentGen.bestIndividuals(1)[0].score
initialstrings = str(list("".join(indv.currentDNA) for indv in currentGen.individualsDict.values()))
print(targetList)
while targetList != currentGen.bestIndividuals(1)[0].currentDNA:
	oldGen = currentGen
	currentGen = Generation(prevGeneration=oldGen)
	genCount +=1
	#print("score "+str(min((indv.score for indv in currentGen.individualsDict.values())))+" generation "+str(genCount)+" genes "+str(min((indv for indv in currentGen.individualsDict.values()),key=lambda indv:indv.score).genes))
	if lastscore ==0:
		while(1):
			pass
	lastscore=currentGen.bestIndividuals(1)[0].score
	if lastscore < bestscore:
		bestscore = lastscore
		print("best score so far: %s, population %s, generations since last print: %s" % (bestscore,len(currentGen.individualsDict.values()),genCount-lastprintgen))
		lastprintgen = genCount
print("Final generation count: "+str(genCount),"Target string: "+targetString,"Initial generation size: "+str(initialGenSize),sep="\n") #"Initial strings: "+initialstrings,
