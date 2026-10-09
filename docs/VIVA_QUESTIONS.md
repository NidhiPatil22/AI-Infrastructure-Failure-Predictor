# AIML Laboratory Viva Voce Examination Questions & Answers

This document provides 30+ technical questions and answers designed for academic laboratory viva voce examinations on the **AI Urban Infrastructure Failure Predictor**.

---

## Section 1: Computer Vision & Road Damage Detection

### Q1: Why can't a standard pretrained YOLOv8 model (trained on COCO) detect road potholes and cracks directly?
**Answer:** The COCO dataset comprises 80 common object classes (such as cars, persons, dogs, bicycles, and traffic lights). It contains **zero labels for asphalt surface distress** like potholes or alligator cracks. Claiming that a generic COCO-pretrained model detects road damage is incorrect; specialized transfer learning on road distress datasets (e.g., RDD2020/RDD2022) or domain-specific morphological image processing is strictly required.

### Q2: What role does OpenCV's CLAHE algorithm play in road surface inspection?
**Answer:** CLAHE stands for **Contrast Limited Adaptive Histogram Equalization**. Asphalt roads suffer from extreme lighting inconsistencies (shadows from trees, overexposure from direct sun). Global histogram equalization amplifies high-frequency asphalt noise. CLAHE computes equalization over small contextual tiles (e.g., $8 \times 8$) and clips contrast amplification at a predefined limit (e.g., 3.0), accentuating dark pothole depressions and hairline crack fissures without blowing out background asphalt texture.

### Q3: How do contour circularity and aspect ratio distinguish potholes from cracks?
**Answer:**
- **Circularity** is defined as $C = \frac{4 \pi \cdot \text{Area}}{\text{Perimeter}^2}$. A circle has $C = 1.0$. Potholes exhibit circularity $C > 0.40$ and balanced aspect ratios ($0.5 \le \frac{w}{h} \le 2.0$).
- **Longitudinal/Transverse cracks** exhibit elongated aspect ratios ($\frac{w}{h} > 2.5$ or $< 0.4$) and low circularity ($C < 0.25$) due to high perimeter relative to area.

### Q4: What is the fundamental difference between image-based road damage detection and tabular failure prediction?
**Answer:**
- **Image-Based Detection (CV):** Evaluates instantaneous 2D spatial surface distress at the macro scale (visual anomalies, depth fissures, raveling).
- **Tabular Failure Prediction (ML):** Evaluates longitudinal temporal degradation using multi-variate continuous telemetry (age, load cycles, cumulative rainfall, corrosion rate, past maintenance frequency) to forecast structural collapse and Remaining Useful Life.

---

## Section 2: Machine Learning, Experiment Tracking & AutoML

### Q5: Why is MLflow necessary in an ML engineering pipeline?
**Answer:** MLflow provides systematic reproducibility and governance across the model development lifecycle. It logs exact hyperparameters ($C$, max_depth, n_estimators), training duration, code commit versions, evaluation metrics (Accuracy, F1, ROC-AUC, RMSE), and artifacts (confusion matrices, serialized model binaries), preventing undocumented trial-and-error experiments.

### Q6: How does FLAML Tabular optimize model search compared to standard Grid Search?
**Answer:** Grid Search exhausts computational resources by evaluating predetermined Cartesian combinations without learning from past iterations. FLAML uses cost-effective, budget-aware optimization (**CFO / BlendSearch**), prioritizing low-cost models (like ExtraTrees and LightGBM) initially and dynamically spending search budget on the most promising hyperparameter subspaces, achieving better F1-scores in seconds.

### Q7: What is data leakage and how was it prevented in this implementation?
**Answer:** Data leakage occurs when information from outside the training dataset (such as test set statistics) influences model training, producing overly optimistic evaluation metrics that fail in production. Here, data leakage was prevented by:
1. Splitting data into 80% train and 20% test before calculating medians, scalers, or transformations.
2. Fitting all feature pipelines strictly on `X_train` and applying `transform()` on `X_test`.

### Q8: Why evaluate classification models using ROC-AUC and F1-score rather than simple Accuracy?
**Answer:** Municipal infrastructure failure datasets are inherently imbalanced (e.g., only 10%–20% of monitored assets experience imminent failure). A naive classifier predicting "No Failure" for every asset achieves 80%–90% accuracy but has zero utility. F1-score balances Precision and Recall, while ROC-AUC evaluates discrimination capability across all classification probability thresholds.

