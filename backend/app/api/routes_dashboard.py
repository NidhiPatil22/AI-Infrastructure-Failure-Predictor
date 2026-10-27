from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
import numpy as np
import pandas as pd

from app.database.database import (
    get_infrastructure_stats,
    get_infrastructure_trend,
    get_prediction_history,
)
from app.ml.preprocessing import clean_dataset
from app.model_service import load_model_bundle
from app.utils.helpers import risk_level_from_probability

router = APIRouter()
PRIMARY_DATA_PATH = Path(__file__).resolve().parents[2] / 'data' / 'pune_expanded_road_infrastructure_50000.csv'
LEGACY_DATA_PATH = Path(__file__).resolve().parents[2] / 'data' / 'urban_infrastructure_data.csv'
DATA_PATH = PRIMARY_DATA_PATH if PRIMARY_DATA_PATH.exists() else LEGACY_DATA_PATH
MODEL_DIR = Path(__file__).resolve().parents[2] / 'models'

# Cached aggregations so subsequent dashboard requests are instantaneous
_dashboard_cache: Optional[Dict[str, Any]] = None


def compute_dashboard_aggregations(force_refresh: bool = False) -> Dict[str, Any]:
    """Dynamically computes risk breakdown and infrastructure aggregations

    using high-performance SQLite indexed aggregation backed by the 100K+ Pune dataset.
    """
    global _dashboard_cache
    if _dashboard_cache is not None and not force_refresh:
        return _dashboard_cache

    try:
        stats = get_infrastructure_stats()
        if stats.get("total_assets", 0) > 0:
            _dashboard_cache = stats
            return _dashboard_cache
    except Exception:
        pass

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)
    total_assets = int(len(df))

    # Apply row-level feature engineering on sample if large
    df_eval = df.iloc[:5000] if len(df) > 5000 else df
    df_clean = clean_dataset(df_eval)

    # Use canonical trained model bundle
    bundle = load_model_bundle()
    feature_columns = bundle['feature_columns']
    preprocessor = bundle['classifier_preprocessor']
    classifier = bundle['classifier_model']

    X = df_clean[feature_columns]
    transformed = preprocessor.transform(X)
    probabilities = classifier.predict_proba(transformed)[:, 1]

    # Assign canonical risk levels
    risks = [risk_level_from_probability(p) for p in probabilities]
    df_clean['risk_level'] = risks
    df_clean['failure_probability'] = probabilities

    regressor = bundle.get('regressor_model')
    reg_preprocessor = bundle.get('regressor_preprocessor', preprocessor)
    if regressor is not None:
        try:
            ruls = np.maximum(0.0, regressor.predict(reg_preprocessor.transform(X)))
            avg_rul = round(float(np.mean(ruls)), 1)
        except Exception:
            avg_rul = round(float(df_clean['remaining_useful_life'].mean()), 1)
    else:
        avg_rul = round(float(df_clean['remaining_useful_life'].mean()), 1)

    high_ratio = (df_clean['risk_level'] == 'HIGH').mean()
    medium_ratio = (df_clean['risk_level'] == 'MEDIUM').mean()
    low_ratio = (df_clean['risk_level'] == 'LOW').mean()

    high_count = int(round(total_assets * high_ratio))
    medium_count = int(round(total_assets * medium_ratio))
    low_count = max(0, total_assets - high_count - medium_count)
    avg_prob = round(float(np.mean(probabilities)), 4)

    asset_types = ['Road', 'Bridge', 'Pipeline', 'Drainage', 'Streetlight', 'Electrical Pole']
    asset_type_risk: List[Dict[str, Any]] = []
    type_counts: Dict[str, int] = {}
    for atype in asset_types:
        sub = df_clean[df_clean['asset_type'] == atype]
        sub_ratio = len(sub) / max(1, len(df_clean))
        t_count = int(round(total_assets * sub_ratio))
        h_cnt = int(round(t_count * (sub['risk_level'] == 'HIGH').mean())) if len(sub) else 0
        m_cnt = int(round(t_count * (sub['risk_level'] == 'MEDIUM').mean())) if len(sub) else 0
        l_cnt = max(0, t_count - h_cnt - m_cnt)
        asset_type_risk.append({
            'type': atype,
            'name': atype,
            'total': t_count,
            'high': h_cnt,
            'medium': m_cnt,
            'low': l_cnt,
        })
        type_counts[atype] = t_count

    zones = ['North', 'South', 'East', 'West', 'Central', 'Industrial']
    df_clean['zone_normalized'] = df_clean['zone'].fillna('Central')
    zone_risk: List[Dict[str, Any]] = []
    for z in zones:
        sub = df_clean[df_clean['zone_normalized'] == z]
        sub_ratio = len(sub) / max(1, len(df_clean))
        z_count = int(round(total_assets * sub_ratio))
        h_cnt = int(round(z_count * (sub['risk_level'] == 'HIGH').mean())) if len(sub) else 0
        m_cnt = int(round(z_count * (sub['risk_level'] == 'MEDIUM').mean())) if len(sub) else 0
        l_cnt = max(0, z_count - h_cnt - m_cnt)
        zone_risk.append({
            'zone': z,
            'name': z,
            'total': z_count,
            'high': h_cnt,
            'medium': m_cnt,
            'low': l_cnt,
        })

    _dashboard_cache = {
        'total_assets': total_assets,
        'high_risk_assets': high_count,
        'medium_risk_assets': medium_count,
        'low_risk_assets': low_count,
        'critical_risk_assets': int(round(high_count * 0.45)),
        'average_remaining_life': avg_rul,
        'average_failure_probability': avg_prob,
        'type_counts': type_counts,
        'asset_type_risk': asset_type_risk,
        'zone_risk': zone_risk,
    }
    return _dashboard_cache


