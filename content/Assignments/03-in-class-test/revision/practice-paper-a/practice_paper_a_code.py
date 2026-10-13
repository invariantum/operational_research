"""Verification code for 5CM522 Practice Paper A.

This file is deliberately self-contained so it matches the style of the
module examples more closely.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pyomo.environ import Binary, ConcreteModel, Constraint, NonNegativeReals, Objective, Set, SolverFactory, Var, maximize, minimize, value


def get_solver():
    """Return an available Pyomo solver and its name."""
    for name in ("appsi_highs", "highs"):
        solver = SolverFactory(name)
        if solver.available(False):
            return solver, name
    raise RuntimeError("No suitable Pyomo solver is available.")


SOLVER, SOLVER_NAME = get_solver()


def get_output_dir() -> Path:
    """Choose a sensible output directory for scripts and notebooks."""
    if "google.colab" in sys.modules:
        return Path("/content")
    if "__file__" in globals():
        return Path(__file__).resolve().parent
    return Path.cwd()


# Generated files go to an output/ subfolder so the published answer workbook next to
# this script is never overwritten.
WORKBOOK_PATH = get_output_dir() / "output" / "practice_paper_a_forecasting.xlsx"


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


def question_1_lp():
    """Desk and shelving production plan."""
    model = ConcreteModel()
    model.desks = Var(domain=NonNegativeReals)
    model.shelves = Var(domain=NonNegativeReals)

    model.objective = Objective(expr=58 * model.desks + 46 * model.shelves, sense=maximize)
    model.carpentry = Constraint(expr=5 * model.desks + 3 * model.shelves <= 120)
    model.finishing = Constraint(expr=2 * model.desks + 4 * model.shelves <= 96)
    model.minimum_shelves = Constraint(expr=model.shelves >= 8)

    SOLVER.solve(model)

    revised = ConcreteModel()
    revised.desks = Var(domain=NonNegativeReals)
    revised.shelves = Var(domain=NonNegativeReals)
    revised.objective = Objective(expr=58 * revised.desks + 46 * revised.shelves, sense=maximize)
    revised.carpentry = Constraint(expr=5 * revised.desks + 3 * revised.shelves <= 120)
    revised.finishing = Constraint(expr=2 * revised.desks + 4 * revised.shelves <= 96)
    revised.minimum_shelves = Constraint(expr=revised.shelves >= 8)
    revised.share = Constraint(expr=revised.shelves >= 0.30 * (revised.desks + revised.shelves))
    SOLVER.solve(revised)

    print("\nQUESTION 1")
    print("Baseline desks =", value(model.desks))
    print("Baseline shelves =", value(model.shelves))
    print("Baseline contribution =", value(model.objective))
    print("With 30% shelving share, desks =", value(revised.desks))
    print("With 30% shelving share, shelves =", value(revised.shelves))
    print("Revised contribution =", value(revised.objective))


def question_2_milp():
    """Project selection MILP."""
    projects = ["A", "B", "C", "D", "E", "F"]
    cost = {"A": 6, "B": 8, "C": 5, "D": 9, "E": 4, "F": 7}
    benefit = {"A": 14, "B": 17, "C": 11, "D": 20, "E": 9, "F": 15}

    model = ConcreteModel()
    model.P = Set(initialize=projects)
    model.x = Var(model.P, domain=Binary)

    model.objective = Objective(expr=sum(benefit[p] * model.x[p] for p in model.P), sense=maximize)
    model.budget = Constraint(expr=sum(cost[p] * model.x[p] for p in model.P) <= 21)
    model.dependency = Constraint(expr=model.x["D"] <= model.x["B"])
    model.incompatible = Constraint(expr=model.x["A"] + model.x["F"] <= 1)
    model.choice = Constraint(expr=model.x["C"] + model.x["E"] >= 1)

    SOLVER.solve(model)

    chosen = [p for p in model.P if value(model.x[p]) > 0.5]
    print("\nQUESTION 2")
    print("Chosen projects:", chosen)
    print("Total cost:", sum(cost[p] for p in chosen))
    print("Total benefit:", value(model.objective))


def question_3_mst():
    """Minimum spanning tree by Kruskal's rule."""
    edges = [
        ("A", "B", 6), ("A", "C", 4), ("A", "D", 9), ("B", "C", 5),
        ("B", "E", 7), ("C", "D", 6), ("C", "E", 8), ("C", "F", 6),
        ("D", "E", 5), ("D", "F", 7), ("D", "G", 8), ("E", "F", 3),
        ("E", "G", 4), ("F", "G", 5),
    ]
    parent = {}

    def find(node):
        parent.setdefault(node, node)
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(node_a, node_b):
        root_a = find(node_a)
        root_b = find(node_b)
        if root_a != root_b:
            parent[root_b] = root_a

    mst_edges = []
    total_cost = 0
    for start, end, weight in sorted(edges, key=lambda row: row[2]):
        if find(start) != find(end):
            union(start, end)
            mst_edges.append((start, end, weight))
            total_cost += weight

    backup_edge = min([edge for edge in edges if edge not in mst_edges], key=lambda row: row[2])

    print("\nQUESTION 3")
    print("MST edges:", mst_edges)
    print("MST total cost:", total_cost)
    print("Cheapest backup edge:", backup_edge)
    print("Revised network cost:", total_cost + backup_edge[2])