---

## Section 3: Search Space Management & Combinatorial Optimization

### Q9: Formulate the maintenance scheduling problem mathematically.
**Answer:** It is a 0-1 Multi-Constraint Knapsack Problem:
$$\max_{S \subseteq \mathcal{A}} f(S) = \sum_{i \in S} \Delta R_i \cdot W_i \quad \text{subject to} \quad \sum_{i \in S} C_i \le B, \quad \sum_{i \in S} H_i \le H_{\max}$$
Where $\Delta R_i$ is failure risk reduction, $W_i$ is criticality weight, $C_i$ is repair cost, $H_i$ is crew hours, $B$ is financial budget, and $H_{\max}$ is team capacity.

### Q10: Why does Hill Climbing fail to find the global optimum in maintenance scheduling?
**Answer:** Steepest-ascent Hill Climbing only transitions to immediate 1-step improving neighbors. If a heavy "greedy lure" asset provides a large initial gain (e.g., 0.85) but exhausts 95% of the budget, Hill Climbing selects it. From that state, adding any other asset violates budget constraints, and removing the heavy asset temporarily decreases the objective value. Hill Climbing terminates at the local optimum, unable to discover that selecting three smaller complementary assets yields a combined risk reduction of 1.35 (+58.8% higher).

### Q11: How does Beam Search overcome the local-optimum limitation of Hill Climbing?
**Answer:** Instead of following a single greedy trajectory, Beam Search maintains a beam of the top $\beta$ candidate subsets at each expansion layer. By exploring $\beta$ diverse parallel partial plans, it avoids getting trapped when an individually high-cost asset blocks better combinations.

### Q12: Explain the role of the Tabu List and Aspiration Criterion in Tabu Search.
**Answer:**
- **Tabu List:** A recency-based short-term memory that records recently modified asset IDs for a tenure of $T$ iterations. Moves reversing these assets are forbidden, preventing cyclical bouncing between the same states and forcing exploration of non-improving neighborhoods.
- **Aspiration Criterion:** A rule that overrides the tabu restriction if a forbidden move achieves an objective strictly superior to the best global objective found so far ($f(S') > f(S^*)$).

---

## Section 4: Data Structures

### Q13: Why are SciPy CSR sparse matrices appropriate for encoded categorical features?
**Answer:** When one-hot encoding categorical attributes like `zone` and `asset_type`, the resulting feature matrix contains >95% zero elements. A dense NumPy array allocates 8 bytes for every zero. SciPy Compressed Sparse Row (CSR) matrices store only non-zero values, column indices, and row pointers, reducing memory consumption by over 90% and accelerating sparse matrix multiplication.

### Q14: Why is a binary heap (priority queue) superior to an array for emergency asset dispatch?
**Answer:**
- Inserting a new real-time risk prediction into a sorted array takes $O(N)$ time, or $O(N \log N)$ to re-sort the whole database.
- A binary heap (via `heapq`) provides $O(\log N)$ insertion and $O(1)$ peek / $O(\log N)$ extraction of the highest-risk asset, enabling real-time emergency triage under high-frequency sensor updates.

### Q15: How does a directed graph model cascading failure in urban infrastructure?
**Answer:** Urban utilities have functional dependencies: power substations feed pumping stations, which feed water mains, which supply fire hydrants and hospitals. By modeling the infrastructure as a directed graph ($G = (V, E)$), we compute **betweenness centrality** to detect critical systemic bottlenecks and traverse descendant subgraphs to identify cascading blackout or outage risks if a root node fails.

---

## Section 5: MLOps, Version Control & Deployment

### Q16: Why should large model weights and virtual environments be excluded from Git?
**Answer:**
- Virtual environments (`.venv/`) contain platform-specific compiled binaries that cannot be run portably across different operating systems.
- Large weights (`.pt`, `.pkl` > 50MB) bloat the Git commit history permanently, causing slow clones and repository corruption. Dependencies should be restored via `requirements.txt` and model weights managed via DVC or artifact repositories.

### Q17: What is the architectural difference between serving via Streamlit vs. FastAPI?
**Answer:**
- **Streamlit:** Best suited for human-in-the-loop interactive exploration, laboratory demonstrations, and visual analytics with reactive Python widgets.
- **FastAPI:** Built on Starlette and Uvicorn as an asynchronous ASGI microservice, designed for high-throughput headless REST API consumption by external frontends, mobile apps, and automated IoT sensor ingestion pipelines.
