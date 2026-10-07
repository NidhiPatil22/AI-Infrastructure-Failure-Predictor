from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd

from app.ml.classification import train_classification_models
from app.ml.clustering import train_clustering
from app.ml.regression import train_regression_models

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'urban_infrastructure_data.csv'
MODEL_DIR = ROOT / 'models'
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def save_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload, indent=2), encoding='utf-8')


def main():
    df = pd.read_csv(DATA_PATH)

    classification = train_classification_models(df)
    regression = train_regression_models(df)
    clustering = train_clustering(df)

    bundle = {
        'classifier_model': classification['model'],
        'classifier_preprocessor': classification['preprocessor'],
        'regressor_model': regression['model'],
        'regressor_preprocessor': regression['preprocessor'],
        'feature_columns': classification['feature_columns'],
        'classification_metrics': classification['metrics'],
        'regression_metrics': regression['metrics'],
        'clustering_summary': clustering['cluster_summary'],
        'selected_k': clustering['selected_k'],
        'silhouette_values': clustering['silhouette_values'],
    }

    joblib.dump(bundle, MODEL_DIR / 'model_bundle.pkl')
    save_json(MODEL_DIR / 'model_results.json', classification['metrics'])
    save_json(MODEL_DIR / 'regression_results.json', regression['metrics'])
    save_json(MODEL_DIR / 'cluster_results.json', {
        'selected_k': clustering['selected_k'],
        'silhouette_values': clustering['silhouette_values'],
        'cluster_summary': clustering['cluster_summary'],
    })

    print('Model training completed. Artifacts written to', MODEL_DIR)


if __name__ == '__main__':
    main()
