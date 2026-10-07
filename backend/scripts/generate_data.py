from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'urban_infrastructure_data.csv'
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

ASSET_TYPES = ['Road', 'Bridge', 'Pipeline', 'Drainage', 'Streetlight', 'Electrical Pole']
ZONES = ['North', 'South', 'East', 'West', 'Central', 'Industrial']
MATERIALS = ['Concrete', 'Steel', 'PVC', 'Asphalt', 'Copper', 'Composite']


random.seed(42)
np.random.seed(42)


def generate_row(idx: int):
    asset_type = random.choice(ASSET_TYPES)
    zone = random.choice(ZONES)
    material = random.choice(MATERIALS)
    age_years = max(1.0, min(60.0, round(np.random.normal(18, 10), 2)))
    traffic_density = max(10, min(95, round(np.random.normal(55, 20), 2)))
    average_load = max(20, min(180, round(np.random.normal(95, 30), 2)))
    annual_rainfall = max(200, min(3500, round(np.random.normal(1200, 600), 2)))
    average_temperature = max(-5, min(45, round(np.random.normal(25, 9), 2)))
    maintenance_count = max(0, min(25, int(np.random.normal(4, 2))))
    days_since_maintenance = max(0, min(600, round(np.random.normal(120, 80), 2)))
    days_since_inspection = max(0, min(900, round(np.random.normal(180, 100), 2)))
    structural_score = max(20, min(100, round(np.random.normal(72, 18), 2)))
    corrosion_level = max(0, min(100, round(np.random.normal(35, 20), 2)))
    previous_failures = max(0, min(8, int(np.random.normal(1.5, 1.5))))
    usage_intensity = max(10, min(100, round(np.random.normal(58, 18), 2)))

    risk_score = (
        (age_years / 60) * 18
        + (corrosion_level / 100) * 20
        + (max(0, 365 - days_since_maintenance) / 365) * 8
        + (previous_failures * 8)
        + (max(0, 100 - structural_score) / 100) * 25
        + (traffic_density / 100) * 15
        + (maintenance_count * 2)
    )

    if zone == 'Industrial':
        risk_score += 12
    if asset_type in {'Bridge', 'Pipeline'}:
        risk_score += 10
    if material == 'Steel':
        risk_score += 5

    failure_probability = min(0.98, max(0.05, risk_score / 100))
    failure = 1 if random.random() < failure_probability else 0
    remaining_useful_life = max(1.0, 30 - (age_years * 0.7) - (corrosion_level * 0.2) + (structural_score * 0.18) - (days_since_maintenance * 0.02))

    row = {
        'asset_id': f'ASSET-{idx:04d}',
        'asset_type': asset_type,
        'zone': zone,
        'material': material,
        'age_years': age_years,
        'traffic_density': traffic_density,
        'average_load': average_load,
        'annual_rainfall': annual_rainfall,
        'average_temperature': average_temperature,
        'maintenance_count': maintenance_count,
        'days_since_maintenance': days_since_maintenance,
        'days_since_inspection': days_since_inspection,
        'structural_score': structural_score,
        'corrosion_level': corrosion_level,
        'previous_failures': previous_failures,
        'usage_intensity': usage_intensity,
        'failure': failure,
        'remaining_useful_life': round(remaining_useful_life, 2),
    }

    if idx % 50 == 0:
        row['days_since_maintenance'] = np.nan
    if idx % 100 == 0:
        row['structural_score'] = None
    if idx % 150 == 0:
        row['zone'] = None
    if idx % 200 == 0:
        row['material'] = None
    if idx % 250 == 0:
        row['age_years'] = round(age_years + 20, 2)
    if idx % 300 == 0:
        row['previous_failures'] = 0

    return row


def main():
    rows = [generate_row(i) for i in range(1, 2201)]
    df = pd.DataFrame(rows)
    df.to_csv(DATA_PATH, index=False)
    print(f'Generated {len(df)} rows and saved to {DATA_PATH}')


if __name__ == '__main__':
    main()
