"""
Script to train AutoML model using FLAML Tabular and generate
a head-to-head comparison against manual models on identical test data.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd

from app.ml.automl import run_automl_training
DATA_PATH = ROOT / "data" / "urban_infrastructure_data.csv"
REPORTS_DIR = ROOT / "reports"
MODELS_DIR = ROOT / "models"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    print("Starting FLAML AutoML Benchmark...")
    automl_res = run_automl_training(data_path=DATA_PATH, time_budget_sec=25)

    # Save trained AutoML model
    automl_model = automl_res["automl_model"]
    joblib.dump(automl_model, MODELS_DIR / "automl_classifier.pkl")

    # Load manual models results for direct comparison
    mlflow_results_path = REPORTS_DIR / "mlflow_experiment_results.json"
    manual_models = []
    if mlflow_results_path.exists():
        all_exp = json.loads(mlflow_results_path.read_text(encoding="utf-8"))
        manual_models = [e for e in all_exp if e["task"] == "Classification"]

    comparison = {
        "automl_summary": automl_res["automl_metrics"],
        "comparison_table": [
            {
                "Model": m["model_name"],
                "Type": "Manual Baseline",
                "Accuracy": m["accuracy"],
                "Precision": m["precision"],
                "Recall": m["recall"],
                "F1_Score": m["f1_score"],
                "ROC_AUC": m["roc_auc"],
                "Training_Time_Sec": m["train_time_sec"],
            }
            for m in manual_models
        ] + [
            {
                "Model": automl_res["automl_metrics"]["model_type"],
                "Type": "AutoML (FLAML)",
                "Accuracy": automl_res["automl_metrics"]["accuracy"],
                "Precision": automl_res["automl_metrics"]["precision"],
                "Recall": automl_res["automl_metrics"]["recall"],
                "F1_Score": automl_res["automl_metrics"]["f1_score"],
                "ROC_AUC": automl_res["automl_metrics"]["roc_auc"],
                "Training_Time_Sec": automl_res["automl_metrics"]["actual_training_seconds"],
            }
        ],
        "methodology": {
            "data_split": "80% Train, 20% Held-out Test (Stratified by failure target)",
            "leakage_prevention": "Strict train-test isolation: feature imputers, transformations, and model fitting applied only on training split; evaluated once on unseen test fold.",
            "computational_environment": "CPU training with time-budget bounded search (25s budget).",
        },
    }

    out_file = REPORTS_DIR / "automl_comparison_results.json"
    out_file.write_text(json.dumps(comparison, indent=2), encoding="utf-8")
    print(f"\nAutoML training completed successfully. Results saved to {out_file}")
    print("Comparison summary:")
    print(pd.DataFrame(comparison["comparison_table"]).to_string(index=False))


if __name__ == "__main__":
    main()
