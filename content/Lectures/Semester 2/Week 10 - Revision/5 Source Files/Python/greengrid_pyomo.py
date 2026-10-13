"""Pyomo solution for the GreenGrid Energy question from Week 10 revision."""

from __future__ import annotations

from pyomo.environ import Binary, ConcreteModel, Constraint, Objective, Set, SolverFactory, Var, maximize, value


def get_solver():
    for name in ("appsi_highs", "highs"):
        solver = SolverFactory(name)
        if solver.available(False):
            return solver
    raise RuntimeError("No suitable Pyomo solver is available.")


PROJECTS = ["A", "B", "C", "D", "E", "F"]
COST = {"A": 6, "B": 8, "C": 5, "D": 9, "E": 4, "F": 7}
BENEFIT = {"A": 14, "B": 17, "C": 11, "D": 20, "E": 9, "F": 15}


def build_model(exactly_four: bool = False):
    model = ConcreteModel()
    model.P = Set(initialize=PROJECTS)
    model.x = Var(model.P, domain=Binary)
    model.objective = Objective(expr=sum(BENEFIT[p] * model.x[p] for p in model.P), sense=maximize)
    model.budget = Constraint(expr=sum(COST[p] * model.x[p] for p in model.P) <= 21)
    model.dependency = Constraint(expr=model.x["D"] <= model.x["B"])
    model.incompatible = Constraint(expr=model.x["A"] + model.x["F"] <= 1)
    model.choice = Constraint(expr=model.x["C"] + model.x["E"] >= 1)
    if exactly_four:
        model.count = Constraint(expr=sum(model.x[p] for p in model.P) == 4)
    return model


def chosen_projects(model):
    return [p for p in model.P if value(model.x[p]) > 0.5]


def main():
    solver = get_solver()

    baseline = build_model()
    solver.solve(baseline)
    print("Baseline chosen projects:", chosen_projects(baseline))
    print("Baseline total cost:", sum(COST[p] for p in chosen_projects(baseline)))
    print("Baseline total benefit:", value(baseline.objective))

    revised = build_model(exactly_four=True)
    result = solver.solve(revised, load_solutions=False)
    termination = getattr(result.solver, "termination_condition", "unknown")
    print("Exactly-four termination condition:", termination)
    if str(termination).lower() != "optimal":
        print("Exactly-four version is infeasible under the given rules and budget.")


if __name__ == "__main__":
    main()
