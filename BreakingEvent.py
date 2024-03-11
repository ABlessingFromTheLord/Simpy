import simpy


# Define a function to check if the variable x reaches 10
def check_variable(env, x):
    while True:
        if x.value >= 10:
            return env.event()
        else:
            # Yield a timeout event to let the simulation run
            yield env.timeout(1)  # Adjust the timeout value as needed


# Define a process that modifies the variable x over time
def variable_process(env, x):
    while True:
        # Modify the variable x
        # For demonstration purposes, we'll increment x by 1 every time step
        x.value += 1
        print("Current value of x:", x.value)

        # Yield a timeout event to let the simulation run
        yield env.timeout(1)  # Adjust the timeout value as needed


# Create a SimPy environment
env = simpy.Environment()


# Define a shared variable x
class SharedVariable:
    def __init__(self):
        self.value = 0


# Instantiate the shared variable
x = SharedVariable()

# Start the variable process
env.process(variable_process(env, x))

# Start the event checking process
env.process(check_variable(env, x).process())

# Run the simulation
env.run(until=lambda: x.value >= 10)

print("Variable x has reached 10!")
