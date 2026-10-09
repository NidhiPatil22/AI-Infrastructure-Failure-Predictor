"""
MLflow Experiment Tracking Script for Urban Infrastructure Failure Predictor
Logs classification and regression experiments, hyperparameters, dataset metadata,
evaluation metrics, confusion matrix artifacts, and serialized model files to MLflow.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import time

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Disable MLflow tracing hint and enable file store / sqlite store
os.environ["MLFLOW_DISABLE_AGENT_HINT"] = "1"
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "urban_infrastructure_data.csv"
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
MLRUNS_DB = ROOT / "data" / "mlflow_tracking.db"
ARTIFACTS_DIR = ROOT / "reports" / "mlflow_artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def plot_and_save_confusion_matrix(y_true, y_pred, model_name: str, save_path: Path):
    """Generates and saves a confusion matrix visualization."""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(4.5, 3.8))
    cax = ax.matshow(cm, cmap="Blues", alpha=0.85)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color="black", fontsize=11, fontweight="bold")
    fig.colorbar(cax)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Operational (0)", "Failure (1)"])
    ax.set_yticklabels(["Operational (0)", "Failure (1)"])
    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("True Label")
    ax.set_title(f"Confusion Matrix: {model_name}", pad=14, fontsize=10, fontweight="bold")
    plt.tight_layout()
    fig.savefig(save_path, dpi=150)
    plt.close(fig)


def run_experiments():
    db_uri = f"sqlite:///{MLRUNS_DB.as_posix()}"
    mlflow.set_tracking_uri(db_uri)
    experiment_name = "Urban_Infrastructure_Failure_Prediction"
    mlflow.set_experiment(experiment_name)

    print(f"Loading dataset from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)

    # Feature engineering matching app/ml/preprocessing.py
    feature_cols = [
        "age_years", "traffic_density", "average_load", "annual_rainfall",
        "average_temperature", "maintenance_count", "days_since_maintenance",
        "days_since_inspection", "structural_score", "corrosion_level",
        "previous_failures", "usage_intensity",
    ]
    # Add domain interaction features
    df["infrastructure_age"] = df["age_years"] * (1 + df["usage_intensity"] / 100.0)
    df["maintenance_frequency"] = df["maintenance_count"] / (df["age_years"] + 1.0)
    df["inspection_gap"] = df["days_since_inspection"] / 365.0
    df["failure_history_score"] = df["previous_failures"] * 1.5
    df["load_stress"] = df["traffic_density"] * df["average_load"] / 1000.0
    df["environmental_stress"] = (df["annual_rainfall"] / 1000.0) * (df["corrosion_level"] / 50.0)
    df["overall_condition_score"] = (
        df["structural_score"] - (df["corrosion_level"] * 0.4) - (df["days_since_maintenance"] / 30.0)
    )

    all_features = feature_cols + [
        "infrastructure_age", "maintenance_frequency", "inspection_gap",
        "failure_history_score", "load_stress", "environmental_stress", "overall_condition_score",
    ]

    # Impute and clean
    X = df[all_features].fillna(df[all_features].median())
    y_clf = df["failure"]
    y_reg = df["remaining_useful_life"]

    # Classification Split
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X, y_clf, test_size=0.20, random_state=42, stratify=y_clf
    )

    # Regression Split
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
        X, y_reg, test_size=0.20, random_state=42
    )

    dataset_metadata = {
        "dataset_name": "urban_infrastructure_data.csv",
        "total_records": len(df),
        "total_features": len(all_features),
        "test_size": 0.20,
        "random_state": 42,
    }

    experiment_records = []

    # =========================================================================
    # PART 1: CLASSIFICATION EXPERIMENTS
    # =========================================================================
    classification_models = {
        "Logistic Regression": {
            "model": LogisticRegression(max_iter=1500, class_weight="balanced", random_state=42),
            "params": {"max_iter": 1500, "class_weight": "balanced", "solver": "lbfgs"},
        },
        "Decision Tree": {
            "model": DecisionTreeClassifier(max_depth=7, min_samples_split=10, random_state=42),
            "params": {"max_depth": 7, "min_samples_split": 10, "criterion": "gini"},
        },
        "Random Forest": {
            "model": RandomForestClassifier(n_estimators=250, max_depth=8, class_weight="balanced", random_state=42),
            "params": {"n_estimators": 250, "max_depth": 8, "class_weight": "balanced"},
        },
        "Gradient Boosting": {
            "model": GradientBoostingClassifier(n_estimators=180, learning_rate=0.08, max_depth=5, random_state=42),
            "params": {"n_estimators": 180, "learning_rate": 0.08, "max_depth": 5},
        },
    }

    print("\n--- Running Classification Experiments with MLflow Tracking ---")
    for model_name, cfg in classification_models.items():
        with mlflow.start_run(run_name=f"Clf_{model_name.replace(' ', '_')}"):
            # 1. Log tags and dataset metadata
            mlflow.set_tag("task", "classification")
            mlflow.set_tag("model_family", model_name)
            for k, v in dataset_metadata.items():
                mlflow.log_param(f"dataset_{k}", v)

            # 2. Log model hyperparameters
            for pk, pv in cfg["params"].items():
                mlflow.log_param(pk, pv)

            # 3. Train model
            t0 = time.time()
            model = cfg["model"]
            model.fit(X_train_c, y_train_c)
            train_duration = round(time.time() - t0, 3)

            # 4. Evaluate metrics
            y_pred = model.predict(X_test_c)
            y_prob = model.predict_proba(X_test_c)[:, 1] if hasattr(model, "predict_proba") else y_pred

            acc = float(accuracy_score(y_test_c, y_pred))
            prec = float(precision_score(y_test_c, y_pred, zero_division=0))
            rec = float(recall_score(y_test_c, y_pred, zero_division=0))
            f1 = float(f1_score(y_test_c, y_pred, zero_division=0))
            roc_auc = float(roc_auc_score(y_test_c, y_prob))

            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1_score", f1)
            mlflow.log_metric("roc_auc", roc_auc)
            mlflow.log_metric("train_duration_sec", train_duration)

            # 5. Save & log confusion matrix artifact
            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)
                cm_img_path = tmp_path / f"confusion_matrix_{model_name.replace(' ', '_')}.png"
                plot_and_save_confusion_matrix(y_test_c, y_pred, model_name, cm_img_path)
                mlflow.log_artifact(str(cm_img_path), artifact_path="plots")

                # Save model joblib artifact
                model_path = tmp_path / f"{model_name.lower().replace(' ', '_')}.joblib"
                joblib.dump(model, model_path)
                mlflow.log_artifact(str(model_path), artifact_path="models")

            record = {
                "experiment_id": mlflow.active_run().info.run_id,
                "task": "Classification",
                "model_name": model_name,
                "parameters": cfg["params"],
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "roc_auc": round(roc_auc, 4),
                "train_time_sec": train_duration,
            }
            experiment_records.append(record)
            print(f"Logged [{model_name}] -> Accuracy: {acc:.4f}, F1: {f1:.4f}, ROC-AUC: {roc_auc:.4f}")

    # =========================================================================
    # PART 2: REGRESSION EXPERIMENTS (Remaining Useful Life)
    # =========================================================================
    regression_models = {
        "Linear Regression": {
            "model": LinearRegression(),
            "params": {"fit_intercept": True},
        },
        "Ridge Regression": {
            "model": Ridge(alpha=1.5, random_state=42),
            "params": {"alpha": 1.5, "fit_intercept": True},
        },
        "Random Forest Regressor": {
            "model": RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42),
            "params": {"n_estimators": 200, "max_depth": 10},
        },
    }

    print("\n--- Running Regression Experiments with MLflow Tracking ---")
    for model_name, cfg in regression_models.items():
        with mlflow.start_run(run_name=f"Reg_{model_name.replace(' ', '_')}"):
            mlflow.set_tag("task", "regression")
            mlflow.set_tag("model_family", model_name)
            for k, v in dataset_metadata.items():
                mlflow.log_param(f"dataset_{k}", v)

            for pk, pv in cfg["params"].items():
                mlflow.log_param(pk, pv)

            t0 = time.time()
            model = cfg["model"]
            model.fit(X_train_r, y_train_r)
            train_duration = round(time.time() - t0, 3)

            y_pred = model.predict(X_test_r)
            mae = float(mean_absolute_error(y_test_r, y_pred))
            mse = float(mean_squared_error(y_test_r, y_pred))
            rmse = float(np.sqrt(mse))
            r2 = float(r2_score(y_test_r, y_pred))

            mlflow.log_metric("mae", mae)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2_score", r2)
            mlflow.log_metric("train_duration_sec", train_duration)

            with tempfile.TemporaryDirectory() as tmp_dir:
                tmp_path = Path(tmp_dir)
                model_path = tmp_path / f"{model_name.lower().replace(' ', '_')}.joblib"
                joblib.dump(model, model_path)
                mlflow.log_artifact(str(model_path), artifact_path="models")

            record = {
                "experiment_id": mlflow.active_run().info.run_id,
                "task": "Regression",
                "model_name": model_name,
                "parameters": cfg["params"],
                "mae": round(mae, 4),
                "mse": round(mse, 4),
                "rmse": round(rmse, 4),
                "r2_score": round(r2, 4),
                "train_time_sec": train_duration,
            }
            experiment_records.append(record)
            print(f"Logged [{model_name}] -> MAE: {mae:.4f}, RMSE: {rmse:.4f}, R2: {r2:.4f}")

    # Save summary report JSON and CSV
    results_json = REPORTS_DIR / "mlflow_experiment_results.json"
    results_csv = REPORTS_DIR / "mlflow_experiment_summary.csv"

    results_json.write_text(json.dumps(experiment_records, indent=2), encoding="utf-8")
    pd.DataFrame(experiment_records).to_csv(results_csv, index=False)

    print(f"\nAll experiments successfully tracked in MLflow ({MLRUNS_DB}).")
    print(f"Report artifacts saved to {results_json} and {results_csv}")
    return experiment_records


if __name__ == "__main__":
    run_experiments()
