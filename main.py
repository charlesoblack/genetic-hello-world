#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python 3.6.4

import random
import time
import string

random.seed(time.time())
allChars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ,.:;!@#$%^&*()-_=+<>/?[]}{|~')
targetString = input("Target string?\n")
targetList = list(targetString)
startList = [random.choice(allChars) for i in range(len(targetString))]
startString = "".join(startList)
currentGenList = startList

def scoreString(string,target):
	score = 0
	for i in range(len(target)):
		multiplier = ord(string[i])-ord(target[i])
		score += multiplier*multiplier
	return score

def nextGen(string):
	pass

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

generation = 0
while currentGenList != targetList:
	newList = mutate(currentGenList)
	if scoreString(currentGenList,targetList) > scoreString(newList,targetList):
		currentGenList = newList
		print("".join(currentGenList)+", "+str(generation))
	generation += 1
	time.sleep(0.001)

print("Final generation count: "+str(generation),"Initial string: "+"".join(startList),"Target string: "+"".join(currentGenList),sep="\n")
	