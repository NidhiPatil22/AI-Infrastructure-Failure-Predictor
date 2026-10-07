from __future__ import annotations

from fastapi import APIRouter

from app.database.database import get_prediction_history

router = APIRouter()


@router.get('/infrastructure')
def infrastructure_assets():
    history = get_prediction_history(limit=20)
    return {
        'assets': [
            {
                'asset_id': record['asset_id'],
                'asset_type': record['asset_type'],
                'zone': record['zone'],
                'risk_level': record['risk_level'],
                'remaining_useful_life': record['remaining_useful_life'],
                'recommendation': record['recommendation'],
            }
            for record in history
        ],
    }
