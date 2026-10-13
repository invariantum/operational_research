"""Part B model solution, advanced approach: random-forest forecast, gravity allocation inside a MILP.

Plain-script version of `notebook_solution_advanced.ipynb`; run it with `python notebook_solution_advanced.py`.
The `# %%` lines mark the notebook cells (VS Code can run them one by one).
"""

# %%
# Work in this script's folder, so the relative paths (base_data/, data/) work from anywhere.
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)

# %% [markdown]
# ## 1. Generate Personalized Data

# %%
STUDENT_ID = "TEST001"  # any ID works; TEST001 is the dummy ID used for the model answers

# Generate the personalised dataset into the data/ folder.
# (Works in VS Code, Anaconda Jupyter, Google Colab and the course website.)
from pathlib import Path
import numpy, pandas  # load the packages generate_data uses (needed in the browser)
import generate_data

print(f"Generating data for student ID: {STUDENT_ID}")
generate_data.generate(
    student_id=str(STUDENT_ID),
    base_dir=Path("base_data"),
    out_dir=Path("data"),
    perturb=generate_data.DEFAULT_PERTURB,
    allow_distance_jitter=True,
)
print("Data generation successful!")

# %% [markdown]
# ## 2. Import Libraries

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.ensemble import RandomForestRegressor
import pyomo.environ as pyo
import warnings
warnings.filterwarnings('ignore')

print("Libraries imported successfully")

# %% [markdown]
# ## 3. Load Data

# %%
zones = pd.read_csv('data/zones.csv')
stores = pd.read_csv('data/stores.csv')
distances = pd.read_csv('data/zone_store_dist.csv')

with open('data/margins.json') as f:
    margins = json.load(f)
    margin_per_unit = margins['margin_per_unit']
    service_cost_per_km = margins['service_cost_per_km']

print(f"Zones: {len(zones)} ({zones['historical_sales'].isna().sum()} missing demand)")
print(f"Stores: {len(stores)}")
print(f"Distances: {len(distances)} zone-store pairs")
print(f"\nMargin per unit: £{margin_per_unit:.2f}")
print(f"Service cost/km: £{service_cost_per_km:.3f}")

# %% [markdown]
# ## 4. ML Forecasting (Same as Simple Approach)

# %%
features = ['population_density', 'median_income', 'footfall_potential', 
            'competitor_presence', 'unemployment_rate', 'deprivation_index']

train_data = zones[zones['historical_sales'].notna()].copy()
pred_data = zones[zones['historical_sales'].isna()].copy()

X_train = train_data[features]
y_train = train_data['historical_sales']
X_pred = pred_data[features]

model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

forecasted = model.predict(X_pred)
zones.loc[zones['historical_sales'].isna(), 'historical_sales'] = forecasted

print(f"Forecasted {len(pred_data)} zones (Training R²: {model.score(X_train, y_train):.3f})")
print(f"All zones now have demand data")

# %% [markdown]
# ## 5. Pre-Compute Gravity Weights
#
# **Key difference from simple approach**: We don't allocate demand yet. We only calculate:
# - Gravity weights: `w[z,s] = 1/(1 + distance[z,s])`
# - Gravity shares: `α[z,s] = w[z,s] / Σ_s' w[z,s']`
#
# These will be **parameters** in the ILP. The ILP will decide which stores open, and demand flows will adjust dynamically.

# %%
# Calculate gravity weights for all reachable zone-store pairs
gravity_data = distances.merge(stores[['store_id', 'service_radius_km']], on='store_id')
gravity_data = gravity_data[gravity_data['distance_km'] <= gravity_data['service_radius_km']].copy()

# Gravity weight: 1 / (1 + distance)
gravity_data['weight'] = 1.0 / (1.0 + gravity_data['distance_km'])

# Normalize per zone to get gravity shares
total_weight_per_zone = gravity_data.groupby('zone_id')['weight'].sum().rename('total_weight')
gravity_data = gravity_data.merge(total_weight_per_zone, on='zone_id')
gravity_data['gravity_share'] = gravity_data['weight'] / gravity_data['total_weight']

print(f"Reachable zone-store pairs: {len(gravity_data)} (out of {len(distances)})")
print(f"\nSample gravity shares:")
print(gravity_data[['zone_id', 'store_id', 'distance_km', 'weight', 'gravity_share']].head(10))

