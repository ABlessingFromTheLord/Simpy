import random as rnd
import numpy as np

# parameters or variables to vary
NUMBER_OF_EMPLOYEES = 2
AVG_SUPPORT_TIME = 5
CUSTOMER_INTERVAL = 2
SIM_TIME = 120

# accessible variables
customers_handled = 0

env = simpy.Environment()

class CallCenter:

    def __init__(self, env, num_employees, support_time):
        self.env = env
        self.staff = sp.Resource(env, num_employees)
        self.support_time = support_time

    # action function or where the support takes place
    def support(self, customer):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        print(f"Support finished for  {customer} at {self.env.now:.2f}")

def customer(env, name, call_center):
        global customers_handled
        print(f"Customer {name} enters waiting queue at {env.now:.2f}!")
        with call_center.staff.request() as request:
            yield request
            print(f"Customer {name} enters call at {env.now:.2f}")
            yield env.process(call_center.support(name))
            print(f"Customer {name} left call at {env.now:.2f}")
            customers_handled += 1


# Setting up the whole thing
def setup(env, num_employees, support_time, customer_interval):
    call_center = CallCenter(env, num_employees, support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(rnd.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, call_center))

print("Starting call center simulation")
env.process(setup(env, NUMBER_OF_EMPLOYEES, AVG_SUPPORT_TIME, CUSTOMER_INTERVAL))
env.run(until=SIM_TIME)

print("Customers handled: " + str(customers_handled))