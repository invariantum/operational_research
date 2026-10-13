#!/usr/bin/env python3
"""
generate_data.py

Deterministically generates a *student-specific* dataset instance for the
Yodafone Retail Reopening Optimisation coursework.

Design goals
------------
- Same student_id -> identical outputs across runs (deterministic).
- Different student_id -> numerically different instance, same structure.
- Controlled perturbations (bounded) to avoid pathological cases.
- Reproducible via a manifest.json file capturing seed and multipliers.

Expected base inputs (lecturer-provided)
----------------------------------------
By default, this script expects a base dataset folder containing:

  base_data/
    zones_base.csv
    stores_base.csv
    zone_store_dist_base.csv
    margins_base.json

Outputs (student-specific)
--------------------------
  data/
    zones.csv
    stores.csv
    zone_store_dist.csv
    margins.json
    manifest.json

Usage
-----
  python generate_data.py --student_id 100000000
  python generate_data.py --student_id 100000000 --base_dir base_data --out_dir data

By default both folders are resolved relative to this script, so the command
works from any working directory.

Notes
-----
- The script perturbs only *parameters*, not structure: row counts and keys remain unchanged.
- If your base data uses different column names, adjust the CANDIDATE_COLUMNS lists below.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# -----------------------------
# Configuration / assumptions
# -----------------------------

SCRIPT_DIR = Path(__file__).resolve().parent

BASE_FILES = {
    "zones": "zones_base.csv",
    "stores": "stores_base.csv",
    "dist": "zone_store_dist_base.csv",
    "margins": "margins_base.json",
}

OUTPUT_FILES = {
    "zones": "zones.csv",
    "stores": "stores.csv",
    "dist": "zone_store_dist.csv",
    "margins": "margins.json",
    "manifest": "manifest.json",
}

# Candidate columns to perturb (only those that exist will be used).
ZONES_DEMAND_COLUMNS = [
    "historical_sales",
    "sales",
    "demand",
    "units_sold",
    "target",  # if you used a generic ML target name
]
ZONES_SOCIO_COLUMNS = [
    "population_density",
    "median_income",
    "footfall_potential",
    "competitor_presence",
    "unemployment_rate",
    "deprivation_index",
]

STORES_CAPACITY_COLUMNS = [
    "capacity",
    "max_units",
    "service_capacity",
]

STORES_OPEN_COST_COLUMNS = [
    "fixed_opening_cost",
    "opening_cost",
    "fixed_cost",
]

STORES_REOPEN_COST_COLUMNS = [
    "reopen_cost",
    "restart_cost",
    "reactivation_cost",
]

DISTANCE_COLUMNS = [
    "distance_km",
    "distance",
    "km",
]

# Keys / ID columns (must exist or be inferred)
ZONE_ID_COLUMNS = ["zone_id", "zone", "zoneID", "ZoneID", "id_zone"]
STORE_ID_COLUMNS = ["store_id", "store", "storeID", "StoreID", "id_store"]

# Default perturbation bounds (tuned to be conservative and feasible).
DEFAULT_PERTURB = {
    # Demand is the “main” personalised driver.
    "demand_mult_min": 0.80,
    "demand_mult_max": 1.20,
    "demand_noise_sigma": 0.10,  # higher multiplicative lognormal noise for stronger divergence

    # Costs and capacities: widened jitter to shift optimal openings.
    "open_cost_mult_min": 0.85,
    "open_cost_mult_max": 1.15,
    "capacity_mult_min": 0.85,
    "capacity_mult_max": 1.15,

    # Socioeconomic inputs: moderate jitter to decorrelate feature rankings.
    "socio_mult_min": 0.90,
    "socio_mult_max": 1.10,

    # Distances: keep tiny jitter enabled; small changes can break ties without changing geography.
    "distance_mult_min": 0.99,
    "distance_mult_max": 1.01,

    # Margin and per-km service cost: widen regime spread for clearer profitability differences.
    "margin_regimes": {
        "low": 0.90,
        "mid": 1.00,
        "high": 1.12,
    },
    "service_cost_regimes": {
        "low": 0.90,
        "mid": 1.00,
        "high": 1.12,
    },
}


@dataclass(frozen=True)
class InstanceSpec:
    student_id: str
    seed: int
    demand_mult: float
    open_cost_mult: float
    capacity_mult: float
    socio_mult: float
    distance_mult: float
    margin_regime: str
    service_cost_regime: str


# -----------------------------
# Helpers
# -----------------------------

def stable_seed_from_student_id(student_id: str) -> int:
    """
    Convert an arbitrary student_id string to a stable 32-bit seed.
    Using SHA-256 avoids simple predictability (and handles leading zeros).
    """
    h = hashlib.sha256(student_id.encode("utf-8")).hexdigest()
    # Take 8 hex chars -> 32-bit
    return int(h[:8], 16)


def pick_uniform(rng: np.random.Generator, a: float, b: float) -> float:
    return float(rng.uniform(a, b))


def first_existing_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def require_id_column(df: pd.DataFrame, candidates: List[str], label: str) -> str:
    col = first_existing_column(df, candidates)
    if col is None:
        raise ValueError(
            f"Could not find an ID column for {label}. "
            f"Tried: {candidates}. Present columns: {list(df.columns)[:30]}..."
        )
    return col


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clip_nonnegative(series: pd.Series) -> pd.Series:
    # keep type; clip to >= 0
    return series.clip(lower=0)


def apply_multiplier_to_columns(
    df: pd.DataFrame,
    cols: List[str],
    mult: float,
    *,
    noise: Optional[np.random.Generator] = None,
    noise_sigma: float = 0.0,
    nonnegative: bool = True,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Multiply specified columns by mult, optionally with multiplicative lognormal noise.
    Only applies to columns that exist and are numeric.
    Returns df and list of columns actually modified.
    """
    modified: List[str] = []
    for c in cols:
        if c not in df.columns:
            continue
        if not pd.api.types.is_numeric_dtype(df[c]):
            continue

        x = df[c].astype(float)

        if noise is not None and noise_sigma > 0:
            # multiplicative lognormal noise: exp(N(0, sigma)) with small sigma
            eps = noise.normal(loc=0.0, scale=noise_sigma, size=len(x))
            factor = mult * np.exp(eps)
        else:
            factor = mult

        y = x * factor
        if nonnegative:
            y = np.maximum(y, 0.0)

        # Preserve integer-ness when the original is integer-like
        if pd.api.types.is_integer_dtype(df[c]):
            df[c] = np.rint(y).astype(int)
        else:
            df[c] = y

        modified.append(c)

    return df, modified