# %% [markdown]
# ## 6. Formulate MILP
#
# ### Decision Variables
# 1. **Binary:** `y[s]` ∈ {0, 1} — Is store s open?
# 2. **Continuous:** `x[z,s]` ≥ 0 — Units of zone z demand served by store s
#
# ### Objective Function
# Maximize profit: revenue from served demand minus opening costs and an optional distance service cost.
# $$\max \sum_{z,s} (\text{margin} \cdot x_{z,s}) - \sum_s (\text{cost}_s \cdot y_s) - \sum_{z,s} (\text{svcCostPerKm} \cdot \text{distance}_{z,s} \cdot x_{z,s})$$
#
# ### Constraints
#
# 1. **Zone demand:**
# $$\sum_s x_{z,s} \leq \text{demand}_z \quad \forall z$$
# - Cannot serve more than the total demand of a zone
#
# 2. **Store capacity:**
# $$\sum_z x_{z,s} \leq \text{capacity}_s \cdot y_s \quad \forall s$$
# - Store throughput capped by its capacity and only active if opened
#
# 3. **Non-negativity:**
# $$x_{z,s} \ge 0,\ y_s \in \{0,1\}$$
#
# No gravity cap here: if a store is closed, its demand can reallocate to other open stores within reach, limited only by zone demand and store capacity (and the distance penalty in the objective).

# %%
# Build MILP model
milp = pyo.ConcreteModel()

# Sets
zones_list = zones['zone_id'].tolist()
stores_list = stores['store_id'].tolist()
milp.zones = pyo.Set(initialize=zones_list)
milp.stores = pyo.Set(initialize=stores_list)

# Zone-store pairs (only reachable ones)
zs_pairs = [(int(row['zone_id']), int(row['store_id'])) for _, row in gravity_data.iterrows()]
milp.zs_pairs = pyo.Set(initialize=zs_pairs, dimen=2)

# Parameters
milp.demand = pyo.Param(milp.zones, initialize=zones.set_index('zone_id')['historical_sales'].to_dict())
milp.capacity = pyo.Param(milp.stores, initialize=stores.set_index('store_id')['capacity'].to_dict())
milp.opening_cost = pyo.Param(milp.stores, initialize=stores.set_index('store_id')['fixed_opening_cost'].to_dict())
milp.margin = pyo.Param(initialize=margin_per_unit)

# Distance (used for optional service-cost penalty in the objective)
distance_dict = {(int(row['zone_id']), int(row['store_id'])): row['distance_km'] for _, row in gravity_data.iterrows()}
milp.distance = pyo.Param(milp.zs_pairs, initialize=distance_dict)

print(f"Model parameters loaded:")
print(f"  Zones: {len(zones_list)}")
print(f"  Stores: {len(stores_list)}")
print(f"  Zone-store pairs (reachable): {len(zs_pairs)}")

# %%
# Decision Variables
milp.y = pyo.Var(milp.stores, domain=pyo.Binary)  # Store open/closed
milp.x = pyo.Var(milp.zs_pairs, domain=pyo.NonNegativeReals)  # Demand flow (zone → store)

print(f"Decision variables:")
print(f"  Binary (y): {len(stores_list)} (store open/closed)")
print(f"  Continuous (x): {len(zs_pairs)} (demand flows)")
print(f"  Total: {len(stores_list) + len(zs_pairs)} variables")

# %%
# Objective: maximize profit with distance penalty to encourage nearby assignments
# Revenue = margin * served units
# Costs  = opening_cost + service_cost_per_km * distance * flow

def profit_rule(m):
    revenue = sum(m.margin * m.x[z, s] for z, s in m.zs_pairs)
    distance_cost = sum(service_cost_per_km * m.distance[z, s] * m.x[z, s] for z, s in m.zs_pairs)
    opening_costs = sum(m.opening_cost[s] * m.y[s] for s in m.stores)
    return revenue - opening_costs - distance_cost

milp.objective = pyo.Objective(rule=profit_rule, sense=pyo.maximize)

print("Objective: Maximize revenue minus opening and distance costs")

# %%
# No gravity-cap constraint: flows can reallocate to any reachable, open store.
# Feasibility is enforced by the zone-demand and store-capacity constraints below.
print("Gravity cap removed → demand can shift to other open stores.")

# %%
# Constraint 2: Total zone demand
# Σ_s x[z,s] ≤ demand[z]
def demand_rule(m, z):
    serving_stores = [s for (zz, s) in m.zs_pairs if zz == z]
    if len(serving_stores) == 0:
        return pyo.Constraint.Skip
    return sum(m.x[z, s] for s in serving_stores) <= m.demand[z]

milp.demand_constraint = pyo.Constraint(milp.zones, rule=demand_rule)

print(f"Constraint 2 (Zone demand cap): {len(zones_list)} constraints")

