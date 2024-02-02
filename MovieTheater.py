import simpy
import random
import statistics

wait_times = []
executions = 0
exceptions = 0


# The movie theater class itself
class Theater:
    def __init__(self, this_env):
        self.env = this_env
        self.broken = False
        self.amount = 10
        self.already_called = False
        self.time = 100
        self.process = None

    def breaking(self):
        while True:
            yield self.env.timeout(80)
            break_or_not = random.random() > 0.5
            print(break_or_not)
            # if true then machine breaks down, else continues running

            if break_or_not and not self.broken:
                self.process.interrupt()

    def check_ticket(self, time):
        while True:
            start = self.env.now
            try:
                print("We are executing normally")
                global executions
                executions += 1
                yield self.env.timeout(100)  # since working in minutes, so 3 seconds
                time = 0

            except simpy.Interrupt:
                self.broken = True
                global exceptions
                exceptions += 1
                print("yaaayyyy entered exception")
                time -= (self.env.now - start)  # remaining time from when breakdown occurred
                yield self.env.timeout(100)
                self.broken = False

    def running(self):
        self.env.process(self.breaking())
        self.process = env.process(self.check_ticket(self.time))
        yield self.process


env = simpy.Environment()
theater = Theater(env)
env.process(theater.running())
env.run(until=86400)

print("simulation is done", "executions: ", executions, "exceptions: ", exceptions)