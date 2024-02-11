from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
import numpy as np

# Define constants
MACHINE_A_CAPACITY = 20
MACHINE_B_CAPACITY = 60
ORDER_X = 0
ORDER_Y = 0
REM_X = 0
REM_Y = 0

TEMP_ORDER_X = 0
TEMP_ORDER_Y = 0


def set_test_values(order_x, order_y, rem_x, rem_y):
    global ORDER_X
    ORDER_X = order_x
    global ORDER_Y
    ORDER_Y = order_y
    global REM_X
    REM_X = rem_x
    global REM_Y
    REM_Y = rem_y


def get_true_order_balance():
    global TEMP_ORDER_X
    global ORDER_X
    if REM_X >= ORDER_X:
        TEMP_ORDER_X = REM_X - ORDER_X
        ORDER_X = 0
    else:
        TEMP_ORDER_X = ORDER_X - REM_X
        ORDER_X = TEMP_ORDER_X

    global TEMP_ORDER_Y
    global ORDER_Y
    if REM_Y >= ORDER_Y:
        TEMP_ORDER_Y = REM_Y - ORDER_Y
        ORDER_Y = 0
    else:
        TEMP_ORDER_Y = ORDER_Y - REM_Y
        ORDER_Y = TEMP_ORDER_Y


set_test_values(60, 60, 10, 90)
get_true_order_balance()


class JobShopScheduling(Problem):
    def __init__(self):
        super().__init__(n_var=2, n_obj=1, n_constr=0, xl=np.array([0, 0]), xu=np.array([ORDER_X, ORDER_Y]))

    def _evaluate(self, x, out, *args, **kwargs):
        total_x = np.zeros(len(x))
        total_y = np.zeros(len(x))

        for i in range(len(x)):
            if x[i, 0] > 0:

                total_x[i] = MACHINE_A_CAPACITY * x[i, 0]
            if x[i, 1] > 0:
                total_y[i] = MACHINE_B_CAPACITY * x[i, 1]
        fitness = np.abs(total_x - TEMP_ORDER_X) + np.abs(total_y - TEMP_ORDER_Y)
        out["F"] = fitness[:, None]  # Reshape to match the expected shape
        out["G"] = np.zeros((len(x), 0))  # No constraints for now


problem = JobShopScheduling()


algorithm = NSGA2(
    pop_size=100,
    n_offsprings=50,
    eliminate_duplicates=True
)

res = minimize(problem,
               algorithm,
               ('n_gen', 1000),
               seed=1,
               verbose=True)

print("Best solution found: %s" % res.X)
print(round(res.X[0]))
print(round(res.X[1]))