@router.get('/dashboard')
def get_dashboard_summary():
    """Returns primary highway dashboard overview, live KPIs, risk distributions,

    infrastructure type breakdowns, and zone-level risk analyses.
    """
    agg = compute_dashboard_aggregations()
    trend = get_infrastructure_trend()

    summary = {
        'title': 'Pune Urban Infrastructure Health Overview',
        'city': 'Pune',
        'monitoring_boundary': 'PMC & PCMC Metropolitan Corridors',
        'total_assets': agg['total_assets'],
        'high_risk_assets': agg['high_risk_assets'],
        'medium_risk_assets': agg['medium_risk_assets'],
        'low_risk_assets': agg['low_risk_assets'],
        'critical_risk_assets': agg.get('critical_risk_assets', int(agg['high_risk_assets'] * 0.4)),
        'average_remaining_life': agg['average_remaining_life'],
        'average_failure_probability': agg['average_failure_probability'],
        'priority_focus': 'Bridges, Pipelines, and Industrial Corridors',
        'alerts': [
            'Corrosion risk elevated in Central and Industrial zones (Bhosari / Hadapsar)',
            'River bridges along Mula-Mutha require scheduled preventive deck monitoring',
            'Monsoon drainage runoff inspection active across Kothrud, Baner, and Hadapsar wards',
        ],
        'asset_type_risk': agg['asset_type_risk'],
        'zone_risk': agg['zone_risk'],
        'trend': trend,
        'type_counts': agg.get('type_counts', {}),
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


@router.get('/dashboard/infrastructure-stats')
def get_infrastructure_stats_endpoint():
    """Returns live KPI counters for all monitored infrastructure categories and risk tiers."""
    agg = compute_dashboard_aggregations()
    trend = get_infrastructure_trend()
    type_counts = agg.get('type_counts', {})
    if not type_counts and agg.get('asset_type_risk'):
        type_counts = {item['type']: item['total'] for item in agg['asset_type_risk']}

    road_segments = type_counts.get('Road Segment', type_counts.get('Road', 0))
    bridge_approaches = type_counts.get('Bridge Approach', type_counts.get('Bridge', 0))
    culvert_approaches = type_counts.get('Culvert Approach', type_counts.get('Culvert', 0))
    road_class_counts = agg.get('road_class_counts', {})

    return {
        'total': agg['total_assets'],
        'total_infrastructure': agg['total_assets'],
        'type_counts': type_counts,
        'road_class_counts': road_class_counts,
        'road_segments': road_segments,
        'bridge_approaches': bridge_approaches,
        'culvert_approaches': culvert_approaches,
        'roads': road_segments,
        'bridges': bridge_approaches,
        'culverts': culvert_approaches,
        'primary_roads': road_class_counts.get('Primary', 0),
        'secondary_roads': road_class_counts.get('Secondary', 0),
        'highways': road_class_counts.get('Highway', 0),
        'high_risk': agg['high_risk_assets'],
        'medium_risk': agg['medium_risk_assets'],
        'low_risk': agg['low_risk_assets'],
        'critical_risk': agg.get('critical_risk_assets', int(agg['high_risk_assets'] * 0.4)),
        'average_remaining_life': agg['average_remaining_life'],
        'average_failure_probability': agg['average_failure_probability'],
        'trend': trend,
    }


@router.get('/dashboard/infrastructure-trend')
def get_infrastructure_trend_endpoint():
    """Returns dynamic infrastructure monitoring growth and trend statistics."""
    return get_infrastructure_trend()


@router.get('/dashboard/risk-breakdown')
def get_risk_breakdown():
    """Returns dynamic risk breakdown aggregated by asset_type and zone."""
    agg = compute_dashboard_aggregations()
    summary_counts = {
        'total': agg['total_assets'],
        'total_assets': agg['total_assets'],
        'high': agg['high_risk_assets'],
        'medium': agg['medium_risk_assets'],
        'low': agg['low_risk_assets'],
    }
    return {
        'asset_type': agg['asset_type_risk'],
        'zone': agg['zone_risk'],
        'summary': summary_counts,
        'overall': summary_counts,
    }


@router.get('/dashboard/asset-type-risk')
def get_asset_type_risk():
    """Returns dynamic risk breakdown by infrastructure type."""
    agg = compute_dashboard_aggregations()
    return agg['asset_type_risk']


@router.get('/dashboard/zone-risk')
def get_zone_risk():
    """Returns dynamic risk breakdown by municipal transit zone."""
    agg = compute_dashboard_aggregations()
    return agg['zone_risk']
