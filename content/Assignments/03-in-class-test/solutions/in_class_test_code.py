"""Worked coded solutions for the 5CM522 May 2026 in-class test.

This version is intended to be easy to run in Google Colab as well as locally.

Colab quick start:
1. Upload this file and `worked_solution_snippets.py` to the Colab session.
2. Run:
       !pip install pyomo simpy ortools openpyxl highspy
3. Then run:
       import in_class_test_code as exam
       results = exam.run_all_solutions()
       exam.print_all_solutions(results)

If you want the forecasting workbook from Question 5:
       results = exam.run_all_solutions(export_workbook=True)

The code is organised by question, and each question returns plain Python data
or pandas DataFrames so it can be inspected directly in a notebook.
"""

from __future__ import annotations

import random
from functools import lru_cache
from pathlib import Path

import importlib

try:
    import numpy as np
    import pandas as pd
    import simpy
    from pyomo.environ import (
        Binary,
        ConcreteModel,
        Constraint,
        ConstraintList,
        NonNegativeIntegers,
        NonNegativeReals,
        Objective,
        Set,
        SolverFactory,
        Var,
        maximize,
        minimize,
        value,
    )
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        f"Missing package '{exc.name}'. In Google Colab run:\n"
        "!pip install pyomo simpy ortools openpyxl highspy"
    ) from exc


def load_cp_sat():
    """Return OR-Tools' CP-SAT module, or None where OR-Tools is unavailable.

    OR-Tools has no WebAssembly build, so in the browser (the course website) the job shop
    in Question 6 is solved with an equivalent Pyomo + HiGHS model instead. It returns the
    same makespan, status and schedule as CP-SAT (see `solve_job_shop_milp`).
    """
    try:
        return importlib.import_module("ortools.sat.python.cp_model")
    except ImportError:
        return None


cp_model = load_cp_sat()


COLAB_INSTALL_COMMAND = "!pip install pyomo simpy ortools openpyxl highspy"
# Generated workbooks go to an output/ subfolder next to this file (or the current folder in
# Colab), so the published answer workbook is never overwritten.
DEFAULT_WORKBOOK_PATH = (
    Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
) / "output" / "in_class_test_forecasting.xlsx"

Q1_CONTINUOUS_DOMAIN = NonNegativeReals
Q1_INTEGER_DOMAIN = NonNegativeIntegers

Q2_SITES = ["A", "B", "C", "D", "E", "F"]
Q2_DISTRICTS = [1, 2, 3, 4, 5, 6]
Q2_COSTS = {"A": 16, "B": 11, "C": 15, "D": 14, "E": 13, "F": 10}
Q2_COVERAGE = {
    "A": [1, 2, 4],
    "B": [1, 3],
    "C": [2, 3, 5],
    "D": [4, 5, 6],
    "E": [2, 5, 6],
    "F": [3, 4, 6],
}

Q3_DEPOTS = ["P1", "P2", "P3"]
Q3_HUBS = ["H1", "H2"]
Q3_CLINICS = ["C1", "C2", "C3", "C4"]
Q3_SUPPLY = {"P1": 100, "P2": 120, "P3": 80}
Q3_DEMAND = {"C1": 70, "C2": 60, "C3": 80, "C4": 50}
Q3_DEPOT_TO_HUB = {
    ("P1", "H1"): 4,
    ("P1", "H2"): 6,
    ("P2", "H1"): 5,
    ("P2", "H2"): 3,
    ("P3", "H1"): 6,
    ("P3", "H2"): 4,
}
Q3_HUB_TO_CLINIC = {
    ("H1", "C1"): 4,
    ("H1", "C2"): 6,
    ("H1", "C3"): 7,
    ("H1", "C4"): 5,
    ("H2", "C1"): 5,
    ("H2", "C2"): 4,
    ("H2", "C3"): 3,
    ("H2", "C4"): 6,
}

Q5_DATA = [380, 505, 455, 590, 410, 550, 500, 645, 445, 600, 540, 705, 490, 660, 590, 775]

Q6_FLOW_SHOP_JOBS = {"J1": (8, 4), "J2": (3, 9), "J3": (6, 5), "J4": (7, 2), "J5": (4, 6)}
Q6_JOB_SHOP_DATA = {
    "A": [("M1", 3), ("M3", 5), ("M2", 2)],
    "B": [("M2", 4), ("M1", 2), ("M3", 6)],
    "C": [("M3", 3), ("M2", 4), ("M1", 3)],
    "D": [("M1", 2), ("M2", 6), ("M3", 4)],
}


