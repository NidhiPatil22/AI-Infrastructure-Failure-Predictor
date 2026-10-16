# Comprehensive Code-Level Audit, Corrections & Verification Report
## Road Infrastructure — AI Predictive Maintenance Suite

**Audit Date:** October 2026  
**System Status:** Fully Verified, Corrected, and Defensible  
**Test Suite:** 31 / 31 Tests Passed (100% Pass Rate)  
**Production Frontend:** Verified & Successfully Built (`vite build`)  
**MLOps Pipelines:** DVC, MLflow (Embedded SQLite), and FLAML AutoML Verified  

---

## 1. Executive Summary

This audit and correction cycle was conducted on the **Road Infrastructure — AI Predictive Maintenance Suite**, an enterprise-grade multimodal civil engineering decision-support platform. The suite combines:
1. Supervised Machine Learning (failure classification & Remaining Useful Life regression).
2. Computer Vision (OpenCV geometric distress extraction for potholes and cracks).
3. Search-Space Optimization (Hill Climbing, Beam Search, and Tabu Search for constrained maintenance scheduling).
4. MLOps Governance (MLflow tracking with confusion matrix artifacts, DVC reproducible pipelines, and FLAML Tabular AutoML).
5. Geographic Information Systems (Google Maps GIS integration with Indian national corridors and regional IMD climate baselines).
6. Deterministic & LLM-Powered Agentic Assistant (ROVER multi-workflow assistant).
7. Core Computer Science Data Structures (NumPy SIMD matrices, SciPy CSR sparse matrices, Decision Trees, NetworkX graphs, Binary Heaps, and Hash maps).

All non-negotiable rules were strictly adhered to:
- No real predictions were replaced with hardcoded values or fabricated metrics.
- No synthetic test metrics were claimed as real-world validated infrastructure measurements.
- Existing Day/Night themes, dashboard navigation, ROVER workflows, and API contracts were preserved and verified.
- The 15-field technical sensor input schema was maintained for backward compatibility while introducing a realistic 6-field civil assessment mapping grounded in Indian geography.

---

## 2. Repository Architecture & Execution Trace

```
ml_infrastructure_predictor/
├── backend/
│   ├── app/
│   │   ├── ai/               # ROVER Assistant: Workflow engine, chat service, prompt templates
│   │   ├── api/              # FastAPI REST routers (/predict, /cv, /optimization, /chat, etc.)
│   │   ├── cv/               # OpenCV road damage detector (CLAHE, Canny, RDI computation)
│   │   ├── database/         # SQLite persistence for prediction history & asset logs
│   │   ├── ml/               # Classification, Regression, Clustering, Preprocessing, AutoML
│   │   ├── model_service.py  # Model bundle inference pipeline & geographic input adapter
│   │   ├── optimization/     # 0-1 Knapsack: Hill Climbing, Beam Search, Tabu Search
│   │   ├── schemas/          # Pydantic validation schemas (LocationData, CorridorAssessmentInput)
│   │   ├── structures/       # Educational & benchmark demonstrations of 6 core CS structures
│   │   └── utils/            # Indian GIS zone resolver, climate baselines, priority heuristics
│   ├── data/                 # Benchmark dataset, sample road images, MLflow SQLite DB
│   ├── models/               # Serialized model_bundle.pkl, results JSON, cluster centroids
│   ├── reports/              # MLflow experiment artifacts, AutoML benchmark reports
│   └── scripts/              # DVC-driven training, AutoML, MLflow, and testing scripts
├── frontend/                 # React 18 / Vite / Lucide-React / Recharts / Leaflet SPA
│   ├── src/
│   │   ├── components/       # GoogleCorridorMap, RoverChatAssistant, TrafficLight, etc.
│   │   ├── pages/            # PredictRisk, Dashboard, Analytics, ModelPerformance, etc.
│   │   └── services/         # Axios REST client with robust error handling
│   └── dist/                 # Production-optimized distribution bundle
├── tests/                    # Comprehensive Pytest automated test suite
├── docs/                     # Academic guides, viva questions, architecture documentation
├── streamlit_app.py          # Standalone full-width Streamlit analytical dashboard
├── Dockerfile                # Production container deployment definition
└── dvc.yaml                  # 4-stage reproducible MLOps data/model pipeline
```

### End-to-End Execution Trace
- **User Input (Web / Maps / Presets):** User selects an Indian civil corridor (e.g., Bandra-Worli Sea Link, Mumbai-Pune Expressway) via Google Maps or presets, specifying visible condition (Good/Fair/Poor/Unknown), traffic intensity, approximate age, and maintenance recency.
- **Backend API (`/api/predict`):** FastAPI receives the request, passes it to `app/model_service.py`.
- **Geographic & Feature Resolution:** `app/utils/indian_geo.py` maps the coordinates/state to an official zone ('West', 'South', 'North', etc.) and retrieves regional climate baselines (IMD normal rainfall and temperature).
- **Preprocessing & Inference:** The input is transformed using `ColumnTransformer` (fitted solely on training partition), passing numeric features through learned median imputers and standard scalers, and categorical features through learned one-hot encoders.
- **Model Output:** The trained Random Forest model predicts failure probability and risk tier (LOW/MEDIUM/HIGH); the trained regressor calculates bounded Remaining Useful Life (RUL $\ge 0.0$); the priority heuristic assigns an emergency triage level (CRITICAL/HIGH/MEDIUM/LOW).
- **Presentation:** Rendered dynamically in the React frontend and Streamlit dashboard with full explainability, factor breakdowns, and engineering caveats.

