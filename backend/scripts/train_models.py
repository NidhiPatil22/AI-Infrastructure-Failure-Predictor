from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd

from app.ml.classification import train_classification_models
from app.ml.clustering import train_clustering
from app.ml.regression import train_regression_models
PRIMARY_DATA_PATH = ROOT / 'data' / 'pune_expanded_road_infrastructure_50000.csv'
LEGACY_DATA_PATH = ROOT / 'data' / 'urban_infrastructure_data.csv'
DATA_PATH = PRIMARY_DATA_PATH if PRIMARY_DATA_PATH.exists() else LEGACY_DATA_PATH
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
        'sample_counts': classification.get('sample_counts'),
        'selection_criterion': classification.get('selection_criterion'),
        'best_classifier_name': classification.get('best_model_name'),
        'best_regressor_name': regression.get('best_model_name'),
        'clustering_summary': clustering['cluster_summary'],
        'selected_k': clustering['selected_k'],
        'silhouette_values': clustering['silhouette_values'],
    }

    joblib.dump(bundle, MODEL_DIR / 'model_bundle.pkl')
    save_json(MODEL_DIR / 'model_results.json', {
        'models': classification['metrics'],
        'best_model': classification.get('best_model_name'),
        'sample_counts': classification.get('sample_counts'),
        'selection_criterion': classification.get('selection_criterion'),
    })
    save_json(MODEL_DIR / 'regression_results.json', {
        'models': regression['metrics'],
        'best_model': regression.get('best_model_name'),
        'sample_counts': regression.get('sample_counts'),
    })
    save_json(MODEL_DIR / 'cluster_results.json', {
        'selected_k': clustering['selected_k'],
        'silhouette_values': clustering['silhouette_values'],
        'cluster_summary': clustering['cluster_summary'],
    })

    print('Model training completed. Artifacts written to', MODEL_DIR)


if __name__ == '__main__':
    main()
