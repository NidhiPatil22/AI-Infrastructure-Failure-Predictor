from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter

from app.database.database import get_prediction_history

router = APIRouter()
MODEL_DIR = Path(__file__).resolve().parents[2] / 'models'


@router.get('/dashboard')
def get_dashboard_summary():
    summary = {
        'title': 'Urban Infrastructure Health Overview',
        'total_assets': 2200,
        'high_risk_assets': 348,
        'medium_risk_assets': 742,
        'average_remaining_life': 16.8,
        'priority_focus': 'Bridges and Industrial pipelines',
        'alerts': [
            'Corrosion risk increased in Central and Industrial zones',
            'Bridge decks have the highest maintenance backlog',
            'Routine inspections are overdue in North and East zones',
        ],
    }

    model_results_path = MODEL_DIR / 'model_results.json'
    if model_results_path.exists():
        try:
            with model_results_path.open('r', encoding='utf-8') as fh:
                metrics = json.load(fh)
            summary['classification_metrics'] = metrics
        except Exception:
            pass

    recent_history = get_prediction_history(limit=5)
    summary['recent_predictions'] = recent_history
    return summary