@lru_cache(maxsize=1)
def get_solver():
    """Return an available Pyomo solver.

    In Colab, `highspy` usually makes the HiGHS solver available.
    """
    for name in ("appsi_highs", "highs"):
        solver = SolverFactory(name)
        if solver.available(False):
            return solver
    raise RuntimeError(
        "No suitable Pyomo solver is available. In Google Colab run:\n"
        "!pip install pyomo highspy"
    )


def solve_pyomo_model(model):
    """Solve a Pyomo model using the cached solver."""
    get_solver().solve(model)
    return model


def rounded_dict(data, digits=4):
    """Round numeric values inside a simple dictionary for cleaner notebook output."""
    rounded = {}
    for key, item in data.items():
        if isinstance(item, float):
            rounded[key] = round(item, digits)
        else:
            rounded[key] = item
    return rounded


def dataframe_to_records(frame, digits=4):
    """Convert a DataFrame to rounded records for JSON-style display."""
    return frame.round(digits).to_dict(orient="records")


def build_q1_model(domain, printing_hours=84, finishing_hours=60, require_premium_share=False):
    """Build the Riverside Signs production model."""
    model = ConcreteModel()
    model.standard = Var(domain=domain)
    model.premium = Var(domain=domain)
    model.objective = Objective(expr=42 * model.standard + 36 * model.premium, sense=maximize)
    model.printing = Constraint(expr=4 * model.standard + 2 * model.premium <= printing_hours)
    model.finishing = Constraint(expr=2 * model.standard + 3 * model.premium <= finishing_hours)
    model.market = Constraint(expr=model.premium <= 18)
    if require_premium_share:
        model.premium_share = Constraint(expr=model.premium >= 0.30 * (model.standard + model.premium))
    return model


def solve_q1_variant(domain):
    """Solve the Q1 model for one domain choice: continuous or integer."""
    baseline = solve_pyomo_model(build_q1_model(domain))
    plus_printing = solve_pyomo_model(build_q1_model(domain, printing_hours=90))
    plus_finishing = solve_pyomo_model(build_q1_model(domain, finishing_hours=66))
    premium_share = solve_pyomo_model(build_q1_model(domain, require_premium_share=True))

    standard = value(baseline.standard)
    premium = value(baseline.premium)
    contribution = value(baseline.objective)

    return rounded_dict(
        {
            "baseline_standard": standard,
            "baseline_premium": premium,
            "baseline_contribution": contribution,
            "printing_slack": 84 - (4 * standard + 2 * premium),
            "finishing_slack": 60 - (2 * standard + 3 * premium),
            "market_slack": 18 - premium,
            "plus_6_printing_contribution": value(plus_printing.objective),
            "plus_6_finishing_contribution": value(plus_finishing.objective),
            "value_per_printing_hour": (value(plus_printing.objective) - contribution) / 6,
            "value_per_finishing_hour": (value(plus_finishing.objective) - contribution) / 6,
            "premium_share_standard": value(premium_share.standard),
            "premium_share_premium": value(premium_share.premium),
            "premium_share_contribution": value(premium_share.objective),
        }
    )


def question_1_results():
    """Return the continuous and integer answers for Question 1."""
    return {
        "continuous": solve_q1_variant(Q1_CONTINUOUS_DOMAIN),
        "integer": solve_q1_variant(Q1_INTEGER_DOMAIN),
    }


def build_q2_model(with_backup=False, forbid_bf=False):
    """Build the drone site set-covering model."""
    model = ConcreteModel()
    model.sites = Set(initialize=Q2_SITES)
    model.districts = Set(initialize=Q2_DISTRICTS)
    model.open = Var(model.sites, domain=Binary)
    model.objective = Objective(
        expr=sum(Q2_COSTS[site] * model.open[site] for site in model.sites),
        sense=minimize,
    )
    model.cover = Constraint(
        model.districts,
        rule=lambda m, district: sum(m.open[site] for site in m.sites if district in Q2_COVERAGE[site]) >= 1,
    )
    if with_backup:
        model.backup_for_6 = Constraint(
            expr=sum(model.open[site] for site in model.sites if 6 in Q2_COVERAGE[site]) >= 2
        )
    if forbid_bf:
        model.no_bf = Constraint(expr=model.open["B"] + model.open["F"] <= 1)
    return model


