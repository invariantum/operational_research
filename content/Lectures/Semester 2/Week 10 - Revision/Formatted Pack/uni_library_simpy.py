"""Very simple SimPy examples for the Week 10 university library question.

Students can change the ADVISERS value and run the file again.

There are two separate models:
1. A standard first-come-first-served queue
2. A priority-user queue
"""

import random

import simpy


def basic_helpdesk_simulation():
    """Standard queue for parts (b) and (c)."""

    # Students can change this value and rerun the file.
    ADVISERS = 2

    ARRIVAL_RATE_PER_HOUR = 10
    MEAN_SERVICE_MINUTES = 7
    RUN_MINUTES = 360
    RANDOM_SEED = 24
    TARGET_WAIT = 8

    rng = random.Random(RANDOM_SEED)
    wait_times = []

    def arrivals(env, desk):
        while True:
            # Time until the next student arrives.
            interarrival = rng.expovariate(ARRIVAL_RATE_PER_HOUR / 60.0)
            yield env.timeout(interarrival)

            env.process(student(env, desk))

    def student(env, desk):
        arrival_time = env.now

        # The student joins the queue and waits for an adviser.
        with desk.request() as request:
            yield request

            wait = env.now - arrival_time
            wait_times.append(wait)

            # Once service starts, service time is random.
            service_time = rng.expovariate(1.0 / MEAN_SERVICE_MINUTES)
            yield env.timeout(service_time)

    env = simpy.Environment()
    desk = simpy.Resource(env, capacity=ADVISERS)
    env.process(arrivals(env, desk))

    # Stop the simulation at the end of the session.
    env.run(until=RUN_MINUTES)

    served = len(wait_times)

    print("STANDARD MODEL")
    print("Advisers =", ADVISERS)
    print("Students served =", served)
    print("Average wait =", sum(wait_times) / served if served else 0.0)
    print("Maximum wait =", max(wait_times) if served else 0.0)
    print(
        "Percent waiting less than",
        TARGET_WAIT,
        "minutes =",
        100 * sum(wait < TARGET_WAIT for wait in wait_times) / served if served else 0.0,
    )
    print()


def priority_helpdesk_simulation():
    """Priority-user queue for part (d)."""

    # Students can change this value and rerun the file.
    ADVISERS = 3

    ARRIVAL_RATE_PER_HOUR = 15
    MEAN_SERVICE_MINUTES = 7
    RUN_MINUTES = 360
    RANDOM_SEED = 24
    PRIORITY_SHARE = 0.10
    TARGET_WAIT = 8

    rng = random.Random(RANDOM_SEED)
    all_waits = []
    priority_waits = []
    standard_waits = []

    def arrivals(env, desk):
        while True:
            interarrival = rng.expovariate(ARRIVAL_RATE_PER_HOUR / 60.0)
            yield env.timeout(interarrival)

            # Some students are marked as priority users.
            is_priority = rng.random() < PRIORITY_SHARE
            env.process(student(env, desk, is_priority))

    def student(env, desk, is_priority):
        arrival_time = env.now

        # Smaller number = higher priority in SimPy.
        if is_priority:
            priority_level = 0
        else:
            priority_level = 1

        with desk.request(priority=priority_level) as request:
            yield request

            wait = env.now - arrival_time
            all_waits.append(wait)

            if is_priority:
                priority_waits.append(wait)
            else:
                standard_waits.append(wait)

            service_time = rng.expovariate(1.0 / MEAN_SERVICE_MINUTES)
            yield env.timeout(service_time)

    env = simpy.Environment()
    desk = simpy.PriorityResource(env, capacity=ADVISERS)
    env.process(arrivals(env, desk))
    # Stop the simulation at the end of the session.
    env.run(until=RUN_MINUTES)

    served = len(all_waits)

    print("PRIORITY MODEL")
    print("Advisers =", ADVISERS)
    print("Students served =", served)
    print(
        "Overall percent waiting less than",
        TARGET_WAIT,
        "minutes =",
        100 * sum(wait < TARGET_WAIT for wait in all_waits) / served if served else 0.0,
    )
    print("Priority average wait =", sum(priority_waits) / len(priority_waits) if priority_waits else 0.0)
    print("Standard average wait =", sum(standard_waits) / len(standard_waits) if standard_waits else 0.0)
    print()


if __name__ == "__main__":
    basic_helpdesk_simulation()
    priority_helpdesk_simulation()
