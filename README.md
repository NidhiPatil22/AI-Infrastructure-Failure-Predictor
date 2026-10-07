# AI Urban Infrastructure Failure Predictor

This project is a college-level AIML mini-project that predicts urban infrastructure failure risk and recommends maintenance actions using a full-stack stack with React + Vite on the frontend and FastAPI + scikit-learn on the backend.

## Project idea

The system evaluates infrastructure assets such as roads, bridges, pipelines, drainage systems, streetlights, and electrical poles. It predicts:

- failure probability
- failure risk category
- remaining useful life
- maintenance priority
- recommended action
- key risk factors

## Features

- Synthetic but realistic infrastructure dataset with ~2000 records
- Data preprocessing and feature engineering
- Classification models for failure prediction
- Regression models for remaining useful life estimation
- K-Means clustering and PCA analysis
- Explainable AI using feature importance and rule-based reasoning
- React dashboard with charts, analytics, and risk prediction forms
- FastAPI backend with SQLite history storage

## Tech stack

- Frontend: React, Vite, React Router, Axios, Recharts
- Backend: FastAPI, pandas, numpy, scikit-learn, joblib
- Database: SQLite
- ML: Logistic Regression, Decision Tree, Random Forest, Linear Regression, Random Forest Regressor, K-Means, PCA

## Local setup

### Backend

1. Open a terminal in backend/
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `.venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Generate the synthetic dataset: `python scripts/generate_data.py`
6. Train the ML models: `python scripts/train_models.py`
7. Run the backend: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

### Frontend

1. Open a terminal in frontend/
2. Install dependencies: `npm install`
3. Start the React app: `npm run dev`
4. Set the API URL in `frontend/.env` if needed: `VITE_API_URL=http://localhost:8000`

## Model output

The project saves trained artifacts in backend/models/.

- classifier.pkl
- regressor.pkl
- kmeans.pkl
- preprocessor.pkl
- model_results.json
- feature_importance.json
- cluster_results.json

## Demo workflow

1. Open the frontend dashboard.
2. Navigate to Predict Risk.
3. Enter asset data and click Predict Failure Risk.
4. Review the risk explanation, recommendation, and maintenance priority.
5. Use the Analytics and Model Performance pages to understand model output.

## Viva-friendly explanation

The project combines data handling, machine learning, and a simple AI recommendation engine. It is intentionally designed to be understandable and easy to modify for academic demonstrations.
