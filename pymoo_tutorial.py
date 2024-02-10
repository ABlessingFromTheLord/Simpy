import time

from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.config import Config

Config.warnings['not_compiled'] = False
import numpy as np


# Define the Knapsack Problem class
class MyKnapsackProblem(Problem):
    def __init__(self, items, capacity, min_fitness, variables):
        self.items = items
        self.capacity = capacity
        self.min_fitness = min_fitness
        super().__init__(n_var=variables, n_obj=1, n_constr=1, xl=0, xu=1)

    def _evaluate(self, x, out, *args, **kwargs):
        num_solutions = x.shape[0]  # Number of solutions provided

        fitness_values = np.zeros(num_solutions)
        constraint_values = np.zeros(num_solutions)

        for i in range(num_solutions):
            total_value = 0
            total_weight = 0

            for j, item in enumerate(self.items):
                if x[i, j] > 0:
                    total_value += item[1]
                    total_weight += item[2]

            if total_weight > self.capacity:
                # Constraint: Total weight should not exceed capacity
                constraint_values[i] = total_weight - self.capacity
                # Assign high objective value to discard this solution
                fitness_values[i] = -1
            else:
                # Check if total value meets the minimum fitness threshold
                if total_value >= self.min_fitness:
                    fitness_values[i] = total_value
                    constraint_values[i] = 0
                else:
                    # Assign low objective value to discourage this solution
                    fitness_values[i] = total_value
                    # Assign high constraint value to discourage this solution
                    constraint_values[i] = self.min_fitness - total_value

        # Assign values to dictionary
        out["F"] = fitness_values
        out["G"] = constraint_values


things_1 = [
    ('Laptop', 500, 2200),
    ('Headphones', 150, 160),
    ('Coffee Mug', 60, 350),
    ('Notepad', 40, 333),
    ('Water Bottle', 30, 192),
]

things_2 = [
    ('Laptop', 500, 2200),
    ('Headphones', 150, 160),
    ('Coffee Mug', 60, 350),
    ('Notepad', 40, 333),
    ('Water Bottle', 30, 192),
    ('Mints', 5, 25),
    ('Socks', 10, 38),
    ('Tissues', 15, 80),
    ('Phone', 500, 200),
    ('Baseball Cap', 100, 70)
]


class AlgorithmRunner:
    def __init__(self, things, fitness, capacity):
        self.things = things
        self.fitness = fitness
        self.capacity = capacity

    def run_algorithm(self):
        problem = MyKnapsackProblem(self.things, self.capacity, self.fitness, len(self.things))
        sampling = BinaryRandomSampling()
        crossover = TwoPointCrossover()
        mutation = BitflipMutation()

        algorithm = NSGA2(pop_size=100,
                          sampling=sampling,
                          crossover=crossover,
                          mutation=mutation,
                          eliminate_duplicates=True
                          )

        termination = get_termination("n_gen", 100)

        start = time.time()

        res = minimize(problem,
                       algorithm,
                       termination,
                       verbose=False)

        duration = time.time() - start
        return res.X


def genome_to_things(gene, things):
    result = []
    results = []

    if not isinstance(gene[0], np.ndarray):
        for i in range(len(things)):
            if gene[i] == 1:
                result.append(things[i][0])
        return result
    else:
        k = len(gene) - 1
        while k >= 0:
            temp = []
            for i in range(len(things)):
                if gene[k][i] == 1:
                    temp.append(things[i][0])
            results.append(temp)
            k -= 1
        return results


algo_1 = AlgorithmRunner(things_1, 740, 3000)
algo_2 = AlgorithmRunner(things_2, 1310, 3000)

gene_1 = algo_1.run_algorithm()
gene_2 = algo_2.run_algorithm()

print("Best solution found:")
print(f"best solution: {genome_to_things(gene_1, things_1)}")
print(f"best solution: {genome_to_things(gene_2, things_2)}")
#print(f"Time taken: {duration}")
