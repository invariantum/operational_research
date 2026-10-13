#!/usr/bin/env python3
"""
create_base_data.py

Utility to synthesize lecturer-provided base data for the 5CM522 Part B coursework.
Generates four files under base_data/:
  - zones_base.csv
  - stores_base.csv
  - zone_store_dist_base.csv
  - margins_base.json

This is a convenience script for preparing a rich, non-toy dataset before release.
It is staff-only: do not include it in the repository given to students.

Usage:
    python create_base_data.py                      # writes to output/base_data next to this script
    python create_base_data.py --out_dir some/folder

With the default seed (2026) it reproduces the published base_data/ files exactly.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd

# Default sizes: pool used to sample per-student subsets
# Lecturer uses full pool; students get deterministic subset per ID
DEFAULT_NUM_ZONES = 500
DEFAULT_NUM_STORES = 120

# Rough UK bounding box for lat/lon sampling (not precise, just plausible)
UK_LAT_RANGE: Tuple[float, float] = (50.0, 57.8)
UK_LON_RANGE: Tuple[float, float] = (-5.8, 1.8)


def haversine(lat1, lon1, lat2, lon2) -> np.ndarray:
    """Great-circle distance in km for vectorized inputs."""
    R = 6371.0
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c


def generate_zones(n_zones: int, rng: np.random.Generator) -> pd.DataFrame:
    # Generate zones with minimum spacing to avoid unrealistic clustering
    # Use a grid-based approach with small random offsets for realistic spatial distribution
    grid_size = int(np.ceil(np.sqrt(n_zones)))
    lat_step = (UK_LAT_RANGE[1] - UK_LAT_RANGE[0]) / grid_size
    lon_step = (UK_LON_RANGE[1] - UK_LON_RANGE[0]) / grid_size
    
    lats, lons = [], []
    for i in range(grid_size):
        for j in range(grid_size):
            if len(lats) < n_zones:
                base_lat = UK_LAT_RANGE[0] + (i + 0.5) * lat_step
                base_lon = UK_LON_RANGE[0] + (j + 0.5) * lon_step
                # Add small jitter (~20% of grid cell) for realism
                lat = base_lat + rng.normal(0, 0.15)
                lon = base_lon + rng.normal(0, 0.15)
                lats.append(lat)
                lons.append(lon)
    
    lat = np.array(lats)
    lon = np.array(lons)

    # Socioeconomic signals with variation
    population_density = rng.lognormal(mean=5.5, sigma=0.6, size=n_zones)  # people per km^2
    median_income = rng.normal(loc=32000, scale=6500, size=n_zones)
    median_income = np.clip(median_income, 18000, None)
    footfall_potential = rng.lognormal(mean=8.5, sigma=0.8, size=n_zones)
    competitor_presence = rng.binomial(1, 0.45, size=n_zones)
    unemployment_rate = np.clip(rng.normal(0.055, 0.02, size=n_zones), 0.01, 0.15)
    deprivation_index = rng.uniform(0, 100, size=n_zones)

    # Annual demand per zone: 250-350 units
    # Represents annual retail/logistics throughput in a geographic zone
    base_demand = 280 + 0.008 * population_density + 0.00015 * footfall_potential
    base_demand *= rng.normal(1.0, 0.11, size=n_zones)
    base_demand *= np.where(competitor_presence == 1, rng.uniform(0.80, 0.92, size=n_zones), 1.0)
    base_demand *= np.where(median_income > 36000, rng.uniform(1.05, 1.12, size=n_zones), 1.0)
    historical_sales = np.clip(base_demand, 100, None)

    zones = pd.DataFrame(
        {
            "zone_id": np.arange(1, n_zones + 1),
            "lat": lat,
            "lon": lon,
            "population_density": population_density,
            "median_income": median_income,
            "footfall_potential": footfall_potential,
            "competitor_presence": competitor_presence,
            "unemployment_rate": unemployment_rate,
            "deprivation_index": deprivation_index,
            "historical_sales": historical_sales,
        }
    )
    return zones


def generate_stores(n_stores: int, rng: np.random.Generator) -> pd.DataFrame:
    lat = rng.uniform(*UK_LAT_RANGE, size=n_stores)
    lon = rng.uniform(*UK_LON_RANGE, size=n_stores)

    # Store capacity: 8000-12000 units annually
    # MUCH higher than avg zone demand (~320 units) to create overcapacity
    # When stores overlap, they compete for limited zone demand → cannibalization effect
    capacity = rng.integers(8000, 12000, size=n_stores)
    # Reopening cost: £60k-£120k (realistic for restarting closed locations)
    fixed_opening_cost = rng.integers(60_000, 120_000, size=n_stores)
    # COVID reopening cost: 30% of normal (abbreviated reopening)
    reopen_cost = (fixed_opening_cost * 0.30).astype(int)
    service_radius_km = rng.uniform(15, 50, size=n_stores)

    stores = pd.DataFrame(
        {
            "store_id": np.arange(1, n_stores + 1),
            "lat": lat,
            "lon": lon,
            "capacity": capacity,
            "fixed_opening_cost": fixed_opening_cost,
            "reopen_cost": reopen_cost,
            "service_radius_km": service_radius_km,
        }
    )
    return stores


def generate_distances(zones: pd.DataFrame, stores: pd.DataFrame) -> pd.DataFrame:
    # Vectorized distance matrix
    z_lat = zones["lat"].to_numpy()[:, None]
    z_lon = zones["lon"].to_numpy()[:, None]
    s_lat = stores["lat"].to_numpy()[None, :]
    s_lon = stores["lon"].to_numpy()[None, :]

    dist_matrix = haversine(z_lat, z_lon, s_lat, s_lon)

    z_ids = zones["zone_id"].to_numpy()
    s_ids = stores["store_id"].to_numpy()

    zone_ids = np.repeat(z_ids, len(s_ids))
    store_ids = np.tile(s_ids, len(z_ids))
    distances = dist_matrix.reshape(-1)

    df = pd.DataFrame(
        {
            "zone_id": zone_ids,
            "store_id": store_ids,
            "distance_km": distances,
        }
    )
    return df


def generate_margins(rng: np.random.Generator) -> dict:
    # Margin per unit: £300-450 (moderate margins)
    margin_per_unit = float(rng.uniform(300, 450))
    # Service cost per km (vehicle ops, fuel, driver time)
    service_cost_per_km = float(rng.uniform(0.10, 0.20))
    return {
        "margin_per_unit": margin_per_unit,
        "service_cost_per_km": service_cost_per_km,
        "notes": "Annual basis: demand in units/year, costs in GBP. Personalised scaling applied by generate_data.py",
    }


def main():
    parser = argparse.ArgumentParser(description="Create synthetic base_data for 5CM522 Part B coursework.")
    parser.add_argument("--num_zones", type=int, default=DEFAULT_NUM_ZONES)
    parser.add_argument("--num_stores", type=int, default=DEFAULT_NUM_STORES)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument(
        "--out_dir",
        default=str(Path(__file__).resolve().parent / "output" / "base_data"),
        help="Output directory for base files (default: output/base_data next to this script).",
    )
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    zones = generate_zones(args.num_zones, rng)
    stores = generate_stores(args.num_stores, rng)
    dists = generate_distances(zones, stores)
    margins = generate_margins(rng)

    zones.to_csv(out_dir / "zones_base.csv", index=False)
    stores.to_csv(out_dir / "stores_base.csv", index=False)
    dists.to_csv(out_dir / "zone_store_dist_base.csv", index=False)
    with (out_dir / "margins_base.json").open("w", encoding="utf-8") as f:
        json.dump(margins, f, indent=2)

    print(f"Wrote base data to {out_dir}")
    print("Files: zones_base.csv, stores_base.csv, zone_store_dist_base.csv, margins_base.json")
    print(f"Zones: {len(zones)} rows; Stores: {len(stores)} rows; Distances: {len(dists)} rows")


if __name__ == "__main__":
    main()
