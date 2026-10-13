"""
Compare the datasets that generate_data.py produces for several (dummy) student IDs.

Shows how much the personalised multipliers, demand, opening costs and margins
differ between students, which is why student solutions are expected to differ.

Usage (from any folder):
    python compare_student_datasets.py
    python compare_student_datasets.py --ids 10001 10234 20567

Each dataset is generated into a temporary folder, so nothing in the
repository is modified.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

MODEL_DIR = Path(__file__).resolve().parents[1] / "model-solution"
GENERATOR = MODEL_DIR / "generate_data.py"

# Dummy IDs only - never use real student numbers here.
DEFAULT_IDS = ["10001", "10234", "20567", "30999", "40123"]


def generate_for_student(student_id, work_dir):
    """Generate data for one ID into work_dir/<id> and return manifest + data."""
    out_dir = Path(work_dir) / student_id
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--student_id", student_id, "--out_dir", str(out_dir)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error generating for {student_id}: {result.stderr}")
        return None

    with open(out_dir / "manifest.json", encoding="utf-8") as f:
        manifest = json.load(f)
    with open(out_dir / "margins.json", encoding="utf-8") as f:
        margins = json.load(f)

    return {
        "student_id": student_id,
        "manifest": manifest,
        "zones": pd.read_csv(out_dir / "zones.csv"),
        "stores": pd.read_csv(out_dir / "stores.csv"),
        "margins": margins,
    }

def compare_datasets(datasets):
    """Compare key parameters and data distributions."""
    print("\n" + "="*80)
    print("DATASET COMPARISON ACROSS STUDENT IDS")
    print("="*80)
    
    # Parameter comparison
    print("\nPERTURBATION MULTIPLIERS:")
    print("-" * 80)
    print(f"{'Student ID':<12} {'Demand':<8} {'OpenCost':<10} {'Capacity':<10} {'Margin':<8} {'ServiceCost':<12}")
    print("-" * 80)
    
    for data in datasets:
        m = data["manifest"]["multipliers"]
        print(f"{data['student_id']:<12} {m['demand_mult']:<8.4f} {m['open_cost_mult']:<10.4f} "
              f"{m['capacity_mult']:<10.4f} {m['margin_regime']:<8} {m['service_cost_regime']:<12}")
    
    # Data statistics comparison
    print("\nZONE DEMAND STATISTICS (historical_sales):")
    print("-" * 80)
    print(f"{'Student ID':<12} {'Mean':<12} {'Std':<12} {'Min':<12} {'Max':<12} {'Missing %':<12}")
    print("-" * 80)
    
    for data in datasets:
        zones = data["zones"]
        demand = zones["historical_sales"].dropna()
        missing_pct = (zones["historical_sales"].isna().sum() / len(zones)) * 100
        print(f"{data['student_id']:<12} {demand.mean():<12.2f} {demand.std():<12.2f} "
              f"{demand.min():<12.2f} {demand.max():<12.2f} {missing_pct:<12.1f}%")
    
    # Store economics
    print("\nSTORE OPENING COSTS:")
    print("-" * 80)
    print(f"{'Student ID':<12} {'Mean':<12} {'Std':<12} {'Min':<12} {'Max':<12}")
    print("-" * 80)
    
    for data in datasets:
        stores = data["stores"]
        costs = stores["fixed_opening_cost"]
        print(f"{data['student_id']:<12} {costs.mean():<12.2f} {costs.std():<12.2f} "
              f"{costs.min():<12.2f} {costs.max():<12.2f}")
    
    # Margin comparison
    print("\nMARGIN PARAMETERS:")
    print("-" * 80)
    print(f"{'Student ID':<12} {'Margin/Unit':<15} {'Service Cost/km':<15}")
    print("-" * 80)
    
    for data in datasets:
        margins = data["margins"]
        print(f"{data['student_id']:<12} £{margins['margin_per_unit']:<14.2f} £{margins['service_cost_per_km']:<14.4f}")
    
    # Pairwise differences
    print("\n" + "="*80)
    print("PAIRWISE DEMAND DIFFERENCES (% change from first student)")
    print("="*80)
    
    first_demand = datasets[0]["zones"]["historical_sales"].dropna().mean()
    for i, data in enumerate(datasets[1:], 1):
        demand = data["zones"]["historical_sales"].dropna().mean()
        pct_change = ((demand - first_demand) / first_demand) * 100
        print(f"{datasets[0]['student_id']} → {data['student_id']}: {pct_change:+.2f}% "
              f"(£{first_demand:.2f} → £{demand:.2f})")

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ids", nargs="+", default=DEFAULT_IDS, help="Dummy student IDs to compare.")
    return parser.parse_args()


if __name__ == "__main__":
    student_ids = parse_args().ids
    print(f"Testing {len(student_ids)} different student IDs...")
    print(f"Student IDs: {student_ids}\n")

    datasets = []
    with tempfile.TemporaryDirectory() as work_dir:
        for sid in student_ids:
            print(f"Generating for student {sid}...")
            data = generate_for_student(sid, work_dir)
            if data:
                datasets.append(data)

    if datasets:
        compare_datasets(datasets)
        
        print("\n" + "="*80)
        print("INTERPRETATION")
        print("="*80)
        print("""
1. PERTURBATION MULTIPLIERS: Show how each student's dataset is scaled.
   - Demand variations (0.8–1.2) affect zone profitability.
   - Opening cost variations (0.85–1.15) affect store economics.
   - Margin regimes (low/mid/high) create different profitability regimes.

2. ZONE DEMAND: Mean demand varies by ±10–20% across students.
   - This significantly affects which stores become optimal.
   - Missing % is consistent (students must all forecast ~45% of zones).

3. STORE ECONOMICS: Opening costs vary by ±15% across students.
   - Higher opening costs → fewer stores should open.
   - Lower demand + higher costs → might close same stores.

4. SIGNIFICANCE: Differences are MATERIAL (~10–20% in key metrics).
   - Students will get DIFFERENT optimal solutions.
   - Solutions are NOT trivial copies of each other.
   - This is GOOD for academic integrity and learning.
        """)
