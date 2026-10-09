# Engineering Development Log

This document records the architectural decisions, milestones, implementation hurdles, and concrete engineering solutions encountered while extending the **AI Urban Infrastructure Failure Predictor**.

---

## Milestone Timeline & Module Implementations

### Milestone 1: Version Control & Repository Hygiene
- **Task:** Standardize `.gitignore` and document branching/commit conventions.
- **Problem Encountered:** Previous `.gitignore` omitted MLflow databases, `.dvc` cache folders, and large `.pt`/`.onnx` checkpoints, risking massive binary bloating in Git history.
- **Solution:** Re-architected `.gitignore` with strict patterns for virtual environments, OS files, model binaries, tracking databases, and experiment artifacts. Authored `docs/version_control_guide.md`.

### Milestone 2: Computer Vision Road Damage Detection
- **Task:** Integrate OpenCV image preprocessing and Ultralytics YOLO for detecting road distress (potholes, cracks, ravelling).
- **Technical Nuance & Problem:**
  - Off-the-shelf YOLO models (e.g., `yolov8n.pt` trained on COCO) only detect common objects (cars, pedestrians, traffic lights). Claiming that generic COCO weights identify road distress is technically incorrect.
- **Solution:**
  - Developed `backend/app/cv/road_damage_detector.py` combining OpenCV's CLAHE histogram enhancement, Gaussian noise suppression, and Canny edge extraction with morphological shape-factor contour filtering (circularity and aspect ratios to isolate potholes vs. cracks).
  - Provided support for fine-tuned RDD YOLO weights alongside explicit validation warnings to maintain scientific integrity.
  - Implemented procedural synthetic road asphalt image generator (`generate_sample_road_images`) so users can test immediately on standard road samples.

### Milestone 3: Search Space Management & Maintenance Scheduling
- **Task:** Implement and benchmark Hill Climbing, Beam Search, and Tabu Search under budget and crew-capacity constraints.
- **Theoretical Challenge:** Proving that Hill Climbing can get trapped in suboptimal states under realistic municipal knapsack constraints.
- **Solution:**
  - Developed `backend/app/optimization/maintenance_scheduler.py` with shared objective function $f(S) = \sum_{i \in S} \Delta R_i \cdot W_i$.
  - Constructed an empirical counterexample: a single heavy "greedy lure" asset provides 0.85 risk reduction but exhausts 95% of budget, while three complementary assets yield 1.35 risk reduction (+58.8% higher). Hill Climbing terminates at 0.85, whereas Beam Search ($\beta \ge 2$) and Tabu Search discover the global optimum (1.35).

### Milestone 4: Experiment Tracking with MLflow
- **Task:** Track hyperparameters, dataset metadata, evaluation metrics, and artifacts across classification and regression experiments.
- **Implementation Problem:** MLflow 3.x deprecated the raw filesystem tracking store (`./mlruns`), throwing an exception when initialized with file URIs.
- **Solution:** Configured MLflow to use an embedded SQLite database backend (`sqlite:///data/mlflow_tracking.db`) with `MLFLOW_ALLOW_FILE_STORE=true`. Logged both classification (Accuracy, Precision, Recall, F1, ROC-AUC) and regression (MAE, RMSE, R²) experiments, confusion matrix plots, and serialized model artifacts.

### Milestone 5: AutoML Integration & Leakage Prevention
- **Task:** Integrate FLAML Tabular AutoML and compare against manual baselines.
- **Implementation Hurdles:**
  - Initial import failed due to missing `xgboost` and `lightgbm` native wheels on the machine.
  - Risk of data leakage if feature encoders or median imputers are fit across the entire dataset prior to splitting.
- **Solution:**
  - Installed compatible `xgboost` and `lightgbm` packages for Windows.
  - Enforced strict train-test separation: imputed and fitted transformers strictly on `X_train`, evaluating on `X_test`. AutoML selected `ExtraTree` / `XGB_LimitDepth`, achieving 0.7075 F1-score with 25s search budget.

### Milestone 6: Core Data Structures Integration
- **Task:** Demonstrate the 6 fundamental data structures used across the solution.
- **Solution:** Authored `backend/app/structures/data_structures_demo.py` showcasing:
  1. NumPy contiguous 1D vectors and 2D matrices (SIMD linear algebra).
  2. SciPy CSR sparse matrices (saving 98% memory on one-hot categorical matrices).
  3. Binary Decision Trees (transparent threshold partition graphs).
  4. NetworkX Directed Graphs (topological utility cascades and betweenness centrality bottlenecks).
  5. Heapq Binary Min/Max Heaps (O(log N) emergency triage queues).
  6. Hash Dictionaries (O(1) asset ID lookup).

### Milestone 7: Primary Streamlit Application & MLOps
- **Task:** Create the primary multi-page Streamlit application (`streamlit_app.py`), Dockerfile, and DVC pipeline.
- **Solution:**
  - Authored an 8-page interactive Streamlit dashboard integrating all modules with `@st.cache_resource` and `@st.cache_data`.
  - Built production `Dockerfile`, `.dockerignore`, and `dvc.yaml` pipeline.
  - Retained full backward compatibility with the existing React frontend and FastAPI backend.
