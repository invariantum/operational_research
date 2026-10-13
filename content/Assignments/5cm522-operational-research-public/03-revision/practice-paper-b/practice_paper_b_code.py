"""Verification code for 5CM522 Practice Paper B.

This file is deliberately self-contained so it matches the style of the
module examples more closely.
"""

from __future__ import annotations

import importlib
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import simpy
from pyomo.environ import Binary, ConcreteModel, Constraint, NonNegativeReals, Objective, Set, SolverFactory, Var, maximize, minimize, value


def get_solver():
    """Return an available Pyomo solver."""
    for name in ("appsi_highs", "highs"):
        solver = SolverFactory(name)
        if solver.available(False):
            return solver
    raise RuntimeError("No suitable Pyomo solver is available.")


SOLVER = get_solver()


def load_cp_sat():
    """Return OR-Tools' CP-SAT module, or None where OR-Tools is unavailable.

    OR-Tools has no WebAssembly build, so in the browser (JupyterLite) the job shop
    in Question 1 is solved with an equivalent Pyomo + HiGHS model instead. Both give
    the same optimal makespan; when several schedules are optimal they may show a
    different (equally good) one.
    """
    try:
        return importlib.import_module("ortools.sat.python.cp_model")
    except ImportError:
        return None


cp_model = load_cp_sat()


def get_output_dir() -> Path:
    """Choose a sensible output directory for scripts and notebooks."""
    if "google.colab" in sys.modules:
        return Path("/content")
    if "__file__" in globals():
        return Path(__file__).resolve().parent
    return Path.cwd()


# Generated files go to an output/ subfolder so the published answer workbook next to
# this script is never overwritten.
WORKBOOK_PATH = get_output_dir() / "output" / "practice_paper_b_forecasting.xlsx"


def build_forecasting_tables(data: list[int], validation_start: int, future_periods: list[int]):
    """Build forecasting tables using the centred moving-average method taught in class."""
    periods = np.arange(1, len(data) + 1)
    quarters = ((periods - 1) % 4) + 1
    train_end = validation_start - 1

    df = pd.DataFrame({"t": periods, "quarter": quarters, "actual": data})
    df["ma4"] = np.nan
    df["cma"] = np.nan

    train_series = pd.Series(data[:train_end])
    moving_average_4 = train_series.rolling(4).mean()
    cma = ((moving_average_4 + moving_average_4.shift(-1)) / 2).shift(-1)

    df.loc[df["t"] <= train_end, "ma4"] = moving_average_4.to_numpy()
    df.loc[df["t"] <= train_end, "cma"] = cma.to_numpy()

    train = df[df["t"] <= train_end].copy()
    cma_rows = train[train["cma"].notna()].copy()
    cma_rows["add_seasonal"] = cma_rows["actual"] - cma_rows["cma"]
    cma_rows["mult_seasonal"] = cma_rows["actual"] / cma_rows["cma"]

    additive_indices = cma_rows.groupby("quarter")["add_seasonal"].mean()
    additive_indices = additive_indices - additive_indices.mean()

    multiplicative_indices = cma_rows.groupby("quarter")["mult_seasonal"].mean()
    multiplicative_indices = multiplicative_indices / multiplicative_indices.mean()

    train["deseasonalised_add"] = train["actual"] - train["quarter"].map(additive_indices)
    train["deseasonalised_mult"] = train["actual"] / train["quarter"].map(multiplicative_indices)

    trend_slope, trend_intercept = np.polyfit(cma_rows["t"], cma_rows["cma"], 1)

    validation = df[df["t"] >= validation_start].copy()
    validation["add_trend"] = trend_slope * validation["t"] + trend_intercept
    validation["mult_trend"] = trend_slope * validation["t"] + trend_intercept
    validation["add_forecast"] = validation["add_trend"] + validation["quarter"].map(additive_indices)
    validation["mult_forecast"] = validation["mult_trend"] * validation["quarter"].map(multiplicative_indices)
    validation["add_abs_error"] = (validation["actual"] - validation["add_forecast"]).abs()
    validation["mult_abs_error"] = (validation["actual"] - validation["mult_forecast"]).abs()

    future_quarters = ((np.array(future_periods) - 1) % 4) + 1
    future = pd.DataFrame({"t": future_periods, "quarter": future_quarters})
    future["add_trend"] = trend_slope * future["t"] + trend_intercept
    future["mult_trend"] = trend_slope * future["t"] + trend_intercept
    future["add_forecast"] = future["add_trend"] + future["quarter"].map(additive_indices)
    future["mult_forecast"] = future["mult_trend"] * future["quarter"].map(multiplicative_indices)

    summary = {
        "additive_indices": additive_indices.to_dict(),
        "multiplicative_indices": multiplicative_indices.to_dict(),
        "mad_additive": float(validation["add_abs_error"].mean()),
        "mad_multiplicative": float(validation["mult_abs_error"].mean()),
        "trend_intercept": float(trend_intercept),
        "trend_slope": float(trend_slope),
        "better_model": "additive"
        if validation["add_abs_error"].mean() <= validation["mult_abs_error"].mean()
        else "multiplicative",
    }

    return {
        "data": df,
        "cma_rows": cma_rows,
        "train": train,
        "validation": validation,
        "future": future,
        "summary": summary,
    }


