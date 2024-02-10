import time
from collections import namedtuple
from functools import partial
from random import choices, randint, randrange, random
from typing import List, Optional, Callable, Tuple

# definitions
Genome = List[int]
Population = List[Genome]
Thing = namedtuple('Thing', ['name', 'value', 'weight'])

# instances
things = [
    Thing('Laptop', 500, 2200),
    Thing('Headphones', 150, 160),
    Thing('Coffee Mug', 60, 350),
    Thing('Notepad', 40, 333),
    Thing('Water Bottle', 30, 192),
]

more_things = [
                  Thing('Mints', 5, 25),
                  Thing('Socks', 10, 38),
                  Thing('Tissues', 15, 80),
                  Thing('Phone', 500, 200),
                  Thing('Baseball Cap', 100, 70),
              ] + things

# functions as parameters
PopulateFunc = Callable[[], Population]  # takes no parameters, returns solutions
FitnessFunc = Callable[[Genome], int]  # takes genome and returns fitness value to make correct choice
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]  # returns new fit solutions from population
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]  # returns two new genomes from two genomes
MutationFunc = Callable[[Genome], Genome]  # returns mutated genome with a certain probability
PrinterFunc = Callable[[Population, int, FitnessFunc], None]


# returns a genome, random list of 0's and 1's
def generate_genome(length: int) -> Genome:
    return choices([0, 1], k=length)


# returns a population, i.e,  a list of genomes
def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


#  fitness function evaluates the fitness of the solution
def fitness(genome: Genome, things: [Thing], weight_limit: int) -> int:
    if len(genome) != len(things):
        raise ValueError("genome and things must be of the same length")

    weight = 0
    value = 0

    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += thing.weight
            value += thing.value

            if weight > weight_limit:
                return 0

    return value


# select a pair of solutions that will be a parents of the two new solutions for the next generation
# select solutions with most fitness with high probability
def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    return choices(
        population=population,
        weights=[fitness_func(genome) for genome in population],
        k=2  # draw twice from population to get a pair
    )


# takes two genomes as parameters and returns two genomes as outputs
#  randomly cut the index at index i and join them crossing 1 and b
def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of same length")

    length = len(a)
    if length < 2:
        return a, b  # cannot cut since length is 1

    p = randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


# takes genome and changes it with a certain probability
# this changes 1 to 0 and 0 to 1
def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    for _ in range(num):  # choosing a random index
        index = randrange(len(genome))

        if random() > probability:
            genome[index] = genome[index]
        else:
            genome[index] = abs(genome[index] - 1)  # abs incase it is 0 - 1

    return genome


def genome_to_string(genome: Genome) -> str:
    return "".join(map(str, genome))


# simulating the actual evolution
def run_evolution(
        populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100,  # max generation to run of not reaching fitness limit before this
        printer: Optional[PrinterFunc] = None) \
        -> Tuple[Population, int]:
    population = populate_func()  # getting first ever generation

    #  looping for the evolution limit
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        if printer is not None:
            printer(population, i, fitness_func)

        if fitness_func(population[0]) >= fitness_limit:
            break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_func(population, fitness_func)  # select parents
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])  # get two children form the parents
            offspring_a = mutation_func(offspring_a)  # expand variety
            offspring_b = mutation_func(offspring_b)  # expand variety
            next_generation += [offspring_a, offspring_b]

        population = next_generation  # replace current population with next generation and restart

    population = sorted(
        population,
        key=lambda genome: fitness_func(genome),
        reverse=True
    )

    return population, i


#  instantiating the solution to run
start = time.time()
population, generations = run_evolution(
    # for things test with a fitness of 740
    # for more_things test with a fitness of 1310

    populate_func=partial(
        generate_population, size=10, genome_length=len(more_things)
    ),
    fitness_func=partial(
        fitness, things=more_things, weight_limit=3000
    ),
    fitness_limit=1310,
    generation_limit=100
)
end = time.time()


# printing the current genome after evolution by checking if bit is set
def genome_to_things(genome: Genome, things: [Thing]) -> [Thing]:
    result = []

    for i, thing in enumerate(more_things):
        if genome[i] == 1:
            result += [thing.name]

    return result


print(f"number of generations: {generations}")
print(f"time: {end - start}s")
print(f"best solution: {genome_to_things(population[0], more_things)}")

print(genome_to_string(population[0]))