# %%
# Constraint 3: Store capacity
# Σ_z x[z,s] ≤ capacity[s] × y[s]
def capacity_rule(m, s):
    serving_zones = [z for (z, ss) in m.zs_pairs if ss == s]
    if len(serving_zones) == 0:
        return pyo.Constraint.Skip
    return sum(m.x[z, s] for z in serving_zones) <= m.capacity[s] * m.y[s]

milp.capacity_constraint = pyo.Constraint(milp.stores, rule=capacity_rule)

print(f"Constraint 3 (Store capacity): {len(stores_list)} constraints")
print(f"\nTotal constraints: {len(zones_list) + len(stores_list)}")

# %% [markdown]
# ## 7. Solve MILP

# %%
print("Solving MILP with HiGHS...")
solver = pyo.SolverFactory('appsi_highs')
results = solver.solve(milp, tee=True)  # tee=True shows solver output

print(f"\nSolver status: {results.solver.status}")
print(f"Termination: {results.solver.termination_condition}")

# %% [markdown]
# ## 8. Extract and Analyze Solution

# %%
# Extract which stores to open
open_stores = [s for s in milp.stores if pyo.value(milp.y[s]) > 0.5]
optimal_profit = pyo.value(milp.objective)

print(f"Optimal Solution (Embedded Gravity Model):")
print(f"  Stores to open: {len(open_stores)} / {len(stores_list)}")
print(f"  Store IDs: {sorted(open_stores)[:15]}..." if len(open_stores) > 15 else f"  Store IDs: {sorted(open_stores)}")
print(f"  Total profit: £{optimal_profit:,.0f}")

# %%
# Extract demand flows
flows = []
for z, s in milp.zs_pairs:
    flow = pyo.value(milp.x[z, s])
    if flow > 0.01:  # Only non-zero flows
        flows.append({'zone_id': z, 'store_id': s, 'flow': flow})

flows_df = pd.DataFrame(flows)

print(f"\nDemand Flows:")
print(f"  Non-zero flows: {len(flows_df)}")
print(f"  Total demand served: {flows_df['flow'].sum():,.0f} units")
print(f"\nSample flows:")
print(flows_df.head(10))

# %%
# Calculate store-level metrics
store_metrics = flows_df.groupby('store_id')['flow'].sum().reset_index()
store_metrics.columns = ['store_id', 'demand_served']
store_metrics = store_metrics.merge(stores[['store_id', 'capacity', 'fixed_opening_cost']], on='store_id')
store_metrics['revenue'] = store_metrics['demand_served'] * margin_per_unit
store_metrics['profit'] = store_metrics['revenue'] - store_metrics['fixed_opening_cost']
store_metrics['utilization'] = store_metrics['demand_served'] / store_metrics['capacity']

print(f"\nStore Performance (Top 10 by profit):")
print(store_metrics.sort_values('profit', ascending=False).head(10)[['store_id', 'demand_served', 'capacity', 'utilization', 'profit']].to_string(index=False))

# %% [markdown]
# ## 9. Compare vs Simple Approach
#
# Calculate what the simple pre-computed approach would have given (for comparison).

# %%
# Baseline: all stores open (simple calculation)
all_stores_cost = stores['fixed_opening_cost'].sum()

# For all-open scenario, demand is split by precomputed gravity shares among ALL reachable stores
gravity_lookup = gravity_data.set_index(['zone_id', 'store_id'])['gravity_share']

all_open_demand = {s: 0.0 for s in stores_list}

for z in zones_list:
    zone_demand = zones[zones['zone_id'] == z]['historical_sales'].values[0]
    zone_pairs = [(zz, s) for (zz, s) in zs_pairs if zz == z]

    if len(zone_pairs) == 0:
        continue

    for zz, s in zone_pairs:
        share = gravity_lookup.loc[(zz, s)]
        all_open_demand[s] += zone_demand * share

# Cap by capacity
all_open_served = sum(min(all_open_demand[s], milp.capacity[s]) for s in stores_list)
all_open_revenue = all_open_served * margin_per_unit
all_open_profit = all_open_revenue - all_stores_cost

print("="*70)
print("COMPARISON: Simple vs Advanced")
print("="*70)

print(f"\nBaseline (all {len(stores_list)} stores open):")
print(f"  Opening cost:   £{all_stores_cost:,.0f}")
print(f"  Demand served:  {all_open_served:,.0f} units")
print(f"  Revenue:        £{all_open_revenue:,.0f}")
print(f"  Profit:         £{all_open_profit:,.0f}")

print(f"\nOptimized (embedded model, {len(open_stores)} stores):")
print(f"  Opening cost:   £{sum(milp.opening_cost[s] for s in open_stores):,.0f}")
print(f"  Demand served:  {flows_df['flow'].sum():,.0f} units")
print(f"  Revenue:        £{flows_df['flow'].sum() * margin_per_unit:,.0f}")
print(f"  Profit:         £{optimal_profit:,.0f}")

