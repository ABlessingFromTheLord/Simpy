import simpy
import random
import statistics

wait_times = []


# The movie theater class itself
class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.num_servers = simpy.Resource(env, num_servers)
        self.num_ushers = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60) # since working in minutes, so 3 seconds

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 6))

    