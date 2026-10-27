"""
Reproducible Synthetic Pune Urban Infrastructure Telemetry Generator.

Generates statistically varied civil infrastructure records (>=100,000 rows)
restricted strictly to the Pune city monitoring boundary (PMC / PCMC).

Labels:
- Verified Synthetic / Benchmarking Data
- Civil Infrastructure Domain Physics (Non-negative RUL, realistic degradation)
"""
from __future__ import annotations

import argparse
from pathlib import Path
import random
import sys
import time

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config.location_config import PUNE_BOUNDS, PUNE_ZONES, is_within_pune
from app.database.database import sync_dataframe_to_db

DATA_PATH = ROOT / "data" / "urban_infrastructure_data.csv"
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

ASSET_TYPES = ["Road", "Bridge", "Pipeline", "Drainage", "Streetlight", "Electrical Pole"]
MATERIALS = ["Concrete", "Steel", "PVC", "Asphalt", "Copper", "Composite"]
ZONES = ["North", "South", "East", "West", "Central", "Industrial"]


def generate_pune_dataset(num_rows: int = 100000, seed: int = 42) -> pd.DataFrame:
    """Generates a statistically varied, geographically bounded Pune infrastructure dataset.

    All coordinates fall strictly within the Pune municipal boundary (18.42 - 18.64, 73.74 - 73.98).
    """
    np.random.seed(seed)
    random.seed(seed)

    print(f"Generating {num_rows:,} synthetic Pune infrastructure records (Seed={seed})...")
    t0 = time.time()

    # Pre-sample discrete variables
    asset_types = np.random.choice(ASSET_TYPES, size=num_rows, p=[0.28, 0.12, 0.18, 0.14, 0.15, 0.13])
    materials = np.random.choice(MATERIALS, size=num_rows)
    zones = np.random.choice(ZONES, size=num_rows, p=[0.18, 0.18, 0.20, 0.18, 0.14, 0.12])

    # Continuous variables with realistic distributions
    age_years = np.clip(np.round(np.random.normal(18.5, 9.5, size=num_rows), 2), 1.0, 60.0)
    traffic_density = np.clip(np.round(np.random.normal(55.0, 18.0, size=num_rows), 2), 10.0, 95.0)
    average_load = np.clip(np.round(np.random.normal(95.0, 28.0, size=num_rows), 2), 20.0, 180.0)

    # Pune regional climate (Monsoon rainfall 750-1600mm, temperature 18-36°C)
    annual_rainfall = np.clip(np.round(np.random.normal(1050.0, 220.0, size=num_rows), 2), 650.0, 2200.0)
    average_temperature = np.clip(np.round(np.random.normal(26.5, 3.8, size=num_rows), 2), 16.0, 39.0)

    maintenance_count = np.clip(np.random.poisson(lam=4.2, size=num_rows), 0, 20)
    days_since_maintenance = np.clip(np.round(np.random.exponential(scale=110.0, size=num_rows), 2), 0.0, 600.0)
    days_since_inspection = np.clip(np.round(np.random.exponential(scale=160.0, size=num_rows), 2), 0.0, 900.0)

    structural_score = np.clip(np.round(np.random.normal(71.0, 16.5, size=num_rows), 2), 20.0, 100.0)
    corrosion_level = np.clip(np.round(np.random.normal(36.0, 19.0, size=num_rows), 2), 0.0, 100.0)
    previous_failures = np.clip(np.random.poisson(lam=1.2, size=num_rows), 0, 8)
    usage_intensity = np.clip(np.round(np.random.normal(58.0, 17.0, size=num_rows), 2), 10.0, 100.0)

    # Geographic coordinates bounded by zone
    lats = np.zeros(num_rows, dtype=np.float64)
    lngs = np.zeros(num_rows, dtype=np.float64)
    wards = []
    localities = []

    for i in range(num_rows):
        z = zones[i]
        cfg = PUNE_ZONES[z]
        bounds = cfg["bounds"]
        # Jitter coordinates inside zone bounding box
        lat = bounds["min_lat"] + random.random() * (bounds["max_lat"] - bounds["min_lat"])
        lng = bounds["min_lng"] + random.random() * (bounds["max_lng"] - bounds["min_lng"])

        # Clamp strictly to Pune city boundary
        lat = max(PUNE_BOUNDS["min_latitude"] + 0.005, min(PUNE_BOUNDS["max_latitude"] - 0.005, lat))
        lng = max(PUNE_BOUNDS["min_longitude"] + 0.005, min(PUNE_BOUNDS["max_longitude"] - 0.005, lng))

        lats[i] = round(lat, 6)
        lngs[i] = round(lng, 6)
        wards.append(random.choice(cfg["wards"]))
        localities.append(random.choice(cfg["localities"]))

    # Defensible degradation physics for failure target & RUL
    # Risk calculation incorporating age, corrosion, maintenance delay, structural score, and usage
    base_risk = (
        (age_years / 60.0) * 20.0
        + (corrosion_level / 100.0) * 22.0
        + (np.maximum(0.0, 365.0 - days_since_maintenance) / 365.0) * 6.0
        + (previous_failures * 7.0)
        + (np.maximum(0.0, 100.0 - structural_score) / 100.0) * 26.0
        + (traffic_density / 100.0) * 14.0
        + (maintenance_count * 1.5)
    )

    # Asset type and zone specific modifiers
    zone_mod = np.where(zones == "Industrial", 10.0, 0.0)
    type_mod = np.where(np.isin(asset_types, ["Bridge", "Pipeline"]), 8.0, 0.0)
    mat_mod = np.where(materials == "Steel", 4.0, 0.0)

    risk_score = base_risk + zone_mod + type_mod + mat_mod
    failure_probability = np.clip(risk_score / 100.0, 0.04, 0.96)

    # Stochastic failure incident based on probability
    rand_draw = np.random.uniform(0.0, 1.0, size=num_rows)
    failure = (rand_draw < failure_probability).astype(int)

    # RUL (Remaining Useful Life in years) - strictly non-negative
    rul_raw = (
        32.0
        - (age_years * 0.65)
        - (corrosion_level * 0.18)
        + (structural_score * 0.17)
        - (days_since_maintenance * 0.015)
        - (traffic_density * 0.04)
    )
    remaining_useful_life = np.round(np.maximum(0.0, rul_raw), 2)

    # Overall condition score
    condition_score = np.round(
        np.clip((structural_score * 0.6) + ((100.0 - corrosion_level) * 0.4), 0.0, 100.0), 1
    )

    # Risk level classification
    risk_level = np.where(
        failure_probability >= 0.70, "HIGH",
        np.where(failure_probability >= 0.35, "MEDIUM", "LOW")
    )

    asset_ids = [f"ASSET-{i:06d}" for i in range(1, num_rows + 1)]

    df = pd.DataFrame({
        "asset_id": asset_ids,
        "asset_type": asset_types,
        "zone": zones,
        "pune_ward": wards,
        "locality": localities,
        "latitude": lats,
        "longitude": lngs,
        "material": materials,
        "age_years": age_years,
        "traffic_density": traffic_density,
        "average_load": average_load,
        "annual_rainfall": annual_rainfall,
        "average_temperature": average_temperature,
        "maintenance_count": maintenance_count,
        "days_since_maintenance": days_since_maintenance,
        "days_since_inspection": days_since_inspection,
        "structural_score": structural_score,
        "corrosion_level": corrosion_level,
        "previous_failures": previous_failures,
        "usage_intensity": usage_intensity,
        "condition_score": condition_score,
        "failure_probability": np.round(failure_probability, 4),
        "risk_level": risk_level,
        "remaining_useful_life": remaining_useful_life,
        "failure": failure,
    })

    # Introduce sparse realistic missingness for imputer testing (0.5% - 1%)
    # Keep it minimal so domain validation passes cleanly
    nan_mask_maint = np.random.choice([False, True], size=num_rows, p=[0.985, 0.015])
    df.loc[nan_mask_maint, "days_since_maintenance"] = np.nan

    nan_mask_struct = np.random.choice([False, True], size=num_rows, p=[0.99, 0.01])
    df.loc[nan_mask_struct, "structural_score"] = np.nan

    duration = time.time() - t0
    print(f"Generated {len(df):,} records in {duration:.2f} seconds.")
    return df


def main():
    parser = argparse.ArgumentParser(description="Generate Pune Infrastructure Telemetry Dataset")
    parser.add_argument("--rows", type=int, default=100000, help="Number of records to generate (min 100000)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible generation")
    parser.add_argument("--skip-db", action="store_true", help="Skip synchronizing SQLite database")
    args = parser.parse_args()

    num_rows = max(100000, args.rows)
    df = generate_pune_dataset(num_rows=num_rows, seed=args.seed)

    # Verify Pune boundary
    all_within = all(is_within_pune(lat, lng) for lat, lng in zip(df["latitude"], df["longitude"]))
    assert all_within, "Verification failed: some generated coordinates fall outside Pune bounds!"

    # Save to CSV
    print(f"Saving dataset to {DATA_PATH}...")
    df.to_csv(DATA_PATH, index=False)
    print(f"CSV saved ({DATA_PATH.stat().st_size / (1024*1024):.2f} MB).")

    # Sync to SQLite for high-speed indexing & spatial queries
    if not args.skip_db:
        print("Synchronizing SQLite database infrastructure.db...")
        sync_dataframe_to_db(df)
        print("Database synchronized successfully.")


if __name__ == "__main__":
    main()
