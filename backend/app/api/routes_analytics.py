from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter

router = APIRouter()
MODEL_DIR = Path(__file__).resolve().parents[2] / 'models'


@router.get('/analytics')
def get_analytics():
    payload = {
        'model_summary': {
            'classification_models': ['Logistic Regression', 'Decision Tree', 'Random Forest', 'Random Forest (Tuned)'],
            'regression_models': ['Linear Regression', 'Random Forest Regressor'],
            'clustering': 'K-Means with PCA',
        },
        'insights': [
            'Corrosion level and maintenance gap are the strongest predictors for risk.',
            'Older bridges and pipelines are more likely to require urgent maintenance.',
            'Industrial and central zones produce the highest failure concentration.',
        ],
    }

    for filename in ['model_results.json', 'regression_results.json', 'cluster_results.json']:
        path = MODEL_DIR / filename
        if path.exists():
            try:
                with path.open('r', encoding='utf-8') as fh:
                    payload[filename.replace('.json', '')] = json.load(fh)
            except Exception:
                pass

    return payload
