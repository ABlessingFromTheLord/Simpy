from pymoo.model.problem import Problem
from pymoo.algorithms.genetic_algorithm import GeneticAlgorithm
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize
from pymoo.util.termination.default import SingleObjectiveDefaultTermination
import numpy as np

# Define the knapsack problem class
class KnapsackProblem(Problem):
    def __init__(self):
        super().__init__(n_var=5, n_obj=1, n_constr=2, xl=0, xu=1, elementwise_evaluation=True)

    def _evaluate(self, x, out, *args, **kwargs):
        values = [500, 150, 60, 40, 30]
        weights = [2200, 160, 350, 333, 192]
        fitness = np.dot(x, values)
        weight = np.dot(x, weights)
        out["F"] = -fitness  # maximize
        out["G"] = [weight - 3000, fitness - 740]  # constraints

# Define the genetic algorithm settings
algorithm = GeneticAlgorithm(
    pop_size=100,
    sampling=get_sampling("bin_random"),
    crossover=get_crossover("bin_hux"),
    mutation=get_mutation("bin_bitflip"),
    eliminate_duplicates=True
)

# Create the knapsack problem instance
problem = KnapsackProblem()

# Define termination criteria
termination = SingleObjectiveDefaultTermination()

# Run the genetic algorithm
res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               verbose=True)

# Print the best solution found
print("Best solution found:")
print("X =", res.X)
print("Fitness =", -res.F[0])
