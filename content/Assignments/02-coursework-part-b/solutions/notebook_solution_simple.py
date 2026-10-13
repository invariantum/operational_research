"""Part B model solution, simple approach: random-forest forecast, fixed demand allocation, binary ILP.

Plain-script version of `notebook_solution_simple.ipynb`; run it with `python notebook_solution_simple.py`.
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
from sklearn.metrics import r2_score, mean_absolute_error
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
print(f"Distances: {len(distances)}")
print(f"\nMargin per unit: £{margin_per_unit:.2f}")
print(f"Service cost/km: £{service_cost_per_km:.3f}")

# %% [markdown]
# ## 4. Exploratory Data Analysis

# %%
print("Zone demand (where available):")
print(zones['historical_sales'].describe())

print("\nStore economics:")
print(stores[['capacity', 'fixed_opening_cost']].describe())

# %% [markdown]
# ## 5. ML Forecasting

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

print(f"Training R²: {model.score(X_train, y_train):.3f}")
print(f"\nFeature importance:")
for feat, imp in sorted(zip(features, model.feature_importances_), key=lambda x: -x[1])[:3]:
    print(f"  {feat}: {imp:.3f}")

# %%
forecasted = model.predict(X_pred)
zones.loc[zones['historical_sales'].isna(), 'historical_sales'] = forecasted

print(f"Forecasted {len(pred_data)} zones")
print(f"No missing values: {zones['historical_sales'].isna().sum() == 0}")

# %% [markdown]
# ## 6. Pre-Compute Demand Allocation (Simple Approach)
#
# **Key assumption:** Calculate demand each store would capture if **all 80 stores were open**, then use ILP to select subset.
#
# **Method:**
# 1. For each zone, find all stores within service radius
# 2. Apply gravity model to split zone demand: `weight = 1/(1+distance)`
# 3. Each store gets `zone_demand × (its_weight / total_weight)`
# 4. Store the allocated demand per store
# 5. ILP decides which stores to open (demand allocation is **fixed**)

# %%
# Pre-compute demand allocation assuming all stores open
store_allocated_demand = {}

for store_id in stores['store_id'].values:
    store_allocated_demand[store_id] = 0.0

# For each zone, split demand among reachable stores
for zone_id in zones['zone_id'].values:
    zone_demand = zones[zones['zone_id'] == zone_id]['historical_sales'].values[0]
    
    # Find stores that can serve this zone
    zone_dists = distances[distances['zone_id'] == zone_id].copy()
    zone_dists = zone_dists.merge(stores[['store_id', 'service_radius_km']], on='store_id')
    zone_dists = zone_dists[zone_dists['distance_km'] <= zone_dists['service_radius_km']]
    
    if len(zone_dists) == 0:
        continue  # Zone not served by any store
    
    # Gravity model: weight inversely proportional to distance
    zone_dists['weight'] = 1.0 / (1.0 + zone_dists['distance_km'])
    total_weight = zone_dists['weight'].sum()
    zone_dists['allocated'] = zone_demand * (zone_dists['weight'] / total_weight)
    
    # Add to each store's total
    for _, row in zone_dists.iterrows():
        store_allocated_demand[row['store_id']] += row['allocated']

# Create dataframe
demand_alloc = pd.DataFrame([
    {'store_id': sid, 'allocated_demand': demand}
    for sid, demand in store_allocated_demand.items()
])

# Merge with store data
demand_alloc = demand_alloc.merge(stores[['store_id', 'capacity', 'fixed_opening_cost']], on='store_id')

# Cap by capacity
demand_alloc['usable_demand'] = demand_alloc[['allocated_demand', 'capacity']].min(axis=1)
demand_alloc['revenue'] = demand_alloc['usable_demand'] * margin_per_unit
demand_alloc['profit_if_opened'] = demand_alloc['revenue'] - demand_alloc['fixed_opening_cost']

print("Pre-computed demand allocation (assuming all stores open):")
print(demand_alloc[['store_id', 'allocated_demand', 'usable_demand', 'profit_if_opened']].head(10))
print(f"\nTotal allocated demand: {demand_alloc['usable_demand'].sum():.0f} units")
print(f"Total zone demand: {zones['historical_sales'].sum():.0f} units")

# %% [markdown]
# ## 7. Formulate Binary ILP
#
# **Decision Variables:**
# - `y[s]` ∈ {0, 1} for each store s (open or closed)
#
# **Objective:**
# $$\text{Maximize} \quad \sum_s (\text{revenue}_s - \text{cost}_s) \cdot y_s$$
#
# where:
# - $\text{revenue}_s = \text{usable_demand}_s \times \text{margin_per_unit}$
# - $\text{cost}_s = \text{fixed_opening_cost}_s$
#
# **Constraints:**
# - None (unconstrained facility location)
# - *(Could add: budget constraint, minimum coverage, etc.)*

# %%
# Build ILP model
model_ilp = pyo.ConcreteModel()

# Sets
store_ids = demand_alloc['store_id'].tolist()
model_ilp.stores = pyo.Set(initialize=store_ids)

# Parameters (profit per store if opened)
profit_dict = demand_alloc.set_index('store_id')['profit_if_opened'].to_dict()
model_ilp.profit_per_store = pyo.Param(model_ilp.stores, initialize=profit_dict)

# Decision variables: binary (open/closed)
model_ilp.y = pyo.Var(model_ilp.stores, domain=pyo.Binary)

# Objective: maximize total profit
def obj_rule(m):
    return sum(m.profit_per_store[s] * m.y[s] for s in m.stores)

model_ilp.objective = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

print("ILP model formulated")
print(f"Variables: {len(store_ids)} binary (store open/closed)")
print(f"Constraints: 0 (unconstrained)")

# %%
# Solve
solver = pyo.SolverFactory('appsi_highs')
results = solver.solve(model_ilp, tee=False)

print(f"Solver status: {results.solver.status}")
print(f"Termination condition: {results.solver.termination_condition}")

# %% [markdown]
# ## 8. Extract Solution

# %%
# Extract which stores to open
open_stores = [s for s in model_ilp.stores if pyo.value(model_ilp.y[s]) > 0.5]
optimal_profit = pyo.value(model_ilp.objective)

print(f"Optimal solution:")
print(f"  Stores to open: {len(open_stores)} / {len(store_ids)}")
print(f"  Store IDs: {sorted(open_stores)[:10]}..." if len(open_stores) > 10 else f"  Store IDs: {sorted(open_stores)}")
print(f"  Total profit: £{optimal_profit:,.0f}")

# Calculate metrics for open stores
open_data = demand_alloc[demand_alloc['store_id'].isin(open_stores)]
print(f"\n  Total opening cost: £{open_data['fixed_opening_cost'].sum():,.0f}")
print(f"  Total revenue: £{open_data['revenue'].sum():,.0f}")
print(f"  Total demand served: {open_data['usable_demand'].sum():,.0f} units")

# %% [markdown]
# ## 9. Compare vs Baseline

# %%
# Baseline: open all stores
all_profit = demand_alloc['profit_if_opened'].sum()
all_cost = demand_alloc['fixed_opening_cost'].sum()
all_revenue = demand_alloc['revenue'].sum()
all_demand = demand_alloc['usable_demand'].sum()

print("="*70)
print("SOLUTION COMPARISON")
print("="*70)

print(f"\nBaseline (all {len(store_ids)} stores):")
print(f"  Opening cost: £{all_cost:,.0f}")
print(f"  Revenue:      £{all_revenue:,.0f}")
print(f"  Profit:       £{all_profit:,.0f}")
print(f"  Demand:       {all_demand:,.0f} units")

print(f"\nOptimized ({len(open_stores)} stores):")
print(f"  Opening cost: £{open_data['fixed_opening_cost'].sum():,.0f}")
print(f"  Revenue:      £{open_data['revenue'].sum():,.0f}")
print(f"  Profit:       £{optimal_profit:,.0f}")
print(f"  Demand:       {open_data['usable_demand'].sum():,.0f} units")

improvement = optimal_profit - all_profit
pct_improvement = 100 * improvement / abs(all_profit) if all_profit != 0 else 0

print(f"\nImprovement:")
print(f"  Profit gain:  £{improvement:+,.0f} ({pct_improvement:+.1f}%)")
print(f"  Stores saved: {len(store_ids) - len(open_stores)} ({100*(len(store_ids)-len(open_stores))/len(store_ids):.0f}%)")
print("="*70)

# %% [markdown]
# ## 10. Sensitivity Analysis

# %%
# Test: what if demand forecasts are off by ±10%?
sensitivity_results = []

for multiplier in [0.9, 0.95, 1.0, 1.05, 1.1]:
    # Adjust demand
    adjusted_alloc = demand_alloc.copy()
    adjusted_alloc['allocated_demand'] *= multiplier
    adjusted_alloc['usable_demand'] = adjusted_alloc[['allocated_demand', 'capacity']].min(axis=1)
    adjusted_alloc['revenue'] = adjusted_alloc['usable_demand'] * margin_per_unit
    adjusted_alloc['profit_if_opened'] = adjusted_alloc['revenue'] - adjusted_alloc['fixed_opening_cost']
    
    # Rebuild model
    test_model = pyo.ConcreteModel()
    test_model.stores = pyo.Set(initialize=store_ids)
    test_model.profit_per_store = pyo.Param(test_model.stores, initialize=adjusted_alloc.set_index('store_id')['profit_if_opened'].to_dict())
    test_model.y = pyo.Var(test_model.stores, domain=pyo.Binary)
    test_model.objective = pyo.Objective(expr=sum(test_model.profit_per_store[s]*test_model.y[s] for s in test_model.stores), sense=pyo.maximize)
    
    solver.solve(test_model, tee=False)
    
    n_open = sum(1 for s in test_model.stores if pyo.value(test_model.y[s]) > 0.5)
    profit = pyo.value(test_model.objective)
    
    sensitivity_results.append({
        'demand_multiplier': multiplier,
        'stores_open': n_open,
        'profit': profit
    })

sens_df = pd.DataFrame(sensitivity_results)
print("\nSensitivity: Demand ±10%")
print(sens_df)

# %%
# Plot sensitivity
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(sens_df['demand_multiplier'], sens_df['stores_open'], marker='o')
plt.xlabel('Demand Multiplier')
plt.ylabel('Stores to Open')
plt.title('Sensitivity: Stores vs Demand')
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(sens_df['demand_multiplier'], sens_df['profit']/1e6, marker='o', color='green')
plt.xlabel('Demand Multiplier')
plt.ylabel('Profit (£M)')
plt.title('Sensitivity: Profit vs Demand')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 10. Key Takeaways
#
# ### Approach Used: Pre-Computed Demand
# - **Assumption**: Demand allocation fixed (calculated assuming all stores open)
# - **Model**: Simple binary ILP (80 variables, 0 constraints)
# - **Pros**: Fast to solve, easy to implement
# - **Cons**: Less accurate (doesn't account for dynamic demand reallocation)
#
# ### Results
# - Opening all stores: £X profit
# - Optimized: Open Y stores → £Z profit
# - Improvement: £W saved
#
# ### Insights
# 1. **ML forecasting critical**: ~35% of zones needed demand prediction
# 2. **Not all stores should open**: Opening all wastes capacity and incurs unnecessary costs
# 3. **Selective reopening**: Only stores with high demand/low cost should open
# 4. **Robust to uncertainty**: ±10% demand variation changes profit by X% but decision is stable
#
# ### Limitations
# - Demand allocation is **approximated** (assumes all stores open during pre-computation)
# - More sophisticated model (embedded gravity) would give truly optimal solution
# - No budget constraints or coverage requirements included