def selected_sites(model):
    """Return the sites selected in a binary model."""
    return [site for site in Q2_SITES if value(model.open[site]) > 0.5]


def coverage_by_district(sites):
    """Show which chosen sites cover each district."""
    return {district: [site for site in sites if district in Q2_COVERAGE[site]] for district in Q2_DISTRICTS}


def question_2_results():
    """Return the baseline and revised Q2 solutions."""
    baseline = solve_pyomo_model(build_q2_model())
    revised = solve_pyomo_model(build_q2_model(with_backup=True, forbid_bf=True))

    baseline_sites = selected_sites(baseline)
    revised_sites = selected_sites(revised)

    return {
        "baseline_sites": baseline_sites,
        "baseline_cost": round(value(baseline.objective), 4),
        "baseline_coverage": coverage_by_district(baseline_sites),
        "revised_sites": revised_sites,
        "revised_cost": round(value(revised.objective), 4),
        "revised_coverage": coverage_by_district(revised_sites),
    }


def build_q3_model(h1_cap=None, h1_c2_min=None, allow_direct_c4=False):
    """Build the PolarAid transhipment model."""
    model = ConcreteModel()
    model.depots = Set(initialize=Q3_DEPOTS)
    model.hubs = Set(initialize=Q3_HUBS)
    model.clinics = Set(initialize=Q3_CLINICS)
    model.inflow = Var(model.depots, model.hubs, domain=NonNegativeReals)
    model.outflow = Var(model.hubs, model.clinics, domain=NonNegativeReals)

    objective = sum(Q3_DEPOT_TO_HUB[d, h] * model.inflow[d, h] for d in model.depots for h in model.hubs)
    objective += sum(Q3_HUB_TO_CLINIC[h, c] * model.outflow[h, c] for h in model.hubs for c in model.clinics)

    if allow_direct_c4:
        model.direct_p3_c4 = Var(domain=NonNegativeReals, bounds=(0, 20))
        objective += 9 * model.direct_p3_c4

    model.objective = Objective(expr=objective, sense=minimize)
    model.supply = Constraint(
        model.depots,
        rule=lambda m, depot: sum(m.inflow[depot, hub] for hub in m.hubs) <= Q3_SUPPLY[depot],
    )
    # If the emergency arc is allowed, it covers part of clinic C4's existing
    # 50-unit demand rather than creating a new requirement.
    model.demand = Constraint(
        model.clinics,
        rule=lambda m, clinic: sum(m.outflow[hub, clinic] for hub in m.hubs)
        + (m.direct_p3_c4 if allow_direct_c4 and clinic == "C4" else 0)
        == Q3_DEMAND[clinic],
    )
    model.balance = Constraint(
        model.hubs,
        rule=lambda m, hub: sum(m.inflow[depot, hub] for depot in m.depots)
        == sum(m.outflow[hub, clinic] for clinic in m.clinics),
    )

    if h1_cap is not None:
        model.h1_capacity = Constraint(expr=sum(model.outflow["H1", clinic] for clinic in model.clinics) <= h1_cap)
    if h1_c2_min is not None:
        model.h1_c2_minimum = Constraint(expr=model.outflow["H1", "C2"] >= h1_c2_min)
    if allow_direct_c4:
        # Direct shipments use part of P3's original 80-unit supply.
        model.p3_total_supply = Constraint(
            expr=sum(model.inflow["P3", hub] for hub in model.hubs) + model.direct_p3_c4 <= Q3_SUPPLY["P3"]
        )
    return model


def q3_non_zero_flows(model):
    """Extract only the positive flows for compact reporting."""
    rows = []
    for depot in model.depots:
        for hub in model.hubs:
            flow = value(model.inflow[depot, hub])
            if flow > 1e-6:
                rows.append(("Depot to Hub", depot, hub, round(flow, 4)))
    for hub in model.hubs:
        for clinic in model.clinics:
            flow = value(model.outflow[hub, clinic])
            if flow > 1e-6:
                rows.append(("Hub to Clinic", hub, clinic, round(flow, 4)))
    return rows


def question_3_results():
    """Return baseline, disrupted, and emergency-route Q3 results."""
    baseline = solve_pyomo_model(build_q3_model())
    disrupted = solve_pyomo_model(build_q3_model(h1_cap=130, h1_c2_min=30))
    emergency = solve_pyomo_model(build_q3_model(h1_cap=130, h1_c2_min=30, allow_direct_c4=True))

    return {
        "baseline_cost": round(value(baseline.objective), 4),
        "baseline_flows": q3_non_zero_flows(baseline),
        "revised_cost": round(value(disrupted.objective), 4),
        "revised_flows": q3_non_zero_flows(disrupted),
        "emergency_cost": round(value(emergency.objective), 4),
        "emergency_flows": q3_non_zero_flows(emergency),
        "direct_p3_c4": round(value(emergency.direct_p3_c4), 4),
    }