def load_json(path: Path) -> Dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(obj: Dict, path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)


def display_path(path: Path) -> str:
    """Return a short, machine-independent version of a path for logs and the manifest.

    Absolute paths would leak the local user name / folder layout into the
    manifest and into notebook outputs, so paths are shown relative to the
    current working directory where possible.
    """
    try:
        return os.path.relpath(path)
    except ValueError:  # e.g. different drive on Windows
        return path.name


# -----------------------------
# Core generation logic
# -----------------------------

def build_instance_spec(student_id: str, perturb: Dict) -> InstanceSpec:
    seed = stable_seed_from_student_id(student_id)
    rng = np.random.default_rng(seed)

    demand_mult = pick_uniform(rng, perturb["demand_mult_min"], perturb["demand_mult_max"])
    open_cost_mult = pick_uniform(rng, perturb["open_cost_mult_min"], perturb["open_cost_mult_max"])
    capacity_mult = pick_uniform(rng, perturb["capacity_mult_min"], perturb["capacity_mult_max"])
    socio_mult = pick_uniform(rng, perturb["socio_mult_min"], perturb["socio_mult_max"])
    distance_mult = pick_uniform(rng, perturb["distance_mult_min"], perturb["distance_mult_max"])

    # regime selection keeps margins/costs interpretable
    margin_regime = rng.choice(list(perturb["margin_regimes"].keys()))
    service_cost_regime = rng.choice(list(perturb["service_cost_regimes"].keys()))

    return InstanceSpec(
        student_id=student_id,
        seed=seed,
        demand_mult=demand_mult,
        open_cost_mult=open_cost_mult,
        capacity_mult=capacity_mult,
        socio_mult=socio_mult,
        distance_mult=distance_mult,
        margin_regime=str(margin_regime),
        service_cost_regime=str(service_cost_regime),
    )








