"""Arc-based Pyomo transhipment solution for Northfield Relief from Practice Paper A."""

from __future__ import annotations

from pyomo.environ import ConcreteModel, Constraint, NonNegativeReals, Objective, Set, SolverFactory, Var, minimize, value


def get_solver():
    for name in ("appsi_highs", "highs"):
        solver = SolverFactory(name)
        if solver.available(False):
            return solver
    raise RuntimeError("No suitable Pyomo solver is available.")


SUPPLIERS = ["D1", "D2", "D3"]
CONSUMERS = ["C1", "C2", "C3", "C4"]
TRANSHIP = ["H1", "H2"]
EDGES = [(i, j) for i in SUPPLIERS for j in TRANSHIP] + [(i, j) for i in TRANSHIP for j in CONSUMERS]

SUPPLY = {"D1": 100, "D2": 90, "D3": 110}
DEMAND = {"C1": 60, "C2": 70, "C3": 80, "C4": 75}
TRANSPORT_COST = {
    ("D1", "H1"): 5, ("D1", "H2"): 7,
    ("D2", "H1"): 4, ("D2", "H2"): 6,
    ("D3", "H1"): 6, ("D3", "H2"): 3,
    ("H1", "C1"): 4, ("H1", "C2"): 6, ("H1", "C3"): 5, ("H1", "C4"): 7,
    ("H2", "C1"): 6, ("H2", "C2"): 4, ("H2", "C3"): 3, ("H2", "C4"): 5,
}


def build_model(h1_capacity: int | None = None, ban_h2_c3: bool = False):
    model = ConcreteModel()
    model.Suppliers = Set(initialize=SUPPLIERS)
    model.Consumers = Set(initialize=CONSUMERS)
    model.Tranship = Set(initialize=TRANSHIP)
    model.Edges = Set(initialize=EDGES, dimen=2)
    model.x = Var(model.Edges, domain=NonNegativeReals)

    def objective_rule(model):
        return sum(TRANSPORT_COST[i, j] * model.x[i, j] for (i, j) in model.Edges)

    def supply_constraint_rule(model, i):
        return sum(model.x[i, j] for j in model.Tranship) <= SUPPLY[i]

    def demand_constraint_rule(model, j):
        return sum(model.x[i, j] for i in model.Tranship) == DEMAND[j]

    def tranship_constraint_rule(model, v):
        return sum(model.x[i, j] for (i, j) in model.Edges if j == v) - sum(model.x[i, j] for (i, j) in model.Edges if i == v) == 0

    model.objective = Objective(rule=objective_rule, sense=minimize)
    model.supply_constraint = Constraint(model.Suppliers, rule=supply_constraint_rule)
    model.demand_constraint = Constraint(model.Consumers, rule=demand_constraint_rule)
    model.tranship_constraint = Constraint(model.Tranship, rule=tranship_constraint_rule)

    if h1_capacity is not None:
        model.h1_capacity_constraint = Constraint(expr=sum(model.x["H1", j] for j in model.Consumers) <= h1_capacity)

    if ban_h2_c3:
        model.route_block_constraint = Constraint(expr=model.x["H2", "C3"] == 0)

    return model


def non_zero_shipments(model):
    rows = []
    for i, j in model.Edges:
        shipped = value(model.x[i, j])
        if shipped > 1e-6:
            rows.append((i, j, shipped))
    return rows


def main():
    solver = get_solver()

    baseline = build_model()
    solver.solve(baseline)
    print("Baseline total cost:", value(baseline.objective))
    print("Baseline non-zero shipments:", non_zero_shipments(baseline))

    disrupted = build_model(h1_capacity=130, ban_h2_c3=True)
    solver.solve(disrupted)
    print("\nDisrupted total cost:", value(disrupted.objective))
    print("Disrupted non-zero shipments:", non_zero_shipments(disrupted))

    extra = build_model(h1_capacity=150, ban_h2_c3=True)
    solver.solve(extra)
    print("\nWith 20 extra units at H1 total cost:", value(extra.objective))
    print("With 20 extra units at H1 non-zero shipments:", non_zero_shipments(extra))
    print("\nSaving from extra capacity:", value(disrupted.objective) - value(extra.objective))


if __name__ == "__main__":
    main()
