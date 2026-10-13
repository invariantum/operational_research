# Data dictionary — Coursework Part B (Yodafone store network)

All data is **synthetic**. It was generated for teaching (UK-shaped coordinates, plausible but invented
economics) and describes no real people, shops or places.

## Base data (`02-coursework-part-b/starter/base_data/`)

The lecturer-provided pool from which every student's dataset is sampled. Do not edit.

### `zones_base.csv` — 500 rows, one per geographic demand zone

| Column | Type | Unit / range | Meaning |
|---|---|---|---|
| `zone_id` | int | 1–500 | Zone identifier |
| `lat`, `lon` | float | degrees | Zone centre (UK bounding box) |
| `population_density` | float | people per km² | Lognormal |
| `median_income` | float | GBP per year | ≥ 18,000 |
| `footfall_potential` | float | index | Lognormal |
| `competitor_presence` | int | 0 / 1 | 1 = a competitor operates in the zone |
| `unemployment_rate` | float | 0.01–0.15 | Share of working-age population |
| `deprivation_index` | float | 0–100 | Higher = more deprived |
| `historical_sales` | float | units per year | Annual demand (≈ 250–350 typical) |

### `stores_base.csv` — 120 rows, one per candidate store

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `store_id` | int | 1–120 | Store identifier |
| `lat`, `lon` | float | degrees | Store location |
| `capacity` | int | units per year | Maximum demand the store can serve (8,000–12,000) |
| `fixed_opening_cost` | int | GBP | Cost of opening the store (60k–120k) |
| `reopen_cost` | int | GBP | Reduced cost of reopening a closed store (30% of opening cost) |
| `service_radius_km` | float | km | Zones further away than this cannot be served (15–50) |

### `zone_store_dist_base.csv` — 60,000 rows (500 zones × 120 stores)

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `zone_id` | int | | Zone |
| `store_id` | int | | Store |
| `distance_km` | float | km | Great-circle distance |

### `margins_base.json`

| Key | Unit | Meaning |
|---|---|---|
| `margin_per_unit` | GBP per unit | Profit margin on each unit of demand served |
| `service_cost_per_km` | GBP per unit-km | Distance-based service cost |

## Personalised data (`starter/data/`, created by `generate_data.py`)

`python generate_data.py --student_id <ID>` samples and perturbs the base pool deterministically
from the ID (SHA-256 seed), so each student gets a different but equivalent problem:

| File | Rows | Differences from the base file |
|---|---|---|
| `zones.csv` | 300 | Random subset; IDs renumbered from 0; demand × 0.8–1.2 with lognormal noise; socio-economic columns × 0.9–1.1; **33–50% of `historical_sales` set to blank** (to be forecast) |
| `stores.csv` | 80 | Random subset; IDs renumbered from 0; capacity and opening cost × 0.85–1.15; locations jittered (≈ 8 km) |
| `zone_store_dist.csv` | 24,000 | Matching subset; distances × 0.99–1.01 |
| `margins.json` | — | Margin and service cost scaled by a low / mid / high regime (0.90 / 1.00 / 1.12) |
| `manifest.json` | — | Seed, multipliers and regimes used (for reproducibility); paths are stored relative |

`data/` is generated, so it is listed in `.gitignore` and never committed.