def run_it_helpdesk(arrival_rate_per_hour, mean_service_minutes, technicians, run_minutes, seed, target_wait):
    """Simulate the baseline helpdesk with one exponential service distribution."""
    rng = random.Random(seed)
    waits = []

    def student(env, desk):
        arrival_time = env.now
        with desk.request() as request:
            yield request
            waits.append(env.now - arrival_time)
            service_time = rng.expovariate(1.0 / mean_service_minutes)
            yield env.timeout(service_time)

    def arrivals(env, desk):
        while True:
            interarrival = rng.expovariate(arrival_rate_per_hour / 60.0)
            yield env.timeout(interarrival)
            if env.now > run_minutes:
                break
            env.process(student(env, desk))

    env = simpy.Environment()
    desk = simpy.Resource(env, capacity=technicians)
    env.process(arrivals(env, desk))
    env.run(until=run_minutes + 10000)

    served = len(waits)
    return rounded_dict(
        {
            "served": served,
            "avg_wait": sum(waits) / served if served else 0.0,
            "max_wait": max(waits) if served else 0.0,
            "pct_under_target": 100 * sum(wait < target_wait for wait in waits) / served if served else 0.0,
        }
    )


def run_mixed_service_helpdesk(
    arrival_rate_per_hour,
    technicians,
    run_minutes,
    seed,
    target_wait,
    complex_share=0.25,
    standard_mean_minutes=6.0,
    complex_mean_minutes=14.0,
):
    """Simulate the mixed-service helpdesk used in Question 4(d)."""
    rng = random.Random(seed)
    waits = []
    complex_cases = 0

    def student(env, desk, is_complex):
        nonlocal complex_cases
        arrival_time = env.now
        with desk.request() as request:
            yield request
            waits.append(env.now - arrival_time)
            if is_complex:
                complex_cases += 1
            mean_service = complex_mean_minutes if is_complex else standard_mean_minutes
            service_time = rng.expovariate(1.0 / mean_service)
            yield env.timeout(service_time)

    def arrivals(env, desk):
        while True:
            interarrival = rng.expovariate(arrival_rate_per_hour / 60.0)
            yield env.timeout(interarrival)
            if env.now > run_minutes:
                break
            env.process(student(env, desk, rng.random() < complex_share))

    env = simpy.Environment()
    desk = simpy.Resource(env, capacity=technicians)
    env.process(arrivals(env, desk))
    env.run(until=run_minutes + 10000)

    served = len(waits)
    return rounded_dict(
        {
            "served": served,
            "avg_wait": sum(waits) / served if served else 0.0,
            "max_wait": max(waits) if served else 0.0,
            "pct_under_target": 100 * sum(wait < target_wait for wait in waits) / served if served else 0.0,
            "complex_cases": complex_cases,
        }
    )


def question_4_results():
    """Return the baseline, busy-period, and mixed-service simulation results."""
    baseline = run_it_helpdesk(9, 8, 2, 420, 42, 10)
    busy = {technicians: run_it_helpdesk(13, 8, technicians, 420, 42, 10) for technicians in (2, 3, 4)}

    recommended = next(
        technicians for technicians in (2, 3, 4) if busy[technicians]["avg_wait"] < 8
    )
    mixed = run_mixed_service_helpdesk(13, recommended, 420, 42, 10)

    return {
        "baseline": baseline,
        "busy": busy,
        "recommended_technicians": recommended,
        "mixed": mixed,
    }


