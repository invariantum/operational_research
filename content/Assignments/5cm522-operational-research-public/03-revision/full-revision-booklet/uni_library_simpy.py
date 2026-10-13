"""SimPy solution for the university library help-desk question from Practice Paper B."""

from __future__ import annotations

import random

import pandas as pd
import simpy


def run_helpdesk_simulation(arrival_rate_per_hour: float, mean_service_minutes: float, advisers: int, run_minutes: int, seed: int, target_wait: float):
    rng = random.Random(seed)
    wait_times = []

    def arrivals(env, desk):
        student_number = 0
        while True:
            interarrival = rng.expovariate(arrival_rate_per_hour / 60.0)
            yield env.timeout(interarrival)
            if env.now > run_minutes:
                break
            student_number += 1
            env.process(student(env, f"S{student_number}", desk))

    def student(env, name, desk):
        del name
        arrival_time = env.now
        with desk.request() as request:
            yield request
            wait = env.now - arrival_time
            wait_times.append(wait)
            service_time = rng.expovariate(1.0 / mean_service_minutes)
            yield env.timeout(service_time)

    env = simpy.Environment()
    desk = simpy.Resource(env, capacity=advisers)
    env.process(arrivals(env, desk))
    env.run(until=run_minutes + 10000)

    served = len(wait_times)
    return {
        "served": served,
        "average_wait": sum(wait_times) / served if served else 0.0,
        "maximum_wait": max(wait_times) if served else 0.0,
        "percent_under_target": 100 * sum(wait < target_wait for wait in wait_times) / served if served else 0.0,
    }


def run_priority_helpdesk(arrival_rate_per_hour: float, mean_service_minutes: float, advisers: int, run_minutes: int, seed: int, priority_share: float, target_wait: float):
    rng = random.Random(seed)
    results = []

    def arrivals(env, desk):
        student_number = 0
        while True:
            interarrival = rng.expovariate(arrival_rate_per_hour / 60.0)
            yield env.timeout(interarrival)
            if env.now > run_minutes:
                break
            student_number += 1
            is_priority = rng.random() < priority_share
            env.process(student(env, f"S{student_number}", desk, is_priority))

    def student(env, name, desk, is_priority):
        arrival_time = env.now
        priority_level = 0 if is_priority else 1
        with desk.request(priority=priority_level) as request:
            yield request
            wait = env.now - arrival_time
            results.append({"student": name, "priority": is_priority, "wait": wait})
            service_time = rng.expovariate(1.0 / mean_service_minutes)
            yield env.timeout(service_time)

    env = simpy.Environment()
    desk = simpy.PriorityResource(env, capacity=advisers)
    env.process(arrivals(env, desk))
    env.run(until=run_minutes + 10000)

    output = pd.DataFrame(results)
    standard = output[output["priority"] == False]
    priority = output[output["priority"] == True]
    return {
        "served": int(len(output)),
        "overall_percent_under_target": float(100 * (output["wait"] < target_wait).mean()) if len(output) else 0.0,
        "priority_average_wait": float(priority["wait"].mean()) if len(priority) else 0.0,
        "standard_average_wait": float(standard["wait"].mean()) if len(standard) else 0.0,
    }


def main():
    baseline = run_helpdesk_simulation(10, 7, 2, 360, 24, 8)
    print("Baseline with 2 advisers:", baseline)

    rows = []
    for advisers in (2, 3, 4):
        result = run_helpdesk_simulation(15, 7, advisers, 360, 24, 8)
        rows.append(
            {
                "advisers": advisers,
                "served": result["served"],
                "avg_wait": round(result["average_wait"], 4),
                "max_wait": round(result["maximum_wait"], 4),
                "pct_below_8": round(result["percent_under_target"], 4),
            }
        )
    print("\nPeak-period table:")
    print(pd.DataFrame(rows).to_string(index=False))

    priority_result = run_priority_helpdesk(15, 7, 3, 360, 24, 0.10, 8)
    print("\nPriority extension with 3 advisers:", priority_result)


if __name__ == "__main__":
    main()