def sample_from_distribution(random_number: float, values: list[int], probabilities: list[float]) -> int:
    """Lookup helper for the weekly Monte Carlo simulation."""
    running_total = 0.0
    for value_choice, probability in zip(values, probabilities):
        running_total += probability
        if random_number <= running_total + 1e-12:
            return value_choice
    return values[-1]


def question_4_simulation():
    """Weekly capacity simulation using the fixed random numbers from the paper."""
    delivery_rn = [0.119, 0.503, 0.512, 0.860, 0.103, 0.223, 0.601, 0.557, 0.783, 0.548, 0.731, 0.768]
    demand_rn = [0.751, 0.587, 0.240, 0.614, 0.111, 0.817, 0.450, 0.815, 0.685, 0.679, 0.210, 0.252]

    deliveries = [
        sample_from_distribution(u, [6, 7, 8, 9, 10], [0.10, 0.20, 0.35, 0.25, 0.10])
        for u in delivery_rn
    ]
    demands = [
        sample_from_distribution(u, [5, 6, 7, 8, 9], [0.15, 0.25, 0.30, 0.20, 0.10])
        for u in demand_rn
    ]

    def run_capacity(capacity: int):
        opening_stock = 0
        rows = []
        total_cost = 0
        for week, (delivered, demanded) in enumerate(zip(deliveries, demands), start=1):
            stock_available = opening_stock + delivered
            sales = min(stock_available, demanded)
            closing_stock = stock_available - sales
            overflow = max(0, closing_stock - capacity)
            cost = 18 * capacity + 30 * overflow
            rows.append((week, opening_stock, delivered, demanded, sales, closing_stock, overflow, cost))
            total_cost += cost
            opening_stock = closing_stock
        return rows, total_cost, total_cost / len(rows)

    print("\nQUESTION 4")
    baseline_rows, total_cost, average_cost = run_capacity(7)
    for row in baseline_rows:
        print(row)
    print("Total cost for capacity 7 =", total_cost)
    print("Average weekly cost for capacity 7 =", average_cost)
    for capacity in (6, 7, 8, 9):
        _, cap_total, cap_average = run_capacity(capacity)
        print(f"Capacity {capacity}: total cost = {cap_total}, average cost = {cap_average}")


def question_5_forecasting():
    """Forecasting workbook in the style used in the tutorials."""
    data = [510, 620, 570, 690, 548, 662, 608, 742, 590, 708, 646, 792, 636, 760, 692, 852]
    tables = build_forecasting_tables(data, validation_start=13, future_periods=[17, 18, 19, 20])
    export_forecasting_workbook(WORKBOOK_PATH, tables)

    summary = tables["summary"]
    validation = tables["validation"]
    future = tables["future"]

    print("\nQUESTION 5")
    print("Seasonal indices:")
    print(pd.DataFrame({"quarter": [1, 2, 3, 4], "additive": [summary["additive_indices"][q] for q in [1, 2, 3, 4]], "multiplicative": [summary["multiplicative_indices"][q] for q in [1, 2, 3, 4]]}).round(4).to_string(index=False))
    print("Validation table:")
    print(validation[["t", "actual", "add_forecast", "mult_forecast", "add_abs_error", "mult_abs_error"]].round(4).to_string(index=False))
    print("Better model:", summary["better_model"])
    print("2024 forecasts:")
    print(future[["t", "quarter", "add_forecast", "mult_forecast"]].round(4).to_string(index=False))
    print("Workbook written to:", Path("output") / WORKBOOK_PATH.name)


