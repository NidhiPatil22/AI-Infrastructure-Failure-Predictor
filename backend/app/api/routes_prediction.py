from __future__ import annotations

from typing import Any, Dict, List, Union
from fastapi import APIRouter, HTTPException, Request

from app.database.database import save_prediction_history
from app.model_service import build_prediction_payload
from app.schemas.prediction_schema import AssetInput, CorridorAssessmentInput
from app.utils.indian_geo import POPULAR_INDIAN_CORRIDORS

router = APIRouter()


@router.get('/corridors')
def get_popular_corridors() -> List[Dict[str, Any]]:
    """Returns curated major civil corridors across India for quick assessment."""
    return POPULAR_INDIAN_CORRIDORS


@router.get('/prediction-demo')
def prediction_demo():
    sample = {
        'asset_id': 'ASSET-001',
        'asset_type': 'Bridge',
        'zone': 'West',
        'material': 'Concrete',
        'age_years': 27.0,
        'traffic_density': 78.0,
        'average_load': 120.0,
        'annual_rainfall': 1650.0,
        'average_temperature': 28.5,
        'maintenance_count': 6.0,
        'days_since_maintenance': 210.0,
        'days_since_inspection': 320.0,
        'structural_score': 58.0,
        'corrosion_level': 72.0,
        'previous_failures': 2,
        'usage_intensity': 83.0,
        'location': {
            'address': 'Bandra-Worli Sea Link, Mumbai, Maharashtra, India',
            'latitude': 19.0330,
            'longitude': 72.8164,
            'city': 'Mumbai',
            'state': 'Maharashtra',
        },
    }
    return build_prediction_payload(sample)


@router.post('/predict')
async def predict_risk(request: Request):
    """Predicts failure risk and RUL.

    Accepts either simplified realistic inputs (CorridorAssessmentInput)
    with real Indian location, or legacy 15-field technical sensor inputs (AssetInput).
    """
    try:
        body = await request.json()
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object")

        response = build_prediction_payload(body)
        save_prediction_history(response)
        return response
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail='Model bundle is not trained yet. Run the training script first.',
        ) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f'Prediction failed: {str(exc)}') from exc
