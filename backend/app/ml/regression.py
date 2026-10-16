import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.ml.preprocessing import build_preprocessor, clean_dataset


def train_regression_models(df: pd.DataFrame):
    """Trains and benchmarks 3 regression models for Remaining Useful Life (RUL) estimation.

    Target Definition:
    Remaining Useful Life (years) represents an engineering simulation target derived
    from asset degradation factors. Negative predictions are strictly bounded at 0.0 (end-of-life).

    Zero-Data-Leakage Protocol:
    The dataset is partitioned into 80% train and 20% untouched test BEFORE
    any missing-value imputation or numerical scaling.
    """
    df = clean_dataset(df)
    feature_columns = [
        'asset_type', 'zone', 'material', 'age_years', 'traffic_density', 'average_load',
        'annual_rainfall', 'average_temperature', 'maintenance_count', 'days_since_maintenance',
        'days_since_inspection', 'structural_score', 'corrosion_level', 'previous_failures',
        'usage_intensity'
    ]
    feature_columns += [
        'infrastructure_age', 'maintenance_frequency', 'inspection_gap', 'failure_history_score',
        'maintenance_delay_score', 'environmental_stress', 'load_stress', 'overall_condition_score'
    ]

    X = df[feature_columns]
    y = df['remaining_useful_life']

    # 80/20 train/test split - untouched test partition
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocessor fitted strictly on training partition
    preprocessor = build_preprocessor(X_train)
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    sample_counts = {
        'total_samples': len(df),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
    }

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(random_state=42, n_estimators=150, max_depth=10),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=42, n_estimators=120, learning_rate=0.08, max_depth=4),
    }

    metrics = {}
    for name, model in models.items():
        t0 = time.perf_counter()
        model.fit(X_train_t, y_train)
        fit_duration = round(time.perf_counter() - t0, 3)

        pred_raw = model.predict(X_test_t)
        negative_count = int(np.sum(pred_raw < 0))
        # Physically defensible bounding: RUL cannot be negative (0.0 implies complete structural end-of-life)
        pred = np.clip(pred_raw, 0.0, None)

        metrics[name] = {
            'mae': round(float(mean_absolute_error(y_test, pred)), 4),
            'rmse': round(float(np.sqrt(mean_squared_error(y_test, pred))), 4),
            'r2': round(float(r2_score(y_test, pred)), 4),
            'negative_predictions_raw_count': negative_count,
            'fit_time_sec': fit_duration,
        }

    best_model_name = max(metrics, key=lambda key: metrics[key]['r2'])
    return {
        'preprocessor': preprocessor,
        'model': models[best_model_name],
        'metrics': metrics,
        'sample_counts': sample_counts,
        'best_model_name': best_model_name,
        'feature_columns': feature_columns,
    }
