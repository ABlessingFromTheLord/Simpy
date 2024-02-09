from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.ga import GA
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
    def __init__(self):
        super().__init__(n_var=5, n_obj=1, n_constr=1, xl=0, xu=1)
        self.weights = np.array([500, 150, 60, 40, 30])  # weights of items
        self.values = np.array([2200, 160, 350, 333, 192])  # values of items
        self.names = ['Laptop', 'Headphones', 'Coffe Mug', 'Notepad', 'Water Bottle']
        self.capacity = 3000

    def _evaluate(self, x, out, *args, **kwargs):
        out["F"] = -np.sum(self.values * x, axis=1)
        out["G"] = (np.sum(self.weights * x, axis=1) - self.capacity)




problem = MyKnapsackProblem()
sampling = BinaryRandomSampling()
crossover = TwoPointCrossover()
mutation = BitflipMutation()

algorithm = GA(
    pop_size=100,
    sampling=sampling,
    crossover=crossover,
    mutation=mutation,
    eliminate_duplicates=True
)

termination = get_termination("n_gen", 100)

res = minimize(problem,
               algorithm,
               termination,
               verbose=False)

print("Best solution found:")
print("Items to choose:")
for i in range(len(res.X)):
    if res.X[i] > 0:
        print(f"{problem.names[i]}")
print("Total value:", -res.F[0])
#print("Total weight:", np.sum([problem.weights[i][2] * res.X[i] for i in range(len(res.X))]))
