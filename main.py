#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6.4

import random
import time
import heapq

# create ASCII versions of images with pillow?

random.seed(time.time())
all_chars = ('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
             '0123456789 ,.:;!@#$%^&*()-_=+<>/?[]}{|~')
target = input("Target string?\n")


class Generation():

    def __init__(self, size=None, prev=None):
        self.individuals = []

        if size is not None:
            for i in range(size):
                if len(self.males) == 0:
                    self.individuals.append(Individual(gender='Male'))
                elif len(self.females) == 0:
                    self.individuals.append(Individual(gender='Female'))
                else:
                    self.individuals.append(Individual())

        elif prev is not None:
            parent_count = len(prev.individuals) // 20
            parents = {'Male': [], 'Female': []}
            for gender in parents:
                parents[gender] = prev.best_individuals(parent_count, gender)

            best = prev.best_individuals(1)[0]
            second = prev.best_individuals(2)[1]

            gen_growth = second.score // best.score

            self.breed(parents, len(prev.individuals) + gen_growth)

    @property
    def males(self):
        return [indv for indv in self.individuals if indv.gender == 'Male']

    @property
    def females(self):
        return [indv for indv in self.individuals if indv.gender == 'Female']

    def segregated(self, gender):
        if gender == 'Male':
            return self.males
        else:
            return self.females

    def breed(self, specimens_by_gender, pop_size):
        for i in range(pop_size):
            male = random.choice(specimens_by_gender['Male'])
            female = random.choice(specimens_by_gender['Female'])

            if len(self.males) == 0:
                self.individuals.append(Individual(male,
                                                   female,
                                                   gender='Male'))
            elif len(self.females) == 0:
                self.individuals.append(Individual(male,
                                                   female,
                                                   gender='Female'))
            else:
                self.individuals.append(Individual(male,
                                                   female))
        return

    def best_individuals(self, n, gender=None):
        if gender is not None:
            return heapq.nsmallest(n,
                                   self.segregated(gender),
                                   key=lambda indv: indv.score)
        return heapq.nsmallest(n,
                               self.individuals,
                               key=lambda indv: indv.score)

    def worst_individuals(self, n, gender=None):
        if gender is not None:
            return heapq.nlargest(n,
                                  self.segregated(gender),
                                  key=lambda indv: indv.score)
        return heapq.nlargest(n,
                              self.individuals,
                              key=lambda indv: indv.score)


class Individual():

    def __init__(self, first=None, other=None, gender=None):
        if first is None and other is None:
            self.currentDNA = [random.choice(all_chars) for i in target]
            self.genes = self.DNA2Genes()

        elif first.gender != other.gender:
            self.genes = []
            for n, gene in enumerate(first.genes):
                self.genes.append(random.choice([gene,
                                                 other.genes[n]]
                                                ))

            self.currentDNA = [char for gene in self.genes for char in gene]
            if random.randrange(0, 100) > 10:
                self.currentDNA = self.mutate()
                self.genes = self.DNA2Genes()

        self.currentDNA = ''.join(self.currentDNA)
        self.gender = gender or random.choice(['Male', 'Female'])
        self.score = self.score_individual(target)

    def score_individual(self, target_genes):
        score = 0
        for i, gene in enumerate(target_genes):
            multiplier = ord(self.currentDNA[i]) - ord(gene)
            score += multiplier * multiplier
        return score

    def DNA2Genes(self):
        fourth = len(self.currentDNA) // 4
        genes = [self.currentDNA[:fourth],
                 self.currentDNA[fourth:2 * fourth],
                 self.currentDNA[2 * fourth: - fourth],
                 self.currentDNA[- fourth:]
                 ]
        return genes

    def mutate(self):
        for count in range(random.randrange(len(self.currentDNA))):
            chance = random.randrange(0, 7)
            char = random.randrange(len(self.currentDNA))

            if chance == 0:
                pass
            if char < (len(self.currentDNA) - 1) and char > 1:
                if chance == 1:
                    self.currentDNA[char] = self.currentDNA[char + 1]
                if chance == 2:
                    self.currentDNA[char] = self.currentDNA[char - 1]
            if char < (len(self.currentDNA) - 2) and char > 2:
                if chance == 3:
                    self.currentDNA[char] = self.currentDNA[char + 2]
                if chance == 4:
                    self.currentDNA[char] = self.currentDNA[char - 2]
            if chance == 5:
                self.currentDNA[char] = chr(ord(self.currentDNA[char]) + 1)
            if chance == 6:
                self.currentDNA[char] = chr(ord(self.currentDNA[char]) - 1)
        return self.currentDNA


gen_count = 0

best = 99999
lastprintgen = 0
initial_gen_size = random.randrange(100, 150) * 2
current_gen = Generation(size=initial_gen_size)

while target != current_gen.best_individuals(1)[0].currentDNA:
    old_gen = current_gen
    current_gen = Generation(prev=old_gen)
    gen_count += 1

    last = current_gen.best_individuals(1)[0].score
    if last < best:
        best = last
        print("best score so far: %s,"
              " population %s,"
              " generations since last print: %s"
              % (best,
                 len(current_gen.individuals),
                 gen_count - lastprintgen))
        lastprintgen = gen_count

print("Final generation count: {}".format(gen_count),
      "Target string: {}".format(target),
      "Initial generation size: {}".format(initial_gen_size),
      sep="\n")
