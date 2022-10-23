# The Genetic Algorithm

# Implementing genetic algorithm on a population of a given
# size to attain the goal of reaching a given target.

# DISCLAIMER:
# I will be using the word "genome" to indicate
# the creatures in the genetic evolution algorithm

# AIM:
# To create a algorithm that will, by the process of evolution, teach a populaion
# to navigate towards a desired goal

# GENETIC ALGORITHM
# [step 1] A population, on it's first generation is left to roam randomly inside the canvas.
#
# [step 2] The next generation is bred from the best performers, selected based on a fitness function of the first generation in hopes to
#          recreate the genes that made the genomes to go in the desired direction.
#
# [step 3] Some genes of the next generation is mutated[randomly changed] based on a MUTATION RATE, this, in theory, will bring
#          some variance in the behaviors of the genomes to better replicate natural evolution.
#
# [step 4] The above steps are followed for many generation untill the genomes are almost perfectly skilled to reach the given target
#          due to generations of evolution and mutation.


import pygame
from pygame.locals import *
import random
import math

pygame.font.init()

# ------------------------------------------------------global variables--------------------------------------------------------- #

width = 720
height = 480
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("Genetic Algorithm")

# ---------------------------------------------------configuration constants------------------------------------------------------ #

POPULATION_SIZE = 100
MUTATION_RATE = 0.02
GENE_LENGTH = 10000
FONT_SIZE = 14
ARCADE_FONT = pygame.font.SysFont("Arial", FONT_SIZE)

# --------------------------------------------------------Genome Class------------------------------------------------------------ #


class Genome(object):
    def __init__(self, target):
        self.gene_length = GENE_LENGTH
        self.gene = []
        self.x = width // 2
        self.y = 10
        self.step = 0
        self.target = target
        self.fitness = -1
        self.dead = False
        self.generation = -1

    def create_genes(self):
        for _ in range(self.gene_length):
            x_direction = random.uniform(-1, 1)
            y_direction = random.uniform(-1, 1)
            self.gene.append([x_direction, y_direction])

    def draw(self):
        pygame.draw.circle(display, (0, 170, 200),
                           (self.x, self.y), 4)

    def move(self):
        self.x += self.gene[self.step][0]
        self.y += self.gene[self.step][1]
        self.step += 1

        if self.step >= self.gene_length:
            self.fitness = self.calc_fitness()
            self.dead = True

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
        for i in range(self.gene_length):
            if i % 2 == 0:
                child.gene.append(self.gene[i])
            else:
                child.gene.append(partner.gene[i])

        return child

    def mutate(self):
        for i in range(GENE_LENGTH):
            mutation_probability = round(random.uniform(0, 1), 2)
            if mutation_probability == MUTATION_RATE:
                mutated_gene_x = random.uniform(-1, 1)
                mutated_gene_y = random.uniform(-1, 1)
                self.gene[i] = [mutated_gene_x, mutated_gene_y]

# -------------------------------------------------------Population Class--------------------------------------------------------- #


class Population(object):
    def __init__(self, target):
        self.target = target
        self.population = []
        self.generation = 0

    def populate(self):
        self.population = [Genome(self.target) for _ in range(POPULATION_SIZE)]
        for genome in self.population:
            genome.create_genes()
            genome.generation = self.generation

    def natural_selection(self):
        mating_pool = []
        for genome in self.population:
            fitness_ratio = math.floor(max(genome.fitness, 0) * 100)
            for _ in range(fitness_ratio):
                mating_pool.append(genome)

        return mating_pool

    def breed(self):
        generation_dead = all([genome.dead for genome in self.population])
        if generation_dead:
            self.population = self.natural_selection()
            children = Population(self.target)

            for _ in range(POPULATION_SIZE):
                father_genome = random.choice(self.population)
                mother_genome = random.choice(self.population)
                child_genome = father_genome.crossover(mother_genome)
                child_genome.mutate()
                child_genome.generation = self.generation
                children.population.append(child_genome)

            self.population = children.population
            self.generation += 1


# ---------------------------------------------------------Target Class----------------------------------------------------------- #


class Target(object):
    def __init__(self):
        self.x = width // 2
        self.y = height - 10
        self.width = 20

    def draw(self):
        pygame.draw.rect(display, (0, 200, 170), (
            self.x - self.width // 2, self.y - self.width // 2, self.width, self.width))

# -----------------------------------------------------------DEBUG FUNC------------------------------------------------------------ #


def config_str(name, config_var):
    content = name + str(round(float(config_var), 2))
    render_text = ARCADE_FONT.render(content, 1, pygame.Color("Cyan"))
    return render_text


def print_config_vars(vars, y, rez):
    for var in vars:
        display.blit(config_str(var[0], var[1]), (10, y))
        y += rez

# -----------------------------------------------------------Game Loop------------------------------------------------------------ #


def main():
    run = True
    food = Target()
    population = Population(food)
    population.populate()
    clock = pygame.time.Clock()
    avg_fitness = 0
    best_fitness = 0

    while run:
        clock.tick()
        config_vars = [
            ["Frame Rate        : ", clock.get_fps()],
            ["Population Size : ", POPULATION_SIZE],
            ["Mutation Rate     : ", MUTATION_RATE],
            ["Gene Length       : ", GENE_LENGTH],
            ["Generation          : ", population.generation],
            ["Average Fitness : ", avg_fitness],
            ["Best Fitness       : ", best_fitness],
        ]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        display.fill((0, 0, 0))
        for genome in population.population:
            genome.draw()
            genome.move()

        food.draw()
        fitness_list = [genome.calc_fitness()
                        for genome in population.population]
        avg_fitness = sum(fitness_list) / POPULATION_SIZE
        best_fitness = max(avg_fitness, best_fitness)
        population.breed()
        print_config_vars(config_vars, 10, FONT_SIZE + 2)

        pygame.display.flip()


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------------------------------------------------------------------- #