def select_subset(
    zones: pd.DataFrame,
    stores: pd.DataFrame,
    dist: pd.DataFrame,
    rng: np.random.Generator,
    num_zones: int,
    num_stores: int,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Select deterministic random subsets of zones and stores per student.
    Remaps all IDs (in zones, stores, and distance tables) to 0-based indices.
    """
    # Select which rows to keep from zones and stores (by row index)
    zone_row_indices = sorted(rng.choice(len(zones), size=min(num_zones, len(zones)), replace=False))
    store_row_indices = sorted(rng.choice(len(stores), size=min(num_stores, len(stores)), replace=False))
    
    # Extract subset DataFrames
    zones_subset = zones.iloc[zone_row_indices].copy()
    stores_subset = stores.iloc[store_row_indices].copy()
    
    # Get the original 1-based zone_id and store_id values for mapping
    selected_zone_ids_1based = set(zones_subset["zone_id"].tolist())
    selected_store_ids_1based = set(stores_subset["store_id"].tolist())
    
    # Create mappings from old 1-based IDs to new 0-based indices
    zone_id_map = {old_id: new_idx for new_idx, old_id in enumerate(sorted(selected_zone_ids_1based))}
    store_id_map = {old_id: new_idx for new_idx, old_id in enumerate(sorted(selected_store_ids_1based))}
    
    # Update zone_id and store_id columns in the subsets
    zones_subset["zone_id"] = zones_subset["zone_id"].map(zone_id_map)
    zones_subset = zones_subset.reset_index(drop=True)
    
    stores_subset["store_id"] = stores_subset["store_id"].map(store_id_map)
    stores_subset = stores_subset.reset_index(drop=True)
    
    # Filter distance table and remap IDs
    dist_subset = dist[
        (dist["zone_id"].isin(selected_zone_ids_1based)) &
        (dist["store_id"].isin(selected_store_ids_1based))
    ].copy()
    
    dist_subset["zone_id"] = dist_subset["zone_id"].map(zone_id_map)
    dist_subset["store_id"] = dist_subset["store_id"].map(store_id_map)
    dist_subset = dist_subset.reset_index(drop=True)
    
    return zones_subset, stores_subset, dist_subset


def validate_structure(
    zones: pd.DataFrame,
    stores: pd.DataFrame,
    dist: pd.DataFrame,
    zone_id_col: str,
    store_id_col: str,
    distance_col: str,
) -> None:
    # Basic integrity checks: keys exist, joins are consistent, distances non-negative.
    z_ids = set(zones[zone_id_col].astype(str).unique())
    s_ids = set(stores[store_id_col].astype(str).unique())

    # dist must have zone_id and store_id
    if zone_id_col not in dist.columns or store_id_col not in dist.columns:
        raise ValueError(
            f"Distance table must contain '{zone_id_col}' and '{store_id_col}'. "
            f"Present: {list(dist.columns)}"
        )

    dz = set(dist[zone_id_col].astype(str).unique())
    ds = set(dist[store_id_col].astype(str).unique())

    missing_z = dz - z_ids
    missing_s = ds - s_ids

    if missing_z:
        raise ValueError(f"Distance table references unknown zones (showing up to 10): {list(missing_z)[:10]}")
    if missing_s:
        raise ValueError(f"Distance table references unknown stores (showing up to 10): {list(missing_s)[:10]}")

    if (dist[distance_col].astype(float) < 0).any():
        raise ValueError("Negative distances found after perturbation (should not happen).")


def generate(
    student_id: str,
    base_dir: Path,
    out_dir: Path,
    *,
    perturb: Dict,
    allow_distance_jitter: bool,
    num_zones_subset: int = 300,
    num_stores_subset: int = 80,
) -> None:
    """
    Generate student-specific dataset: load base, select subset, perturb, save.
    
    Args:
        student_id: student identifier (used to seed subset selection)
        base_dir: path to base_data/ folder
        out_dir: path to output data/ folder
        perturb: perturbation configuration dict
        allow_distance_jitter: apply small lat/lon jitter to stores
        num_zones_subset: number of zones per student (sampled from base pool)
        num_stores_subset: number of stores per student (sampled from base pool)
    """
    ensure_dir(out_dir)

    # Load base data
    zones_path = base_dir / BASE_FILES["zones"]
    stores_path = base_dir / BASE_FILES["stores"]
    dist_path = base_dir / BASE_FILES["dist"]
    margins_path = base_dir / BASE_FILES["margins"]

    for p in [zones_path, stores_path, dist_path, margins_path]:
        if not p.exists():
            raise FileNotFoundError(f"Missing required base file: {p}")

    zones = pd.read_csv(zones_path)
    stores = pd.read_csv(stores_path)
    dist = pd.read_csv(dist_path)
    margins = load_json(margins_path)

    # Build RNG from student_id
    spec = build_instance_spec(student_id, perturb)
    rng = np.random.default_rng(spec.seed)

    # Select deterministic subsets per student
    zones, stores, dist = select_subset(zones, stores, dist, rng, num_zones_subset, num_stores_subset)

    # Identify key columns
    zone_id_col = require_id_column(zones, ZONE_ID_COLUMNS, "zones")
    store_id_col = require_id_column(stores, STORE_ID_COLUMNS, "stores")
    distance_col = first_existing_column(dist, DISTANCE_COLUMNS)
    if distance_col is None:
        raise ValueError(
            f"Could not find a distance column in zone_store_dist. "
            f"Tried: {DISTANCE_COLUMNS}. Present columns: {list(dist.columns)}"
        )

    # --- Perturb zones: demand and optionally socio features
    zones_before_cols = list(zones.columns)

    # Demand: apply multiplier + small multiplicative noise
    zones, demand_cols_modified = apply_multiplier_to_columns(
        zones,
        ZONES_DEMAND_COLUMNS,
        spec.demand_mult,
        noise=rng,
        noise_sigma=float(perturb["demand_noise_sigma"]),
        nonnegative=True,
    )

    # Socioeconomic features: mild multiplier without noise (or you can add small noise)
    zones, socio_cols_modified = apply_multiplier_to_columns(
        zones,
        ZONES_SOCIO_COLUMNS,
        spec.socio_mult,
        noise=None,
        noise_sigma=0.0,
        nonnegative=True,
    )

    # --- Perturb stores: opening costs and capacity
    stores, open_cost_cols_modified = apply_multiplier_to_columns(
        stores,
        STORES_OPEN_COST_COLUMNS,
        spec.open_cost_mult,
        noise=None,
        noise_sigma=0.0,
        nonnegative=True,
    )
    stores, capacity_cols_modified = apply_multiplier_to_columns(
        stores,
        STORES_CAPACITY_COLUMNS,
        spec.capacity_mult,
        noise=None,
        noise_sigma=0.0,
        nonnegative=True,
    )

    # --- Perturb store locations (lat/lon) per student for stronger divergence
    # Small jitter: ~0.05-0.15 degrees = ~5-15 km at UK latitudes (realistic for store relocation)
    if "lat" in stores.columns and "lon" in stores.columns:
        lat_jitter = rng.normal(0, 0.08, size=len(stores))  # ~8 km stdev
        lon_jitter = rng.normal(0, 0.08, size=len(stores))  # ~8 km stdev
        stores["lat"] = stores["lat"] + lat_jitter
        stores["lon"] = stores["lon"] + lon_jitter

    # --- Distances: default keep fixed; optionally tiny jitter
    if allow_distance_jitter:
        dist, dist_cols_modified = apply_multiplier_to_columns(
            dist,
            [distance_col],
            spec.distance_mult,
            noise=None,
            noise_sigma=0.0,
            nonnegative=True,
        )
    else:
        dist_cols_modified = []

    # --- Margins: apply regime multipliers if keys are present
    # We do not assume exact JSON structure; we look for common keys.
    margin_mult = float(perturb["margin_regimes"][spec.margin_regime])
    service_mult = float(perturb["service_cost_regimes"][spec.service_cost_regime])

    margins_modified: Dict[str, float] = {}
    # Common keys; adjust if your margins.json differs.
    for key in ["margin_per_unit", "avg_margin_per_unit", "unit_margin"]:
        if key in margins and isinstance(margins[key], (int, float)):
            margins[key] = float(margins[key]) * margin_mult
            margins_modified[key] = margin_mult

    for key in ["service_cost_per_km", "cost_per_km", "variable_cost_per_km"]:
        if key in margins and isinstance(margins[key], (int, float)):
            margins[key] = float(margins[key]) * service_mult
            margins_modified[key] = service_mult

    # Validate structure/integrity
    validate_structure(zones, stores, dist, zone_id_col, store_id_col, distance_col)

    # Create missing data: Randomly blank out ~100-150 zones' historical_sales
    # Students will use ML to forecast these missing values
    if "historical_sales" in zones.columns:
        num_zones = len(zones)
        # 33-50% of zones have missing demand (requires forecasting)
        num_missing = rng.integers(int(0.33 * num_zones), int(0.50 * num_zones))
        missing_indices = rng.choice(num_zones, size=num_missing, replace=False)
        zones.loc[missing_indices, "historical_sales"] = np.nan
        
        print(f"  -> Blanked {num_missing}/{num_zones} zones' historical_sales (students must forecast)")

    # Write outputs
    zones.to_csv(out_dir / OUTPUT_FILES["zones"], index=False)
    stores.to_csv(out_dir / OUTPUT_FILES["stores"], index=False)
    dist.to_csv(out_dir / OUTPUT_FILES["dist"], index=False)
    save_json(margins, out_dir / OUTPUT_FILES["margins"])

    manifest = {
        "student_id": spec.student_id,
        "seed": spec.seed,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "base_dir": display_path(base_dir),
        "scenario": "Retail Store Network Optimization - Maximize profit by selecting which stores to open",
        "outputs": {k: v for k, v in OUTPUT_FILES.items() if k != "manifest"},
        "column_mapping": {
            "zone_id_col": zone_id_col,
            "store_id_col": store_id_col,
            "distance_col": distance_col,
        },
        "multipliers": {
            "demand_mult": spec.demand_mult,
            "open_cost_mult": spec.open_cost_mult,
            "capacity_mult": spec.capacity_mult,
            "socio_mult": spec.socio_mult,
            "distance_mult": spec.distance_mult if allow_distance_jitter else 1.0,
            "margin_regime": spec.margin_regime,
            "service_cost_regime": spec.service_cost_regime,
            "margin_mult": margin_mult,
            "service_cost_mult": service_mult,
        },
        "modified_columns": {
            "zones_demand": demand_cols_modified,
            "zones_socio": socio_cols_modified,
            "stores_open_cost": open_cost_cols_modified,
            "stores_capacity": capacity_cols_modified,
            "dist": dist_cols_modified,
            "margins": list(margins_modified.keys()),
        },
        "notes": {
            "structure_preserved": True,
            "distance_jitter_enabled": bool(allow_distance_jitter),
            "demand_noise_sigma": float(perturb["demand_noise_sigma"]),
            "missing_data": {
                "total_zones": int(num_zones),
                "zones_with_forecasted_demand": int(num_missing),
                "zones_with_historical_data": int(num_zones - num_missing),
                "student_task": "Forecast missing historical_sales using ML model trained on zones with data",
            },
            "optimization_problem": {
                "existing_zones": int(num_zones),
                "existing_stores": int(len(stores)),
                "distance_pairs": int(len(dist)),
                "objective": "Choose store subset to maximize (revenue - opening_costs)",
                "constraint": "Store capacity and service radius limits",
            },
        },
    }
    save_json(manifest, out_dir / OUTPUT_FILES["manifest"])


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate student-specific Yodafone OR dataset (deterministic).")
    p.add_argument("--student_id", required=True, help="Student number/ID (string; leading zeros allowed).")
    p.add_argument(
        "--base_dir",
        default=str(SCRIPT_DIR / "base_data"),
        help="Folder containing base *_base files (default: base_data/ next to this script).",
    )
    p.add_argument(
        "--out_dir",
        default=str(SCRIPT_DIR / "data"),
        help="Output folder, created if missing (default: data/ next to this script).",
    )
    p.add_argument(
        "--allow_distance_jitter",
        action="store_true",
        default=True,
        help="Apply tiny deterministic multiplier to distances (default: on).",
    )
    p.add_argument(
        "--no_distance_jitter",
        dest="allow_distance_jitter",
        action="store_false",
        help="Disable distance jitter (keeps base distances).",
    )

    # Optional overrides for perturbation bounds (rarely needed)
    p.add_argument("--demand_mult_min", type=float, default=DEFAULT_PERTURB["demand_mult_min"])
    p.add_argument("--demand_mult_max", type=float, default=DEFAULT_PERTURB["demand_mult_max"])
    p.add_argument("--demand_noise_sigma", type=float, default=DEFAULT_PERTURB["demand_noise_sigma"])

    p.add_argument("--open_cost_mult_min", type=float, default=DEFAULT_PERTURB["open_cost_mult_min"])
    p.add_argument("--open_cost_mult_max", type=float, default=DEFAULT_PERTURB["open_cost_mult_max"])

    p.add_argument("--capacity_mult_min", type=float, default=DEFAULT_PERTURB["capacity_mult_min"])
    p.add_argument("--capacity_mult_max", type=float, default=DEFAULT_PERTURB["capacity_mult_max"])

    p.add_argument("--socio_mult_min", type=float, default=DEFAULT_PERTURB["socio_mult_min"])
    p.add_argument("--socio_mult_max", type=float, default=DEFAULT_PERTURB["socio_mult_max"])

    p.add_argument("--distance_mult_min", type=float, default=DEFAULT_PERTURB["distance_mult_min"])
    p.add_argument("--distance_mult_max", type=float, default=DEFAULT_PERTURB["distance_mult_max"])

    # Margin/cost regimes (keep as-is unless you have strong reasons)
    p.add_argument("--margin_low", type=float, default=DEFAULT_PERTURB["margin_regimes"]["low"])
    p.add_argument("--margin_mid", type=float, default=DEFAULT_PERTURB["margin_regimes"]["mid"])
    p.add_argument("--margin_high", type=float, default=DEFAULT_PERTURB["margin_regimes"]["high"])

    p.add_argument("--service_low", type=float, default=DEFAULT_PERTURB["service_cost_regimes"]["low"])
    p.add_argument("--service_mid", type=float, default=DEFAULT_PERTURB["service_cost_regimes"]["mid"])
    p.add_argument("--service_high", type=float, default=DEFAULT_PERTURB["service_cost_regimes"]["high"])

    return p.parse_args()


def main() -> None:
    args = parse_args()

    perturb = {
        "demand_mult_min": args.demand_mult_min,
        "demand_mult_max": args.demand_mult_max,
        "demand_noise_sigma": args.demand_noise_sigma,
        "open_cost_mult_min": args.open_cost_mult_min,
        "open_cost_mult_max": args.open_cost_mult_max,
        "capacity_mult_min": args.capacity_mult_min,
        "capacity_mult_max": args.capacity_mult_max,
        "socio_mult_min": args.socio_mult_min,
        "socio_mult_max": args.socio_mult_max,
        "distance_mult_min": args.distance_mult_min,
        "distance_mult_max": args.distance_mult_max,
        "margin_regimes": {"low": args.margin_low, "mid": args.margin_mid, "high": args.margin_high},
        "service_cost_regimes": {"low": args.service_low, "mid": args.service_mid, "high": args.service_high},
    }

    base_dir = Path(args.base_dir).resolve()
    out_dir = Path(args.out_dir).resolve()

    generate(
        student_id=str(args.student_id),
        base_dir=base_dir,
        out_dir=out_dir,
        perturb=perturb,
        allow_distance_jitter=bool(args.allow_distance_jitter),
    )

    print(f"Generated dataset for student_id={args.student_id}")
    print(f"Base: {display_path(base_dir)}")
    print(f"Out:  {display_path(out_dir)}")
    print(f"Manifest: {display_path(out_dir / OUTPUT_FILES['manifest'])}")


if __name__ == "__main__":
    main()