def export_forecasting_workbook(output_path: Path, tables):
    """Write the forecasting tables to Excel."""
    summary = tables["summary"]
    summary_df = pd.DataFrame(
        [
            ("MAD additive", summary["mad_additive"]),
            ("MAD multiplicative", summary["mad_multiplicative"]),
            ("Better model", summary["better_model"]),
            ("Trend line", f"T_hat = {summary['trend_intercept']:.2f} + {summary['trend_slope']:.2f}t"),
        ],
        columns=["Item", "Value"],
    )
    seasonal_df = pd.DataFrame(
        {
            "quarter": [1, 2, 3, 4],
            "additive_index": [summary["additive_indices"][q] for q in [1, 2, 3, 4]],
            "multiplicative_index": [summary["multiplicative_indices"][q] for q in [1, 2, 3, 4]],
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        seasonal_df.to_excel(writer, sheet_name="Seasonal Indices", index=False)
        tables["data"].to_excel(writer, sheet_name="Data and CMA", index=False)
        tables["cma_rows"].to_excel(writer, sheet_name="Seasonal Variations", index=False)
        tables["train"].to_excel(writer, sheet_name="Deseasonalised Trend", index=False)
        tables["validation"].to_excel(writer, sheet_name="Validation", index=False)
        tables["future"].to_excel(writer, sheet_name="Future Forecasts", index=False)


def solve_job_shop_milp(job_data):
    """Solve the job shop as a disjunctive MILP with Pyomo + HiGHS (used when OR-Tools is unavailable)."""
    operations = [(job, k) for job, tasks in job_data.items() for k in range(len(tasks))]
    duration = {(job, k): job_data[job][k][1] for job, k in operations}
    machine = {(job, k): job_data[job][k][0] for job, k in operations}
    horizon = sum(duration.values())
    pairs = [
        (a, b)
        for i, a in enumerate(operations)
        for b in operations[i + 1:]
        if machine[a] == machine[b]
    ]

    model = ConcreteModel()
    model.O = Set(initialize=operations, dimen=2)
    model.P = Set(initialize=range(len(pairs)))
    model.start = Var(model.O, domain=NonNegativeReals)
    model.first = Var(model.P, domain=Binary)  # 1 if the first operation of the pair goes first
    model.makespan = Var(domain=NonNegativeReals)
    model.objective = Objective(expr=model.makespan, sense=minimize)

    def precedence(m, job, k):
        if k == 0:
            return Constraint.Skip
        return m.start[job, k] >= m.start[job, k - 1] + duration[job, k - 1]

    model.precedence = Constraint(model.O, rule=precedence)
    model.a_before_b = Constraint(
        model.P,
        rule=lambda m, p: m.start[pairs[p][0]] + duration[pairs[p][0]] <= m.start[pairs[p][1]] + horizon * (1 - m.first[p]),
    )
    model.b_before_a = Constraint(
        model.P,
        rule=lambda m, p: m.start[pairs[p][1]] + duration[pairs[p][1]] <= m.start[pairs[p][0]] + horizon * m.first[p],
    )
    model.finish = Constraint(
        list(job_data),
        rule=lambda m, job: m.makespan >= m.start[job, len(job_data[job]) - 1] + duration[job, len(job_data[job]) - 1],
    )
    SOLVER.solve(model)

    # Several schedules reach the optimal makespan. Among them, take the one that finishes the
    # jobs earliest overall (minimum total completion time), so the schedule is reproducible.
    best = value(model.makespan)
    model.keep_makespan = Constraint(expr=model.makespan <= best + 1e-6)
    model.objective.deactivate()
    last = {job: (job, len(tasks) - 1) for job, tasks in job_data.items()}
    model.total_completion = Objective(
        expr=sum(model.start[last[job]] + duration[last[job]] for job in job_data), sense=minimize
    )
    SOLVER.solve(model)

    rows = []
    for job, k in operations:
        start = int(round(value(model.start[job, k])))
        rows.append({"job": job, "task": k + 1, "machine": machine[job, k], "duration": duration[job, k],
                     "start": start, "end": start + duration[job, k]})
    makespan = int(round(value(model.makespan)))
    return makespan, pd.DataFrame(rows).sort_values(["start", "job", "task"]).reset_index(drop=True)


def solve_job_shop(job_data):
    """Solve a small job shop problem using OR-Tools CP-SAT (Pyomo + HiGHS if OR-Tools is unavailable)."""
    if cp_model is None:
        return solve_job_shop_milp(job_data)
    model = cp_model.CpModel()
    machine_names = sorted({machine for tasks in job_data.values() for machine, _ in tasks})
    machine_index = {name: idx for idx, name in enumerate(machine_names)}
    horizon = sum(duration for tasks in job_data.values() for _, duration in tasks)

    all_tasks = {}
    machine_intervals = {idx: [] for idx in machine_index.values()}

    for job_name, tasks in job_data.items():
        for task_number, (machine_name, duration) in enumerate(tasks):
            suffix = f"{job_name}_{task_number}"
            start = model.NewIntVar(0, horizon, f"start_{suffix}")
            end = model.NewIntVar(0, horizon, f"end_{suffix}")
            interval = model.NewIntervalVar(start, duration, end, f"interval_{suffix}")
            machine_id = machine_index[machine_name]
            all_tasks[(job_name, task_number)] = {
                "machine": machine_name,
                "duration": duration,
                "start": start,
                "end": end,
            }
            machine_intervals[machine_id].append(interval)

    for intervals in machine_intervals.values():
        model.AddNoOverlap(intervals)

    for job_name, tasks in job_data.items():
        for task_number in range(len(tasks) - 1):
            model.Add(all_tasks[(job_name, task_number + 1)]["start"] >= all_tasks[(job_name, task_number)]["end"])

    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, [all_tasks[(job_name, len(tasks) - 1)]["end"] for job_name, tasks in job_data.items()])
    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    solver.parameters.num_search_workers = 8
    solver.Solve(model)

    rows = []
    for job_name, tasks in job_data.items():
        for task_number, (machine_name, duration) in enumerate(tasks):
            task = all_tasks[(job_name, task_number)]
            rows.append(
                {
                    "job": job_name,
                    "task": task_number + 1,
                    "machine": machine_name,
                    "duration": duration,
                    "start": solver.Value(task["start"]),
                    "end": solver.Value(task["end"]),
                }
            )

    return int(solver.Value(makespan)), pd.DataFrame(rows).sort_values(["start", "job", "task"]).reset_index(drop=True)


def question_1_scheduling():
    """Flow shop solved by Johnson's rule and job shop solved in OR-Tools (or Pyomo + HiGHS)."""
    jobs = {"J1": (7, 5), "J2": (3, 8), "J3": (6, 4), "J4": (2, 9), "J5": (5, 6)}

    remaining = dict(jobs)
    front = []
    back = []
    while remaining:
        next_job = min(remaining, key=lambda name: min(remaining[name]))
        m1_time, m2_time = remaining[next_job]
        if m1_time <= m2_time:
            front.append(next_job)
        else:
            back.insert(0, next_job)
        remaining.pop(next_job)
    johnson_sequence = front + back

    def flow_shop_schedule(order):
        machine_1_clock = 0
        machine_2_clock = 0
        rows = []
        for job_name in order:
            m1_time, m2_time = jobs[job_name]
            m1_start = machine_1_clock
            m1_finish = m1_start + m1_time
            machine_1_clock = m1_finish
            m2_start = max(machine_2_clock, m1_finish)
            m2_finish = m2_start + m2_time
            machine_2_clock = m2_finish
            rows.append((job_name, m1_start, m1_finish, m2_start, m2_finish))
        return machine_2_clock, rows

    flow_makespan, flow_schedule = flow_shop_schedule(johnson_sequence)
    original_makespan, _ = flow_shop_schedule(["J1", "J2", "J3", "J4", "J5"])

    job_shop_data = {
        "A": [("M1", 4), ("M3", 5), ("M2", 3)],
        "B": [("M2", 3), ("M1", 4), ("M3", 6)],
        "C": [("M3", 5), ("M2", 2), ("M1", 4)],
        "D": [("M1", 2), ("M2", 6), ("M3", 3)],
    }
    job_shop_makespan, job_shop_schedule = solve_job_shop(job_shop_data)
    c_completion = int(job_shop_schedule[(job_shop_schedule["job"] == "C") & (job_shop_schedule["task"] == 3)]["end"].iloc[0])

    print("\nQUESTION 1")
    print("Johnson sequence:", johnson_sequence)
    print("Flow shop schedule:", flow_schedule)
    print("Johnson makespan:", flow_makespan)
    print("Original-order makespan:", original_makespan)
    solver_name = "OR-Tools CP-SAT" if cp_model is not None else "Pyomo + HiGHS"
    print(f"Job shop makespan ({solver_name}):", job_shop_makespan)
    print("Job C completion time in the optimal job shop schedule:", c_completion)
    print(job_shop_schedule.to_string(index=False))


def question_2_maximum_coverage():
    """Maximum coverage solved as a binary Pyomo model."""
    bases = ["A", "B", "C", "D", "E", "F"]
    districts = [1, 2, 3, 4, 5, 6]
    costs = {"A": 14, "B": 11, "C": 13, "D": 10, "E": 12, "F": 9}
    population = {1: 9000, 2: 12000, 3: 14000, 4: 10000, 5: 11000, 6: 8000}
    coverage = {
        "A": [1, 2, 4], "B": [1, 3], "C": [2, 3, 5],
        "D": [4, 5], "E": [2, 5, 6], "F": [3, 4, 6],
    }

    def build_model(require_district_6=False, forbid_bf=False):
        model = ConcreteModel()
        model.B = Set(initialize=bases)
        model.D = Set(initialize=districts)
        model.x = Var(model.B, domain=Binary)
        model.y = Var(model.D, domain=Binary)

        model.objective = Objective(
            expr=sum(population[d] * model.y[d] for d in model.D),
            sense=maximize,
        )
        model.budget = Constraint(expr=sum(costs[b] * model.x[b] for b in model.B) <= 31)
        model.limit = Constraint(expr=sum(model.x[b] for b in model.B) <= 3)
        model.cover = Constraint(model.D, rule=lambda m, d: m.y[d] <= sum(m.x[b] for b in m.B if d in coverage[b]))

        if require_district_6:
            model.backup_6 = Constraint(expr=sum(model.x[b] for b in model.B if 6 in coverage[b]) >= 1)
        if forbid_bf:
            model.no_bf = Constraint(expr=model.x["B"] + model.x["F"] <= 1)
        return model

    baseline = build_model()
    SOLVER.solve(baseline)
    revised = build_model(require_district_6=True, forbid_bf=True)
    SOLVER.solve(revised)

    print("\nQUESTION 2")
    print("Baseline selected bases:", [b for b in baseline.B if value(baseline.x[b]) > 0.5])
    print("Baseline covered districts:", [d for d in baseline.D if value(baseline.y[d]) > 0.5])
    print("Baseline covered population:", value(baseline.objective))
    print("Revised selected bases:", [b for b in revised.B if value(revised.x[b]) > 0.5])
    print("Revised covered districts:", [d for d in revised.D if value(revised.y[d]) > 0.5])
    print("Revised covered population:", value(revised.objective))


def run_helpdesk_simulation(arrival_rate_per_hour: float, mean_service_minutes: float, advisers: int, run_minutes: int, seed: int, target_wait: float):
    """Simple FCFS help-desk model in the same style as the SimPy teaching examples."""
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


def question_3_simpy():
    """Queueing simulation using SimPy."""
    print("\nQUESTION 3")
    baseline = run_helpdesk_simulation(10, 7, 2, 360, 24, 8)
    print("Baseline with 2 advisers:", baseline)
    for advisers in (2, 3, 4):
        result = run_helpdesk_simulation(15, 7, advisers, 360, 24, 8)
        print(f"Peak scenario with {advisers} advisers:", result)


def question_4_forecasting():
    """Forecasting following the worksheet-style decomposition steps."""
    data = [420, 500, 470, 560, 450, 536, 500, 600, 485, 575, 535, 645, 522, 618, 572, 694]
    tables = build_forecasting_tables(data, validation_start=13, future_periods=[17, 18, 19, 20])
    export_forecasting_workbook(WORKBOOK_PATH, tables)

    summary = tables["summary"]
    validation = tables["validation"]
    future = tables["future"]

    print("\nQUESTION 4")
    print("Seasonal indices:")
    print(pd.DataFrame({"quarter": [1, 2, 3, 4], "additive": [summary["additive_indices"][q] for q in [1, 2, 3, 4]], "multiplicative": [summary["multiplicative_indices"][q] for q in [1, 2, 3, 4]]}).round(4).to_string(index=False))
    print(f"Trend line: T_hat = {summary['trend_intercept']:.2f} + {summary['trend_slope']:.2f}t")
    print("Validation table:")
    print(validation[["t", "actual", "add_forecast", "mult_forecast", "add_abs_error", "mult_abs_error"]].round(4).to_string(index=False))
    print("Better model:", summary["better_model"])
    print("2023 forecasts:")
    print(future[["t", "quarter", "add_forecast", "mult_forecast"]].round(4).to_string(index=False))
    print("Workbook written to:", Path("output") / WORKBOOK_PATH.name)


def question_5_lp():
    """Linear programme solved in Pyomo, including the follow-on checks from the paper."""

    def build_model(share_constraint=False, extra_hours=False):
        model = ConcreteModel()
        model.casings = Var(domain=NonNegativeReals)
        model.inserts = Var(domain=NonNegativeReals)
        if extra_hours:
            model.extra_assembly = Var(domain=NonNegativeReals, bounds=(0, 12))
            model.objective = Objective(
                expr=40 * model.casings + 34 * model.inserts - 3 * model.extra_assembly,
                sense=maximize,
            )
            model.assembly = Constraint(expr=model.casings + 3 * model.inserts <= 90 + model.extra_assembly)
        else:
            model.objective = Objective(expr=40 * model.casings + 34 * model.inserts, sense=maximize)
            model.assembly = Constraint(expr=model.casings + 3 * model.inserts <= 90)

        model.moulding = Constraint(expr=4 * model.casings + 2 * model.inserts <= 100)
        model.market = Constraint(expr=model.inserts <= 24)

        if share_constraint:
            model.share = Constraint(expr=model.inserts >= 0.25 * (model.casings + model.inserts))
        return model

    model = build_model()
    SOLVER.solve(model)
    revised_share = build_model(share_constraint=True)
    SOLVER.solve(revised_share)
    extra_hours_model = build_model(extra_hours=True)
    SOLVER.solve(extra_hours_model)

    print("\nQUESTION 5")
    print("Casings =", value(model.casings))
    print("Inserts =", value(model.inserts))
    print("Maximum contribution =", value(model.objective))
    print("With 25% inserts share, casings =", value(revised_share.casings))
    print("With 25% inserts share, inserts =", value(revised_share.inserts))
    print("Revised contribution =", value(revised_share.objective))
    print("With optional extra assembly, casings =", value(extra_hours_model.casings))
    print("With optional extra assembly, inserts =", value(extra_hours_model.inserts))
    print("Extra hours purchased =", value(extra_hours_model.extra_assembly))
    print("Net contribution with extra hours =", value(extra_hours_model.objective))


def question_6_transportation():
    """Transportation model solved in Pyomo."""
    warehouses = ["W1", "W2", "W3"]
    stores = ["S1", "S2", "S3", "S4"]
    supply = {"W1": 80, "W2": 100, "W3": 90}
    demand = {"S1": 70, "S2": 60, "S3": 80, "S4": 60}
    costs = {
        ("W1", "S1"): 6, ("W1", "S2"): 8, ("W1", "S3"): 10, ("W1", "S4"): 7,
        ("W2", "S1"): 9, ("W2", "S2"): 5, ("W2", "S3"): 7, ("W2", "S4"): 6,
        ("W3", "S1"): 4, ("W3", "S2"): 7, ("W3", "S3"): 6, ("W3", "S4"): 8,
    }

    def build_model(block_w2_s2=False, force_w1_s4_minimum=False):
        model = ConcreteModel()
        model.I = Set(initialize=warehouses)
        model.J = Set(initialize=stores)
        model.x = Var(model.I, model.J, domain=NonNegativeReals)

        model.objective = Objective(
            expr=sum(costs[i, j] * model.x[i, j] for i in model.I for j in model.J),
            sense=minimize,
        )
        model.supply = Constraint(model.I, rule=lambda m, i: sum(m.x[i, j] for j in m.J) == supply[i])
        model.demand = Constraint(model.J, rule=lambda m, j: sum(m.x[i, j] for i in m.I) == demand[j])

        if block_w2_s2:
            model.block_route = Constraint(expr=model.x["W2", "S2"] == 0)
        if force_w1_s4_minimum:
            model.min_route = Constraint(expr=model.x["W1", "S4"] >= 20)
        return model

    baseline = build_model()
    SOLVER.solve(baseline)
    modified = build_model(block_w2_s2=True, force_w1_s4_minimum=True)
    SOLVER.solve(modified)

    def non_zero_shipments(model):
        rows = []
        for i in model.I:
            for j in model.J:
                shipped = value(model.x[i, j])
                if shipped > 1e-6:
                    rows.append((i, j, shipped))
        return rows

    print("\nQUESTION 6")
    print("Baseline cost:", value(baseline.objective))
    print("Baseline shipments:", non_zero_shipments(baseline))
    print("Modified cost:", value(modified.objective))
    print("Modified shipments:", non_zero_shipments(modified))


def main():
    print("Practice Paper B verification script")
    print("Pyomo solver:", SOLVER)
    question_1_scheduling()
    question_2_maximum_coverage()
    question_3_simpy()
    question_4_forecasting()
    question_5_lp()
    question_6_transportation()


if __name__ == "__main__":
    main()