def question_6_transshipment():
    """Transhipment model written in the same arc-flow Pyomo style used in class."""
    suppliers = ["D1", "D2", "D3"]
    consumers = ["C1", "C2", "C3", "C4"]
    tranship = ["H1", "H2"]
    edges = [(i, j) for i in suppliers for j in tranship] + [(i, j) for i in tranship for j in consumers]

    supply = {"D1": 100, "D2": 90, "D3": 110}
    demand = {"C1": 60, "C2": 70, "C3": 80, "C4": 75}
    transport_cost = {
        ("D1", "H1"): 5, ("D1", "H2"): 7,
        ("D2", "H1"): 4, ("D2", "H2"): 6,
        ("D3", "H1"): 6, ("D3", "H2"): 3,
        ("H1", "C1"): 4, ("H1", "C2"): 6, ("H1", "C3"): 5, ("H1", "C4"): 7,
        ("H2", "C1"): 6, ("H2", "C2"): 4, ("H2", "C3"): 3, ("H2", "C4"): 5,
    }

    def build_model(h1_capacity: int | None = None, ban_h2_c3: bool = False):
        model = ConcreteModel()
        model.Suppliers = suppliers
        model.Consumers = consumers
        model.Tranship = tranship
        model.Edges = Set(initialize=edges, dimen=2)
        model.x = Var(model.Edges, domain=NonNegativeReals)

        def objective_rule(model):
            return sum(transport_cost[i, j] * model.x[i, j] for (i, j) in model.Edges)

        def supply_constraint_rule(model, i):
            return sum(model.x[i, j] for j in model.Tranship) <= supply[i]

        def demand_constraint_rule(model, j):
            return sum(model.x[i, j] for i in model.Tranship) == demand[j]

        def tranship_constraint_rule(model, v):
            return sum(model.x[i, j] for (i, j) in model.Edges if j == v) - sum(model.x[i, j] for (i, j) in model.Edges if i == v) == 0

        model.objective = Objective(rule=objective_rule, sense=minimize)
        model.supply_constraint = Constraint(model.Suppliers, rule=supply_constraint_rule)
        model.demand_constraint = Constraint(model.Consumers, rule=demand_constraint_rule)
        model.tranship_constraint = Constraint(model.Tranship, rule=tranship_constraint_rule)

        if h1_capacity is not None:
            model.h1_capacity_constraint = Constraint(
                expr=sum(model.x["H1", j] for j in model.Consumers) <= h1_capacity
            )
        if ban_h2_c3:
            model.route_block_constraint = Constraint(expr=model.x["H2", "C3"] == 0)
        return model

    baseline = build_model()
    SOLVER.solve(baseline)
    disrupted = build_model(h1_capacity=130, ban_h2_c3=True)
    SOLVER.solve(disrupted)
    extra_capacity = build_model(h1_capacity=150, ban_h2_c3=True)
    SOLVER.solve(extra_capacity)

    def flow_rows(model):
        rows = []
        for i, j in model.Edges:
            shipped = value(model.x[i, j])
            if shipped > 1e-6:
                arc_type = "Depot to Hub" if i in suppliers else "Hub to Clinic"
                rows.append((arc_type, i, j, shipped))
        return rows

    print("\nQUESTION 6")
    print("Baseline cost:", value(baseline.objective))
    print(flow_rows(baseline))
    print("Disrupted cost:", value(disrupted.objective))
    print(flow_rows(disrupted))
    print("Extra-capacity cost:", value(extra_capacity.objective))
    print(flow_rows(extra_capacity))


def main():
    print("Practice Paper A verification script")
    print("Pyomo solver:", SOLVER_NAME)
    question_1_lp()
    question_2_milp()
    question_3_mst()
    question_4_simulation()
    question_5_forecasting()
    question_6_transshipment()


if __name__ == "__main__":
    main()