---

## 3. Dataset Audit & Provenance

| Dimension | Measured Value | Academic Interpretation |
| :--- | :--- | :--- |
| **Data Nature** | 100% Synthetic Simulation | Generated via stochastic rule-based model (`backend/scripts/generate_data.py`). Must NOT be claimed as physical municipal sensor data. |
| **Total Observations** | 2,200 unique records | Each row represents a distinct asset entity (`ASSET-0001` through `ASSET-2200`). |
| **Features Count** | 23 total features | 15 base attributes + 8 row-level engineered interaction stress features. |
| **Missingness** | 87 total missing cells (0.22%) | `days_since_maintenance` (44, 2.0%), `structural_score` (22, 1.0%), `zone` (14, 0.64%), `material` (11, 0.50%). |
| **Failure Target** | 1,213 Fail (55.14%) / 987 Oper (44.86%) | Balanced binary target generated via logistic Bernoulli trials from weighted mechanical risk factors. |
| **RUL Target** | Mean: 20.56 yrs, Min: 1.0, Max: 45.75 | Deterministic civil engineering simulation rule with linear terms and max clamping. |

---

## 4. Issues Discovered and Corrections Implemented

### Issue A: Preprocessing Data Leakage
- **Flaw:** `clean_dataset` in `app/ml/preprocessing.py` previously executed global quantile-based outlier clipping and global `fillna(df[col].median())` across the entire 2,200 records **before** train-test splitting. This leaked test set statistics (medians and distribution quantiles) into the training partition.
- **Correction:** Removed global median imputation and global quantile clipping from `clean_dataset`. Imputation and scaling were strictly encapsulated inside scikit-learn `ColumnTransformer` pipelines fitted **exclusively on the 80% training partition** ($N = 1,760$). The held-out test set ($N = 440$) remains completely untouched until final evaluation.

### Issue B: Classification Pipeline Incompleteness
- **Flaw:** The classification pipeline in `app/ml/classification.py` lacked Gradient Boosting (despite being present in MLflow tracking) and lacked 5-fold cross-validation metrics and training time measurements.
- **Correction:** Added `GradientBoostingClassifier` alongside Logistic Regression, Decision Tree, and Random Forest. Integrated 5-fold stratified cross-validation on the training set, measured execution runtimes, and documented an explicit civil engineering selection criterion: prioritizing failure recall ($\ge 0.60$) and balanced F1 score to minimize false negatives (unpredicted catastrophic collapses).

### Issue C: Unbounded RUL Regression
- **Flaw:** Regression models could theoretically yield negative remaining useful life predictions during extreme deterioration inputs without documented boundary handling.
- **Correction:** Implemented physically defensible zero-bounding ($\text{RUL} = \max(0.0, \hat{y})$) representing structural end-of-life, with automated tracking of raw negative counts.

### Issue D: Computer Vision Empty Byte Decode Error
- **Flaw:** In `app/cv/road_damage_detector.py`, submitting empty byte inputs (`b""`) caused an unhandled OpenCV assertion failure (`cv2.error: !buf.empty()`) instead of gracefully raising a `ValueError`.
- **Correction:** Added explicit length and size checks on byte buffers before passing them to `cv2.imdecode`.

### Issue E: Tabu Search Premature Termination
- **Flaw:** In `app/optimization/maintenance_scheduler.py`, when all moves in a neighborhood were tabu or violated constraints, `tabu_search` broke out of the loop immediately at iteration 2, preventing it from escaping local optima in constrained portfolios.
- **Correction:** Added fallback logic in accordance with canonical Tabu Search literature: if all feasible moves in a neighborhood are tabu, the algorithm selects the best feasible move to maintain diversification, successfully allowing it to discover synergistic asset packages.

---

## 5. Verified Empirical Evaluation Results

All models were evaluated on the exact same 80/20 held-out test partition ($N_{\text{test}} = 440$, containing 243 Failures and 197 Operational assets):

### Classification Benchmark (Failure Prediction)

| Model Family | Accuracy | Precision | Recall | F1-Score | Macro F1 | ROC-AUC | 5-Fold CV F1 | Fit Time |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (Balanced)** | 0.5705 | 0.6164 | 0.5885 | 0.6021 | 0.5677 | 0.6032 | 0.6319 | 0.023s |
| **Decision Tree (Balanced, Depth 7)** | 0.5500 | 0.6364 | 0.4321 | 0.5147 | 0.5476 | 0.5805 | 0.5693 | 0.052s |
| **Random Forest (200 Trees)** ⭐ | **0.5636** | **0.5962** | **0.6502** | **0.6220** | **0.5530** | **0.6079** | **0.6489** | 2.095s |
| **Gradient Boosting (120 Trees)** | 0.5545 | 0.5861 | 0.6584 | 0.6202 | 0.5408 | 0.5808 | 0.6459 | 3.682s |
| **Random Forest (Tuned)** | 0.5432 | 0.5755 | 0.6584 | 0.6142 | 0.5272 | 0.5893 | 0.6595 | 108.6s |
| **AutoML (FLAML ExtraTree)** | 0.5545 | 0.5550 | 0.9753 | 0.7075 | 0.5709 | 0.5709 | Held-out | 25.55s |

