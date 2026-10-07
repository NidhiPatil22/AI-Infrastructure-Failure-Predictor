from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.tree import DecisionTreeClassifier

from app.ml.preprocessing import build_preprocessor, clean_dataset

ROOT = Path(__file__).resolve().parents[2]


def train_classification_models(df: pd.DataFrame):
    df = clean_dataset(df)
    feature_columns = ['asset_type', 'zone', 'material', 'age_years', 'traffic_density', 'average_load',
                       'annual_rainfall', 'average_temperature', 'maintenance_count', 'days_since_maintenance',
                       'days_since_inspection', 'structural_score', 'corrosion_level', 'previous_failures',
                       'usage_intensity']
    feature_columns += ['infrastructure_age', 'maintenance_frequency', 'inspection_gap', 'failure_history_score',
                        'maintenance_delay_score', 'environmental_stress', 'load_stress', 'overall_condition_score']

    X = df[feature_columns]
    y = df['failure']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = build_preprocessor(X_train)
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    models = {
        'Logistic Regression': LogisticRegression(max_iter=2000, class_weight='balanced'),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=7),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=300, class_weight='balanced'),
    }

    results = {}
    for name, model in models.items():
        model.fit(X_train_t, y_train)
        y_pred = model.predict(X_test_t)
        y_prob = model.predict_proba(X_test_t)[:, 1]
        results[name] = {
            'accuracy': round(float(accuracy_score(y_test, y_pred)), 4),
            'precision': round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
            'recall': round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
            'f1': round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
            'roc_auc': round(float(roc_auc_score(y_test, y_prob)), 4),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        }

    param_grid = {
        'n_estimators': [150, 250, 350],
        'max_depth': [6, 8, 10, None],
        'min_samples_leaf': [1, 2, 4],
    }
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=42, class_weight='balanced'),
        param_grid=param_grid,
        cv=StratifiedKFold(n_splits=5),
        scoring='f1',
        n_jobs=-1,
    )
    rf_grid.fit(X_train_t, y_train)
    best_rf = rf_grid.best_estimator_
    y_pred_rf = best_rf.predict(X_test_t)
    y_prob_rf = best_rf.predict_proba(X_test_t)[:, 1]
    results['Random Forest (Tuned)'] = {
        'accuracy': round(float(accuracy_score(y_test, y_pred_rf)), 4),
        'precision': round(float(precision_score(y_test, y_pred_rf, zero_division=0)), 4),
        'recall': round(float(recall_score(y_test, y_pred_rf, zero_division=0)), 4),
        'f1': round(float(f1_score(y_test, y_pred_rf, zero_division=0)), 4),
        'roc_auc': round(float(roc_auc_score(y_test, y_prob_rf)), 4),
        'confusion_matrix': confusion_matrix(y_test, y_pred_rf).tolist(),
        'best_params': rf_grid.best_params_,
    }

    best_model_name = max(results, key=lambda key: (results[key]['f1'], results[key]['recall'], results[key]['roc_auc']))
    final_model = best_rf if 'Random Forest' in best_model_name else models[best_model_name.replace(' (Tuned)', '')]

    return {
        'preprocessor': preprocessor,
        'model': final_model,
        'metrics': results,
        'best_model_name': best_model_name,
        'feature_columns': feature_columns,
    }
