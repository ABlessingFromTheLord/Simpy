from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.pntx import TwoPointCrossover
from pymoo.operators.mutation.bitflip import BitflipMutation
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.operators.sampling.rnd import BinaryRandomSampling
from pymoo.config import Config

Config.warnings['not_compiled'] = False
import numpy as np


class NearestIntegerRelation(Problem):
    def __init__(self):
        super().__init__(n_var=3, n_obj=1, n_constr=0, xl=0, xu=100, elementwise_evaluation=True)

    def _evaluate(self, x, out, *args, **kwargs):
        x = x[:, 0]
        e = 300  # Target value for 17x + 11y + 97z
        out["F"] = np.abs(17 * x + 11 * x + 97 * x - e)  # Use only x since x=y=z

        # Constraint: x = y = z
        out["G"] = np.zeros_like(x)



problem = NearestIntegerRelation()
algorithm = NSGA2(pop_size=100)
termination = get_termination("n_gen", 100)

res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               verbose=True)

print("Best solution:", res.X, "Best fitness:", res.F)