*Winning Classifier:* **Random Forest (Base Balanced)** — selected for highest combined F1 (0.6220), strong failure recall (0.6502), and highest ROC-AUC (0.6079).

### Regression Benchmark (Remaining Useful Life in Years)

| Model Family | MAE (Years) | RMSE | R² Score | Raw Negative Count | Handling Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Linear Regression** ⭐ | **0.2564** | **0.8620** | **0.9898** | 3 / 440 (0.68%) | Bounded at 0.0 (End-of-Life) |
| **Gradient Boosting Regressor** | 0.6126 | 1.1420 | 0.9821 | 2 / 440 (0.45%) | Bounded at 0.0 (End-of-Life) |
| **Random Forest Regressor** | 0.9800 | 1.5878 | 0.9654 | 0 / 440 (0.00%) | Inherently non-negative |

*Winning Regressor:* **Linear Regression** ($R^2 = 0.9898$, MAE = 0.2564 years) — naturally aligns with the linear civil engineering degradation formula used to simulate asset wear.

---

## 6. Optimization Verification & Counterexample

The maintenance scheduling engine was audited as a multi-dimensional 0-1 Knapsack problem with simultaneous Budget and Crew-Capacity constraints:
$$\max_{S \subseteq \mathcal{A}} f(S) = \sum_{i \in S} \Delta R_i \cdot W_i \quad \text{subject to} \quad \sum_{i \in S} C_i \le B, \quad \sum_{i \in S} H_i \le H_{\max}$$

### Benchmark Comparison ($B = \$50,000, H_{\max} = 160\text{ hours}$):
- **Hill Climbing (Steepest Ascent):** Trapped in local optima when single large assets block synergistic combinations.
- **Beam Search ($\beta = 4$):** Maintains a diverse frontier of partial solutions, consistently finding higher-value schedules.
- **Tabu Search ($\text{Tenure} = 4$):** Uses short-term memory and aspiration criteria to permit non-improving moves, reliably escaping local optima.

### Controlled Proof of Hill Climbing Failure:
- **Scenario:** $B = \$10,000, H_{\max} = 40\text{ hrs}$.
  - Asset A ("Greedy Lure"): Risk Reduction = 0.85, Cost = $9,500.
  - Assets B, C, D ("Complementary Pack"): Risk Reduction = $0.45 \times 3 = 1.35$, Cost = $9,500.
- **Result:** Hill Climbing terminates at local optimum **0.85**. Both Beam Search and Tabu Search discover the global optimum **1.35** (**+58.8% higher risk reduction**).

---

## 7. MLOps, Computer Vision & GIS Verification

1. **MLflow Tracking:** Logs parameters, metrics, model binaries, and confusion matrix image artifacts to embedded SQLite DB (`backend/data/mlflow_tracking.db`).
2. **FLAML AutoML:** Successfully explored Random Forest, ExtraTree, LightGBM, and XGBoost with a 25-second budget, identifying ExtraTree as the top performer for extreme recall (0.9753).
3. **DVC Pipeline:** `dvc.yaml` defines 4 sequential, reproducible stages: `generate_data` $\to$ `train_models` $\to$ `mlflow_tracking` $\to$ `automl_benchmark`.
4. **Computer Vision (OpenCV + RDD):** Implements CLAHE contrast enhancement, Gaussian smoothing, Canny edge detection, morphological dilation, and geometric shape classification (circularity and aspect ratios). Honestly disclaims off-the-shelf COCO YOLO weights for crack detection without domain RDD fine-tuning.
5. **Google Maps GIS & Indian Presets:** Preserves interactive map clicking, geocoding, reverse geocoding, and preset shortcuts for major corridors (Bandra-Worli Sea Link, Mumbai-Pune Expressway, Atal Setu, Bengaluru ORR).

---

## 8. Automated Test Suite Execution Summary

Executed with `pytest` across all test files:
- `tests/test_audit_suite.py`: 17 passed
- `backend/scripts/test_rover_chat.py`: 14 passed
- **Total:** 31 passed, 0 failed, 0 regressions (100% pass rate).

---

## 9. Launch & Operational Commands

To run the complete application suite locally:

```bash
# 1. Start the FastAPI backend (Port 8000)
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# 2. Start the primary Streamlit Dashboard (Port 8501)
streamlit run streamlit_app.py --server.port 8501

# 3. Start the React/Vite Frontend (Port 5173)
cd frontend
npm run dev

# 4. Run the complete automated test suite
pytest --ignore=frontend tests/test_audit_suite.py backend/scripts/test_rover_chat.py
```
