# MLOps & Reproducibility Guide

This document details the containerization, pipeline versioning, and reproducibility workflows implemented in the **AI Urban Infrastructure Failure Predictor**.

---

## 1. Docker Containerization

The repository contains a production-ready `Dockerfile` and `.dockerignore` for portable, isolated execution across any environment without dependency conflicts.

### A. Build Docker Image
From the repository root directory:
```bash
docker build -t urban-infra-predictor:latest .
```

### B. Run Streamlit Application (Primary Port 8501)
```bash
docker run -d --name infra-app -p 8501:8501 urban-infra-predictor:latest
```
Access the dashboard at [http://localhost:8501](http://localhost:8501).

### C. Run FastAPI Service (Alternative Port 8000)
Override the entrypoint to launch the Uvicorn ASGI server:
```bash
docker run -d --name infra-api -p 8000:8000 urban-infra-predictor:latest \
    uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
Access the REST API docs at [http://localhost:8000/docs](http://localhost:8000/docs).

### D. Multi-Port Dual Serving
To serve both Streamlit and FastAPI simultaneously:
```bash
docker run -d --name infra-dual -p 8501:8501 -p 8000:8000 urban-infra-predictor:latest \
    sh -c "uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"
```

---

## 2. Data & Pipeline Versioning with DVC

Data Version Control (DVC) enables Git-like versioning for tabular datasets, image benchmarks, and model artifacts without checking gigabytes of raw data into Git.

### A. Initialize DVC in Workspace
```bash
# Initialize DVC
dvc init

# Configure local or cloud remote storage (e.g., local directory or AWS S3/GCS)
dvc remote add -d local_storage /tmp/dvc_storage
```

### B. Track Datasets with DVC
```bash
# Track raw infrastructure dataset
dvc add backend/data/urban_infrastructure_data.csv

# Git tracks only the lightweight pointer file
git add backend/data/urban_infrastructure_data.csv.dvc .gitignore
git commit -m "chore(dvc): track raw infrastructure dataset version"
```

### C. Reproducible Multi-Stage Pipelines (`dvc.yaml`)
The pipeline definition in `dvc.yaml` defines four computational stages:
1. `generate_data`: Creates synthetic tabular infrastructure telemetry.
2. `train_models`: Fits baseline scikit-learn models and outputs `model_bundle.pkl`.
3. `mlflow_tracking`: Logs experiments, hyperparameters, and artifacts to MLflow.
4. `automl_benchmark`: Executes FLAML Tabular search and records comparative results.

To execute and reproduce the entire pipeline deterministically:
```bash
# Reproduce pipeline stages
dvc repro

# View pipeline execution DAG
dvc dag
```

---

## 3. Operational Principles
- **No Kubernetes/Kubeflow Overhead:** Standard lightweight containers and local orchestrators suffice for college and research lab evaluation without cluster management overhead.
- **Strict Seed Control:** Random state seeds (`random_state=42`) are enforced across all splits, algorithms, and synthetic generators.
- **Artifact Traceability:** Every serialized model file correlates to a logged MLflow experiment run ID in `backend/reports/mlflow_experiment_results.json`.
