import simpy


def user(env, resource):
    print("before request count variable is ", resource.count)
    print("before request count variable is ", resource.capacity)

    with resource.request() as req:
        yield req
        print(f"Resource is being used at time {env.now}")
        print("count variable is ", resource.count)
        print("count variable is ", resource.capacity)
        yield env.timeout(2)  # Simulate some processing time

    print("after request count variable is ", resource.count)
    print("after request count variable is ", resource.capacity)


env = simpy.Environment()
resource = simpy.Resource(env, capacity=1)
env.process(user(env, resource))

# Run simulation
env.run(until=5)
