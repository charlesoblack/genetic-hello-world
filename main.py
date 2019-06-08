#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import random
import time
import heapq

# create ASCII versions of images with pillow?

random.seed(time.time())
all_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ,.:;!@#$%^&*()-_=+<>/?[]}{|~'
target_string = input("Target string?\n")
target_list = list(target_string)


class Generation():

    def __init__(self, size=None, prev_generation=None):
        self.individuals_dict = {}
        if size is not None and prev_generation is None:
            for i in range(size):
                if not any(indv.gender == 'Male' for indv in self.individuals_dict.values()):
                    print("first male")
                    self.individuals_dict[i] = Individual(forced_gender='Male')
                elif not any(indv.gender == 'Female' for indv in self.individuals_dict.values()):
                    print("first female")
                    self.individuals_dict[i] = Individual(forced_gender='Female')
                else:
                    self.individuals_dict[i] = Individual()
        elif size is None and prev_generation is not None:
            to_breed_count = len(prev_generation.individuals_dict) // 4
            # to_breed_count = (len(prev_generation.individuals_dict)+firstGenScore//prev_generation.best_individuals(1)[0].score)
            to_breed = {'Male': [], 'Female': []}
            for gender in to_breed:
                to_breed[gender] = prev_generation.best_individuals(to_breed_count, gender)
            self.breed(to_breed, len(prev_generation.individuals_dict) + firstGenScore // prev_generation.best_individuals(1)[0].score)

    def breed(self, specimens_by_gender, pop_size):
        while len(self.individuals_dict) < pop_size:
            if not any(indv.gender == 'Male' for indv in self.individuals_dict.values()):
                self.individuals_dict[len(self.individuals_dict)] = Individual(random.choice(specimens_by_gender['Male']), random.choice(specimens_by_gender['Female']), forced_gender='Male')
            elif not any(indv.gender == 'Female' for indv in self.individuals_dict.values()):
                self.individuals_dict[len(self.individuals_dict)] = Individual(random.choice(specimens_by_gender['Male']), random.choice(specimens_by_gender['Female']), forced_gender='Female')
            else:
                self.individuals_dict[len(self.individuals_dict)] = Individual(random.choice(specimens_by_gender['Male']), random.choice(specimens_by_gender['Female']))
        return

    def best_individuals(self, count, gender=None):
        if gender is not None:
            return heapq.nsmallest(count, (indv for indv in self.individuals_dict.values() if indv.gender == gender), key=lambda indv: indv.score)
        if gender is None:
            return heapq.nsmallest(count, self.individuals_dict.values(), key=lambda indv: indv.score)

    def worst_individuals(self, count, gender=None):
        if gender is not None:
            return heapq.nlargest(count, (indv for indv in self.individuals_dict.values() if indv.gender == gender), key=lambda indv: indv.score)
        if gender is None:
            return heapq.nlargest(count, self.individuals_dict.values(), key=lambda indv: indv.score)


class Individual():

    def __init__(self, individual_1=None, individual_2=None, forced_gender=None):
        if individual_1 is None and individual_2 is None:
            self.currentDNA = [random.choice(all_chars) for i in target_string]
            self.genes = DNA2Genes(self.currentDNA)

        elif individual_1 is not None and individual_2 is not None and individual_1.gender != individual_2.gender:
            self.genes = [random.choice([individual_1.genes[count], individual_2.genes[count]]) for count in range(len(individual_1.genes))]
            self.currentDNA = [genepart for gene in self.genes for genepart in gene]
            if random.randrange(0, 100) > 10:
                self.currentDNA = mutate(self.currentDNA)
                self.genes = DNA2Genes(self.currentDNA)

        self.gender = forced_gender or random.choice(['Male', 'Female'])

        self.score = score_individual(self.currentDNA, target_list)


def DNA2Genes(currentDNA):
    genes = [currentDNA[:len(currentDNA) // 4],
             currentDNA[len(currentDNA) // 4:len(currentDNA) // 2],
             currentDNA[len(currentDNA) // 2: - len(currentDNA) // 4],
             currentDNA[- len(currentDNA) // 4:]
             ]
    return genes


def score_individual(current_genes, target_genes):
    score = 0
    for i in range(len(target_genes)):
        multiplier = ord(current_genes[i]) - ord(target_genes[i])
        score += multiplier * multiplier
    return score


def mutate(old_gen_list):
    current_gen_list = list(old_gen_list)
    for count in range(random.randrange(len(old_gen_list))):
        chance = random.randrange(0, 7)
        char = random.randrange(len(current_gen_list))

        if chance == 0:
            pass
        if chance == 1:
            try:
                current_gen_list[char] = current_gen_list[char + 1]
            except IndexError:
                pass
        if chance == 2:
            try:
                current_gen_list[char] = current_gen_list[char - 1]
            except IndexError:
                pass
        if chance == 3:
            try:
                current_gen_list[char] = current_gen_list[char + 2]
            except IndexError:
                pass
        if chance == 4:
            try:
                current_gen_list[char] = current_gen_list[char - 2]
            except IndexError:
                pass
        if chance == 5:
            try:
                current_gen_list[char] = chr(ord(current_gen_list[char]) + 1)
            except IndexError:
                pass
        if chance == 6:
            try:
                current_gen_list[char] = chr(ord(current_gen_list[char]) - 1)
            except IndexError:
                pass
    return current_gen_list


def nextGen(old_generation):
    newGeneration = Generation(old_generation)
    return newGeneration


gen_count = 0
lastscore = 10000
bestscore = 99999
lastprintgen = 0
initial_gen_size = random.randrange(100, 150) * 2
current_gen = Generation(size=initial_gen_size)
firstGenScore = current_gen.best_individuals(1)[0].score
initialstrings = str(["".join(indv.currentDNA) for indv in current_gen.individuals_dict.values()])
print(target_list)
while target_list != current_gen.best_individuals(1)[0].currentDNA:
    old_gen = current_gen
    current_gen = Generation(prev_generation=old_gen)
    gen_count += 1

    lastscore = current_gen.best_individuals(1)[0].score
    if lastscore < bestscore:
        bestscore = lastscore
        print("best score so far: %s, population %s, generations since last print: %s" % (bestscore, len(current_gen.individuals_dict.values()), gen_count - lastprintgen))
        lastprintgen = gen_count
print("Final generation count: {}".format(gen_count),
      "Target string: {}".format(target_string),
      "Initial generation size: {}".format(initial_gen_size),
      sep="\n")
