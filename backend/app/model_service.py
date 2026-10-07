from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

from app.ml.preprocessing import clean_dataset
from app.utils.helpers import format_probability, priority_from_prediction, risk_level_from_probability

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

    input_df = pd.DataFrame([record])
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

    projected = {
        'asset_id': record.get('asset_id', 'ASSET-001'),
        'asset_type': record.get('asset_type'),
        'zone': record.get('zone'),
        'failure_probability': round(float(probability), 4),
        'risk_level': predicted_risk,
        'remaining_useful_life': round(float(remaining_life), 2),
        'priority': priority_from_prediction(float(probability), float(record.get('structural_score', 50)), int(record.get('previous_failures', 0)), float(record.get('days_since_maintenance', 0))),
        'recommendation': recommendation,
        'key_factors': {
            'corrosion_level': record.get('corrosion_level', 0),
            'structural_score': record.get('structural_score', 0),
            'days_since_maintenance': record.get('days_since_maintenance', 0),
            'previous_failures': record.get('previous_failures', 0),
        },
        'failure_probability_percent': format_probability(probability),
    }
    return projected
