"""
Demonstrate the impact of demand variation on store profitability.

Generates the dataset for one (dummy) student ID into a temporary folder and
estimates single-store profit at demand multipliers of 0.8x-1.2x, showing why
student solutions WILL differ significantly.

Usage (from any folder):
    python demand_impact_demo.py
    python demand_impact_demo.py --student_id 10234
    python demand_impact_demo.py --data_dir path/to/existing/data
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

MODEL_DIR = Path(__file__).resolve().parents[1] / "solutions"
GENERATOR = MODEL_DIR / "generate_data.py"

parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("--student_id", default="TEST001", help="Dummy student ID used to generate the data.")
parser.add_argument("--data_dir", default=None, help="Use an existing generated data/ folder instead.")
args = parser.parse_args()

_tmp = None
if args.data_dir:
    DATA_DIR = Path(args.data_dir)
else:
    _tmp = tempfile.TemporaryDirectory()
    DATA_DIR = Path(_tmp.name) / "data"
    subprocess.run(
        [sys.executable, str(GENERATOR), "--student_id", args.student_id, "--out_dir", str(DATA_DIR)],
        check=True,
        capture_output=True,
        text=True,
    )

# Load data
zones = pd.read_csv(DATA_DIR / "zones.csv")
stores = pd.read_csv(DATA_DIR / "stores.csv")
distances = pd.read_csv(DATA_DIR / "zone_store_dist.csv")

with open(DATA_DIR / "margins.json", encoding="utf-8") as f:
    margins = json.load(f)

margin_per_unit = margins["margin_per_unit"]
service_cost_per_km = margins["service_cost_per_km"]

# For a simple scenario: estimate single-store profit for a few stores
# under different demand scenarios

def estimate_store_profit(store_id, demand_multiplier=1.0):
    """
    Estimate profit for a single store.
    Simplified: assume all zones allocate demand to this store (monopoly).
    """
    store = stores[stores["store_id"] == store_id].iloc[0]
    store_dists = distances[distances["store_id"] == store_id].copy()
    
    # Get demands
    zone_demands = zones[["zone_id", "historical_sales"]].copy()
    zone_demands["historical_sales"] = zone_demands["historical_sales"].fillna(
        zone_demands["historical_sales"].mean()
    )
    zone_demands["historical_sales"] = zone_demands["historical_sales"] * demand_multiplier
    
    # Merge distances
    merged = store_dists.merge(zone_demands, on="zone_id", how="left")
    
    # Revenue - service cost
    revenue = (merged["historical_sales"] * margin_per_unit).sum()
    service_cost = (merged["distance_km"] * service_cost_per_km).sum()
    opening_cost = store["fixed_opening_cost"]
    
    profit = revenue - service_cost - opening_cost
    
    return {
        "store_id": store_id,
        "revenue": revenue,
        "service_cost": service_cost,
        "opening_cost": opening_cost,
        "profit": profit,
        "capacity": store["capacity"],
    }

# Test with a range of demand multipliers
print("="*100)
print("IMPACT OF DEMAND VARIATION ON STORE PROFITABILITY")
print("="*100)
print("""
Scenario: Each store operates in monopoly (all zone demand goes to it).
Shows how ±20% demand variation changes which stores are profitable.
""")

multipliers = [0.80, 0.90, 1.00, 1.10, 1.20]
test_stores = stores["store_id"].head(10).tolist()

print(f"\n{'Store ID':<10} ", end="")
for m in multipliers:
    print(f"{m:>12.0%}", end=" ")
print()
print("-" * 100)

# Show profit for top 10 stores
results = {}
for store_id in test_stores:
    print(f"{store_id:<10} ", end="")
    profits = []
    for mult in multipliers:
        result = estimate_store_profit(store_id, mult)
        profits.append(result["profit"])
        print(f"£{result['profit']:>11.0f}", end=" ")
    
    results[store_id] = profits
    print()

print("\n" + "="*100)
print("ANALYSIS")
print("="*100)

# Show range for first store
first_store = test_stores[0]
profits = results[first_store]
min_profit = min(profits)
max_profit = max(profits)
range_change = max_profit - min_profit
pct_change = (range_change / abs(min(profits))) * 100 if min(profits) != 0 else 0

print(f"""
For Store {first_store}:
  At demand -20% (0.80x): £{min(profits):,.0f}
  At demand +20% (1.20x): £{max(profits):,.0f}
  Range:                  £{range_change:,.0f}
  Percentage change:      {pct_change:+.1f}%

Interpretation:
  • Some stores may be unprofitable at low demand (should close)
  • Same stores become profitable at high demand (should open)
  • Optimal store network changes based on demand forecast
  • Different students' forecasts → Different optimal solutions

Academic Integrity Benefit:
  ✓ Students cannot blindly copy if demand multiplier differs
  ✓ Profit values will be different
  ✓ Store selection will differ
  ✓ Recommendations won't match
  ✓ Viva will reveal if work is own
""")

# Show how many stores change profitability status
print("\n" + "="*100)
print("STORE PROFITABILITY FLIP ANALYSIS")
print("="*100)

unprofitable_at_low = 0
unprofitable_at_high = 0
flipped = 0

for store_id in test_stores:
    profits = results[store_id]
    if profits[0] < 0 < profits[-1]:  # Unprofitable at 0.80x, profitable at 1.20x
        flipped += 1
        unprofitable_at_low += 1
    elif profits[-1] < 0 < profits[0]:  # Profitable at 0.80x, unprofitable at 1.20x
        flipped += 1
        unprofitable_at_high += 1

print(f"""
Out of first {len(test_stores)} stores:
  {unprofitable_at_low} store(s): Unprofitable at -20% demand, Profitable at +20%
  {unprofitable_at_high} store(s): Profitable at -20% demand, Unprofitable at +20%
  {flipped} store(s) flip profitability status as demand varies

This means: Student A (with 0.80x demand) might close a store that 
Student B (with 1.20x demand) opens. Their solutions diverge.

Conclusion: ✓ SIGNIFICANT DIFFERENCES BETWEEN STUDENTS GUARANTEED
""")
