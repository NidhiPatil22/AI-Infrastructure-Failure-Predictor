from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.database.database import save_prediction_history
from app.model_service import build_prediction_payload
from app.schemas.prediction_schema import AssetInput

router = APIRouter()


@router.get('/prediction-demo')
def prediction_demo():
    sample = {
        'asset_id': 'ASSET-001',
        'asset_type': 'Bridge',
        'zone': 'Central',
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
    }
    return build_prediction_payload(sample)


@router.post('/predict')
def predict_risk(payload: AssetInput):
    try:
        record = payload.model_dump()
        response = build_prediction_payload(record)
        save_prediction_history(response)
        return response
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail='Model bundle is not trained yet. Run the training script first.') from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=f'Prediction failed: {str(exc)}') from exc
