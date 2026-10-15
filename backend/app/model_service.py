from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import joblib
import pandas as pd

from app.ml.preprocessing import clean_dataset
from app.utils.helpers import format_probability, priority_from_prediction, risk_level_from_probability
from app.utils.indian_geo import map_realistic_inputs_to_model_features, resolve_indian_zone

MODEL_DIR = Path(__file__).resolve().parent.parent / 'models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_model_bundle():
    bundle_path = MODEL_DIR / 'model_bundle.pkl'
    if not bundle_path.exists():
        raise FileNotFoundError('Model bundle not found. Run training first.')
    with bundle_path.open('rb') as fh:
        return joblib.load(fh)


def build_prediction_payload(record: dict) -> dict:
    bundle = load_model_bundle()
    feature_columns = bundle['feature_columns']

    # Detect if record is a simplified/realistic input or legacy technical input
    is_realistic = ('condition' in record or 'traffic_level' in record or 'maintenance_recency' in record or
                    ('structural_score' not in record and 'corrosion_level' not in record))

    if is_realistic:
        model_record, geo_metadata = map_realistic_inputs_to_model_features(record)
    else:
        model_record = record.copy()
        # If location is present in legacy input, resolve zone if not given
        loc = record.get('location') or {}
        addr = loc.get('address') or record.get('address')
        if not model_record.get('zone') and addr:
            model_record['zone'] = resolve_indian_zone(
                address=addr,
                state=loc.get('state'),
                city=loc.get('city'),
                latitude=loc.get('latitude'),
                longitude=loc.get('longitude'),
            )
        geo_metadata = {
            'address': addr or 'Municipal Civil Corridor',
            'latitude': loc.get('latitude') or record.get('latitude'),
            'longitude': loc.get('longitude') or record.get('longitude'),
            'city': loc.get('city'),
            'state': loc.get('state'),
            'resolved_zone': model_record.get('zone', 'Central'),
        }

    input_df = pd.DataFrame([model_record])
    input_df = clean_dataset(input_df)
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    X = input_df[feature_columns]
    preprocessor = bundle['classifier_preprocessor']
    transformed = preprocessor.transform(X)
    probability = bundle['classifier_model'].predict_proba(transformed)[0, 1]
    predicted_risk = risk_level_from_probability(probability)

    regressor = bundle['regressor_model']
    reg_input = input_df[feature_columns]
    remaining_life = max(0.0, float(regressor.predict(preprocessor.transform(reg_input))[0]))

    recommendation = (
        'Immediate inspection and preventive maintenance required.' if predicted_risk == 'HIGH'
        else 'Schedule routine monitoring and targeted repairs.' if predicted_risk == 'MEDIUM'
        else 'Continue regular maintenance with periodic checks.'
    )

    structural_score = float(model_record.get('structural_score', 60.0))
    corrosion_level = float(model_record.get('corrosion_level', 40.0))
    prev_failures = int(model_record.get('previous_failures', 0))
    days_since_maint = float(model_record.get('days_since_maintenance', 180.0))

    priority = priority_from_prediction(
        float(probability),
        structural_score,
        prev_failures,
        days_since_maint,
    )

    projected = {
        'asset_id': model_record.get('asset_id', 'ASSET-001'),
        'asset_type': model_record.get('asset_type'),
        'zone': model_record.get('zone'),
        'material': model_record.get('material', 'Concrete'),
        'age_years': model_record.get('age_years'),
        'failure_probability': round(float(probability), 4),
        'risk_level': predicted_risk,
        'remaining_useful_life': round(float(remaining_life), 2),
        'priority': priority,
        'recommendation': recommendation,
        'location': {
            'address': geo_metadata.get('address'),
            'latitude': geo_metadata.get('latitude'),
            'longitude': geo_metadata.get('longitude'),
            'city': geo_metadata.get('city'),
            'state': geo_metadata.get('state'),
            'resolved_zone': geo_metadata.get('resolved_zone'),
        },
        'geo_metadata': geo_metadata,
        'key_factors': {
            'corrosion_level': round(corrosion_level, 1),
            'structural_score': round(structural_score, 1),
            'days_since_maintenance': round(days_since_maint, 1),
            'previous_failures': prev_failures,
            'traffic_density': round(float(model_record.get('traffic_density', 50.0)), 1),
        },
        'failure_probability_percent': format_probability(probability),
        'data_limitations': (
            'Evaluated via trained Random Forest and linear regression on 2,200 municipal benchmark records. '
            'Location coordinates establish regional environmental baselines. Does not replace statutory civil structural audits.'
        ),
    }
    return projected
