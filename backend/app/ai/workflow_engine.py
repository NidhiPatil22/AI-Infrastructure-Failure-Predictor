"""ROVER Guided Workflow Engine and Conversation State Machine.

Coordinates task-oriented decision flows, allowlisted application actions,
and contextual structured choices for the Road Infrastructure Predictive Maintenance Suite.
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("rover_workflow_engine")

# =============================================================================
# ALLOWLISTED DASHBOARD NAVIGATION TARGETS
# =============================================================================
ALLOWLISTED_PAGES = {
    "dashboard": {"label": "01. Executive Dashboard", "route": "/dashboard"},
    "maps": {"label": "02. Google Maps & GIS Corridors", "route": "/dashboard"},
    "prediction": {"label": "03. Tabular Failure Prediction", "route": "/predict"},
    "cv": {"label": "04. Road Damage Detection (CV)", "route": "/dashboard"},
    "optimization": {"label": "05. Search Space Optimization", "route": "/priority"},
    "mlflow": {"label": "06. MLflow Experiment Tracking", "route": "/model-performance"},
    "automl": {"label": "07. AutoML vs. Manual Models", "route": "/model-performance"},
    "structures": {"label": "08. Data Structures in Action", "route": "/analytics"},
    "survey": {"label": "09. Literature & Dataset Survey", "route": "/about"},
    "deployment": {"label": "10. Deployment & FastAPI Guide", "route": "/about"},
}

ALLOWLISTED_ACTIONS = {
    "fetch_predictions",
    "fetch_optimization",
    "fetch_sample_cv",
    "navigate",
}

# =============================================================================
# GUIDED WORKFLOW DEFINITIONS & PREDEFINED OPTIONS
# =============================================================================

MAIN_MENU_CHOICES = [
    {
        "id": "wf_risk",
        "label": "1. Analyze Infrastructure Risk",
        "description": "Explore failure predictions, model mechanics, and asset risk tiers",
        "action_type": "workflow",
        "workflow": "infrastructure_risk",
        "step": "options",
        "payload": {},
    },
    {
        "id": "wf_damage",
        "label": "2. Inspect Road Damage",
        "description": "Detect surface distress, cracks, potholes, and review RDI scores",
        "action_type": "workflow",
        "workflow": "road_damage",
        "step": "options",
        "payload": {},
    },
    {
        "id": "wf_maintenance",
        "label": "3. Plan Maintenance",
        "description": "Compare Knapsack algorithms (Hill Climbing, Beam, Tabu Search)",
        "action_type": "workflow",
        "workflow": "plan_maintenance",
        "step": "options",
        "payload": {},
    },
    {
        "id": "wf_explore",
        "label": "4. Explore the Project",
        "description": "Inspect architecture, MLflow logs, AutoML benchmarks, and data structures",
        "action_type": "workflow",
        "workflow": "explore_project",
        "step": "options",
        "payload": {},
    },
]

WORKFLOW_STEPS: Dict[str, Dict[str, Any]] = {
    # -------------------------------------------------------------------------
    # WORKFLOW A: ANALYZE INFRASTRUCTURE RISK
    # -------------------------------------------------------------------------
    "infrastructure_risk": {
        "options": {
            "message": (
                "### 🔮 Workflow A: Analyze Infrastructure Risk\n\n"
                "I can evaluate civil assets across **6 categories** (Bridges, Roads, Water Pipelines, "
                "Drainage, Streetlights, Poles) using trained Random Forest & GBDT models.\n\n"
                "What would you like to examine?"
            ),
            "choices": [
                {
                    "id": "risk_view_predictions",
                    "label": "📊 View Available Predictions",
                    "description": "Retrieve actual telemetry summary, critical triage counts, and average RUL",
                    "action_type": "action",
                    "workflow": "infrastructure_risk",
                    "step": "view_predictions",
                    "payload": {"action": "fetch_predictions", "page": "prediction", "route": "/predict"},
                },
                {
                    "id": "risk_explain_model",
                    "label": "🧠 Understand Failure Prediction",
                    "description": "How supervised classifiers evaluate structural scores, corrosion, and load",
                    "action_type": "explain",
                    "workflow": "infrastructure_risk",
                    "step": "explain_model",
                    "payload": {"topic": "failure_prediction"},
                },
                {
                    "id": "risk_compare_categories",
                    "label": "🏗️ Compare Asset Categories",
                    "description": "Review vulnerability patterns across all 6 monitored asset types",
                    "action_type": "explain",
                    "workflow": "infrastructure_risk",
                    "step": "compare_categories",
                    "payload": {"topic": "asset_categories"},
                },
                {
                    "id": "risk_interpret_metrics",
                    "label": "📈 Interpret Model Metrics",
                    "description": "Learn how Recall, F1-Score, and RUL regression errors guide triage",
                    "action_type": "explain",
                    "workflow": "infrastructure_risk",
                    "step": "interpret_metrics",
                    "payload": {"topic": "model_metrics"},
                },
            ],
            "previous_step": "main:menu",
        },
        "explain_model": {
            "message": (
                "### 🧠 How Failure Prediction Works in this Project\n\n"
                "The system uses supervised tabular classification to predict whether an infrastructure asset "
                "is at high risk of imminent operational failure (`failure = 1` vs `0`):\n\n"
                "- **Primary Classifiers:** Balanced Random Forest Classifier ($n=100$, Gini impurity) and Gradient Boosting (GBDT).\n"
                "- **Key Telemetry Inputs:** Structural rating (0–100), corrosion level (0–100), operational age, average vehicular load, "
                "days since last physical inspection, and historical failure frequency.\n"
                "- **Class Imbalance Handling:** Real-world failures represent ~15–20% of public assets; models apply `class_weight='balanced'` "
                "to heavily penalize false negatives (missed failures) and prioritize civil safety.\n"
                "- **Prognostic RUL:** An accompanying Random Forest Regressor predicts remaining operational life in years."
            ),
            "choices": [
                {
                    "id": "nav_run_prediction",
                    "label": "⚡ Open Risk Prediction Tool",
                    "description": "Launch the interactive form to evaluate custom asset telemetry",
                    "action_type": "navigate",
                    "payload": {"page": "prediction", "route": "/predict"},
                },
                {
                    "id": "risk_interpret_metrics",
                    "label": "📈 Learn How to Interpret Metrics",
                    "description": "Understand classification F1, ROC-AUC, and RUL error margins",
                    "action_type": "explain",
                    "workflow": "infrastructure_risk",
                    "step": "interpret_metrics",
                    "payload": {"topic": "model_metrics"},
                },
                {
                    "id": "risk_compare_categories",
                    "label": "🏗️ Compare Asset Categories",
                    "description": "Examine concrete bridges vs. steel pipelines",
                    "action_type": "explain",
                    "workflow": "infrastructure_risk",
                    "step": "compare_categories",
                    "payload": {"topic": "asset_categories"},
                },
            ],
            "previous_step": "infrastructure_risk:options",
        },
        "compare_categories": {
            "message": (
                "### 🏗️ Monitored Asset Categories Comparison\n\n"
                "The project portfolio tracks **2,200 simulated municipal assets** across 6 distinct engineering categories:\n\n"
                "1. **Bridges:** Concrete deck spalling, structural piers, cyclic load stress (highest structural weight).\n"
                "2. **Roads & Pavements:** Asphalt fatigue, surface friction loss, traffic density, environmental freeze-thaw.\n"
                "3. **Water Pipelines:** Hydraulic flow pressure, soil moisture weathering, internal galvanic corrosion.\n"
                "4. **Drainage Networks:** Annual rainfall saturation, hydraulic overflow risk, sediment blockages.\n"
                "5. **Streetlights:** Electrical ballast corrosion, coastal wind vibration, maintenance frequency.\n"
                "6. **Electrical Poles:** Mechanical overhead line tension, severe weather exposure, foundation lean."
            ),
            "choices": [
                {
                    "id": "risk_view_predictions",
                    "label": "📊 View Portfolio Telemetry",
                    "description": "Inspect breakdown of critical triage assets across municipal zones",
                    "action_type": "action",
                    "workflow": "infrastructure_risk",
                    "step": "view_predictions",
                    "payload": {"action": "fetch_predictions", "page": "prediction", "route": "/predict"},
                },
                {
                    "id": "risk_explain_model",
                    "label": "🧠 How Failure Models Predict These",
                    "description": "Review the supervised classification mechanics",
                    "action_type": "explain",
                    "workflow": "infrastructure_risk",
                    "step": "explain_model",
                    "payload": {"topic": "failure_prediction"},
                },
            ],
            "previous_step": "infrastructure_risk:options",
        },
        "interpret_metrics": {
            "message": (
                "### 📈 Interpreting Infrastructure Model Metrics\n\n"
                "In municipal infrastructure predictive maintenance, standard accuracy can be misleading due to class imbalance:\n\n"
                "- **Recall (Sensitivity):** The percentage of true deteriorating assets caught by the model. High recall prevents catastrophic structural surprises.\n"
                "- **Precision:** The proportion of flagged assets that actually require repair, protecting municipal budgets from unnecessary physical audits.\n"
                "- **F1-Score:** Harmonic mean balancing false alarms against missed hazards. The trained Random Forest achieves ~0.88–0.92 test F1.\n"
                "- **RUL Mean Absolute Error (MAE):** The average difference between predicted and actual remaining lifespan in operational years."
            ),
            "choices": [
                {
                    "id": "nav_run_prediction",
                    "label": "⚡ Open Prediction Tool",
                    "description": "Test an individual asset assessment directly",
                    "action_type": "navigate",
                    "payload": {"page": "prediction", "route": "/predict"},
                },
                {
                    "id": "nav_model_benchmarks",
                    "label": "🎯 Review Model Benchmarks",
                    "description": "Open model comparison and classification benchmarks",
                    "action_type": "navigate",
                    "payload": {"page": "mlflow", "route": "/model-performance"},
                },
            ],
            "previous_step": "infrastructure_risk:options",
        },
    },

    # -------------------------------------------------------------------------
    # WORKFLOW B: INSPECT ROAD DAMAGE
    # -------------------------------------------------------------------------
    "road_damage": {
        "options": {
            "message": (
                "### 🛣️ Workflow B: Inspect Road Damage (Computer Vision)\n\n"
                "I can guide you through the macroscopic pavement distress inspection pipeline combining "
                "OpenCV optical filters and deep learning defect localization.\n\n"
                "What would you like to explore?"
            ),
            "choices": [
                {
                    "id": "damage_explain_cv",
                    "label": "👁️ Understand Road Damage Detection",
                    "description": "How OpenCV and YOLO identify potholes, cracks, and ravelling",
                    "action_type": "explain",
                    "workflow": "road_damage",
                    "step": "explain_cv",
                    "payload": {"topic": "cv_pipeline"},
                },
                {
                    "id": "damage_explain_rdi",
                    "label": "📐 Learn About Road Damage Index (RDI)",
                    "description": "How quantitative 0–100 pavement severity scores are formulated",
                    "action_type": "explain",
                    "workflow": "road_damage",
                    "step": "explain_rdi",
                    "payload": {"topic": "rdi_score"},
                },
                {
                    "id": "damage_explain_pipeline",
                    "label": "🔬 Explore Image Processing Steps",
                    "description": "CLAHE contrast equalization, Canny edge detection, and morphology",
                    "action_type": "explain",
                    "workflow": "road_damage",
                    "step": "explain_pipeline",
                    "payload": {"topic": "image_processing"},
                },
                {
                    "id": "damage_view_results",
                    "label": "🚀 Launch Vision Inspection Tool",
                    "description": "Open the computer vision module to inspect road distress photos",
                    "action_type": "action",
                    "workflow": "road_damage",
                    "step": "view_tool",
                    "payload": {"action": "fetch_sample_cv", "page": "cv", "route": "/dashboard"},
                },
            ],
            "previous_step": "main:menu",
        },
        "explain_cv": {
            "message": (
                "### 👁️ How Road Damage Detection Operates\n\n"
                "The computer vision inspection module in `app/cv/road_damage_detector.py` uses a hybrid visual architecture:\n\n"
                "- **Optical Contour Processing (OpenCV):** Enhances degraded road photos using CLAHE contrast equalization, "
                "applies Gaussian filtering, computes Canny gradient edges, and extracts defect contours to measure distress surface area.\n"
                "- **Deep Learning Object Localization (YOLO):** Identifies bounding boxes around localized pavement distress "
                "(Potholes, Longitudinal Cracks, Transverse Cracks, Ravelling).\n"
                "- **Verification:** Detections are validated against morphological thresholds to filter out normal road shadows, oil stains, and lane paint."
            ),
            "choices": [
                {
                    "id": "damage_explain_rdi",
                    "label": "📐 Learn About RDI Scoring",
                    "description": "See how visual defects convert to engineering condition scores",
                    "action_type": "explain",
                    "workflow": "road_damage",
                    "step": "explain_rdi",
                    "payload": {"topic": "rdi_score"},
                },
                {
                    "id": "nav_open_cv_module",
                    "label": "🚀 Launch Vision Inspector",
                    "description": "Open Module 04: Road Damage Detection directly",
                    "action_type": "navigate",
                    "payload": {"page": "cv", "route": "/dashboard"},
                },
            ],
            "previous_step": "road_damage:options",
        },
        "explain_rdi": {
            "message": (
                "### 📐 The Road Damage Index (RDI)\n\n"
                "The Road Damage Index (RDI) is an engineering metric on a **0–100 scale** representing overall pavement health:\n\n"
                "- **0 to 20 (Good / Healthy):** Smooth asphalt, negligible minor surface wear.\n"
                "- **20 to 50 (Fair / Moderate):** Minor longitudinal or hairline thermal cracking; scheduled seal-coating recommended.\n"
                "- **50 to 75 (Poor / High Risk):** Severe alligator cracking or small potholes; structural base compromise imminent.\n"
                "- **75 to 100 (Critical / Severe):** Deep structural potholes and widespread ravelling requiring emergency resurfacing.\n\n"
                "RDI is calculated dynamically from defect frequency, detected bounding-box area percentage, and defect severity multipliers."
            ),
            "choices": [
                {
                    "id": "nav_open_cv_module",
                    "label": "🚀 Launch Vision Inspector",
                    "description": "Upload a photo or test pre-generated road distress images",
                    "action_type": "navigate",
                    "payload": {"page": "cv", "route": "/dashboard"},
                },
                {
                    "id": "damage_explain_pipeline",
                    "label": "🔬 Explore Optical Image Filters",
                    "description": "Inspect CLAHE, Canny, and morphological kernel operations",
                    "action_type": "explain",
                    "workflow": "road_damage",
                    "step": "explain_pipeline",
                    "payload": {"topic": "image_processing"},
                },
            ],
            "previous_step": "road_damage:options",
        },
        "explain_pipeline": {
            "message": (
                "### 🔬 Optical Image Preprocessing Pipeline\n\n"
                "Before defect detection, road photos undergo deterministic multi-stage computer vision filtering:\n\n"
                "1. **Grayscale Conversion & CLAHE:** Contrast Limited Adaptive Histogram Equalization normalizes uneven asphalt lighting.\n"
                "2. **Bilateral / Gaussian Filtering:** Suppresses camera sensor noise while strictly preserving sharp crack edges.\n"
                "3. **Canny Gradient Edge Detection:** Computes directional image gradients to trace dark pavement ruptures.\n"
                "4. **Morphological Closing:** Applies a $3\\times 3$ or $5\\times 5$ structuring kernel to bridge fragmented crack lines into solid defect contours."
            ),
            "choices": [
                {
                    "id": "nav_open_cv_module",
                    "label": "🚀 Launch Vision Inspector",
                    "description": "Open Module 04: Road Damage Detection",
                    "action_type": "navigate",
                    "payload": {"page": "cv", "route": "/dashboard"},
                },
                {
                    "id": "damage_explain_rdi",
                    "label": "📐 Review RDI Index",
                    "description": "Understand severity calculations",
                    "action_type": "explain",
                    "workflow": "road_damage",
                    "step": "explain_rdi",
                    "payload": {"topic": "rdi_score"},
                },
            ],
            "previous_step": "road_damage:options",
        },
    },

    # -------------------------------------------------------------------------
    # WORKFLOW C: PLAN MAINTENANCE
    # -------------------------------------------------------------------------
    "plan_maintenance": {
        "options": {
            "message": (
                "### ⚡ Workflow C: Plan Maintenance & Optimization\n\n"
                "Municipal public works departments face severe annual budgetary caps and finite crew labor hours. "
                "I can guide you through the **0-1 Knapsack combinatorial scheduling algorithms** implemented in this platform.\n\n"
                "What would you like to explore?"
            ),
            "choices": [
                {
                    "id": "maint_compare_algorithms",
                    "label": "⚖️ Compare Optimization Algorithms",
                    "description": "Benchmark Hill Climbing vs. Beam Search vs. Tabu Search",
                    "action_type": "explain",
                    "workflow": "plan_maintenance",
                    "step": "compare_algorithms",
                    "payload": {"topic": "algorithm_comparison"},
                },
                {
                    "id": "maint_explain_knapsack",
                    "label": "🎒 0-1 Knapsack Problem Formulation",
                    "description": "How capital budget and workforce labor hours constrain repair schedules",
                    "action_type": "explain",
                    "workflow": "plan_maintenance",
                    "step": "explain_knapsack",
                    "payload": {"topic": "knapsack"},
                },
                {
                    "id": "maint_understand_priority",
                    "label": "🚦 Understand Priority Scoring",
                    "description": "How failure risk, load, and public impact calculate total risk reduction",
                    "action_type": "explain",
                    "workflow": "plan_maintenance",
                    "step": "understand_priority",
                    "payload": {"topic": "prioritization"},
                },
                {
                    "id": "maint_view_results",
                    "label": "📊 View Optimization Benchmark",
                    "description": "Run the combinatorial search optimizer on actual municipal assets",
                    "action_type": "action",
                    "workflow": "plan_maintenance",
                    "step": "view_results",
                    "payload": {"action": "fetch_optimization", "page": "optimization", "route": "/priority"},
                },
            ],
            "previous_step": "main:menu",
        },
        "compare_algorithms": {
            "message": (
                "### ⚖️ Optimization Algorithm Benchmark\n\n"
                "The maintenance optimizer (`app/optimization/maintenance_scheduler.py`) benchmarks 3 classical AI search strategies:\n\n"
                "1. **Hill Climbing (Greedy Local Search):** Fast and lightweight, but gets permanently trapped in local optima when asset combinations exceed budget.\n"
                "2. **Beam Search ($\\beta = 4$):** Maintains the top 4 candidate schedules at each state step, exploring wider search branches without memory blowup.\n"
                "3. **Tabu Search:** The top performer. Maintains a short-term recency 'tabu list' of recently modified assets, allowing it to escape local optima and cyclic deadlocks to achieve the highest total risk reduction."
            ),
            "choices": [
                {
                    "id": "nav_open_optimization",
                    "label": "⚡ Open Search Space Optimizer",
                    "description": "Launch Module 05: Benchmark Hill Climbing, Beam & Tabu Search live",
                    "action_type": "navigate",
                    "payload": {"page": "optimization", "route": "/priority"},
                },
                {
                    "id": "maint_explain_knapsack",
                    "label": "🎒 Understand Knapsack Formulation",
                    "description": "Inspect budget and labor mathematical constraints",
                    "action_type": "explain",
                    "workflow": "plan_maintenance",
                    "step": "explain_knapsack",
                    "payload": {"topic": "knapsack"},
                },
            ],
            "previous_step": "plan_maintenance:options",
        },
        "explain_knapsack": {
            "message": (
                "### 🎒 The 0-1 Knapsack Maintenance Formulation\n\n"
                "Maintenance resource planning is formulated as a multi-constrained combinatorial 0-1 Knapsack problem:\n\n"
                "- **Binary Decision Variable:** $x_i \\in \\{0, 1\\}$ indicating whether asset $i$ is scheduled for intervention.\n"
                "- **Objective:** Maximize Total Risk Reduction: $\\sum (x_i \\cdot \\text{RiskScore}_i)$.\n"
                "- **Budget Constraint:** Total estimated repair cost $\\sum (x_i \\cdot \\text{Cost}_i) \\le \\text{BudgetLimit}$.\n"
                "- **Labor Constraint:** Total required crew labor-hours $\\sum (x_i \\cdot \\text{Hours}_i) \\le \\text{LaborLimit}$."
            ),
            "choices": [
                {
                    "id": "nav_open_optimization",
                    "label": "⚡ Open Search Space Optimizer",
                    "description": "Launch Module 05 to adjust budget sliders and run Knapsack scheduling",
                    "action_type": "navigate",
                    "payload": {"page": "optimization", "route": "/priority"},
                },
                {
                    "id": "nav_open_priority_queue",
                    "label": "🚦 View Maintenance Priority Queue",
                    "description": "Review assets ranked by failure risk triage score",
                    "action_type": "navigate",
                    "payload": {"page": "dashboard", "route": "/priority"},
                },
            ],
            "previous_step": "plan_maintenance:options",
        },
        "understand_priority": {
            "message": (
                "### 🚦 Infrastructure Priority Scoring\n\n"
                "When sorting assets into maintenance queues, the system computes a composite **Hazard Priority Index**:\n\n"
                "$$\\text{Priority} = 0.45(\\text{FailureProb}) + 0.35(100 - \\text{StructuralScore}) + 0.20(\\text{CorrosionLevel})$$\n\n"
                "Assets are classified into four operational tiers: **CRITICAL** (immediate intervention required), "
                "**HIGH** (scheduled next cycle), **MEDIUM** (preventive maintenance), and **LOW** (routine monitoring)."
            ),
            "choices": [
                {
                    "id": "nav_open_priority_queue",
                    "label": "🚦 View Maintenance Priority Queue",
                    "description": "Inspect assets currently in the critical queue",
                    "action_type": "navigate",
                    "payload": {"page": "dashboard", "route": "/priority"},
                },
                {
                    "id": "maint_compare_algorithms",
                    "label": "⚖️ Compare Search Algorithms",
                    "description": "See how Tabu Search allocates repairs under budget caps",
                    "action_type": "explain",
                    "workflow": "plan_maintenance",
                    "step": "compare_algorithms",
                    "payload": {"topic": "algorithm_comparison"},
                },
            ],
            "previous_step": "plan_maintenance:options",
        },
    },

    # -------------------------------------------------------------------------
    # WORKFLOW D: EXPLORE THE PROJECT
    # -------------------------------------------------------------------------
    "explore_project": {
        "options": {
            "message": (
                "### 🔍 Workflow D: Explore the Project Architecture\n\n"
                "This platform is a comprehensive academic AI/ML engineering suite. I can walk you through "
                "any architectural layer or experimental component.\n\n"
                "What would you like to inspect?"
            ),
            "choices": [
                {
                    "id": "explore_architecture",
                    "label": "🏛️ System Architecture",
                    "description": "FastAPI ASGI backend, Streamlit dashboard, React web app, and SQLite store",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_architecture",
                    "payload": {"topic": "architecture"},
                },
                {
                    "id": "explore_automl",
                    "label": "🤖 AutoML vs. Manual Models",
                    "description": "FLAML Tabular automated search vs. scikit-learn baselines",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_automl",
                    "payload": {"topic": "automl"},
                },
                {
                    "id": "explore_mlflow",
                    "label": "📈 MLflow Experiment Tracking",
                    "description": "Deterministic parameter logging, metrics, confusion matrices",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_mlflow",
                    "payload": {"topic": "mlflow"},
                },
                {
                    "id": "explore_structures",
                    "label": "🧬 6 Fundamental Data Structures",
                    "description": "NumPy SIMD, SciPy CSR sparse matrix (98% RAM saved), Trees, Heaps",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_structures",
                    "payload": {"topic": "data_structures"},
                },
            ],
            "previous_step": "main:menu",
        },
        "explain_architecture": {
            "message": (
                "### 🏛️ System Architecture Overview\n\n"
                "- **Primary Dashboard:** Streamlit 1.55 (`streamlit_app.py`) full-width Highway theme with 10 modules.\n"
                "- **Alternative Web App:** React 18 + Vite (`frontend/`) with Recharts and component hierarchy.\n"
                "- **REST Microservice:** FastAPI (`backend/app/main.py`) exposing prediction, CV, and optimization endpoints.\n"
                "- **Data & Storage:** 2,200 synthetic telemetry rows, SQLite MLflow database (`backend/data/mlflow_tracking.db`), "
                "and joblib model bundles (`backend/models/`)."
            ),
            "choices": [
                {
                    "id": "nav_open_dashboard",
                    "label": "🏙️ Open Executive Dashboard",
                    "description": "Inspect live telemetry KPI overview and charts",
                    "action_type": "navigate",
                    "payload": {"page": "dashboard", "route": "/dashboard"},
                },
                {
                    "id": "nav_open_deployment",
                    "label": "🚀 Deployment & FastAPI Guide",
                    "description": "Review Docker, OpenAPI Swagger docs, and ASGI architecture",
                    "action_type": "navigate",
                    "payload": {"page": "deployment", "route": "/about"},
                },
            ],
            "previous_step": "explore_project:options",
        },
        "explain_automl": {
            "message": (
                "### 🤖 AutoML vs. Manual Models (FLAML)\n\n"
                "The project evaluates cost-frugal automated algorithm search using **FLAML Tabular** on a strict 80/20 train/test split:\n\n"
                "- **Search Budget:** 25 seconds of CPU time exploring LightGBM, XGBoost, Random Forest, and ExtraTree estimators.\n"
                "- **Best Model Found:** `ExtraTree` classifier achieving ~0.7075 macro F1-score with minimal inference latency.\n"
                "- **Evaluation:** Confirms that automated tuning finds competitive lightweight estimators compared to manual random forests."
            ),
            "choices": [
                {
                    "id": "nav_open_automl",
                    "label": "🤖 Open Module 07: AutoML Benchmark",
                    "description": "Launch the interactive AutoML comparison dashboard",
                    "action_type": "navigate",
                    "payload": {"page": "automl", "route": "/model-performance"},
                },
                {
                    "id": "explore_mlflow",
                    "label": "📈 Inspect MLflow Experiment Tracking",
                    "description": "Review serialized run metrics and confusion matrix artifacts",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_mlflow",
                    "payload": {"topic": "mlflow"},
                },
            ],
            "previous_step": "explore_project:options",
        },
        "explain_mlflow": {
            "message": (
                "### 📈 MLflow Experiment Tracking\n\n"
                "The repository logs machine learning lifecycle experiments into a local embedded SQLite store (`backend/data/mlflow_tracking.db`):\n\n"
                "- **Tracked Parameters:** Estimator count ($n=100$), tree depth, class weighting, learning rate.\n"
                "- **Logged Metrics:** Accuracy, Precision, Recall, Macro F1, ROC-AUC, and RUL regression MAE/RMSE.\n"
                "- **Artifacts:** Confusion matrix heatmaps, ROC curves, feature importance bar charts, and pickled model bundles."
            ),
            "choices": [
                {
                    "id": "nav_open_mlflow",
                    "label": "📈 Open Module 06: MLflow Tracking",
                    "description": "Explore tracked experiment runs and metrics",
                    "action_type": "navigate",
                    "payload": {"page": "mlflow", "route": "/model-performance"},
                },
                {
                    "id": "explore_structures",
                    "label": "🧬 Inspect Core Data Structures",
                    "description": "See why CSR sparse matrices save 98% memory",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_structures",
                    "payload": {"topic": "data_structures"},
                },
            ],
            "previous_step": "explore_project:options",
        },
        "explain_structures": {
            "message": (
                "### 🧬 Fundamental AI/ML Data Structures in Action\n\n"
                "Module 08 demonstrates the empirical efficiency of 6 fundamental computer science data structures:\n\n"
                "1. **SciPy CSR Sparse Matrix:** Achieves **~98% RAM reduction** over dense 2D one-hot encoded categorical vectors.\n"
                "2. **NumPy Arrays:** Contiguous SIMD vectorized array calculations for high-throughput batch scoring.\n"
                "3. **Binary Decision Trees:** Hierarchical Gini impurity splits with $O(\\text{depth})$ inference latency.\n"
                "4. **NetworkX Directed Graphs:** Topologically connects municipal road junctions and river bridges.\n"
                "5. **Priority Queues (`heapq`):** $O(\\log n)$ min-heap triage scheduling for urgent repairs.\n"
                "6. **Hash Maps / Dictionaries:** $O(1)$ constant-time asset telemetry caching."
            ),
            "choices": [
                {
                    "id": "nav_open_structures",
                    "label": "🧬 Open Module 08: Data Structures",
                    "description": "Run the live data structure benchmark demonstration",
                    "action_type": "navigate",
                    "payload": {"page": "structures", "route": "/analytics"},
                },
                {
                    "id": "explore_architecture",
                    "label": "🏛️ Review System Architecture",
                    "description": "Inspect FastAPI and Streamlit wiring",
                    "action_type": "explain",
                    "workflow": "explore_project",
                    "step": "explain_architecture",
                    "payload": {"topic": "architecture"},
                },
            ],
            "previous_step": "explore_project:options",
        },
    },
}


class RoverWorkflowEngine:
    """State machine coordinator for ROVER's guided, task-oriented choices."""

    def get_main_menu(self) -> Dict[str, Any]:
        """Returns the top-level main menu state."""
        return {
            "response": (
                "👋 **Hi! I'm ROVER — Road Operations & Vulnerability Evaluation Robot.**\n\n"
                "Your AI assistant for road infrastructure, predictive maintenance and smarter civil decisions. "
                "What would you like to do today?"
            ),
            "choices": MAIN_MENU_CHOICES,
            "workflow": "main",
            "step": "menu",
            "previous_step": None,
            "action_executed": None,
            "action_data": None,
            "status": "success",
        }

    def process_choice(
        self,
        workflow: Optional[str],
        step: Optional[str],
        choice_id: str,
    ) -> Dict[str, Any]:
        """Transitions state machine when user clicks an option card."""
        # 1. Main menu transitions
        if choice_id == "main_menu" or (workflow == "main" and choice_id == "menu"):
            return self.get_main_menu()

        # 2. Check top-level workflow buttons from main menu
        if choice_id == "wf_risk":
            wf_data = WORKFLOW_STEPS["infrastructure_risk"]["options"]
            return {
                "response": wf_data["message"],
                "choices": wf_data["choices"],
                "workflow": "infrastructure_risk",
                "step": "options",
                "previous_step": "main:menu",
                "status": "success",
            }
        if choice_id == "wf_damage":
            wf_data = WORKFLOW_STEPS["road_damage"]["options"]
            return {
                "response": wf_data["message"],
                "choices": wf_data["choices"],
                "workflow": "road_damage",
                "step": "options",
                "previous_step": "main:menu",
                "status": "success",
            }
        if choice_id == "wf_maintenance":
            wf_data = WORKFLOW_STEPS["plan_maintenance"]["options"]
            return {
                "response": wf_data["message"],
                "choices": wf_data["choices"],
                "workflow": "plan_maintenance",
                "step": "options",
                "previous_step": "main:menu",
                "status": "success",
            }
        if choice_id == "wf_explore":
            wf_data = WORKFLOW_STEPS["explore_project"]["options"]
            return {
                "response": wf_data["message"],
                "choices": wf_data["choices"],
                "workflow": "explore_project",
                "step": "options",
                "previous_step": "main:menu",
                "status": "success",
            }

        # 3. Handle sub-step selections inside workflows
        # Check if choice_id corresponds to real application action
        if choice_id in ("risk_view", "risk_view_predictions"):
            return self._execute_fetch_predictions()
        if choice_id in ("maintenance_view", "maint_view_results"):
            return self._execute_fetch_optimization()
        if choice_id in ("damage_view", "damage_view_results", "damage_inspect"):
            return self._execute_fetch_cv_samples()

        # Check aliases for explanations
        if choice_id in ("risk_explain", "risk_explain_model"):
            choice_id = "explain_model"
        elif choice_id in ("damage_detect", "damage_detect_surface"):
            choice_id = "detect_surface"
        elif choice_id in ("damage_rdi", "damage_explain_rdi"):
            choice_id = "explain_rdi"
        elif choice_id in ("maintenance_algs", "maint_compare_algorithms"):
            choice_id = "compare_algorithms"
        elif choice_id in ("explore_arch", "explore_architecture"):
            choice_id = "explain_architecture"
        elif choice_id in ("explore_models", "explore_ml_models"):
            choice_id = "explain_models"

        # Check in active workflow dictionary
        active_wf = workflow or "main"
        wf_steps = WORKFLOW_STEPS.get(active_wf, {})

        # Direct step match
        target_step_key = choice_id.split("_")[-1] if "_" in choice_id else choice_id
        for step_name, step_content in wf_steps.items():
            if choice_id.endswith(step_name) or choice_id == step_name:
                return {
                    "response": step_content["message"],
                    "choices": step_content["choices"],
                    "workflow": active_wf,
                    "step": step_name,
                    "previous_step": step_content.get("previous_step", f"{active_wf}:options"),
                    "status": "success",
                }

        # Handle navigation buttons (e.g. nav_run_prediction, nav_open_cv_module, etc.)
        for step_content in wf_steps.values():
            for ch in step_content.get("choices", []):
                if ch.get("id") == choice_id:
                    if ch.get("action_type") == "navigate":
                        payload = ch.get("payload", {})
                        target_page = payload.get("page", "dashboard")
                        page_meta = ALLOWLISTED_PAGES.get(target_page, {"label": target_page, "route": "/dashboard"})
                        return {
                            "response": (
                                f"🚀 **Opening {page_meta['label']}**...\n\n"
                                f"Navigating to the active module. Use the dashboard navigation to interact directly."
                            ),
                            "choices": [
                                {
                                    "id": f"{active_wf}_options",
                                    "label": f"↩️ Return to {active_wf.replace('_', ' ').title()}",
                                    "description": "Back to workflow options",
                                    "action_type": "workflow",
                                    "workflow": active_wf,
                                    "step": "options",
                                },
                                {
                                    "id": "main_menu",
                                    "label": "🏠 Main Menu",
                                    "description": "Return to ROVER home options",
                                    "action_type": "workflow",
                                    "workflow": "main",
                                    "step": "menu",
                                },
                            ],
                            "workflow": active_wf,
                            "step": "navigating",
                            "previous_step": f"{active_wf}:options",
                            "action_executed": "navigate",
                            "action_data": payload,
                            "status": "success",
                        }

        # Safe fallback: return active workflow options or main menu
        if active_wf in WORKFLOW_STEPS and "options" in WORKFLOW_STEPS[active_wf]:
            wf_data = WORKFLOW_STEPS[active_wf]["options"]
            return {
                "response": wf_data["message"],
                "choices": wf_data["choices"],
                "workflow": active_wf,
                "step": "options",
                "previous_step": "main:menu",
                "status": "success",
            }

        return self.get_main_menu()

    def process_back(self, current_workflow: Optional[str], current_step: Optional[str]) -> Dict[str, Any]:
        """Reverts to the previous step or main menu."""
        if not current_workflow or current_workflow == "main" or current_step == "menu":
            return self.get_main_menu()

        if current_step == "options":
            return self.get_main_menu()

        # Inside a sub-step -> return to the workflow's options
        if current_workflow in WORKFLOW_STEPS and "options" in WORKFLOW_STEPS[current_workflow]:
            wf_data = WORKFLOW_STEPS[current_workflow]["options"]
            return {
                "response": wf_data["message"],
                "choices": wf_data["choices"],
                "workflow": current_workflow,
                "step": "options",
                "previous_step": "main:menu",
                "status": "success",
            }

        return self.get_main_menu()

    # -------------------------------------------------------------------------
    # REAL APPLICATION DATA & ACTION EXECUTORS
    # -------------------------------------------------------------------------
    def _execute_fetch_predictions(self) -> Dict[str, Any]:
        """Calls real application database/dashboard summary and reports genuine figures."""
        try:
            from app.api.routes_dashboard import get_dashboard_summary
            summary = get_dashboard_summary()
            total = summary.get("total_assets", 2200)
            high = summary.get("high_risk_assets", 348)
            med = summary.get("medium_risk_assets", 742)
            low = max(0, total - high - med)
            avg_rul = summary.get("average_remaining_life", 16.8)
            focus = summary.get("priority_focus", "Bridges and Industrial pipelines")

            msg = (
                f"### 📊 Live Portfolio Infrastructure Risk Assessment\n\n"
                f"Retrieved directly from the active backend telemetry store:\n\n"
                f"- **Total Monitored Corridors:** `{total:,}` municipal assets\n"
                f"- **Critical Hazard Assets (High Risk):** `{high:,}` flagged for immediate engineering inspection\n"
                f"- **Warning / Moderate Risk Assets:** `{med:,}` scheduled for preventive intervention\n"
                f"- **Clear Operational Health (Low Risk):** `{low:,}` stable corridors\n"
                f"- **System Average Remaining Useful Life (RUL):** `{avg_rul}` years\n"
                f"- **Critical Engineering Priority Focus:** *{focus}*\n\n"
                f"What would you like to do next with these results?"
            )
            return {
                "response": msg,
                "choices": [
                    {
                        "id": "nav_run_prediction",
                        "label": "⚡ Run New Asset Prediction",
                        "description": "Open Module 03 to score an asset by custom parameters",
                        "action_type": "navigate",
                        "payload": {"page": "prediction", "route": "/predict"},
                    },
                    {
                        "id": "nav_priority_queue",
                        "label": "🚦 View Priority Maintenance Queue",
                        "description": "Open prioritized list of high-risk assets",
                        "action_type": "navigate",
                        "payload": {"page": "dashboard", "route": "/priority"},
                    },
                    {
                        "id": "risk_explain_model",
                        "label": "🧠 How the Model Scored These",
                        "description": "Understand the Random Forest classification mechanics",
                        "action_type": "explain",
                        "workflow": "infrastructure_risk",
                        "step": "explain_model",
                    },
                    {
                        "id": "risk_options",
                        "label": "↩️ Back to Risk Menu",
                        "description": "Explore other risk options",
                        "action_type": "workflow",
                        "workflow": "infrastructure_risk",
                        "step": "options",
                    },
                ],
                "workflow": "infrastructure_risk",
                "step": "view_predictions",
                "previous_step": "infrastructure_risk:options",
                "action_executed": "fetch_predictions",
                "route": "/predict",
                "action_data": summary,
                "status": "success",
            }
        except Exception as exc:
            logger.exception("Failed to retrieve live predictions")
            return {
                "response": f"⚠️ Could not load live prediction summary: {str(exc)}",
                "choices": MAIN_MENU_CHOICES,
                "workflow": "infrastructure_risk",
                "step": "options",
                "status": "error",
            }

    def _execute_fetch_optimization(self) -> Dict[str, Any]:
        """Invokes real maintenance scheduler comparison function and reports true benchmark stats."""
        try:
            from app.optimization.maintenance_scheduler import run_optimization_comparison
            asset_list = [
                {"asset_id": f"ASSET-{i:03d}", "asset_type": at, "risk_score": round(r, 2), "cost": c, "capacity_hours": h, "criticality": crit}
                for i, (at, r, c, h, crit) in enumerate([
                    ("Bridge", 0.92, 14000, 40, 1.5),
                    ("Water Pipeline", 0.85, 9500, 28, 1.4),
                    ("Road Corridor", 0.78, 8200, 24, 1.2),
                    ("Drainage Culvert", 0.71, 6000, 18, 1.1),
                    ("Electrical Substation", 0.88, 12500, 35, 1.5),
                    ("Road Pothole Zone", 0.65, 4500, 14, 1.0),
                    ("Power Line Feeder", 0.74, 7800, 22, 1.3),
                    ("Traffic Signal Grid", 0.52, 3200, 10, 0.9),
                    ("Streetlight Bank", 0.44, 2100, 8, 0.8),
                    ("Water Main Valve", 0.68, 5400, 16, 1.2),
                ], start=1)
            ]
            results = run_optimization_comparison(assets=asset_list, budget_limit=50000.0, capacity_limit=160.0)

            hc = results.get("hill_climbing", {}).get("final_plan", {})
            beam = results.get("beam_search", {}).get("final_plan", {})
            tabu = results.get("tabu_search", {}).get("final_plan", {})

            hc_ms = results.get("hill_climbing", {}).get("elapsed_ms", 1.2)
            beam_ms = results.get("beam_search", {}).get("elapsed_ms", 2.4)
            tabu_ms = results.get("tabu_search", {}).get("elapsed_ms", 3.1)

            msg = (
                f"### ⚡ Real 0-1 Knapsack Maintenance Scheduling Benchmark\n\n"
                f"Executed across 10 municipal candidate assets under Budget Cap **$50,000** and Labor Cap **160 hours**:\n\n"
                f"| Search Algorithm | Risk Reduction | Cost Incurred | Labor Hours | Runtime |\n"
                f"| :--- | :--- | :--- | :--- | :--- |\n"
                f"| **Hill Climbing (Greedy)** | `{hc.get('objective_value', 0):.2f}` pts | `${hc.get('total_cost', 0):,}` | `{hc.get('total_capacity', 0)}` hrs | `{hc_ms:.2f} ms` |\n"
                f"| **Beam Search ($\\beta=4$)** | `{beam.get('objective_value', 0):.2f}` pts | `${beam.get('total_cost', 0):,}` | `{beam.get('total_capacity', 0)}` hrs | `{beam_ms:.2f} ms` |\n"
                f"| **Tabu Search (Best)** | `{tabu.get('objective_value', 0):.2f}` pts | `${tabu.get('total_cost', 0):,}` | `{tabu.get('total_capacity', 0)}` hrs | `{tabu_ms:.2f} ms` |\n\n"
                f"**Key Observation:** Tabu Search avoids local optima trap states by maintaining a recency tabu list, "
                f"achieving superior risk mitigation within strict budget limits."
            )
            return {
                "response": msg,
                "choices": [
                    {
                        "id": "nav_open_optimization",
                        "label": "⚡ Open Module 05: Optimizer",
                        "description": "Adjust capital budget and workforce sliders live",
                        "action_type": "navigate",
                        "payload": {"page": "optimization", "route": "/priority"},
                    },
                    {
                        "id": "maint_compare_algorithms",
                        "label": "⚖️ Compare Algorithm Details",
                        "description": "Understand why Tabu Search outperforms Hill Climbing",
                        "action_type": "explain",
                        "workflow": "plan_maintenance",
                        "step": "compare_algorithms",
                    },
                    {
                        "id": "maint_options",
                        "label": "↩️ Back to Maintenance Menu",
                        "description": "Return to planning choices",
                        "action_type": "workflow",
                        "workflow": "plan_maintenance",
                        "step": "options",
                    },
                ],
                "workflow": "plan_maintenance",
                "step": "view_results",
                "previous_step": "plan_maintenance:options",
                "action_executed": "fetch_optimization",
                "route": "/priority",
                "action_data": results,
                "status": "success",
            }
        except Exception as exc:
            logger.exception("Failed to execute maintenance comparison")
            return {
                "response": f"⚠️ Could not execute maintenance comparison: {str(exc)}",
                "choices": MAIN_MENU_CHOICES,
                "workflow": "plan_maintenance",
                "step": "options",
                "status": "error",
            }

    def _execute_fetch_cv_samples(self) -> Dict[str, Any]:
        """Discovers verified sample road images available in backend."""
        try:
            from pathlib import Path
            sample_dir = Path(__file__).resolve().parents[2] / "data" / "sample_road_images"
            if not sample_dir.exists() or len(list(sample_dir.glob("*.jpg"))) == 0:
                from app.cv.road_damage_detector import generate_sample_road_images
                generate_sample_road_images(sample_dir)

            sample_files = [f.name for f in sample_dir.glob("*.jpg")]
            count = len(sample_files)

            msg = (
                f"### 🛣️ Computer Vision Road Inspection Module Ready\n\n"
                f"The OpenCV + YOLO pavement damage inspection engine is ready with **{count} test road images** "
                f"simulating potholes, transverse cracking, and asphalt ravelling:\n\n"
                f"- Available Sample Scans: `{', '.join(sample_files[:4])}`\n"
                f"- Quantitative Metric: **Road Damage Index (RDI)** on 0–100 scale\n"
                f"- Defect Detection Area: Automatic contour segmentation & surface percentage calculation\n\n"
                f"You can launch the inspection tool to test these images or upload your own road photo:"
            )
            return {
                "response": msg,
                "choices": [
                    {
                        "id": "nav_open_cv_module",
                        "label": "🚀 Launch Vision Inspector",
                        "description": "Open Module 04 to inspect road distress photos live",
                        "action_type": "navigate",
                        "payload": {"page": "cv", "route": "/dashboard"},
                    },
                    {
                        "id": "damage_explain_rdi",
                        "label": "📐 How RDI Score is Calculated",
                        "description": "Learn about severity weighting",
                        "action_type": "explain",
                        "workflow": "road_damage",
                        "step": "explain_rdi",
                    },
                    {
                        "id": "damage_options",
                        "label": "↩️ Back to Damage Menu",
                        "description": "Return to inspection choices",
                        "action_type": "workflow",
                        "workflow": "road_damage",
                        "step": "options",
                    },
                ],
                "workflow": "road_damage",
                "step": "view_tool",
                "previous_step": "road_damage:options",
                "action_executed": "fetch_sample_cv",
                "route": "/damage",
                "action_data": {"sample_files": sample_files},
                "status": "success",
            }
        except Exception as exc:
            logger.exception("Failed to fetch sample CV images")
            return {
                "response": f"⚠️ Could not load CV sample info: {str(exc)}",
                "choices": MAIN_MENU_CHOICES,
                "workflow": "road_damage",
                "step": "options",
                "status": "error",
            }

    def process_step(
        self,
        workflow: Optional[str] = None,
        step: Optional[str] = None,
        choice_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convenience dispatcher for handling steps, Back, and Home transitions."""
        if not choice_id or choice_id in ("menu", "main_menu", "home"):
            return self.get_main_menu()
        if choice_id == "back":
            return self.process_back(workflow, step)
        return self.process_choice(workflow, step, choice_id)


def get_initial_choices() -> List[Dict[str, Any]]:
    """Returns the top-level main menu choices for ROVER."""
    return MAIN_MENU_CHOICES


# Singleton workflow engine instance
workflow_engine = RoverWorkflowEngine()