def build_forecasting_tables(data, validation_start, future_periods):
    """Build the forecasting tables for Question 5.

    The steps follow the same decomposition approach used in class:
    centred moving averages, seasonal indices, a linear trend fitted to the
    CMA values, then validation and future forecasting.
    """
    periods = np.arange(1, len(data) + 1)
    quarters = ((periods - 1) % 4) + 1

    data_frame = pd.DataFrame({"t": periods, "quarter": quarters, "actual": data})

    training = data_frame[data_frame["t"] <= validation_start - 1].copy()
    training_actual = pd.Series(training["actual"].to_list())
    moving_average_4 = training_actual.rolling(4).mean()

    # Display the 4-MA in the central gap used in hand calculations:
    # periods 1-4 are shown at t=2, periods 2-5 at t=3, and so on.
    training["ma4"] = moving_average_4.shift(-2).to_numpy()

    # The centred 4-quarter moving average is then the mean of adjacent 4-MAs,
    # so with 12 training periods it is available only for periods 3 to 10.
    training["cma"] = (training["ma4"].shift(1) + training["ma4"]) / 2

    data_frame["ma4"] = np.nan
    data_frame["cma"] = np.nan
    data_frame.loc[training.index, ["ma4", "cma"]] = training[["ma4", "cma"]].to_numpy()

    cma_rows = training.dropna(subset=["cma"]).copy()
    cma_rows["add_seasonal"] = cma_rows["actual"] - cma_rows["cma"]
    cma_rows["mult_seasonal"] = cma_rows["actual"] / cma_rows["cma"]

    additive_indices = cma_rows.groupby("quarter")["add_seasonal"].mean()
    additive_indices = additive_indices - additive_indices.mean()

    multiplicative_indices = cma_rows.groupby("quarter")["mult_seasonal"].mean()
    multiplicative_indices = multiplicative_indices / multiplicative_indices.mean()

    training["deseasonalised_add"] = training["actual"] - training["quarter"].map(additive_indices)
    training["deseasonalised_mult"] = training["actual"] / training["quarter"].map(multiplicative_indices)

    trend_slope, trend_intercept = np.polyfit(cma_rows["t"], cma_rows["cma"], 1)
    training["trend"] = trend_slope * training["t"] + trend_intercept

    validation = data_frame[data_frame["t"] >= validation_start].copy()
    validation["add_trend"] = trend_slope * validation["t"] + trend_intercept
    validation["mult_trend"] = validation["add_trend"]
    validation["add_forecast"] = validation["add_trend"] + validation["quarter"].map(additive_indices)
    validation["mult_forecast"] = validation["mult_trend"] * validation["quarter"].map(multiplicative_indices)
    validation["add_squared_error"] = (validation["actual"] - validation["add_forecast"]) ** 2
    validation["mult_squared_error"] = (validation["actual"] - validation["mult_forecast"]) ** 2

    future = pd.DataFrame(
        {
            "t": future_periods,
            "quarter": ((np.array(future_periods) - 1) % 4) + 1,
        }
    )
    future["add_trend"] = trend_slope * future["t"] + trend_intercept
    future["mult_trend"] = future["add_trend"]
    future["add_forecast"] = future["add_trend"] + future["quarter"].map(additive_indices)
    future["mult_forecast"] = future["mult_trend"] * future["quarter"].map(multiplicative_indices)

    summary = {
        "additive_indices": additive_indices.to_dict(),
        "multiplicative_indices": multiplicative_indices.to_dict(),
        "trend_slope": float(trend_slope),
        "trend_intercept": float(trend_intercept),
        "mse_additive": float(validation["add_squared_error"].mean()),
        "mse_multiplicative": float(validation["mult_squared_error"].mean()),
        "better_model": "additive"
        if validation["add_squared_error"].mean() <= validation["mult_squared_error"].mean()
        else "multiplicative",
    }

    return {
        "data": data_frame,
        "cma_rows": cma_rows,
        "train": training,
        "validation": validation,
        "future": future,
        "summary": summary,
    }