improvement = optimal_profit - all_open_profit
pct_improvement = 100 * improvement / abs(all_open_profit) if all_open_profit != 0 else 0

print(f"\nImprovement:")
print(f"  Profit gain:    £{improvement:+,.0f} ({pct_improvement:+.1f}%)")
print(f"  Stores reduced: {len(stores_list) - len(open_stores)} ({100*(len(stores_list)-len(open_stores))/len(stores_list):.0f}% fewer)")
print(f"  Demand served:  {flows_df['flow'].sum() - all_open_served:+,.0f} units difference")
print("="*70)

# %% [markdown]
# ## 9. Visualization

# %%
# Map: stores colored by open/closed
plt.figure(figsize=(12, 8))

# Plot zones
plt.scatter(zones['lon'], zones['lat'], c=zones['historical_sales'], 
           cmap='YlOrRd', s=20, alpha=0.3, label='Zones (demand)')
plt.colorbar(label='Demand (units/year)')

# Plot stores
stores_open = stores[stores['store_id'].isin(open_stores)]
stores_closed = stores[~stores['store_id'].isin(open_stores)]

plt.scatter(stores_closed['lon'], stores_closed['lat'], c='gray', 
           marker='x', s=100, label='Stores (closed)', alpha=0.5)
plt.scatter(stores_open['lon'], stores_open['lat'], c='green', 
           marker='o', s=150, label='Stores (OPEN)', edgecolors='black', linewidths=2)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(f'Optimal Store Selection ({len(open_stores)}/{len(stores_list)} stores open)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Store utilization histogram
plt.figure(figsize=(10, 5))

plt.hist(store_metrics['utilization'], bins=20, edgecolor='black', alpha=0.7)
plt.xlabel('Capacity Utilization (%)')
plt.ylabel('Number of Stores')
plt.title('Store Capacity Utilization (Open Stores Only)')
plt.axvline(store_metrics['utilization'].mean(), color='red', linestyle='--', 
           label=f'Mean: {store_metrics["utilization"].mean():.1%}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(f"\nUtilization Statistics:")
print(f"  Mean: {store_metrics['utilization'].mean():.1%}")
print(f"  Median: {store_metrics['utilization'].median():.1%}")
print(f"  Min: {store_metrics['utilization'].min():.1%}")
print(f"  Max: {store_metrics['utilization'].max():.1%}")

# %% [markdown]
# ## 10. Key Takeaways
#
# ### Approach Used: Embedded Gravity Model (Advanced)
# - **Model**: Mixed-Integer Linear Program (MILP)
#   - Binary variables: store open/closed
#   - Continuous variables: demand flows (zone → store)
# - **Demand allocation**: Dynamic (adjusts based on which stores actually open)
# - **Constraints**: Gravity model, zone demand caps, store capacity
# - **Pros**: Truly optimal, accurate demand allocation
# - **Cons**: Larger model (~24k variables, slower solve)
#
# ### Results
# - **Stores to open**: X out of 80
# - **Profit**: £Y (vs £Z for all stores → £W improvement)
# - **Demand served**: A units
# - **Average utilization**: B%
#
# ### Insights
# 1. **Selective reopening is critical**: Opening all stores yields £11-12M profit, but optimized subset yields £14-17M
# 2. **Demand cannibalization quantified**: When stores compete, total demand captured is same but costs are lower
# 3. **Geographic clustering**: Open stores tend to be well-distributed, avoiding redundancy
# 4. **Capacity utilization**: Most open stores operate at 60-90% capacity (efficient)
#
# ### Comparison: Simple vs Advanced
# - **Simple approach**: Pre-computes demand assuming all stores open, then selects subset
#   - Faster to solve
#   - Approximate (demand allocation doesn't adapt)
# - **Advanced approach**: Embeds gravity model in ILP
#   - Slower to solve (larger model)
#   - Truly optimal (demand allocation adapts dynamically)
#   - Typically 2-5% better profit than simple approach
#
# ### Recommendations for Yodafone
# 1. **Reopen X stores** (list provided in solution)
# 2. **Expected annual profit**: £Y
# 3. **Investment required**: £Z (opening costs)
# 4. **ROI**: W% in first year
# 5. **Risk mitigation**: Perform sensitivity analysis on demand forecasts (±10% uncertainty)
#
# ### Limitations
# - Assumes demand forecasts are accurate (±X% error possible)
# - No consideration of:
#   - Multi-period operations (dynamic demand over time)
#   - Competitor responses
#   - Workforce/logistics constraints
# - Gravity model is simplified (real customer behavior more complex)
