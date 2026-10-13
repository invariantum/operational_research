"""
Job shop scheduling tutorial answers, solved as a mixed-integer linear program
with Pyomo (runs in the browser, Colab and Anaconda).

Each job is a list of (machine, processing time) in the order the operations must
be done. Minimise the makespan C_max:

  s[j,k] >= s[j,k-1] + p[j,k-1]                    operations of a job in order
  s[j,k] >= s[i,l] + p[i,l] - M (1 - y)            two operations on the same machine
  s[i,l] >= s[j,k] + p[j,k] - M y                  do not overlap (y = 1: (j,k) first)
  C_max  >= s[j,last] + p[j,last]                  makespan covers every job
"""
import matplotlib.pyplot as plt
import pyomo.environ as pyo


def solve_job_shop(jobs, title=""):
    ops = [(j, k) for j, job in enumerate(jobs) for k in range(len(job))]
    mach = {(j, k): jobs[j][k][0] for (j, k) in ops}
    p = {(j, k): jobs[j][k][1] for (j, k) in ops}
    big_m = sum(p.values())  # no schedule is longer than doing everything one after another
    pairs = [(a, b) for a in ops for b in ops if a < b and mach[a] == mach[b]]

    m = pyo.ConcreteModel()
    m.s = pyo.Var(ops, within=pyo.NonNegativeReals)   # start times
    m.y = pyo.Var(pairs, within=pyo.Binary)           # 1 if the first op of the pair goes first
    m.cmax = pyo.Var(within=pyo.NonNegativeReals)
    m.obj = pyo.Objective(expr=m.cmax, sense=pyo.minimize)

    m.order = pyo.ConstraintList()
    for (j, k) in ops:
        if k > 0:
            m.order.add(m.s[j, k] >= m.s[j, k - 1] + p[j, k - 1])
    m.no_overlap = pyo.ConstraintList()
    for (a, b) in pairs:
        m.no_overlap.add(m.s[b] >= m.s[a] + p[a] - big_m * (1 - m.y[a, b]))
        m.no_overlap.add(m.s[a] >= m.s[b] + p[b] - big_m * m.y[a, b])
    m.makespan = pyo.ConstraintList()
    for j, job in enumerate(jobs):
        last = (j, len(job) - 1)
        m.makespan.add(m.cmax >= m.s[last] + p[last])

    pyo.SolverFactory('appsi_highs').solve(m)

    print(f"{title}  optimal makespan = {pyo.value(m.cmax):g}")
    for (j, k) in sorted(ops, key=lambda o: (mach[o], pyo.value(m.s[o]))):
        start = pyo.value(m.s[j, k])
        print(f"  Machine {mach[j, k]}: Job {j} task {k}  start {start:g}  end {start + p[j, k]:g}")

    fig, ax = plt.subplots(figsize=(8, 0.6 * (max(mach.values()) + 2)))
    for (j, k) in ops:
        start = pyo.value(m.s[j, k])
        ax.barh(mach[j, k], p[j, k], left=start, color=f"C{j}", edgecolor="black")
        ax.text(start + p[j, k] / 2, mach[j, k], f"J{j}", ha="center", va="center", fontsize=8)
    ax.set_yticks(sorted(set(mach.values())))
    ax.set_yticklabels([f"Machine {i}" for i in sorted(set(mach.values()))])
    ax.invert_yaxis()
    ax.set_xlabel("Time")
    ax.set_title(f"{title}: makespan {pyo.value(m.cmax):g}")
    plt.show()
    return pyo.value(m.cmax)


# Each job: list of (machine, processing time) in operation order.
# Machines are numbered from 0 (Problems 2 and 3: A/M1 = 0, B/M2 = 1, ...).

# Problem 1  (J0: M0 M1 M2 / J1: M0 M2 M1 / J2: M1 M3 M2)
jobs_1 = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 4), (2, 3), (1, 1)],
    [(1, 2), (3, 3), (2, 2)]
]
solve_job_shop(jobs_1, "Problem 1")

# Problem 2  (machines A, B, C, D = 0, 1, 2, 3)
jobs_2 = [
    [(0, 3), (1, 2), (2, 4), (3, 3)],
    [(1, 5), (0, 3), (3, 2)],
    [(2, 2), (3, 1), (0, 4), (1, 4)],
    [(3, 4), (2, 3), (1, 5)]
]
solve_job_shop(jobs_2, "Problem 2")

# Problem 3  (machines M1..M5 = 0..4)
jobs_3 = [
    [(0, 4), (1, 2), (2, 3), (3, 5), (4, 2)],
    [(2, 2), (3, 1), (1, 3), (4, 4)],
    [(0, 3), (1, 4), (2, 2), (3, 3)]
]
solve_job_shop(jobs_3, "Problem 3")
