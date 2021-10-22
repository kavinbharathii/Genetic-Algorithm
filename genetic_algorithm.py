# The Genetic Algorithm

# Implementing genetic algorithm on a population of 50 individuals
# to attain the goal of reaching a given target.

# DISCLAIMER:
# I will be using the word "genome" to indicate
# the creatures in the genetic evolution algorithm

import pygame
from pygame.locals import *
import random
import math

pygame.font.init()

# ---------------------------------------------------global variables------------------------------------------------------ #

width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Genetic Algorithm")


POPULATION_SIZE = 50
MUTATION_RATE = 0.02
GENE_LENGTH = 500

# ----------------------------------------------------Genome Class------------------------------------------------------- #


class Genome(object):
    def __init__(self, target):
        self.gene_length = GENE_LENGTH
        self.gene = []
        self.x = width // 2
        self.y = 10
        self.step = 0
        self.target = target
        self.generation = 0

    def create_genes(self):
        for _ in range(self.gene_length):
            x_direction = random.uniform(-1, 1)
            y_direction = random.uniform(-1, 1)
            self.gene.append([x_direction, y_direction])

    def draw(self):
        pygame.draw.circle(display, (0, 170, 200),
                           (self.x, self.y), 4)

    def move(self):
        for i in self.gene:
            self.x += i[0]
            self.y += i[1]

    def calc_distance(self):
        # using pythagoras' theorem to fing the shortest distance between the
        # genome and the give target
        perpendicular = abs(self.target.x - self.x)
        base = abs(self.target.y - self.y)
        dist = math.sqrt(perpendicular**2 + base**2)
        return dist

    def calc_fitness(self):
        # using a fitness function to find the fitness of
        # the specific genome, and use it as the metric to
        # improve it's probability of becoming a parent
        dist = self.calc_distance()
        normalized_dist = dist / height
        fitness = 1 - normalized_dist
        return fitness

    def crossover(self, partner):
        child = Genome(self.target)
        for i in range(GENE_LENGTH):
            if i % 2 == 0:
                child.gene.append(self.gene[i])
            else:
                child.gene.append(partner.gene[i])

        return child

    def mutate(self):
        for i in range(GENE_LENGTH):
            mutation_probability = round(random.uniform(-1, 1), 2)
            if mutation_probability == MUTATION_RATE:
                mutated_gene_x = random.uniform(-1, 1)
                mutated_gene_y = random.uniform(-1, 1)
                self.gene[i] = [mutated_gene_x, mutated_gene_y]


# ---------------------------------------------------Target Class------------------------------------------------------ #


class Target(object):
    def __init__(self):
        self.x = width // 2
        self.y = height - 10
        self.width = 20

    def draw(self):
        pygame.draw.rect(display, (0, 200, 170), (
            self.x - self.width // 2, self.y - self.width // 2, self.width, self.width))

# ---------------------------------------------------Population Class------------------------------------------------------ #


class Population(object):
    def __init__(self, target):
        self.target = target
        self.population = []
        self.generation = 0

    def populate(self):
        self.population = [Genome(self.target) for _ in range(POPULATION_SIZE)]
        for genome in self.population:
            genome.create_genes()

    def breed(self):
        children = []
        for _ in range(POPULATION_SIZE):
            father_genome = random.choice(self.population)
            mother_genome = random.choice(self.population)
            child_genome = father_genome.crossover(mother_genome)
            children.append(child_genome)

        # set the children population as the new generation
        self.population = children

    # ---------------------------------------------------Main Loop------------------------------------------------------ #


def natural_selection(fitness_population):
    mating_pool = []
    for pop in fitness_population:
        probability = math.floor(max(pop[1], 0) * 100)
        for _ in range(probability):
            mating_pool.append(pop[0])

    return mating_pool


def main():
    run = True
    food = Target()
    population = [Genome(food) for _ in range(POPULATION_SIZE)]
    # population = [Genome()]
    for genome in population:
        genome.create_genes()

    fitness_list = []
    generation = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        display.fill((0, 0, 0))
        for genome in population:
            # genome.draw()
            genome.move()
        food.draw()
        for genome in population:
            fitness = genome.calc_fitness()
            fitness_list.append((genome, fitness))

        fitness_list.sort(key=lambda x: x[1])
        fitness_list[::-1]
        mating_pool = natural_selection(fitness_population=fitness_list)
        mating_pool = mating_pool[:POPULATION_SIZE]
        population = breed(mating_pool, food)
        fitness_list = []
        pygame.display.flip()


if __name__ == "__main__":
    main()
