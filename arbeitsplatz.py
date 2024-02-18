import simpy

def process1(env):
    while True:
        # Process logic here
        print("time in process1 is ", env.now)
        yield env.timeout(10)  # Example: wait for 1 time unit

def process2(env):
    while True:
        # Process logic here
        print("time in process2 is ", env.now)
        yield env.timeout(10)  # Example: wait for 2 time units

def running_concurrently(env):
    env.process(process1(env))
    env.process(process2(env))
    yield env.timeout(0)


env = simpy.Environment()

# Create SimPy processes within the simulation environment
env.process(running_concurrently(env))
# Run the simulation until time 10
env.run(until=100)
