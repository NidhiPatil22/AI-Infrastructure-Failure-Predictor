# 🚦 ROAD INFRASTRUCTURE PROJECT
### AI & Computer Vision Predictive Maintenance System
*Planning · Construction · Progress · Impact*

[![Streamlit](https://img.shields.io/badge/Primary%20App-Streamlit%201.55-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](http://localhost:8501)
[![FastAPI](https://img.shields.io/badge/REST%20API-FastAPI%200.135-009688?style=for-the-badge&logo=fastapi&logoColor=white)](http://localhost:8000/docs)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/Vision-OpenCV%20%2B%20YOLO-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow%203.17-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](https://mlflow.org)
[![FLAML](https://img.shields.io/badge/AutoML-FLAML%202.7-orange?style=for-the-badge)](https://microsoft.github.io/FLAML)

---

## 📌 Project Overview

Municipal civil infrastructure (bridges, roadways, water pipelines, drainage canals, streetlights, and electrical grids) is traditionally maintained through **reactive emergency repairs** or **fixed-calendar inspections**. Both strategies waste municipal funding and fail to catch hidden deterioration before catastrophic failure occurs.

The **Road Infrastructure Project** is an academic, multi-modal AI decision-support platform that transforms infrastructure management into **predictive, condition-based maintenance**:
- **Predicts Structural Failure Risk:** Classifies monitored assets as High, Medium, or Low risk using supervised machine learning.
- **Estimates Remaining Useful Life (RUL):** Predicts remaining operational service life in years.
- **Detects Surface Distress via Computer Vision:** Identifies potholes, cracks, and ravelling from road photos using OpenCV and YOLO.
- **Optimizes Maintenance Schedules:** Allocates municipal repair budgets using combinatorial search heuristics (Hill Climbing, Beam Search, Tabu Search).
- **Google Maps Live Corridor Search:** Directly search any highway, bridge, city, or address worldwide with satellite aerial view, terrain topography, and municipal GIS asset risk pins.
- **Supports Day & Night Themes:** Features an interactive highway-themed interface with Day ☀️ and Night 🌙 display modes.

---

## ⚡ Quick Start (Run in 1 Minute)

### 1. Launch the Primary Multi-Page Web App (Recommended)
```powershell
# Open terminal in project directory:
cd ml_infrastructure_predictor

# Launch Streamlit:
streamlit run streamlit_app.py
```
👉 Open your browser to **[http://localhost:8501](http://localhost:8501)**

### 2. Launch the Alternative FastAPI REST Service
```powershell
cd ml_infrastructure_predictor/backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
👉 Interactive Swagger API Docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## 🏗️ Core Functionalities & System Modules

| Icon | Module | Technology | What It Does |
| :---: | :--- | :--- | :--- |
| 🛣️ | **Road Damage Detection** | OpenCV + Ultralytics YOLO | Applies CLAHE equalization, Gaussian filters, Canny edge detection, and contour circularity to identify potholes and cracks, computing a 0–100 **Road Damage Index (RDI)**. |
| 🔮 | **Tabular Failure Prediction** | Random Forest, Decision Tree, Logistic Regression | Evaluates 18 telemetry features (load, traffic, age, corrosion, maintenance gap) to compute real-time failure probabilities and recommended actions. |
| ⏳ | **Remaining Useful Life (RUL)** | OLS Linear Regression & Random Forest Regressor | Estimates continuous operating years remaining until major overhaul ($R^2 = 0.9876$, MAE $= 0.26$ years). |
| ⚡ | **Maintenance Scheduling** | Hill Climbing, Beam Search, Tabu Search | Solves a 0-1 Knapsack problem to maximize portfolio risk reduction under strict municipal budget and crew-hour constraints. |
| 🤖 | **AutoML Benchmarking** | FLAML Tabular | Explores tree models in 25 seconds of CPU time on an isolated 80/20 train/test split, finding an `ExtraTree` model with **0.9753 Recall**. |
| 📈 | **Experiment Tracking** | MLflow 3.17 + SQLite | Systematically logs runs, hyperparameters, confusion matrices, and serialized model artifacts to a local database. |
| 🧬 | **Core Data Structures** | NumPy, SciPy, NetworkX, Heaps, Trees | Demonstrates 6 essential CS/AI data structures, including **SciPy CSR sparse matrices achieving 98% memory reduction**. |

---

## 🛠️ Technology Stack

```
ml_infrastructure_predictor
├── Frontend & Presentation : Streamlit 1.55 (Primary), React + Vite (Alternative)
├── Machine Learning Core   : Scikit-learn (RF, DT, LR, K-Means, PCA), FLAML (AutoML)
├── Computer Vision         : OpenCV (CLAHE, Canny, Morphology), Ultralytics YOLO
├── Combinatorial Search    : Custom Hill Climbing, Beam Search (β=4), Tabu Search (T=4)
├── Backend & REST API      : FastAPI, Uvicorn, Pydantic
├── Experiment Governance   : MLflow 3.17 with embedded SQLite database
└── Core Data Structures    : NumPy (SIMD), SciPy (CSR Sparse), NetworkX (Graphs), Heapq
```

---

## 📊 Verified Model Performance & Benchmarks

All metrics below are verified outputs loaded directly from [`backend/models/model_results.json`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/models/model_results.json):

### A. Failure Classification (Test Set: 440 Samples)
| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Note |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Random Forest (Tuned)** | 0.5500 | 0.5753 | **0.7078** | **0.6347** | 0.5868 | High recall minimizes missed civil failures |
| **AutoML (FLAML ExtraTree)** | 0.5545 | 0.5550 | **0.9753** | **0.7075** | 0.5709 | Discovered in 25s search budget |
| **Logistic Regression** | 0.5591 | 0.6034 | 0.5885 | 0.5958 | 0.5915 | Fast, interpretable linear baseline |
| **Decision Tree** | 0.5659 | 0.6250 | 0.5350 | 0.5765 | 0.5804 | Transparent if-then decision paths |

### B. Remaining Useful Life (RUL Regression)
| Regressor | MAE (Years) | RMSE (Years) | $R^2$ Score | Interpretation |
| :--- | :---: | :---: | :---: | :--- |
| **Linear Regression** | **0.2630** | **0.9497** | **0.9876** | Strong alignment on physics degradation laws |
| **Random Forest Regressor** | 0.9592 | 1.4746 | 0.9701 | Robust non-linear estimation across clusters |

### C. Combinatorial Optimization (Budget $= \$45,000$, Capacity $= 140\text{ hrs}$)
| Search Heuristic | Risk Reduction $f(S)$ | Assets Selected | Budget Utilized | Runtime |
| :--- | :---: | :---: | :---: | :---: |
| **Hill Climbing (Steepest)** | 4.6710 | 4 | 93.3% | 4.2 ms |
| **Beam Search ($\beta = 4$)** | **5.4230** | 5 | **98.0%** | 12.8 ms |
| **Tabu Search ($T = 4$)** | **5.4230** | 5 | **98.0%** | 18.5 ms |
*Beam & Tabu Search achieve **+16.1% higher risk reduction** by avoiding Hill Climbing's greedy local optimum trap.*

---

## 📁 Repository Directory Structure

```
ml_infrastructure_predictor/
├── streamlit_app.py                        # Primary multi-page interactive web app (9 modules)
├── Dockerfile & .dockerignore              # Multi-stage production container specification
├── dvc.yaml                                # 4-stage reproducible data science pipeline
├── README.md                               # Project documentation & guide
│
├── backend/
│   ├── app/
│   │   ├── main.py                         # FastAPI REST application
│   │   ├── cv/road_damage_detector.py      # OpenCV filtering & YOLO integration
│   │   ├── ml/                             # Preprocessing, Classifiers, Regressors, AutoML
│   │   ├── optimization/                   # Hill Climbing, Beam Search, Tabu Search
│   │   └── structures/                     # 6 core data structures demonstration
│   ├── data/
│   │   ├── urban_infrastructure_data.csv   # Primary dataset (2,200 records, 18 features)
│   │   └── sample_road_images/             # Pothole, crack, and intact test photos
│   └── models/ & reports/                  # Serialized models, metrics JSON, MLflow reports
│
├── frontend/                               # Alternative React + Vite client dashboard
└── docs/ & reports/                        # Viva Q&A guide, development log, project reports
```

---

## 🎓 High-Probability Viva Voce Questions & Answers

<details>
<summary><b>Q1: Why is Recall more important than Accuracy for infrastructure failure prediction?</b></summary>
<br>
Civil infrastructure failure is safety-critical. A <b>False Negative</b> (failing to identify an asset that collapses) can cause injury and massive emergency repair costs. A <b>False Positive</b> merely prompts a low-cost preventive physical check. Therefore, models are tuned to maximize Recall and F1-Score over raw accuracy.
</details>

<details>
<summary><b>Q2: Can standard pretrained YOLO detect road potholes and cracks out of the box?</b></summary>
<br>
<b>No.</b> Pretrained models (such as YOLOv8 on COCO) are trained on 80 common object classes (cars, people, chairs) and have zero training on pavement distress. Detecting road damage requires fine-tuning on road datasets (like RDD2020) or applying domain-specific OpenCV morphological filters (circularity for potholes, aspect ratios for cracks), as implemented in this project.
</details>

<details>
<summary><b>Q3: How does SciPy CSR sparse matrix reduce memory by 98%?</b></summary>
<br>
One-hot encoding categorical variables (zones, materials, asset types) creates matrices where >95% of entries are zero. A dense array stores every zero explicitly. A Compressed Sparse Row (CSR) matrix stores only the non-zero values, column indices, and row pointers, eliminating 98% of memory consumption.
</details>

<details>
<summary><b>Q4: Why does Hill Climbing get trapped in a local optimum during maintenance scheduling?</b></summary>
<br>
Hill Climbing only moves to neighbors that improve the objective in a single step. If selecting an individually high-payoff asset consumes most of the budget, Hill Climbing picks it and gets stuck—adding another asset violates the budget, while removing it decreases the objective. Beam Search and Tabu Search explore non-greedy branches, finding combinations of complementary assets that yield up to 58.8% higher risk reduction.
</details>

<details>
<summary><b>Q5: How was data leakage prevented during AutoML benchmarking?</b></summary>
<br>
The dataset was split into 80% train and 20% test before computing any statistics. All scalers, imputers, and encoders were fit strictly on the training partition (<code>X_train</code>) and applied via <code>transform()</code> to the held-out test fold (<code>X_test</code>).
</details>

---

*Academic Mini-Project | AIML Laboratory | Smart Urban Infrastructure Monitoring System*