def export_forecasting_workbook(output_path, tables):
    """Write the Question 5 tables to Excel.

    In Colab the file will appear in the current working directory and can then
    be downloaded from the file panel.
    """
    output_path = Path(output_path)
    summary = tables["summary"]

    summary_frame = pd.DataFrame(
        [
            ("MSE additive", summary["mse_additive"]),
            ("MSE multiplicative", summary["mse_multiplicative"]),
            ("Better model", summary["better_model"]),
        ],
        columns=["Item", "Value"],
    )
    seasonal_frame = pd.DataFrame(
        {
            "quarter": [1, 2, 3, 4],
            "additive_index": [summary["additive_indices"][quarter] for quarter in [1, 2, 3, 4]],
            "multiplicative_index": [summary["multiplicative_indices"][quarter] for quarter in [1, 2, 3, 4]],
        }
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_frame.to_excel(writer, sheet_name="Summary", index=False)
        seasonal_frame.to_excel(writer, sheet_name="Seasonal Indices", index=False)
        tables["data"].to_excel(writer, sheet_name="Data and CMA", index=False)
        tables["cma_rows"].to_excel(writer, sheet_name="Seasonal Variations", index=False)
        tables["train"].to_excel(writer, sheet_name="Trend and Deseasonalised", index=False)
        tables["validation"].to_excel(writer, sheet_name="Validation", index=False)
        tables["future"].to_excel(writer, sheet_name="Future Forecasts", index=False)

    return output_path


def display_path(path):
    """Path relative to this file's folder when possible, so printed output shows no user name."""
    base = DEFAULT_WORKBOOK_PATH.parent.parent
    try:
        return Path(path).resolve().relative_to(base).as_posix()
    except ValueError:
        return Path(path).name


def question_5_results(export_workbook=False, workbook_path=DEFAULT_WORKBOOK_PATH, include_tables=False):
    """Return the decomposition results for Question 5."""
    tables = build_forecasting_tables(Q5_DATA, validation_start=13, future_periods=[17, 18, 19, 20])
    workbook = None
    if export_workbook:
        workbook = export_forecasting_workbook(workbook_path, tables)

    summary = tables["summary"]
    results = {
        "summary": rounded_dict(
            {
                "mse_additive": summary["mse_additive"],
                "mse_multiplicative": summary["mse_multiplicative"],
                "better_model": summary["better_model"],
            }
        ),
        "additive_indices": rounded_dict(summary["additive_indices"]),
        "multiplicative_indices": rounded_dict(summary["multiplicative_indices"]),
        "data_and_cma": dataframe_to_records(tables["data"][["t", "actual", "ma4", "cma"]]),
        "validation": dataframe_to_records(
            tables["validation"][["t", "actual", "add_forecast", "mult_forecast", "add_squared_error", "mult_squared_error"]]
        ),
        "future": dataframe_to_records(tables["future"][["t", "quarter", "add_forecast", "mult_forecast"]]),
        "workbook_path": display_path(workbook) if workbook else None,
    }
    if include_tables:
        results["tables"] = tables
    return results


def johnson_sequence(jobs):
    """Return the Johnson order for a two-machine flow shop."""
    remaining = dict(jobs)
    front = []
    back = []

    while remaining:
        next_job = min(remaining, key=lambda job: min(remaining[job]))
        m1_time, m2_time = remaining.pop(next_job)
        if m1_time <= m2_time:
            front.append(next_job)
        else:
            back.insert(0, next_job)

    return front + back


def flow_shop_schedule(jobs, order):
    """Build a two-machine flow-shop schedule for a chosen order."""
    machine_1_time = 0
    machine_2_time = 0
    rows = []

    for job in order:
        m1_time, m2_time = jobs[job]
        m1_start = machine_1_time
        m1_end = m1_start + m1_time
        machine_1_time = m1_end

        m2_start = max(machine_2_time, m1_end)
        m2_end = m2_start + m2_time
        machine_2_time = m2_end

        rows.append(
            {
                "job": job,
                "m1_start": m1_start,
                "m1_end": m1_end,
                "m2_start": m2_start,
                "m2_end": m2_end,
            }
        )

    return {
        "makespan": machine_2_time,
        "schedule": pd.DataFrame(rows),
    }


SCHEDULE_COLUMNS = ["job", "task", "machine", "duration", "start", "end"]


def solve_job_shop_milp(job_data, due_dates=None, fixed_starts=None):
    """Solve the job shop as a disjunctive MILP with Pyomo + HiGHS (used without OR-Tools).

    Returns (status, makespan, schedule) with the same meaning as the CP-SAT version.
    Several schedules can reach the optimal makespan; to make the answer reproducible each
    operation, taken in job order (A1, A2, ..., B1, ...), gets the earliest start that keeps
    the makespan optimal. For Question 6 this gives the CP-SAT schedule in the written solutions.
    """
    from pyomo.opt import TerminationCondition

    solver = get_solver()
    operations = [(job, k) for job, tasks in job_data.items() for k in range(len(tasks))]
    duration = {(job, k): job_data[job][k][1] for job, k in operations}
    machine = {(job, k): job_data[job][k][0] for job, k in operations}
    horizon = sum(duration.values())
    last = {job: (job, len(tasks) - 1) for job, tasks in job_data.items()}
    pairs = [(a, b) for i, a in enumerate(operations) for b in operations[i + 1:] if machine[a] == machine[b]]

    model = ConcreteModel()
    model.start = Var(operations, domain=NonNegativeReals, bounds=(0, horizon))
    model.first = Var(range(len(pairs)), domain=Binary)  # 1 if the first operation of the pair goes first
    model.makespan = Var(domain=NonNegativeReals, bounds=(0, horizon))
    model.precedence = Constraint(
        [(job, k) for job, k in operations if k > 0],
        rule=lambda m, job, k: m.start[job, k] >= m.start[job, k - 1] + duration[job, k - 1],
    )
    model.a_before_b = Constraint(
        range(len(pairs)),
        rule=lambda m, p: m.start[pairs[p][0]] + duration[pairs[p][0]] <= m.start[pairs[p][1]] + horizon * (1 - m.first[p]),
    )
    model.b_before_a = Constraint(
        range(len(pairs)),
        rule=lambda m, p: m.start[pairs[p][1]] + duration[pairs[p][1]] <= m.start[pairs[p][0]] + horizon * m.first[p],
    )
    model.finish = Constraint(list(job_data), rule=lambda m, job: m.makespan >= m.start[last[job]] + duration[last[job]])
    if fixed_starts:
        model.fixed = Constraint(list(fixed_starts), rule=lambda m, job, k: m.start[job, k] == fixed_starts[job, k])
    if due_dates:
        model.due = Constraint(list(due_dates), rule=lambda m, job: m.start[last[job]] + duration[last[job]] <= due_dates[job])
    model.objective = Objective(expr=model.makespan, sense=minimize)

    result = solver.solve(model, load_solutions=False)
    if result.solver.termination_condition != TerminationCondition.optimal:
        status = "INFEASIBLE" if "infeasible" in str(result.solver.termination_condition).lower() else "UNKNOWN"
        return status, None, pd.DataFrame(columns=SCHEDULE_COLUMNS)
    solver.solve(model)
    best = value(model.makespan)

    model.keep_makespan = Constraint(expr=model.makespan <= best + 1e-6)
    model.objective.deactivate()
    model.earliest = ConstraintList()
    for op in operations:
        model.tie_break = Objective(expr=model.start[op], sense=minimize)
        solver.solve(model)
        model.earliest.add(model.start[op] <= value(model.start[op]) + 1e-6)
        model.del_component(model.tie_break)

    rows = []
    for job, k in operations:
        start = int(round(value(model.start[job, k])))
        rows.append({"job": job, "task": k + 1, "machine": machine[job, k], "duration": duration[job, k],
                     "start": start, "end": start + duration[job, k]})
    schedule = pd.DataFrame(rows, columns=SCHEDULE_COLUMNS).sort_values(["start", "job", "task"]).reset_index(drop=True)
    return "OPTIMAL", int(round(best)), schedule


def solve_job_shop(job_data, due_dates=None, fixed_starts=None, return_status=False):
    """Solve the job-shop scheduling problem with OR-Tools CP-SAT (Pyomo + HiGHS without OR-Tools).

    A fixed start can be used for a dummy blocking task.
    Example: add `{"BLOCK": [("M2", 3)]}` to `job_data` and pass
    `fixed_starts={("BLOCK", 0): 6}` to block M2 from time 6 to 9.
    """
    if cp_model is None:
        status, makespan, schedule = solve_job_shop_milp(job_data, due_dates, fixed_starts)
        result = {"status": status, "makespan": makespan, "schedule": schedule}
        if return_status:
            return result
        if makespan is None:
            raise RuntimeError(f"Job shop model did not solve successfully: {status}")
        return makespan, schedule

    model = cp_model.CpModel()
    machine_names = sorted({machine for tasks in job_data.values() for machine, _ in tasks})
    horizon = sum(duration for tasks in job_data.values() for _, duration in tasks)

    tasks = {}
    machine_intervals = {machine: [] for machine in machine_names}

    for job_name, job_tasks in job_data.items():
        for task_index, (machine_name, duration) in enumerate(job_tasks):
            suffix = f"{job_name}_{task_index}"
            start = model.NewIntVar(0, horizon, f"start_{suffix}")
            end = model.NewIntVar(0, horizon, f"end_{suffix}")
            interval = model.NewIntervalVar(start, duration, end, f"interval_{suffix}")
            tasks[(job_name, task_index)] = {
                "machine": machine_name,
                "duration": duration,
                "start": start,
                "end": end,
            }
            machine_intervals[machine_name].append(interval)

    if fixed_starts:
        for task_key, start_time in fixed_starts.items():
            model.Add(tasks[task_key]["start"] == start_time)

    for intervals in machine_intervals.values():
        model.AddNoOverlap(intervals)

    # Each task in a job must wait for the previous task to finish.
    for job_name, job_tasks in job_data.items():
        for task_index in range(len(job_tasks) - 1):
            model.Add(tasks[(job_name, task_index + 1)]["start"] >= tasks[(job_name, task_index)]["end"])

    if due_dates:
        for job_name, due_date in due_dates.items():
            last_task = len(job_data[job_name]) - 1
            model.Add(tasks[(job_name, last_task)]["end"] <= due_date)

    makespan = model.NewIntVar(0, horizon, "makespan")
    model.AddMaxEquality(makespan, [tasks[(job_name, len(job_tasks) - 1)]["end"] for job_name, job_tasks in job_data.items()])
    model.Minimize(makespan)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 42
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result = {
            "status": solver.StatusName(status),
            "makespan": None,
            "schedule": pd.DataFrame(columns=["job", "task", "machine", "duration", "start", "end"]),
        }
        if return_status:
            return result
        raise RuntimeError(f"Job shop model did not solve successfully: {result['status']}")

    rows = []
    for job_name, job_tasks in job_data.items():
        for task_index, (machine_name, duration) in enumerate(job_tasks):
            task = tasks[(job_name, task_index)]
            rows.append(
                {
                    "job": job_name,
                    "task": task_index + 1,
                    "machine": machine_name,
                    "duration": duration,
                    "start": solver.Value(task["start"]),
                    "end": solver.Value(task["end"]),
                }
            )

    result = {
        "status": solver.StatusName(status),
        "makespan": int(solver.Value(makespan)),
        "schedule": pd.DataFrame(rows).sort_values(["start", "job", "task"]).reset_index(drop=True),
    }
    if return_status:
        return result
    return result["makespan"], result["schedule"]


def question_6_results():
    """Return the flow-shop and job-shop results for Question 6."""
    johnson_order = johnson_sequence(Q6_FLOW_SHOP_JOBS)
    johnson = flow_shop_schedule(Q6_FLOW_SHOP_JOBS, johnson_order)
    original = flow_shop_schedule(Q6_FLOW_SHOP_JOBS, ["J1", "J2", "J3", "J4", "J5"])

    baseline_job_shop = solve_job_shop(Q6_JOB_SHOP_DATA, return_status=True)
    revised_job_shop_data = dict(Q6_JOB_SHOP_DATA)
    revised_job_shop_data["BLOCK"] = [("M2", 3)]
    revised_job_shop = solve_job_shop(
        revised_job_shop_data,
        due_dates={"D": 15},
        fixed_starts={("BLOCK", 0): 6},
        return_status=True,
    )

    return {
        "johnson_sequence": johnson_order,
        "johnson_makespan": johnson["makespan"],
        "johnson_schedule": dataframe_to_records(johnson["schedule"]),
        "original_makespan": original["makespan"],
        "original_schedule": dataframe_to_records(original["schedule"]),
        "job_shop_status": baseline_job_shop["status"].lower(),
        "job_shop_makespan": baseline_job_shop["makespan"],
        "job_shop_schedule": dataframe_to_records(baseline_job_shop["schedule"]),
        "deadline_and_downtime_status": revised_job_shop["status"].lower(),
        "deadline_and_downtime_makespan": revised_job_shop["makespan"],
        "deadline_and_downtime_schedule": dataframe_to_records(revised_job_shop["schedule"]),
    }


def run_all_solutions(export_workbook=False, workbook_path=DEFAULT_WORKBOOK_PATH, include_q5_tables=False):
    """Run the full worked solution pack and return all results."""
    return {
        "q1": question_1_results(),
        "q2": question_2_results(),
        "q3": question_3_results(),
        "q4": question_4_results(),
        "q5": question_5_results(
            export_workbook=export_workbook,
            workbook_path=workbook_path,
            include_tables=include_q5_tables,
        ),
        "q6": question_6_results(),
    }


def print_all_solutions(results):
    """Pretty-print the results from `run_all_solutions()`."""
    print("5CM522 Worked Coded Solutions")
    print("Colab install command:", COLAB_INSTALL_COMMAND)

    for question, result in results.items():
        print(f"\n{question.upper()}")
        print(result)


def main():
    """Run and print the whole solution pack."""
    results = run_all_solutions(export_workbook=True)
    print_all_solutions(results)


if __name__ == "__main__":
    main()
