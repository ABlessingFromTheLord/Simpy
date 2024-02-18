import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

# Define the setup time matrix (replace this with your actual setup time data)
setup_times = np.array([[0, 2, 3],
                        [2, 0, 1],
                        [3, 1, 0]])


# Define the problem class
class JobSchedulingProblem(Problem):
    def __init__(self, setup):
        super().__init__(n_var=len(setup_times), n_obj=1, n_constr=0, xl=0, xu=len(setup_times)-1, type_var=int)
        self.setup_times = setup

    def _evaluate(self, X, out, *args, **kwargs):
        setup_times = np.array(self.setup_times)
        F = np.zeros((X.shape[0], 1))
        for i in range(X.shape[0]):
            x = X[i].astype(int)  # Convert to integer array
            setup_time = 0
            for j in range(len(x) - 1):
                setup_time += setup_times[x[j], x[j+1]]
            F[i, 0] = setup_time
        out["F"] = F


# Instantiate the problem
problem = JobSchedulingProblem(setup_times)

# Configure the NSGA-II algorithm
algorithm = NSGA2(pop_size=100)

# Run the optimization
res = minimize(problem,
               algorithm,
               ('n_gen', 100),
               seed=1,
               verbose=True)

# Visualize the results
best_solution = res.X[np.argmin(res.F[:, 0])]
best_setup_time = res.F[np.argmin(res.F[:, 0])]
print("Best solution:", best_solution)
print("Best setup time:", best_setup_time)
