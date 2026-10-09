from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.ml.preprocessing import build_preprocessor, clean_dataset


def train_regression_models(df: pd.DataFrame):
    df = clean_dataset(df)
    feature_columns = ['asset_type', 'zone', 'material', 'age_years', 'traffic_density', 'average_load',
                       'annual_rainfall', 'average_temperature', 'maintenance_count', 'days_since_maintenance',
                       'days_since_inspection', 'structural_score', 'corrosion_level', 'previous_failures',
                       'usage_intensity']
    feature_columns += ['infrastructure_age', 'maintenance_frequency', 'inspection_gap', 'failure_history_score',
                        'maintenance_delay_score', 'environmental_stress', 'load_stress', 'overall_condition_score']

    X = df[feature_columns]
    y = df['remaining_useful_life']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = build_preprocessor(X_train)
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(random_state=42, n_estimators=300),
    }

    metrics = {}
    for name, model in models.items():
        model.fit(X_train_t, y_train)
        pred = model.predict(X_test_t)
        metrics[name] = {
            'mae': round(float(mean_absolute_error(y_test, pred)), 4),
            'rmse': round(float(np.sqrt(mean_squared_error(y_test, pred))), 4),
            'r2': round(float(r2_score(y_test, pred)), 4),
        }

    best_model_name = max(metrics, key=lambda key: metrics[key]['r2'])
    return {
        'preprocessor': preprocessor,
        'model': models[best_model_name],
        'metrics': metrics,
        'best_model_name': best_model_name,
        'feature_columns': feature_columns,
    }
