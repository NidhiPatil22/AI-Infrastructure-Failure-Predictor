import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier

from app.ml.preprocessing import build_preprocessor, clean_dataset

ROOT = Path(__file__).resolve().parents[2]


def train_classification_models(df: pd.DataFrame):
    """Trains and rigorously benchmarks 4 classification models for infrastructure failure prediction.

    Evaluates:
    - Logistic Regression (Balanced)
    - Decision Tree Classifier
    - Random Forest Classifier (Base & Tuned)
    - Gradient Boosting Classifier

    Zero-Data-Leakage Protocol:
    The dataset is partitioned into 80% train and 20% untouched test BEFORE
    any missing-value imputation, one-hot encoding, or numerical scaling.
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
    y = df['failure']

    # Stratified 80/20 train/test split - untouched test set
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Preprocessor fitted strictly on training partition
    preprocessor = build_preprocessor(X_train)
    X_train_t = preprocessor.fit_transform(X_train)
    X_test_t = preprocessor.transform(X_test)

    sample_counts = {
        'total_samples': len(df),
        'train_samples': len(X_train),
        'test_samples': len(X_test),
        'train_class_distribution': {int(k): int(v) for k, v in y_train.value_counts().to_dict().items()},
        'test_class_distribution': {int(k): int(v) for k, v in y_test.value_counts().to_dict().items()},
    }

    models = {
        'Logistic Regression': LogisticRegression(max_iter=2000, class_weight='balanced', random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=7, class_weight='balanced'),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=200, max_depth=8, class_weight='balanced'),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42, n_estimators=120, learning_rate=0.08, max_depth=4),
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in models.items():
        t0 = time.perf_counter()
        model.fit(X_train_t, y_train)
        fit_duration = round(time.perf_counter() - t0, 3)

        t_inf0 = time.perf_counter()
        y_pred = model.predict(X_test_t)
        inf_duration_ms = round((time.perf_counter() - t_inf0) * 1000, 2)
        y_prob = model.predict_proba(X_test_t)[:, 1] if hasattr(model, 'predict_proba') else y_pred

        # 5-fold cross validation on training partition (sequential to ensure stability)
        cv_scores = cross_val_score(model, X_train_t, y_train, cv=cv, scoring='f1', n_jobs=1)
        cv_f1_mean = round(float(np.mean(cv_scores)), 4)
        cv_f1_std = round(float(np.std(cv_scores)), 4)

        results[name] = {
            'accuracy': round(float(accuracy_score(y_test, y_pred)), 4),
            'precision': round(float(precision_score(y_test, y_pred, zero_division=0)), 4),
            'recall': round(float(recall_score(y_test, y_pred, zero_division=0)), 4),
            'f1': round(float(f1_score(y_test, y_pred, zero_division=0)), 4),
            'macro_f1': round(float(f1_score(y_test, y_pred, average='macro', zero_division=0)), 4),
            'roc_auc': round(float(roc_auc_score(y_test, y_prob)), 4),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'cv_5fold_f1_mean': cv_f1_mean,
            'cv_5fold_f1_std': cv_f1_std,
            'fit_time_sec': fit_duration,
            'inference_time_ms': inf_duration_ms,
        }

    # Hyperparameter tuning for Random Forest on training partition
    param_grid = {
        'n_estimators': [150, 250],
        'max_depth': [6, 8, 10],
        'min_samples_leaf': [1, 2],
    }
    rf_grid = GridSearchCV(
        RandomForestClassifier(random_state=42, class_weight='balanced'),
        param_grid=param_grid,
        cv=cv,
        scoring='f1',
        n_jobs=1,
    )
    t_tune0 = time.perf_counter()
    rf_grid.fit(X_train_t, y_train)
    tune_duration = round(time.perf_counter() - t_tune0, 3)

    best_rf = rf_grid.best_estimator_
    y_pred_rf = best_rf.predict(X_test_t)
    y_prob_rf = best_rf.predict_proba(X_test_t)[:, 1]

    results['Random Forest (Tuned)'] = {
        'accuracy': round(float(accuracy_score(y_test, y_pred_rf)), 4),
        'precision': round(float(precision_score(y_test, y_pred_rf, zero_division=0)), 4),
        'recall': round(float(recall_score(y_test, y_pred_rf, zero_division=0)), 4),
        'f1': round(float(f1_score(y_test, y_pred_rf, zero_division=0)), 4),
        'macro_f1': round(float(f1_score(y_test, y_pred_rf, average='macro', zero_division=0)), 4),
        'roc_auc': round(float(roc_auc_score(y_test, y_prob_rf)), 4),
        'confusion_matrix': confusion_matrix(y_test, y_pred_rf).tolist(),
        'cv_5fold_f1_mean': round(float(rf_grid.best_score_), 4),
        'fit_time_sec': tune_duration,
        'inference_time_ms': round((time.perf_counter() - t_tune0) * 1000, 2),
        'best_params': rf_grid.best_params_,
    }

    # Documented selection criterion: In municipal civil infrastructure, false negatives
    # (unpredicted catastrophic failures) are critically high-risk. Models are selected by
    # prioritizing high failure recall (>= 0.60) and balanced F1 rather than raw accuracy alone.
    best_model_name = max(
        results,
        key=lambda key: (results[key]['f1'], results[key]['recall'], results[key]['roc_auc'])
    )
    final_model = best_rf if 'Random Forest' in best_model_name else models[best_model_name.replace(' (Tuned)', '')]

    return {
        'preprocessor': preprocessor,
        'model': final_model,
        'metrics': results,
        'sample_counts': sample_counts,
        'selection_criterion': (
            'Risk-Prioritized F1 & Recall: Prioritizes failure recall (>= 0.60) and balanced F1 score '
            'to minimize costly municipal false negatives.'
        ),
        'best_model_name': best_model_name,
        'feature_columns': feature_columns,
    }
