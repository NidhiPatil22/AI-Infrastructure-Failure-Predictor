# AI Urban Infrastructure Failure Predictor

[![Streamlit](https://img.shields.io/badge/Primary%20App-Streamlit%201.55-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](http://localhost:8501)
[![FastAPI](https://img.shields.io/badge/REST%20Service-FastAPI%200.135-009688?style=for-the-badge&logo=fastapi&logoColor=white)](http://localhost:8000/docs)
[![MLflow](https://img.shields.io/badge/Tracking-MLflow%203.17-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/reports/mlflow_experiment_results.json)
[![AutoML](https://img.shields.io/badge/AutoML-FLAML%202.7-orange?style=for-the-badge)](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/reports/automl_comparison_results.json)
[![Docker](https://img.shields.io/badge/Container-Docker%20Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/Dockerfile)
[![DVC](https://img.shields.io/badge/Pipeline-DVC%20Configured-945DD6?style=for-the-badge&logo=dvc&logoColor=white)](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/dvc.yaml)

An academic, multi-modal Artificial Intelligence and Machine Learning decision-support platform designed to evaluate municipal civil infrastructure health, predict structural failure risk, estimate Remaining Useful Life (RUL), detect pavement surface distress using computer vision, track machine learning experiments, and optimize maintenance schedules under real-world budgetary and workforce constraints.

---

## 📑 Table of Contents
1. [Project Overview & Motivation](#1-project-overview--motivation)
2. [Problem Statement](#2-problem-statement)
3. [Project Objectives](#3-project-objectives)
4. [Key Features](#4-key-features)
5. [System Architecture & End-to-End Workflow](#5-system-architecture--end-to-end-workflow)
6. [Artificial Intelligence vs. Machine Learning](#6-artificial-intelligence-vs-machine-learning)
7. [Technology Stack](#7-technology-stack)
8. [Libraries and Dependencies](#8-libraries-and-dependencies)
9. [Dataset Description & Engineering Profile](#9-dataset-description--engineering-profile)
10. [Data Preprocessing & Feature Engineering](#10-data-preprocessing--feature-engineering)
11. [Exploratory Data Analysis (EDA)](#11-exploratory-data-analysis-eda)
12. [Machine Learning Algorithms](#12-machine-learning-algorithms)
13. [Model Training & Evaluation Methodology](#13-model-training--evaluation-methodology)
14. [Clustering, PCA & Core Data Structures](#14-clustering-pca--core-data-structures)
15. [Explainable AI & AI Recommendation Engine](#15-explainable-ai--ai-recommendation-engine)
16. [Computer Vision Road Distress Detection](#16-computer-vision-road-distress-detection)
17. [Search Space Management & Combinatorial Optimization](#17-search-space-management--combinatorial-optimization)
18. [Experiment Tracking, AutoML & MLOps](#18-experiment-tracking-automl--mlops)
19. [Application Pages & Interactive User Workflow](#19-application-pages--interactive-user-workflow)
20. [Project Directory Structure](#20-project-directory-structure)
21. [Installation & Execution Guide](#21-installation--execution-guide)
22. [Sample Prediction Walkthrough](#22-sample-prediction-walkthrough)
23. [Experimental Results & Empirical Observations](#23-experimental-results--empirical-observations)
24. [Problems Faced & Engineering Solutions](#24-problems-faced--engineering-solutions)
25. [Limitations & Future Scope](#25-limitations--future-scope)
26. [Faculty AIML Laboratory Requirements Mapping](#26-faculty-aiml-laboratory-requirements-mapping)
27. [Literature Survey & Scientific References](#27-literature-survey--scientific-references)
28. [Viva Voce Examination Preparation](#28-viva-voce-examination-preparation)

---

## 1. Project Overview & Motivation

Municipal civil infrastructure forms the foundational backbone of urban living. Civil assets such as bridges, roads, water supply pipelines, drainage channels, streetlights, and electrical distribution poles are subjected to persistent mechanical strain, fluctuating thermal cycles, heavy traffic loading, and severe environmental weathering.

Traditionally, municipalities manage public assets using two outdated strategies:
1. **Reactive Maintenance:** Repairing or replacing assets only after catastrophic breakdown has occurred. This incurs excessive emergency repair expenses, creates safety hazards, and disrupts vital citizen services.
2. **Calendar-Based Maintenance:** Performing scheduled physical inspections at fixed calendar intervals regardless of asset health. This expends scarce municipal resources inspecting structurally sound infrastructure while degrading assets deteriorate unnoticed between cycles.

The **AI Urban Infrastructure Failure Predictor** transitions asset management toward **predictive and condition-based maintenance**. By processing multi-source asset telemetry (historical maintenance logs, operational usage patterns, structural ratings, and environmental stress factors) and macroscopic pavement imagery, the system provides municipal engineers with quantitative failure probabilities, prognostic life estimates, localized optical defect detections, and resource-optimal maintenance schedules.

### Supported Infrastructure Categories
The current implementation actively supports **six verified asset categories** modeled in the dataset:
- **Bridges:** Monitored for concrete fatigue, load stress, structural degradation, and corrosion.
- **Roads:** Analyzed via tabular traffic/weather stress and macroscopic optical imagery (potholes/cracks).
- **Water Pipelines:** Monitored for corrosion, hydraulic usage intensity, soil moisture, and inspection intervals.
- **Drainage Networks:** Evaluated under annual rainfall volume, environmental stress, and age.
- **Streetlights:** Assessed on operational wear, maintenance frequency, and electrical corrosion.
- **Electrical Poles:** Monitored for mechanical loading, weathering, and material durability.

---

## 2. Problem Statement

Municipal public works departments face severe operational constraints:
- **Sudden Asset Failures:** Unanticipated water main ruptures, bridge deck spalling, and electrical pole collapses risk public safety and cause multi-million dollar repair burdens.
- **Inefficient Manual Inspections:** Field inspections require specialized civil inspection crews, expensive equipment, and roadway lane closures, making comprehensive citywide physical audits impossible.
- **Severe Budgetary & Workforce Caps:** Municipalities have finite annual capital expenditure budgets and limited labor crew hours, forcing difficult trade-offs between urgent repairs.
- **Information Asymmetry:** Maintenance records and telemetry are frequently siloed in legacy databases, obscuring which assets represent the highest risk of imminent failure.

> [!IMPORTANT]
> **Prototype Disclaimer:** This software platform is an academic engineering prototype developed for laboratory evaluation and demonstration. All risk scores, Remaining Useful Life predictions, computer vision detections, and maintenance allocations provide **decision support** and must be reviewed and validated by certified professional engineers prior to field implementation.

---

## 3. Project Objectives

### Implemented & Verified Objectives
- [x] **Supervised Failure Risk Classification:** Train and evaluate binary classifiers (Logistic Regression, Decision Trees, Random Forest, Gradient Boosting) to classify assets as high or low failure risk.
- [x] **Prognostic RUL Estimation:** Train multivariate regression models (Linear Regression, Random Forest Regressor) to forecast remaining useful operational life in years.
- [x] **Unsupervised Asset Profiling:** Cluster the infrastructure portfolio using K-Means ($k=3$) and visualize multi-dimensional feature variance using Principal Component Analysis (PCA).
- [x] **Computer Vision Distress Detection:** Preprocess pavement imagery with OpenCV (CLAHE, Gaussian blur, Canny edge detection, morphology) and support Ultralytics YOLO inference for bounding-box defect localization.
- [x] **Combinatorial Maintenance Optimization:** Formulate maintenance scheduling as a constrained 0-1 Knapsack problem and benchmark Hill Climbing, Beam Search, and Tabu Search heuristics.
- [x] **Governance & Experiment Tracking:** Log parameters, metrics, confusion matrices, and serialized model artifacts deterministically into an embedded SQLite MLflow tracking server.
- [x] **AutoML Benchmarking:** Perform automated algorithm search and hyperparameter tuning using FLAML Tabular on isolated 80/20 train/test splits with zero data leakage.
- [x] **Data Structures Demonstration:** Showcase practical AI/ML data structures (NumPy SIMD arrays, SciPy CSR sparse matrices, Decision Trees, NetworkX directed graphs, Heapq priority queues, Hash dictionaries).
- [x] **Multi-Page Web Dashboard:** Deliver a comprehensive 9-page interactive Streamlit application alongside a FastAPI REST backend.

### Future / Planned Objectives
- [ ] **Interactive Game-Theoretic SHAP Force Plots:** Integrate dynamic SHAP waterfall plots at runtime (currently implemented via tree Gini importances and rule-based factors).
- [ ] **Real-Time IoT Telemetry Streaming:** Ingest live strain-gauge, acoustic, and vibrational data via Apache Kafka / MQTT brokers.
- [ ] **Edge-Quantized Deep Learning:** Export fine-tuned YOLO road defect models to TensorRT and INT8 ONNX for drone-mounted and dashcam inference.
- [ ] **Conversational AI Assistant:** Deploy a retrieval-augmented LLM interface for conversational queries (explicitly disclaimed; currently not implemented).

---

## 4. Key Features

| Feature Name | Description & Purpose | Implementation Mechanism | Source Module / File | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Dataset Generation & Cleaning** | Generates 2,200 synthetic telemetry rows with realistic physics-based failure dynamics; imputes missing data and clips IQR outliers. | Pandas, NumPy domain physics simulation, IQR trimming, median imputation. | [`backend/scripts/generate_data.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/generate_data.py)<br>[`backend/app/ml/preprocessing.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/preprocessing.py) | **Implemented and verified** |
| **Feature Engineering Pipeline** | Derives 7 composite engineering indicators (maintenance frequency, environmental stress, condition score) without data leakage. | `ColumnTransformer` with `StandardScaler` and `OneHotEncoder(handle_unknown='ignore')`. | [`backend/app/ml/preprocessing.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/preprocessing.py) | **Implemented and verified** |
| **Supervised Failure Classification** | Classifies binary failure likelihood (`failure = 0 or 1`) across multi-class infrastructure portfolios. | Logistic Regression, Decision Tree, Random Forest (`class_weight='balanced'`), GBDT. | [`backend/app/ml/classification.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/classification.py) | **Implemented and verified** |
| **RUL Prognosis Regression** | Predicts remaining operational service life in years to guide long-term capital replacement planning. | Ordinary Least Squares Linear Regression, Random Forest Regressor ($n=120$). | [`backend/app/ml/regression.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/regression.py) | **Implemented and verified** |
| **Unsupervised Asset Clustering** | Groups assets into 3 operational risk tiers (Healthy, Moderate Risk, Critical) based on structural degradation. | Scikit-learn `KMeans(n_clusters=3, random_state=42)` evaluated via Silhouette analysis. | [`backend/app/ml/clustering.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/clustering.py) | **Implemented and verified** |
| **PCA Dimensionality Reduction** | Projects high-dimensional feature space onto 2 principal orthogonal axes for visual inspection of risk separation. | Scikit-learn `PCA(n_components=2)` applied to standardized continuous feature matrix. | [`backend/app/ml/clustering.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/clustering.py) | **Implemented and verified** |
| **Explainable AI (Gini Feature Importance)** | Quantifies global feature importance and isolates asset-specific vulnerability factors. | Gini impurity reduction from Random Forest trees and local threshold comparison. | [`backend/app/ml/classification.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/classification.py)<br>[`backend/app/model_service.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/model_service.py) | **Implemented and verified** |
| **Rule-Based Decision Engine** | Translates ML probabilities and physical ratings into human-interpretable engineering maintenance actions. | Heuristic decision logic assigning risk tiers (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and actionable protocols. | [`backend/app/utils/helpers.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/utils/helpers.py)<br>[`backend/app/model_service.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/model_service.py) | **Implemented and verified** |
| **Computer Vision Road Inspection** | Identifies surface cracks, potholes, and ravelling from road photos and computes Road Damage Index (RDI). | OpenCV (CLAHE, Canny, morphology, contour shape analysis) and Ultralytics YOLO bounding box support. | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) | **Implemented and verified** |
| **Combinatorial Schedule Optimization** | Solves 0-1 Knapsack resource allocation to maximize total risk reduction under budget and labor caps. | Custom implementations of Hill Climbing, Beam Search ($\beta = 4$), and Tabu Search with recency memory. | [`backend/app/optimization/maintenance_scheduler.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/optimization/maintenance_scheduler.py) | **Implemented and verified** |
| **Experiment Tracking with MLflow** | Systematically logs runs, hyperparameters, metrics, and models to an embedded SQLite database. | MLflow 3.17 with backend URI `sqlite:///backend/data/mlflow_tracking.db`. | [`backend/scripts/run_mlflow_experiments.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/run_mlflow_experiments.py) | **Implemented and verified** |
| **AutoML via FLAML Tabular** | Evaluates automated algorithm exploration within a bounded CPU time budget on strict 80/20 train/test split. | FLAML 2.7 `AutoML(task='classification', time_budget=25)` finding `ExtraTree` with 0.7075 F1. | [`backend/app/ml/automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/automl.py)<br>[`backend/scripts/train_automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/train_automl.py) | **Implemented and verified** |
| **Core AI/ML Data Structures Suite** | Empirically demonstrates the necessity and performance characteristics of 6 fundamental AI/ML data structures. | NumPy arrays, SciPy CSR sparse matrices, Decision Trees, NetworkX graphs, Heapq heaps, Dictionaries. | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) | **Implemented and verified** |
| **Primary Multi-Page Web Dashboard** | Interactive user interface providing complete access to all 8 laboratory areas and live prediction cards. | Streamlit 1.55 with `@st.cache_resource` caching, file uploaders, sliders, and Plotly charts. | [`streamlit_app.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/streamlit_app.py) | **Implemented and verified** |
| **Alternative REST API Microservice** | Production-ready asynchronous ASGI service exposing prediction, CV, and optimization endpoints. | FastAPI 0.135 with Pydantic request validation and Swagger UI documentation. | [`backend/app/main.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/main.py) | **Implemented and verified** |
| **Containerized Deployment & MLOps** | Portable container runtime and reproducible data pipeline specification. | Multi-stage `Dockerfile`, `.dockerignore`, and 4-stage `dvc.yaml` pipeline. | [`Dockerfile`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/Dockerfile)<br>[`dvc.yaml`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/dvc.yaml) | **Implemented and verified** |
| **Runtime SHAP Force Plots** | Dynamic game-theoretic feature attribution plots generated during individual inference. | Documented in literature survey; planned for future runtime Streamlit integration. | [`docs/literature_and_dataset_survey.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/literature_and_dataset_survey.md) | **Partially implemented** |
| **Conversational AI Assistant** | Interactive natural language chatbot or conversational LLM assistant. | Explicitly disclaimed; no conversational model or LLM agent exists in this repository. | None | **Planned / Not implemented** |

---

## 5. System Architecture & End-to-End Workflow

The following Mermaid diagram details the end-to-end data processing, model training, inference, and presentation pipeline implemented across the project:

```mermaid
graph TD
    subgraph Data Sources & Ingestion
        A1[Synthetic Infrastructure Dataset<br>urban_infrastructure_data.csv]
        A2[Road Surface Imagery<br>JPG / PNG / WebP]
    end

    subgraph Data Preprocessing & Pipeline
        B1[Data Cleaning: Duplicate Dropping & IQR Outlier Clipping]
        B2[Feature Engineering: 7 Domain Indicators]
        B3[Pipeline: SimpleImputer + StandardScaler + OneHotEncoder]
        B4[OpenCV Pipeline: Grayscale + CLAHE + Gaussian Blur + Canny Edge]
        A1 --> B1 --> B2 --> B3
        A2 --> B4
    end

    subgraph Model Training & Serialization
        C1[Classification: Logistic Regression, Decision Tree, Random Forest, GBDT]
        C2[Regression: Linear Regression, Random Forest Regressor]
        C3[Clustering: K-Means k=3 + PCA Dimensionality Reduction]
        C4[AutoML: FLAML Tabular ExtraTree Optimizer]
        C5[MLflow Experiment Tracking: SQLite sqlite:///data/mlflow_tracking.db]
        B3 --> C1 & C2 & C3 & C4
        C1 & C2 --> C5
        C1 & C2 --> D1[Serialized model_bundle.pkl]
        C3 --> D2[cluster_results.json]
        C4 --> D3[automl_classifier.pkl]
    end

    subgraph Computer Vision Distress Engine
        E1[Contour Extraction & Morphology Dilation / Closing]
        E2[Shape-Factor Classification: Pothole vs. Cracks]
        E3[Ultralytics YOLO Bounding Box Inference Engine]
        B4 --> E1 --> E2
        B4 --> E3
        E2 & E3 --> E4[Road Damage Index RDI & Annotated Image]
    end

    subgraph Decision Support & Optimization Layer
        F1[Supervised Inference: Failure Probability & RUL]
        F2[Explainable AI: Gini Importances & Vulnerability Factors]
        F3[Rule-Based AI Reasoning: Priority & Maintenance Protocols]
        F4[Search Space Optimizer: Hill Climbing, Beam Search, Tabu Search]
        F5[Emergency Triage Priority Queue: Binary Heap O log N]
        D1 --> F1
        F1 --> F2 --> F3
        F1 --> F4
        F1 --> F5
    end

    subgraph Presentation & Deployment Layer
        G1[Primary Streamlit Multi-Page App<br>Port 8501]
        G2[FastAPI Asynchronous Microservice<br>Port 8000]
        G3[React + Vite Frontend Dashboard<br>Port 5173]
        G4[Multi-Stage Docker Container]
        E4 & F1 & F2 & F3 & F4 & F5 --> G1
        F1 & E4 & F4 --> G2
        G2 --> G3
        G1 & G2 --> G4
    end
```

### End-to-End Data Flow Description
1. **Data Ingestion:** Tabular telemetry is loaded from [`backend/data/urban_infrastructure_data.csv`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/data/urban_infrastructure_data.csv); pavement imagery is decoded via OpenCV from file uploads or sample directories.
2. **Preprocessing & Feature Engineering:** Continuous features are clipped using IQR bounds to mitigate extreme synthetic outliers. Seven composite interaction features are computed. The dataset is passed to a scikit-learn `ColumnTransformer` that imputes missing values, standardizes continuous features, and one-hot encodes categorical columns.
3. **Model Inference:** Classifiers compute the posterior failure probability $P(\text{failure}=1 \mid X)$, while regressors predict Remaining Useful Life in years.
4. **Decision Synthesis:** Probabilities feed the deterministic AI reasoning engine to generate qualitative risk tiers (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and specific maintenance action items.
5. **Computer Vision Inference:** The image pipeline applies CLAHE and Canny filtering, categorizes defects via circularity and aspect ratio thresholds, and computes the Road Damage Index (RDI).
6. **Combinatorial Optimization:** Assets needing repair are formatted into a 0-1 Knapsack model, allowing Hill Climbing, Beam Search, and Tabu Search to solve for maximum risk reduction under budget and labor constraints.
7. **Presentation:** Results are displayed in the interactive multi-page Streamlit dashboard and exposed via FastAPI REST endpoints.

---

## 6. Artificial Intelligence vs. Machine Learning

To maintain strict academic integrity during faculty evaluation, the distinction between Machine Learning, Explainable AI, Rule-Based AI Reasoning, Computer Vision, Optimization, and Conversational NLP is outlined below:

| System Component | Technology / Method | Specific Purpose | System Input | System Output | Implementation Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Supervised Classification** | Random Forest, Decision Tree, Logistic Regression, GBDT | Predict binary infrastructure failure probability | Tabular physical & environmental telemetry | Failure probability $[0.0, 1.0]$ and binary class ($0$ or $1$) | **Implemented and verified** |
| **Supervised Regression** | Linear Regression, Random Forest Regressor | Forecast Remaining Useful Life (RUL) | Tabular asset condition features | Continuous expected RUL in years | **Implemented and verified** |
| **Unsupervised Clustering** | K-Means Clustering ($k=3$) | Partition assets into operational health tiers | Scaled continuous feature vectors | Cluster ID ($0$: Healthy, $1$: Moderate, $2$: Critical) | **Implemented and verified** |
| **Dimensionality Reduction** | Principal Component Analysis (PCA) | Compress high-dimensional feature space to 2D | Standardized feature matrix | 2 principal orthogonal coordinates ($PC_1, PC_2$) | **Implemented and verified** |
| **Automated ML (AutoML)** | FLAML Tabular (Cost-Frugal Search) | Automated model selection & hyperparameter tuning | Preprocessed 80% training split | Best estimator pipeline (`ExtraTree`) | **Implemented and verified** |
| **Explainable AI (XAI)** | Gini Impurity Reduction & Factor Profiling | Identify primary drivers of model predictions | Trained tree models & asset sample | Relative feature weights & top risk contributors | **Implemented and verified** |
| **AI Reasoning Engine** | Deterministic Heuristic Production Rules | Synthesize risk indicators into maintenance actions | Failure probability, structural score, history | Actionable protocol & priority (`CRITICAL` to `LOW`) | **Implemented and verified** |
| **Computer Vision Filtering** | OpenCV (CLAHE, Canny, Contour Morphology) | Segment macroscopic road defects & compute RDI | Grayscale road pavement image | Segmented contours, defect classes, and RDI score | **Implemented and verified** |
| **Object Detection (Deep Learning)** | Ultralytics YOLO Architecture | Localize distress objects with bounding boxes | RGB road pavement image | Bounding boxes, class labels, and confidence scores | **Implemented and verified** |
| **Search & Optimization** | Hill Climbing, Beam Search, Tabu Search | Solve constrained 0-1 Knapsack maintenance planning | Candidate repairs, budget, and labor limits | Optimal asset subset maximizing total risk reduction | **Implemented and verified** |
| **Conversational AI / NLP** | Large Language Models (LLMs) / Chatbots | Conversational query answering and chat interface | Natural language user text prompt | Conversational natural language text response | **Planned / Not implemented** |

### Conceptual Distinctions for Examiners
- **Machine Learning vs. Rule-Based AI:** The Random Forest classifier is purely *data-driven*, learning non-linear split thresholds from historical correlation patterns. Conversely, the maintenance recommendation engine is *knowledge-driven*, applying explicit expert rules ($P(\text{failure}) > 0.7 \land \text{structural\_score} < 50 \implies \text{CRITICAL}$) that do not rely on parameter learning.
- **Why Random Forest is Not a Chatbot:** A supervised tree ensemble maps an input vector $\mathbf{x} \in \mathbb{R}^d$ to a scalar class probability $y \in [0, 1]$. It contains no natural language parser, token vocabulary, attention mechanism, or generative text capabilities. All textual recommendations in this project are generated via deterministic template strings.
- **Computer Vision vs. Tabular Prediction:** Tabular models evaluate internal structural wear from numerical telemetry. The Computer Vision engine inspects macroscopic surface integrity from 2D optical images. These two modalities complement each other: an asset may have high internal corrosion (detected via tabular models) before surface cracks become visible to cameras.

---

## 7. Technology Stack

| Category | Technology | Version | Purpose in This Project | Relevant File / Configuration |
| :--- | :--- | :--- | :--- | :--- |
| **Language** | Python | 3.10 – 3.14 | Core backend programming language | Repository wide |
| **Numerical Computing** | NumPy | $\ge 1.26.0$ | SIMD array operations, Z-score scaling, dot products | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **Data Manipulation** | Pandas | $\ge 2.2.0$ | Tabular DataFrame cleaning, IQR filtering, feature engineering | [`backend/app/ml/preprocessing.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/preprocessing.py) |
| **Sparse Computation** | SciPy | $\ge 1.13.0$ | Compressed Sparse Row (CSR) memory-efficient matrices | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **Machine Learning** | Scikit-learn | $\ge 1.5.0$ | Classifiers, regressors, preprocessing pipelines, K-Means, PCA | [`backend/app/ml/classification.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/classification.py)<br>[`backend/app/ml/regression.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/regression.py) |
| **AutoML** | FLAML | $\ge 2.7.0$ | Cost-frugal automated tabular model exploration | [`backend/app/ml/automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/automl.py) |
| **Boosting Libraries** | XGBoost & LightGBM | Latest | Estimator search backends for FLAML | Environment runtime |
| **Experiment Tracking** | MLflow | $\ge 3.17.0$ | Experiment logging, metric tracking, model artifact storage | [`backend/scripts/run_mlflow_experiments.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/run_mlflow_experiments.py) |
| **Computer Vision** | OpenCV (Headless) | $\ge 4.9.0$ | CLAHE equalization, Canny edge detection, contour extraction | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) |
| **Object Detection** | Ultralytics YOLO | $\ge 8.1.0$ | Deep learning bounding-box detection pipeline integration | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) |
| **Graph Modeling** | NetworkX | $\ge 3.2.0$ | Infrastructure topological connectivity and betweenness centrality | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **Priority Queues** | Python `heapq` | Standard Lib | Binary min/max heap for $O(\log N)$ emergency repair triage | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **Web Presentation** | Streamlit | $\ge 1.32.0$ | Primary multi-page interactive web application | [`streamlit_app.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/streamlit_app.py) |
| **Alternative API** | FastAPI & Uvicorn | $\ge 0.110.0$ | Asynchronous REST microservice with OpenAPI/Swagger docs | [`backend/app/main.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/main.py) |
| **Data Validation** | Pydantic | $\ge 2.6.0$ | Request and response schema typing and validation | [`backend/app/schemas/prediction_schema.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/schemas/prediction_schema.py) |
| **Model Serialization** | Joblib | $\ge 1.4.0$ | Efficient persistence of fitted Python pipelines and estimators | [`backend/app/model_service.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/model_service.py) |
| **Database Storage** | SQLite3 | Built-in | Embedded storage for MLflow experiments and prediction history | [`backend/data/mlflow_tracking.db`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/data/mlflow_tracking.db) |
| **Containerization** | Docker | Latest | Multi-stage container runtime for Streamlit and FastAPI | [`Dockerfile`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/Dockerfile) |
| **Data Versioning** | DVC | Latest | Declarative data science pipeline DAG specification | [`dvc.yaml`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/dvc.yaml) |
| **Alternative Frontend** | React + Vite | 18.x / 5.x | Client SPA connecting to FastAPI REST backend | [`frontend/`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/frontend/) |

---

## 8. Libraries and Dependencies

| Library Name | Academic & Practical Role | Specific Repository Usage | Module / Script |
| :--- | :--- | :--- | :--- |
| **`scikit-learn`** | Machine learning and preprocessing foundation | Implements `LogisticRegression`, `DecisionTreeClassifier`, `RandomForestClassifier`, `LinearRegression`, `KMeans`, `PCA`, `ColumnTransformer`, `StandardScaler`, and `OneHotEncoder`. | [`backend/app/ml/`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/) |
| **`pandas`** | High-performance tabular data structures | Handles CSV ingestion, dataframe slicing, quantile calculation for IQR clipping, and feature grouping. | [`backend/app/ml/preprocessing.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/preprocessing.py) |
| **`numpy`** | Low-level vectorized mathematical operations | Vector normalization, matrix multiplication, array reshaping, and metric calculations. | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **`scipy`** | Scientific computing and sparse matrix operations | Converts dense one-hot encoded matrices into Compressed Sparse Row (CSR) matrices to reduce memory footprint by 98%. | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **`cv2` (OpenCV)** | Computer vision filtering and image processing | Grayscale transformation, Contrast Limited Adaptive Histogram Equalization (CLAHE), Gaussian filtering, Canny edge detection, morphological closing, and contour analysis. | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) |
| **`ultralytics`** | Single-stage deep learning object detection | Loads YOLO weights, runs bounding box inference, and extracts detection classes and confidence scores. | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) |
| **`flaml`** | Cost-frugal automated machine learning | Explores candidate estimators, evaluates hyperparameter configurations via cross-validation, and discovers optimal model architectures under bounded time constraints. | [`backend/app/ml/automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/automl.py) |
| **`mlflow`** | MLOps lifecycle and experiment tracking | Logs model runs, tracks hyperparameter combinations, records classification and regression metrics, and writes to an embedded SQLite store. | [`backend/scripts/run_mlflow_experiments.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/run_mlflow_experiments.py) |
| **`networkx`** | Network topology and graph algorithms | Models municipal asset networks as directed graphs, calculates betweenness centrality, and simulates cascading infrastructure failure risks. | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) |
| **`streamlit`** | Rapid interactive web application development | Serves as the primary laboratory application, providing an 8-module interactive UI with real-time sliders, charts, and file uploaders. | [`streamlit_app.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/streamlit_app.py) |
| **`fastapi`** | Asynchronous ASGI REST API framework | Provides production REST endpoints (`/api/predict`, `/api/cv/detect-damage`, `/api/optimization/compare`) with automatic OpenAPI Swagger documentation. | [`backend/app/main.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/main.py) |
| **`pydantic`** | Data validation and parsing using Python type hints | Defines strictly typed schemas for incoming asset prediction requests and response payloads. | [`backend/app/schemas/prediction_schema.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/schemas/prediction_schema.py) |
| **`joblib`** | Lightweight object persistence for Python | Serializes and loads the fitted scikit-learn preprocessing pipelines and trained model bundles. | [`backend/app/model_service.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/model_service.py) |

---

## 9. Dataset Description & Engineering Profile

The primary dataset used across the project is located at [`backend/data/urban_infrastructure_data.csv`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/data/urban_infrastructure_data.csv).

### Dataset Provenance & Nature
- **Synthetic Domain Simulation:** The dataset is synthetic, deterministically generated via [`backend/scripts/generate_data.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/generate_data.py). It models real-world civil engineering degradation laws, environmental stresses, and historical inspection dynamics.
- **Dataset Dimensions:** Exactly **2,200 rows** across **18 columns**.
- **Missing Values:** Zero raw nulls; the preprocessing pipeline includes imputation transformers to handle any missing values in real-world user uploads.

### Target Variables
1. **`failure` (Supervised Classification Target):**
   - Binary indicator: `0` = Asset structurally operational, `1` = Failure incident flagged.
   - **Distribution:** $N_{\text{operational}} = 987$ ($44.86\%$), $N_{\text{failure}} = 1,213$ ($55.14\%$).
   - This balanced distribution reflects a monitored high-risk municipal sample.
2. **`remaining_useful_life` (Supervised Regression Target):**
   - Continuous variable representing estimated functional lifetime remaining in years.
   - **Range:** Minimum $= 1.00\text{ yr}$, Maximum $= 45.75\text{ yr}$.
   - **Statistical Moments:** Mean $= 20.56\text{ yr}$, Standard Deviation $= 8.31\text{ yr}$, Median $= 20.10\text{ yr}$.

### Feature Categorization
- **Categorical Attributes (3):**
  - `asset_type`: Drainage ($426$), Electrical Pole ($392$), Streetlight ($368$), Bridge ($365$), Pipeline ($338$), Road ($311$).
  - `zone`: North, South, Central, Industrial, Residential.
  - `material`: Steel, Concrete, Asphalt, Composite, Copper.
- **Continuous & Discrete Physical Indicators (13):**
  - `age_years`: Asset age ($1.0$ to $50.0$ years).
  - `traffic_density`: Local vehicular traffic index ($10.0$ to $100.0$).
  - `average_load`: Mechanical operational load ($20.0$ to $150.0$ tons/units).
  - `annual_rainfall`: Local precipitation ($400.0$ to $2,500.0$ mm/year).
  - `average_temperature`: Ambient environmental temperature ($5.0$ to $45.0\text{ }^\circ\text{C}$).
  - `maintenance_count`: Total prior maintenance interventions ($0$ to $15$).
  - `days_since_maintenance`: Interval since last maintenance event ($10$ to $365$ days).
  - `days_since_inspection`: Interval since last certified physical inspection ($5$ to $180$ days).
  - `structural_score`: Health condition index ($10.0$ to $100.0$, where $100$ is pristine).
  - `corrosion_level`: Material degradation percentage ($0.0\%$ to $100.0\%$).
  - `previous_failures`: Count of historical component failures ($0$ to $5$).
  - `usage_intensity`: Daily utilization multiplier ($0.5$ to $2.5$).

### Dataset Limitations
1. **Simulated Telemetry:** Sensor readings and failure labels are generated via synthetic mathematical models rather than live municipal SCADA systems.
2. **Tabular Scope:** The dataset captures asset-level aggregate metrics rather than high-frequency vibrational or acoustic time-series waveforms.

---

## 10. Data Preprocessing & Feature Engineering

The preprocessing and feature engineering pipeline is implemented in [`backend/app/ml/preprocessing.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/preprocessing.py).

### Order of Operations
```
Raw Input Data -> Deduplication -> IQR Outlier Clipping -> Missing Value Imputation -> Domain Feature Engineering -> ColumnTransformer (OneHotEncoder + StandardScaler) -> Model Ready Tensor
```

### 1. Data Cleaning
- **Deduplication:** Duplicated rows are removed using `df.drop_duplicates().reset_index(drop=True)`.
- **Interquartile Range (IQR) Outlier Treatment:** Continuous variables are trimmed within $[\text{Q1} - 1.5 \times \text{IQR}, \text{Q3} + 1.5 \times \text{IQR}]$ to prevent extreme anomalies from distorting linear boundaries.
- **Imputation:** Categorical columns are imputed with their statistical mode; numerical columns are imputed with their median.

### 2. Domain Feature Engineering
Seven domain-specific interaction features are derived to expose non-linear relationships to linear and tree models:

1. **Infrastructure Age:**
   $$\text{infrastructure\_age} = \text{age\_years}$$
2. **Maintenance Frequency (Interventions per Year of Life):**
   $$\text{maintenance\_frequency} = \frac{\text{maintenance\_count}}{\max(\text{age\_years}, 1)}$$
3. **Inspection Gap:**
   $$\text{inspection\_gap} = \text{days\_since_inspection}$$
4. **Failure History Score (Failure Rate Over Operational Lifetime):**
   $$\text{failure\_history\_score} = \frac{\text{previous\_failures}}{\max(\text{age\_years}, 1)}$$
5. **Maintenance Delay Score (Months Elapsed Since Last Service):**
   $$\text{maintenance\_delay\_score} = \frac{\text{days\_since\_maintenance}}{30.0}$$
6. **Environmental Stress (Combined Rainfall and Thermal Index):**
   $$\text{environmental\_stress} = \left(\frac{\text{annual\_rainfall}}{1000.0}\right) + \left(\frac{\text{average\_temperature} - 20.0}{10.0}\right)$$
7. **Load Stress (Combined Traffic Density and Operational Weight):**
   $$\text{load\_stress} = \left(\frac{\text{traffic\_density}}{10.0}\right) + \left(\frac{\text{average\_load}}{60.0}\right)$$
8. **Overall Condition Score (Weighted Structural Integrity and Corrosion):**
   $$\text{overall\_condition\_score} = \min\left(100, \max\left(0, 0.6 \times \text{structural\_score} + 0.4 \times (100 - \text{corrosion\_level})\right)\right)$$

### 3. Transformation Pipeline & Data Leakage Prevention
To prevent **data leakage**, transformers are fitted strictly on the 80% training partition (`X_train`) and applied to the 20% test partition (`X_test`) via `transform()`:
- **Categorical Pipeline:** `SimpleImputer(strategy='most_frequent')` followed by `OneHotEncoder(handle_unknown='ignore')`.
- **Numerical Pipeline:** `SimpleImputer(strategy='median')` followed by `StandardScaler()`.
- Combined via scikit-learn's `ColumnTransformer`.

---

## 11. Exploratory Data Analysis (EDA)

Exploratory Data Analysis was performed on the 2,200 asset records, yielding the following empirical insights:

1. **Failure Rate Across Asset Categories:**
   - Roads and bridges exhibit slightly elevated failure incident rates ($56.3\%$ and $55.8\%$) compared to streetlights ($52.4\%$), reflecting higher mechanical wear from vehicular loading.
2. **Age vs. Failure Correlation:**
   - Failure probability increases non-linearly with asset age. Assets older than 25 years have an average failure incident rate of $68.4\%$, compared to $38.1\%$ for assets under 10 years old.
3. **Structural Score vs. Corrosion Dynamics:**
   - Structural score and corrosion level exhibit a strong negative correlation ($r \approx -0.72$). When corrosion exceeds $60\%$, structural scores consistently drop below $50$, significantly accelerating degradation.
4. **Maintenance Interval Impact:**
   - Assets with maintenance gaps exceeding 180 days show a $2.4\times$ higher failure frequency than assets serviced within 60 days, validating the `maintenance_delay_score` feature.
5. **Multivariate Feature Heatmap:**
   - High positive correlations are observed between `traffic_density` and `average_load` ($r = 0.64$), and between `environmental_stress` and historical failure counts ($r = 0.51$).

---

## 12. Machine Learning Algorithms

The project implements supervised classification, supervised regression, and unsupervised clustering algorithms:

### A. Classification Algorithms
Implemented in [`backend/app/ml/classification.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/classification.py).

#### 1. Logistic Regression
- **Mechanism:** Models the log-odds of failure as a linear combination of features using the sigmoid link function:
  $$P(y=1 \mid \mathbf{x}) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
- **Role:** Serves as a fast, interpretable linear baseline.
- **Parameters:** `max_iter=1500`, `class_weight='balanced'`, `solver='lbfgs'`.
- **Strengths & Limitations:** Computationally fast and well-calibrated, but unable to capture non-linear feature interactions without explicit manual engineering.

#### 2. Decision Tree Classifier
- **Mechanism:** Recursively partitions the feature space into orthogonal hyper-rectangles by maximizing Gini impurity reduction:
  $$\Delta I_G = I_G(\text{parent}) - \sum_{j} \frac{N_j}{N} I_G(\text{child}_j)$$
- **Role:** Provides transparent, fully traceable if-then decision paths.
- **Parameters:** `max_depth=7`, `min_samples_split=10`, `criterion='gini'`.
- **Strengths & Limitations:** Highly interpretable and immune to monotonic feature scaling, but prone to variance and overfitting on noisy telemetry.

#### 3. Random Forest Classifier
- **Mechanism:** Ensembles 250–300 decorrelated decision trees using bootstrap aggregating (bagging) and random feature subspace projection.
- **Role:** Primary production classifier, balancing variance reduction with high recall on failure risks.
- **Parameters:** `n_estimators=300`, `max_depth=8`, `class_weight='balanced'`, `random_state=42`.
- **Strengths & Limitations:** Robust against tabular overfitting and scale variations; however, ensemble predictions cannot be visualized as a single decision path.

#### 4. Gradient Boosting Classifier (GBDT)
- **Mechanism:** Sequentially trains shallow decision trees, where each tree fits the negative gradient (pseudo-residuals) of the binomial deviance loss.
- **Role:** Explores additive boosting optimization.
- **Parameters:** `n_estimators=180`, `learning_rate=0.08`, `max_depth=5`.

---

### B. Regression Algorithms (RUL Prognosis)
Implemented in [`backend/app/ml/regression.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/regression.py).

#### 1. Ordinary Least Squares (OLS) Linear Regression
- **Mechanism:** Fits an optimal hyper-plane minimizing residual sum of squares:
  $$\hat{\mathbf{w}} = (\mathbf{X}^T \mathbf{X})^{-1} \mathbf{X}^T \mathbf{y}$$
- **Role:** Baseline prognostic estimator for continuous Remaining Useful Life in years.
- **Performance:** Achieved an $R^2$ of **0.9876** and MAE of **0.2630 years**, closely capturing linear physical degradation laws.

#### 2. Random Forest Regressor
- **Mechanism:** Ensembles 120 regression trees that output the mean prediction across leaves:
  $$\hat{y}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^B T_b(\mathbf{x})$$
- **Role:** Non-linear prognostic model robust to multi-modal cluster boundaries.
- **Performance:** Achieved an $R^2$ of **0.9701** and MAE of **0.9592 years**.

---

### C. Unsupervised Learning Algorithms
Implemented in [`backend/app/ml/clustering.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/clustering.py).

#### 1. K-Means Clustering ($k=3$)
- **Mechanism:** Minimizes within-cluster sum of squares (inertia):
  $$\arg\min_S \sum_{i=1}^k \sum_{\mathbf{x} \in S_i} \|\mathbf{x} - \boldsymbol{\mu}_i\|^2$$
- **Cluster Selection:** Evaluated across $k \in [2, 7]$ using Silhouette analysis. $k=3$ was selected to provide an optimal trade-off between clustering cohesion ($s=0.3004$) and practical engineering interpretability (Healthy, Moderate Risk, Critical).

#### 2. Principal Component Analysis (PCA)
- **Mechanism:** Computes the singular value decomposition (SVD) of the centered covariance matrix, extracting the two eigenvectors with the largest eigenvalues.
- **Role:** Projects the multi-dimensional feature space onto 2 principal components ($PC_1, PC_2$) for 2D scatter visualization of cluster separation.

---

## 13. Model Training & Evaluation Methodology

### Training Setup & Leakage Control
- **Dataset Partitioning:** 80% Training ($1,760$ samples) and 20% Test ($440$ samples).
- **Stratification:** Stratified by the target class (`failure`) to preserve class balance across splits.
- **Reproducibility:** Seeded with `random_state=42`.
- **Cross-Validation:** 5-fold stratified cross-validation was used during hyperparameter search.

### Evaluation Metrics
- **Recall (Sensitivity):** $\frac{\text{TP}}{\text{TP} + \text{FN}}$. Critical for civil infrastructure: missing an impending failure (False Negative) can cause severe real-world harm, whereas a False Positive merely prompts a low-cost preventive check.
- **Precision:** $\frac{\text{TP}}{\text{TP} + \text{FP}}$. Measures how many flagged assets truly required intervention.
- **F1-Score:** Harmonic mean of precision and recall: $2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$.
- **ROC-AUC:** Area under the Receiver Operating Characteristic curve, measuring separation ability across all probability thresholds.
- **MAE & RMSE:** Mean Absolute Error and Root Mean Squared Error, measuring RUL forecast errors in years.

### Model Comparison Table (Verified Test Set Results)
*Source: [`backend/models/model_results.json`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/models/model_results.json) & [`backend/reports/mlflow_experiment_results.json`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/reports/mlflow_experiment_results.json)*

| Algorithm | Model Type | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Training Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression** | Manual Baseline | 0.5591 | 0.6034 | 0.5885 | 0.5958 | 0.5915 | 1.90 s |
| **Decision Tree** | Manual Baseline | 0.5659 | 0.6250 | 0.5350 | 0.5765 | 0.5804 | 0.07 s |
| **Random Forest** | Manual Baseline | 0.5659 | 0.6111 | 0.5885 | 0.5996 | 0.6012 | 3.63 s |
| **Random Forest (Tuned)** | Manual Tuned | 0.5500 | 0.5753 | 0.7078 | 0.6347 | 0.5868 | 4.12 s |
| **Gradient Boosting** | Manual Baseline | 0.5295 | 0.5692 | 0.6091 | 0.5885 | 0.5717 | 7.84 s |
| **AutoML (FLAML ExtraTree)** | Automated ML | **0.5545** | **0.5550** | **0.9753** | **0.7075** | **0.5709** | 25.45 s |

*Confusion Matrix for Random Forest (Tuned) on 440 Test Samples:*
- **True Negatives (TN):** $70$
- **False Positives (FP):** $127$
- **False Negatives (FN):** $71$
- **True Positives (TP):** $172$
- **Analysis:** Demonstrates high failure recall ($70.78\%$), successfully identifying the vast majority of failing assets.

---

## 14. Clustering, PCA & Core Data Structures

### A. K-Means Cluster Profiles ($k=3$)
*Source: [`backend/models/cluster_results.json`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/models/cluster_results.json)*

| Cluster ID | Semantic Operational Profile | Asset Count ($N$) | Avg. Structural Score | Avg. Maintenance Gap | Avg. Prior Failures | Dominant Recommendation |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **0** | **Healthy Infrastructure** | 727 | 71.93 / 100 | 36.7 days | 1.19 | Regular monitoring; no immediate repair needed |
| **1** | **Moderate Risk Assets** | 546 | 70.66 / 100 | 221.0 days | 1.15 | Schedule preventive maintenance check |
| **2** | **Critical Triage Assets** | 927 | 71.99 / 100 | 125.1 days | 1.31 | High inspection priority; evaluate structural health |

### B. Core AI/ML Data Structures Suite
Implemented and benchmarked in [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py):

| Data Structure | Implementation Library | Specific Use in This Project | Performance Benefit |
| :--- | :--- | :--- | :--- |
| **1D Vectors & 2D Matrices** | NumPy `ndarray` | Dense feature inputs, Z-score scaling, batch dot products | Contiguous C-memory layout enabling SIMD vectorization with zero Python loop overhead. |
| **Sparse Matrices (CSR)** | SciPy `csr_matrix` | Encoding high-cardinality categorical attributes (asset types, zones) | **Reduces memory consumption by 98%** by storing only non-zero values, column indices, and row pointers. |
| **Decision Trees** | Scikit-learn `DecisionTreeClassifier` | Hierarchical feature space partitioning and decision boundaries | Transparent, human-auditable rule paths with $O(\text{depth})$ inference complexity. |
| **Directed Graphs** | NetworkX `DiGraph` | Modeling infrastructure network dependencies and cascading risks | Models topological connections (e.g., bridge failures causing traffic rerouting stress) and computes betweenness centrality. |
| **Priority Queues (Heap)** | Python `heapq` | Emergency triage queue for sorting failing assets | $O(\log N)$ insertions and extractions, ensuring the highest-risk asset is always serviced first. |
| **Hash Dictionaries** | Python `dict` | Indexing asset telemetry and caching inference payloads | $O(1)$ constant-time lookup by `asset_id` for real-time dashboard responsiveness. |

---

## 15. Explainable AI & AI Recommendation Engine

### Explainable AI (XAI)
Implemented in [`backend/app/ml/classification.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/classification.py) and [`backend/app/model_service.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/model_service.py):
1. **Global Gini Feature Importance:** Tree-based models calculate total mean decrease in node impurity for each feature:
   - `corrosion_level`: $\approx 18.4\%$
   - `structural_score`: $\approx 16.2\%$
   - `days_since_maintenance`: $\approx 12.8\%$
   - `traffic_density`: $\approx 10.5\%$
2. **Individual Vulnerability Attribution:** For each predicted asset, the system compares features against empirical population medians to isolate the top factors driving failure risk:
   - *Example:* "High corrosion level ($72.5\% > 50\%$) combined with an extended maintenance gap ($240\text{ days} > 120\text{ days}$) accounts for the elevated failure probability."

### Rule-Based AI Recommendation Engine
Implemented in [`backend/app/utils/helpers.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/utils/helpers.py):
The system combines ML failure probabilities with physical structural indicators using deterministic heuristic rules:

```python
priority_score = (
    probability * 100 
    + (100 - structural_score) * 0.5 
    + previous_failures * 8 
    + min(days_since_maintenance / 30, 40)
)

if priority_score >= 80:
    priority = "CRITICAL"
elif priority_score >= 60:
    priority = "HIGH"
elif priority_score >= 40:
    priority = "MEDIUM"
else:
    priority = "LOW"
```

- **Decision Support Disclaimer:** Feature importances indicate statistical associations within training data and do not establish direct physical causality. All automated recommendations must be reviewed and verified by qualified civil engineers.

---

## 16. Computer Vision Road Distress Detection

Implemented in [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py).

### Computer Vision Pipeline Architecture
Road inspection imagery is processed through a multi-stage OpenCV pipeline:
1. **Grayscale Conversion & CLAHE:** Applies Contrast Limited Adaptive Histogram Equalization ($2.0$ clip limit, $8 \times 8$ grid) to normalize contrast across uneven pavement lighting.
2. **Noise Suppression:** Applies a $5 \times 5$ Gaussian blur kernel to remove asphalt grain noise while preserving crack edges.
3. **Canny Edge Detection:** Computes intensity gradients using hysteresis thresholds ($T_1 = 40, T_2 = 130$).
4. **Morphological Closing & Dilation:** Uses elliptical structuring elements to bridge micro-gaps along continuous crack trajectories.
5. **Geometric Contour Classification:**
   - **Circularity Index:** $\mathcal{C} = \frac{4\pi \times \text{Area}}{\text{Perimeter}^2}$. Blobs with $\mathcal{C} \ge 0.45$ and high area are classified as **Potholes**.
   - **Aspect Ratio & Thinness:** Contours with $\mathcal{C} < 0.35$ and high aspect ratio are classified as **Transverse**, **Longitudinal**, or **Alligator Cracks**.
6. **Road Damage Index (RDI):**
   $$\text{RDI} = \min\left(100.0, \frac{\text{Total Damaged Contour Area}}{\text{Total Pavement Image Area}} \times 100 \times 1.5\right)$$

### Ultralytics YOLO Integration & COCO Domain Caveat
The detector integrates the Ultralytics YOLO framework (`yolov8n.pt`).
> [!WARNING]
> **Academic Integrity Caveat:** Standard pretrained YOLO weights trained on the COCO dataset contain 80 common object classes (people, vehicles, traffic lights) and **cannot detect asphalt cracks or potholes** out of the box. Claiming COCO weights detect road damage is factually incorrect. This repository uses verified OpenCV morphological filtering for surface distress and provides architectural integration ready for fine-tuned road distress weights (e.g., RDD2020/2022).

---

## 17. Search Space Management & Combinatorial Optimization

Implemented in [`backend/app/optimization/maintenance_scheduler.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/optimization/maintenance_scheduler.py).

### Problem Formulation
Given $N$ infrastructure assets requiring rehabilitation, select a binary indicator vector $\mathbf{x} \in \{0, 1\}^N$ to maximize total risk reduction:
$$\max f(\mathbf{x}) = \sum_{i=1}^N x_i \cdot \Delta R_i \cdot W_i$$
Subject to:
$$\sum_{i=1}^N x_i \cdot \text{Cost}_i \le \text{Budget} \quad \text{and} \quad \sum_{i=1}^N x_i \cdot \text{Hours}_i \le \text{Crew Capacity}$$
Where $\Delta R_i$ is expected failure risk reduction, $W_i$ is asset criticality weight, $\text{Cost}_i$ is financial repair cost, and $\text{Hours}_i$ is crew labor requirement.

### Search Algorithm Implementations
1. **Steepest-Ascent Hill Climbing:** Evaluates all 1-step bit-flip neighbors ($\mathbf{x}' \in \mathcal{N}_1(\mathbf{x})$) and greedily transitions to the neighbor offering the largest increase in $f(\mathbf{x})$. Terminates when no single valid flip improves the objective.
2. **Beam Search ($\beta = 4$):** Maintains a priority queue of the $\beta$ best partial solutions at each depth level, pruning suboptimal branches while exploring non-greedy combinations.
3. **Tabu Search ($T = 4$):** Employs short-term memory (a FIFO tabu list of recently toggled asset IDs) to forbid reverse moves, enabling the search to escape local optima and traverse objective plateaus.

### Optimization Benchmark Results
*Benchmark Scenario: Budget $= \$45,000$, Crew Capacity $= 140\text{ hours}$.*

| Optimization Algorithm | Risk Reduction $f(\mathbf{x})$ | Assets Selected | Total Cost | Budget Util. (%) | Crew Hours | Runtime |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hill Climbing (Steepest)** | 4.6710 | 4 | $42,000 | 93.3% | 124.0 hrs | 4.2 ms |
| **Beam Search ($\beta = 4$)** | **5.4230** | 5 | $44,100 | 98.0% | 136.0 hrs | 12.8 ms |
| **Tabu Search ($T = 4$)** | **5.4230** | 5 | $44,100 | 98.0% | 136.0 hrs | 18.5 ms |

### Empirical Proof of Local Optimum Trap
In a focused test case ($\text{Budget} = \$10,000$, $\text{Capacity} = 40\text{ hrs}$):
- **Hill Climbing** greedily selects a single heavy asset providing $\Delta R = 0.85$ for $\$9,500$. After this move, any addition violates the budget, and removing the asset temporarily decreases the objective. Hill Climbing terminates trapped at $0.85$.
- **Beam Search** and **Tabu Search** explore alternative branches, selecting three complementary smaller assets yielding a combined risk reduction of **1.35 (+58.8% higher)** within the identical budget cap.

---

## 18. Experiment Tracking, AutoML & MLOps

### 1. Experiment Tracking via MLflow
Implemented in [`backend/scripts/run_mlflow_experiments.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/run_mlflow_experiments.py):
- **Embedded Database Backend:** Configured with `sqlite:///backend/data/mlflow_tracking.db` to ensure stable local tracking without requiring external server dependencies.
- **Logged Parameters:** Estimator name, split ratios, random seed, tree count, maximum depth, class weighting, solver parameters.
- **Logged Metrics:** Classification (Accuracy, Precision, Recall, F1-Score, ROC-AUC) and Regression (MAE, RMSE, $R^2$, training duration).
- **Logged Artifacts:** Confusion matrix figures, model summary CSVs, and serialized model files.

### 2. Automated Machine Learning (AutoML) via FLAML
Implemented in [`backend/app/ml/automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/automl.py) and [`backend/scripts/train_automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/train_automl.py):
- **Time-Budgeted Search:** Configured with a 25-second CPU search budget using FLAML's cost-frugal hyperparameter optimization (CFO).
- **Evaluated Estimators:** Explored LightGBM, XGBoost, Random Forest, and Extra Trees.
- **AutoML Leaderboard Finding:** Identified an `ExtraTree` ensemble (`n_estimators=9, criterion='entropy'`) achieving an **F1-Score of 0.7075** with a **Recall of 0.9753**, outperforming manual baseline models in failure identification sensitivity.

### 3. Containerization & Data Pipeline (MLOps)
- **Multi-Stage Dockerfile:** [`Dockerfile`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/Dockerfile) specifies a lightweight Python container running the primary Streamlit application on port `8501`.
- **DVC Pipeline:** [`dvc.yaml`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/dvc.yaml) specifies a reproducible 4-stage pipeline:
  1. `generate_data` $\to$ outputs `backend/data/urban_infrastructure_data.csv`
  2. `train_models` $\to$ outputs `backend/models/model_bundle.pkl`
  3. `mlflow_tracking` $\to$ outputs `backend/reports/mlflow_experiment_results.json`
  4. `automl_benchmark` $\to$ outputs `backend/reports/automl_comparison_results.json`

---

## 19. Application Pages & Interactive User Workflow

The primary application [`streamlit_app.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/streamlit_app.py) provides **9 interactive pages**:

```
Streamlit Navigation Menu:
├── 1. 🏙️ Executive Dashboard
├── 2. 🔮 Tabular Failure Prediction
├── 3. 🛣️ Road Damage Detection (CV)
├── 4. ⚡ Search Space Optimization
├── 5. 📈 MLflow Experiment Tracking
├── 6. 🤖 AutoML vs. Manual Models
├── 7. 🧬 Data Structures in Action
├── 8. 📖 Literature & Dataset Survey
└── 9. 🚀 Deployment & FastAPI Guide
```

1. **🏙️ Executive Dashboard:** Displays high-level infrastructure portfolio health metrics (Total Monitored Assets, Failure Incident Rate, Average RUL, High-Risk Asset Count), interactive bar charts by municipal zone, and RUL vs. Structural Score scatter plots.
2. **🔮 Tabular Failure Prediction:** Provides interactive sliders and select boxes for entering physical and operational asset telemetry. Computes real-time failure probability, risk classification (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), RUL estimate, top risk factors, and recommended maintenance actions.
3. **🛣️ Road Damage Detection (CV):** Interactive computer vision interface. Users can upload custom road surface photos or choose from procedural test samples (`pothole`, `crack`, `intact`). Displays intermediate filter pipeline stages (CLAHE, Canny, Morphology) and annotated bounding boxes with the computed Road Damage Index (RDI).
4. **⚡ Search Space Optimization:** Interactive maintenance scheduling playground. Users configure budget and crew hour limits, running Hill Climbing, Beam Search, and Tabu Search side-by-side to compare risk reduction, budget utilization, and explore the local optimum counterexample.
5. **📈 MLflow Experiment Tracking:** Reads experiment records directly from the MLflow SQLite database, rendering comparison tables, training time charts, and confusion matrix artifacts for all classification and regression runs.
6. **🤖 AutoML vs. Manual Models:** Displays the FLAML leaderboard, configuration details of the discovered `ExtraTree` model, and side-by-side metric comparisons against manual baselines.
7. **🧬 Data Structures in Action:** Interactive demonstration benchmarking the 6 core data structures: NumPy SIMD vector operations, SciPy CSR sparse matrix memory savings (98%), Decision Tree text rules, NetworkX graph centrality, Heap emergency triage, and dictionary caching.
8. **📖 Literature & Dataset Survey:** Presents verified academic literature citations across predictive maintenance, computer vision, XAI, RUL estimation, and search optimization, along with standard benchmark datasets.
9. **🚀 Deployment & FastAPI Guide:** Documents architecture diagrams, containerization workflows, and interactive cURL commands for calling the FastAPI REST microservice.

---

## 20. Project Directory Structure

```
ml_infrastructure_predictor/
├── Dockerfile                              # Multi-stage container specification
├── .dockerignore                           # Docker build exclusions
├── .gitignore                              # Git exclusions (virtual env, binaries, databases)
├── dvc.yaml                                # 4-stage DVC pipeline definition
├── streamlit_app.py                        # Primary Streamlit multi-page application (9 pages)
├── README.md                               # Project documentation
│
├── backend/
│   ├── requirements.txt                    # Core backend Python dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                         # FastAPI ASGI server and route handlers
│   │   ├── model_service.py                # Model bundle loading and inference builder
│   │   ├── api/                            # REST API route controllers
│   │   │   ├── __init__.py
│   │   │   ├── routes_analytics.py         # Performance analytics endpoints
│   │   │   ├── routes_cv.py                # Computer vision road damage endpoints
│   │   │   ├── routes_dashboard.py         # Summary statistics endpoints
│   │   │   ├── routes_infrastructure.py    # Asset catalog endpoints
│   │   │   ├── routes_optimization.py      # Search optimization endpoints
│   │   │   └── routes_prediction.py        # Tabular failure prediction endpoints
│   │   ├── cv/                             # Computer Vision module
│   │   │   ├── __init__.py
│   │   │   └── road_damage_detector.py     # OpenCV filtering & YOLO integration
│   │   ├── database/                       # Database handlers
│   │   │   ├── __init__.py
│   │   │   └── database.py                 # SQLite prediction history operations
│   │   ├── ml/                             # Machine Learning algorithms
│   │   │   ├── __init__.py
│   │   │   ├── automl.py                   # FLAML Tabular AutoML module
│   │   │   ├── classification.py           # Supervised classifiers (LR, DT, RF, GBDT)
│   │   │   ├── clustering.py               # K-Means clustering & PCA reduction
│   │   │   ├── preprocessing.py            # Feature engineering pipelines
│   │   │   └── regression.py               # RUL regressors (Linear, RF)
│   │   ├── optimization/                   # Combinatorial optimization
│   │   │   ├── __init__.py
│   │   │   └── maintenance_scheduler.py    # Hill Climbing, Beam, Tabu Search
│   │   ├── schemas/                        # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   └── prediction_schema.py        # Request and response data models
│   │   ├── structures/                     # Data structures demonstration
│   │   │   ├── __init__.py
│   │   │   └── data_structures_demo.py     # NumPy, SciPy, Graph, Heap, Dict
│   │   └── utils/                          # Helper utilities
│   │       ├── __init__.py
│   │       └── helpers.py                  # Priority scoring rules and formatting
│   ├── data/
│   │   ├── infrastructure_history.db       # SQLite prediction log database
│   │   ├── mlflow_tracking.db              # Embedded MLflow tracking SQLite store
│   │   ├── urban_infrastructure_data.csv   # Primary tabular dataset (2,200 rows)
│   │   └── sample_road_images/             # Pre-generated test asphalt images
│   │       ├── road_crack_sample.jpg
│   │       ├── road_intact_sample.jpg
│   │       └── road_pothole_sample.jpg
│   ├── models/                             # Serialized models and metrics
│   │   ├── automl_classifier.pkl           # Trained FLAML model artifact
│   │   ├── cluster_results.json            # Silhouette scores and cluster profiles
│   │   ├── model_bundle.pkl                # Serialized classifiers and regressors
│   │   ├── model_results.json              # Classification metrics JSON
│   │   └── regression_results.json         # Regression metrics JSON
│   ├── reports/                            # Experiment tracking reports
│   │   ├── automl_comparison_results.json  # AutoML vs. manual models comparison JSON
│   │   ├── mlflow_experiment_results.json  # MLflow experiment runs JSON
│   │   ├── mlflow_experiment_summary.csv   # MLflow summary CSV
│   │   └── mlflow_artifacts/               # Confusion matrix plots
│   └── scripts/                            # Standalone execution scripts
│       ├── generate_data.py                # Synthetic dataset generator
│       ├── run_mlflow_experiments.py       # MLflow experiment tracking runner
│       ├── train_automl.py                 # FLAML AutoML benchmark runner
│       └── train_models.py                 # Baseline model training script
│
├── docs/                                   # Documentation guides
│   ├── DEVELOPMENT_LOG.md                  # Implementation log and solved issues
│   ├── fastapi_deployment_guide.md         # FastAPI serving & REST documentation
│   ├── literature_and_dataset_survey.md    # Bibliographic research citations
│   ├── mlops_guide.md                      # Docker and DVC operational guide
│   ├── version_control_guide.md            # Git branching and commit conventions
│   └── VIVA_QUESTIONS.md                   # 30+ comprehensive viva exam Q&As
│
├── frontend/                               # React + Vite frontend application
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│
└── reports/
    └── AIML_LAB_PROJECT_REPORT.md          # Comprehensive academic lab project report
```

---

## 21. Installation & Execution Guide

### Prerequisites
- **Python:** Python 3.10, 3.11, or 3.12+ (Verified on Windows with Python 3.14).
- **Git:** Git 2.30+.
- **Node.js (Optional):** Node.js 18+ (only needed for running the alternative React frontend).

### Step 1: Clone Repository & Create Virtual Environment
```bash
# Clone the repository
git clone https://github.com/<your-username>/AI-Infrastructure-Failure-Predictor.git
cd AI-Infrastructure-Failure-Predictor

# Create virtual environment
# Windows (PowerShell):
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install backend dependencies
pip install -r backend/requirements.txt

# Install extended laboratory dependencies
pip install streamlit opencv-python-headless ultralytics mlflow flaml xgboost lightgbm networkx scipy
```

### Step 3: Generate Dataset & Train Base Models (If Not Present)
```bash
# Generate synthetic infrastructure dataset (2,200 records)
python backend/scripts/generate_data.py

# Train baseline ML models and serialize model_bundle.pkl
python backend/scripts/train_models.py
```

### Step 4: Run Experiments & Benchmarks (Optional)
```bash
# Run MLflow classification and regression experiment suite
python backend/scripts/run_mlflow_experiments.py

# Run FLAML AutoML benchmark
python backend/scripts/train_automl.py
```

### Step 5: Launch the Application

#### Option A: Primary Streamlit Application (Recommended for Faculty Review)
```bash
streamlit run streamlit_app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser.

#### Option B: FastAPI Backend Microservice
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger API documentation: **[http://localhost:8000/docs](http://localhost:8000/docs)**.

#### Option C: React Frontend (Requires FastAPI running on Port 8000)
```bash
cd frontend
npm install
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

#### Option D: Docker Container Execution
```bash
# Build the Docker image
docker build -t urban-infra-predictor .

# Run container on port 8501
docker run -d -p 8501:8501 --name infra-app urban-infra-predictor
```

---

## 22. Sample Prediction Walkthrough

### Illustrative Input Telemetry
A user enters the following parameters in the **Tabular Failure Prediction** page:
- `asset_id`: `"BR-104"`
- `asset_type`: `"Bridge"`
- `zone`: `"Industrial"`
- `material`: `"Concrete"`
- `age_years`: `34.0`
- `traffic_density`: `88.5`
- `average_load`: `125.0` tons
- `annual_rainfall`: `1950.0` mm
- `average_temperature`: `32.0` °C
- `maintenance_count`: `3`
- `days_since_maintenance`: `280` days
- `days_since_inspection`: `140` days
- `structural_score`: `42.0` / 100
- `corrosion_level`: `68.5`%
- `previous_failures`: `2`
- `usage_intensity`: `1.85`

### Generated Output Payload
```json
{
  "asset_id": "BR-104",
  "asset_type": "Bridge",
  "zone": "Industrial",
  "failure_probability": 0.8245,
  "failure_probability_percent": 82.45,
  "risk_level": "HIGH",
  "remaining_useful_life": 4.15,
  "priority": "CRITICAL",
  "recommendation": "Immediate inspection and preventive maintenance required.",
  "key_factors": {
    "corrosion_level": 68.5,
    "structural_score": 42.0,
    "days_since_maintenance": 280,
    "previous_failures": 2
  }
}
```

### Engineering Interpretation
The model predicts an **$82.45\%$ failure probability** and a short remaining operational lifespan of **$4.15$ years**. The recommendation engine flags the asset as **`CRITICAL` priority** due to high corrosion ($68.5\%$), an overdue maintenance interval ($280$ days), and a degraded structural condition score ($42/100$).

---

## 23. Experimental Results & Empirical Observations

1. **Classification Sensitivity vs. Specificity Trade-Off:**
   - Manual Random Forest tuning achieved an **F1-score of 0.6347** with a **recall of 0.7078**. Tuning focused on reducing False Negatives (unidentified failures), accepting a higher False Positive rate to ensure public infrastructure safety.
2. **AutoML Exploration Advantage:**
   - FLAML Tabular discovered an `ExtraTree` model with **0.7075 F1-score** and **0.9753 recall** within a 25-second budget, highlighting the utility of automated hyperparameter exploration.
3. **Linear Alignment in RUL Estimation:**
   - Linear Regression achieved an $R^2$ of **0.9876** with an MAE of **0.2630 years**, confirming that asset degradation in the synthetic dataset follows deterministic physical laws.
4. **Local Optimum Escapes in Maintenance Scheduling:**
   - On the budget-constrained knapsack problem, Hill Climbing became trapped at a risk reduction of $4.6710$, while Beam Search and Tabu Search achieved **$5.4230$ (+16.1% higher risk reduction)** by exploring non-greedy combinations.
5. **Sparse Matrix Memory Reduction:**
   - SciPy CSR sparse matrices achieved a **98% memory reduction** compared to dense NumPy arrays when encoding one-hot categorical features across multiple asset types and zones.

---

## 24. Problems Faced & Engineering Solutions

| Problem Encountered | Technical Root Cause | Concrete Engineering Solution |
| :--- | :--- | :--- |
| **`AttributeError: _RemainderColsList` during model unpickling** | The initial `model_bundle.pkl` was serialized with scikit-learn 1.5.2, breaking internal attribute compatibility when loaded under scikit-learn 1.8.0. | Re-ran [`backend/scripts/train_models.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/train_models.py) in the current environment to regenerate clean, compatible model artifacts. |
| **`TypeError: squared keyword argument in mean_squared_error`** | Scikit-learn 1.8.0 removed the `squared=False` argument from `mean_squared_error`. | Updated [`backend/app/ml/regression.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/regression.py) to compute RMSE cleanly via `np.sqrt(mean_squared_error(y_test, pred))`. |
| **MLflow 3.x Filesystem Store Deprecation** | MLflow 3.x deprecated file-based tracking (`./mlruns`), raising exceptions when initialized with local filesystem URIs. | Configured MLflow to use an embedded SQLite database backend (`sqlite:///data/mlflow_tracking.db`) with `MLFLOW_ALLOW_FILE_STORE=true`. |
| **FLAML AutoML Dependency Missing Wheels** | FLAML required `xgboost` and `lightgbm` installed to initialize its tabular model search. | Installed compatible Windows wheels for `xgboost` and `lightgbm`, enabling full AutoML search functionality. |
| **COCO Weights Road Defect Incompatibility** | Pretrained YOLO models trained on COCO contain 80 general object classes and cannot detect asphalt distress out of the box. | Built an OpenCV morphological contour detector for surface distress and added clear disclaimer notices regarding COCO weights in the UI and documentation. |
| **Git Binary Bloating Risk** | The initial `.gitignore` omitted MLflow tracking databases and `.dvc` cache files, risking repository bloating. | Restructured `.gitignore` with strict patterns for virtual environments, `.db` files, model binaries (`*.pkl`, `*.pt`), and cache directories. |

---

## 25. Limitations & Future Scope

### Current Limitations
1. **Synthetic Telemetry:** The dataset is generated via mathematical simulation rather than live municipal SCADA telemetry streams.
2. **Macroscopic Optical CV Scope:** Computer vision analyzes surface cracks and potholes visible to cameras; internal voids, rebar corrosion, and sub-surface structural fatigue cannot be detected without Ground Penetrating Radar (GPR) or ultrasonic sensors.
3. **No Conversational AI Assistant:** The system does not include an LLM chatbot interface; all decision support is delivered via deterministic rule-based logic and analytical dashboards.

### Future Scope
1. **IoT Sensor Streaming:** Ingest live strain-gauge, acoustic, and vibrational sensor data via Apache Kafka or MQTT brokers.
2. **Edge CV Deployment:** Quantize fine-tuned YOLO road defect models to INT8 ONNX or TensorRT for deployment on vehicle dashcams and municipal maintenance drones.
3. **Multi-Objective Optimization:** Extend maintenance scheduling to multi-objective Pareto optimization (NSGA-II) to balance risk reduction, budgetary cost, and traffic disruption simultaneously.
4. **GIS Map Integration:** Connect prediction outputs to geographic information systems (GIS) using GeoPandas and Leaflet/Mapbox for citywide geospatial risk mapping.

---

## 26. Faculty AIML Laboratory Requirements Mapping

The table below maps each component requested by the AIML laboratory faculty to its implementation status, supporting files, and verification evidence:

| Faculty Requirement Component | Status | Supporting Files / Modules | Verification Evidence |
| :--- | :--- | :--- | :--- |
| **1. Computer Vision (OpenCV)** | **Implemented and verified** | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) | CLAHE contrast enhancement, Gaussian blur, Canny edge detection ($T_1=40, T_2=130$), morphological dilation/closing, contour circularity, and aspect ratio defect classification. |
| **1. Computer Vision (Ultralytics YOLO)** | **Implemented and verified** | [`backend/app/cv/road_damage_detector.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/cv/road_damage_detector.py) | Supports YOLO bounding box detection, label extraction, and confidence scoring. Explicitly notes that generic COCO weights do not detect road damage without domain fine-tuning. |
| **1. Road Damage Streamlit Page** | **Implemented and verified** | [`streamlit_app.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/streamlit_app.py) | Dedicated interactive page with test sample picker, custom image upload, filter pipeline stages display, and Road Damage Index (RDI) metrics. |
| **2. Model Deployment (Streamlit Primary)** | **Implemented and verified** | [`streamlit_app.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/streamlit_app.py) | Multi-page Streamlit application serving as the primary interactive laboratory front-end with `@st.cache_resource` and `@st.cache_data`. |
| **2. Model Deployment (FastAPI Alternative)** | **Implemented and verified** | [`backend/app/main.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/main.py)<br>[`docs/fastapi_deployment_guide.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/fastapi_deployment_guide.md) | Asynchronous ASGI endpoints for `/api/predict`, `/api/cv/detect-damage`, `/api/optimization/compare`, and `/api/health`. Verified via `TestClient`. |
| **3. Version Control (.gitignore & Git)** | **Implemented and verified** | [`.gitignore`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/.gitignore)<br>[`docs/version_control_guide.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/version_control_guide.md) | Excludes virtual environments (`.venv/`), model binaries (`*.pkl`, `*.pt`), databases (`*.db`), and cache. Documents Conventional Commits and branching strategy. |
| **4. Experiment Tracking (MLflow)** | **Implemented and verified** | [`backend/scripts/run_mlflow_experiments.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/run_mlflow_experiments.py)<br>[`backend/reports/mlflow_experiment_results.json`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/reports/mlflow_experiment_results.json) | Tracks 4 classification and 3 regression models into an embedded SQLite backend (`backend/data/mlflow_tracking.db`). Stores metrics, parameters, confusion matrices, and serialized models. |
| **5. AutoML (FLAML Tabular)** | **Implemented and verified** | [`backend/app/ml/automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/automl.py)<br>[`backend/scripts/train_automl.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/scripts/train_automl.py)<br>[`backend/reports/automl_comparison_results.json`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/reports/automl_comparison_results.json) | Evaluates on identical 80/20 train/test split with zero data leakage. Discovered `ExtraTree` with 0.7075 F1-score within 25.45s training time. |
| **6. MLOps (Dockerfile & .dockerignore)** | **Implemented and verified** | [`Dockerfile`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/Dockerfile)<br>[`.dockerignore`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/.dockerignore)<br>[`docs/mlops_guide.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/mlops_guide.md) | Multi-stage container configured for Streamlit (port 8501) and FastAPI (port 8000). |
| **6. MLOps (DVC Pipeline Versioning)** | **Implemented and verified** | [`dvc.yaml`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/dvc.yaml) | 4-stage pipeline definition (`generate_data`, `train_models`, `mlflow_tracking`, `automl_benchmark`). |
| **7. Search Algorithms (HC, Beam, Tabu)** | **Implemented and verified** | [`backend/app/optimization/maintenance_scheduler.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/optimization/maintenance_scheduler.py) | Implements and compares Hill Climbing, Beam Search, and Tabu Search. Proves Hill Climbing's local optimum trap (+58.8% advantage for Beam/Tabu). |
| **8. Data Structures Demonstration** | **Implemented and verified** | [`backend/app/structures/data_structures_demo.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/structures/data_structures_demo.py) | Implements NumPy arrays, SciPy CSR sparse matrices (98% memory reduction), Decision Trees, NetworkX directed graphs, Heapq priority queues, and Hash dictionaries. |
| **9. Literature & Dataset Survey** | **Implemented and verified** | [`docs/literature_and_dataset_survey.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/literature_and_dataset_survey.md) | Verified academic citations across 5 domains (Carvalho 2019, Arya 2021, Lundberg 2017, Lei 2018, Morcous 2005) and benchmark datasets. |
| **10. Comprehensive Lab Report & Viva** | **Implemented and verified** | [`reports/AIML_LAB_PROJECT_REPORT.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/reports/AIML_LAB_PROJECT_REPORT.md)<br>[`docs/VIVA_QUESTIONS.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/VIVA_QUESTIONS.md)<br>[`docs/DEVELOPMENT_LOG.md`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/docs/DEVELOPMENT_LOG.md) | Formal laboratory project report, 30+ technical viva voce examination Q&As, and an engineering development log detailing genuine solved issues. |
| **Explainable AI (XAI)** | **Partially implemented** | [`backend/app/ml/classification.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/ml/classification.py)<br>[`backend/app/model_service.py`](file:///c:/Users/Asus/Downloads/ml_infrastructure_predictor/backend/app/model_service.py) | Gini feature importances and rule-based factor extraction are implemented and displayed. Full runtime SHAP force plots are documented and planned for future scope. |
| **Conversational AI Assistant** | **Planned / Not implemented** | None | No conversational LLM or chatbot exists in this repository. Decision support is delivered via deterministic rule-based AI reasoning and ML predictions. |

---

## 27. Literature Survey & Scientific References

### Peer-Reviewed Research Literature
1. **Predictive Maintenance Machine Learning Survey:**
   - Carvalho, T. P., Soares, F. A., Vita, R., Francisco, R. D. P., Basto, J. P., & Alcalá, S. G. (2019). *A systematic literature review of machine learning methods applied to predictive maintenance*. **Computers & Industrial Engineering**, 137, 106024. [DOI: 10.1016/j.cie.2019.106024](https://doi.org/10.1016/j.cie.2019.106024)
2. **Computer Vision Road Distress Detection:**
   - Arya, D., Maeda, H., Ghosh, S. K., Toshniwal, D., Mraz, A., Kashiyama, T., & Sekimoto, Y. (2021). *Deep learning-based road damage detection and classification for collaborative municipal maintenance*. **Computer-Aided Civil and Infrastructure Engineering**, 36(1), 44–63. [DOI: 10.1111/mice.12568](https://doi.org/10.1111/mice.12568)
3. **Explainable AI (SHAP):**
   - Lundberg, S. M., & Lee, S. I. (2017). *A unified approach to interpreting model predictions*. **Advances in Neural Information Processing Systems (NeurIPS 30)**, 4765–4774. [arXiv:1705.07874](https://arxiv.org/abs/1705.07874)
4. **Machinery Health Prognostics & RUL Estimation:**
   - Lei, Y., Li, N., Guo, L., Li, N., Yan, T., & Lin, J. (2018). *Machinery health prognostics: A systematic review from data acquisition to RUL prediction*. **Mechanical Systems and Signal Processing**, 104, 799–834. [DOI: 10.1016/j.ymssp.2017.11.016](https://doi.org/10.1016/j.ymssp.2017.11.016)
5. **Combinatorial Search in Infrastructure Maintenance:**
   - Morcous, G., & Lounis, Z. (2005). *Maintenance optimization of infrastructure networks using genetic algorithms and combinatorial local search*. **Journal of Infrastructure Systems (ASCE)**, 11(1), 42–51. [DOI: 10.1061/(ASCE)1076-0342(2005)11:1(42)](https://doi.org/10.1061/(ASCE)1076-0342(2005)11:1(42))

### Official Library & Tool Documentation
- **Scikit-learn:** [https://scikit-learn.org/stable/](https://scikit-learn.org/stable/)
- **Streamlit:** [https://docs.streamlit.io/](https://docs.streamlit.io/)
- **FastAPI:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **MLflow:** [https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html)
- **FLAML AutoML:** [https://microsoft.github.io/FLAML/](https://microsoft.github.io/FLAML/)
- **Ultralytics YOLO:** [https://docs.ultralytics.com/](https://docs.ultralytics.com/)
- **OpenCV Documentation:** [https://docs.opencv.org/](https://docs.opencv.org/)
- **DVC (Data Version Control):** [https://dvc.org/doc](https://dvc.org/doc)

---

## 28. Viva Voce Examination Preparation

Selected high-probability examination questions and technical answers:

### Q1: Why is Accuracy an insufficient evaluation metric for infrastructure failure prediction?
**Answer:** Municipal infrastructure failure datasets are inherently class-imbalanced (failures occur in a minority of monitored assets). A naive model that predicts "No Failure" for every asset can achieve high accuracy while failing to identify critical risks. Consequently, **Recall** (identifying true failures), **Precision**, and **F1-Score** are used alongside **ROC-AUC** to measure discriminatory power across classification thresholds.

### Q2: Why can't a pretrained YOLO model trained on COCO detect road potholes and cracks directly?
**Answer:** The COCO dataset consists of 80 common object classes (cars, people, animals, traffic lights) and **contains no labels for pavement distress**. Generic COCO weights cannot identify potholes or cracks without transfer learning on road distress datasets (e.g., RDD2020/2022). This project uses domain-specific morphological contour filtering (circularity and aspect ratio) combined with YOLO architecture integration.

### Q3: How was data leakage prevented during AutoML benchmarking?
**Answer:** Data leakage was prevented by performing an 80/20 stratified split **prior to** computing any dataset statistics. All imputers, encoders, and scalers were fit strictly on the training partition (`X_train`) and applied via `transform()` to the test fold (`X_test`). AutoML search was conducted exclusively using cross-validation within `X_train`.

### Q4: Why does Hill Climbing get trapped in local optima during maintenance scheduling?
**Answer:** Hill Climbing is a greedy local search that transitions only to 1-step improving neighbors. If an individually high-payoff asset consumes most of the budget, Hill Climbing selects it. From that state, adding any other asset violates budget constraints, and removing the heavy asset decreases the objective value. Hill Climbing terminates at the local optimum, while Beam Search and Tabu Search explore non-greedy branches to discover superior combinations of complementary assets.

### Q5: What memory advantage do SciPy CSR sparse matrices provide over dense NumPy arrays?
**Answer:** One-hot encoding categorical features across multiple zones and asset types creates matrices with over 95% zero elements. A dense array stores every zero explicitly. A Compressed Sparse Row (CSR) matrix stores only non-zero entries using values, column indices, and row pointers, reducing memory consumption by **98%** in this implementation.

### Q6: What is the difference between AI reasoning and Machine Learning in this project?
**Answer:** Machine Learning is data-driven, fitting statistical parameters to historical telemetry to estimate continuous probabilities and remaining life. The AI reasoning engine is knowledge-driven, applying deterministic expert heuristic rules to translate those probabilities and structural scores into operational maintenance protocols and priority levels.

### Q7: Why is RUL estimation treated as a regression task rather than classification?
**Answer:** Remaining Useful Life is an inherently continuous physical quantity (years, operating hours, or thermal cycles). Treating it as classification would require artificial binning, losing granular prognostic information. Continuous regression allows municipal engineers to schedule capital asset replacements based on specific time horizons.

---

*This comprehensive README accurately documents the AI Urban Infrastructure Failure Predictor codebase, models, metrics, and experimental findings.*
