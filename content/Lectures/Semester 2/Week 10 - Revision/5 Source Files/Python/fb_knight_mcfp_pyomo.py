"""Pyomo transportation/transhipment solution for F.B. Knight from Week 10 revision."""

from __future__ import annotations

from pyomo.environ import ConcreteModel, Constraint, NonNegativeReals, Objective, Set, SolverFactory, Var, minimize, value


def get_solver():
    for name in ("appsi_highs", "highs"):
        solver = SolverFactory(name)
        if solver.available(False):
            return solver
    raise RuntimeError("No suitable Pyomo solver is available.")


WAREHOUSES = ["A", "B", "C"]
SHOPS = ["X", "Y", "Z"]
SUPPLY = {"A": 10, "B": 10, "C": 10}  # tens of items
DEMAND = {"X": 7, "Y": 8, "Z": 15}    # tens of items
DIRECT_COST = {
    ("A", "X"): 8, ("A", "Y"): 7, ("A", "Z"): 5,
    ("B", "X"): 12, ("B", "Y"): 3, ("B", "Z"): 9,
    ("C", "X"): 10, ("C", "Y"): 11, ("C", "Z"): 7,
}
TRANSHIP = ["D1", "D2"]
WH_TO_D = {
    ("A", "D1"): 4, ("A", "D2"): 5,
    ("B", "D1"): 3, ("B", "D2"): 2,
    ("C", "D1"): 6, ("C", "D2"): 4,
}
D_TO_SHOP = {
    ("D1", "X"): 4, ("D1", "Y"): 5, ("D1", "Z"): 2,
    ("D2", "X"): 2, ("D2", "Y"): 4, ("D2", "Z"): 4,
}


def build_direct_model(with_restrictions: bool = False):
    model = ConcreteModel()
    model.W = Set(initialize=WAREHOUSES)
    model.S = Set(initialize=SHOPS)
    model.x = Var(model.W, model.S, domain=NonNegativeReals)
    model.objective = Objective(expr=sum(DIRECT_COST[w, s] * model.x[w, s] for w in model.W for s in model.S), sense=minimize)
    model.supply = Constraint(model.W, rule=lambda m, w: sum(m.x[w, s] for s in m.S) == SUPPLY[w])
    model.demand = Constraint(model.S, rule=lambda m, s: sum(m.x[w, s] for w in m.W) == DEMAND[s])
    if with_restrictions:
        model.block = Constraint(expr=model.x["B", "Y"] == 0)
        model.min_ay = Constraint(expr=model.x["A", "Y"] >= 0.5)
    return model


def build_transhipment_model(use_d1: bool, use_d2: bool):
    active = [d for d, use in [("D1", use_d1), ("D2", use_d2)] if use]
    model = ConcreteModel()
    model.W = Set(initialize=WAREHOUSES)
    model.D = Set(initialize=active)
    model.S = Set(initialize=SHOPS)
    model.edges = Set(initialize=[(w, d) for w in model.W for d in model.D] + [(d, s) for d in model.D for s in model.S], dimen=2)
    model.x = Var(model.edges, domain=NonNegativeReals)

    def unit_cost(i, j):
        return WH_TO_D.get((i, j), D_TO_SHOP.get((i, j)))

    model.objective = Objective(expr=sum(unit_cost(i, j) * model.x[i, j] for (i, j) in model.edges), sense=minimize)
    model.supply = Constraint(model.W, rule=lambda m, w: sum(m.x[w, d] for d in m.D) == SUPPLY[w])
    model.demand = Constraint(model.S, rule=lambda m, s: sum(m.x[d, s] for d in m.D) == DEMAND[s])
    model.balance = Constraint(model.D, rule=lambda m, d: sum(m.x[w, d] for w in m.W) == sum(m.x[d, s] for s in m.S))
    return model


def show_non_zero(label, model, index_set):
    print(label)
    for idx in index_set:
        if value(model.x[idx]) > 1e-6:
            print(idx, value(model.x[idx]))
    print("Total cost:", value(model.objective))
    print()


def main():
    solver = get_solver()

    baseline = build_direct_model(False)
    solver.solve(baseline)
    show_non_zero("Baseline direct-shipping solution:", baseline, [(w, s) for w in baseline.W for s in baseline.S])

    revised = build_direct_model(True)
    solver.solve(revised)
    show_non_zero("Restricted direct-shipping solution:", revised, [(w, s) for w in revised.W for s in revised.S])

    for use_d1, use_d2, label in [(True, False, "D1 only"), (False, True, "D2 only"), (True, True, "Both D1 and D2")]:
        model = build_transhipment_model(use_d1, use_d2)
        solver.solve(model)
        show_non_zero(f"Transhipment solution using {label}:", model, list(model.edges))


if __name__ == "__main__":
    main()
