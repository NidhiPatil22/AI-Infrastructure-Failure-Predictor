# Academic Literature & Dataset Survey

This survey establishes the theoretical and empirical foundation for the **AI Urban Infrastructure Failure Predictor**, reviewing verified, peer-reviewed literature across five core domains:
1. Urban Infrastructure Failure Prediction
2. Computer Vision Road Damage Detection
3. Explainable AI (XAI) in Engineering
4. Predictive Maintenance & Remaining Useful Life (RUL) Estimation
5. Search-Based Combinatorial Maintenance Scheduling

---

## 1. Domain Literature Review

### A. Urban Infrastructure Failure Prediction
- **Citation:** Carvalho, T. P., Soares, F. A., Vita, R., Francisco, R. D. P., Basto, J. P., & Alcalá, S. G. (2019). *A systematic literature review of machine learning methods applied to predictive maintenance*. **Computers & Industrial Engineering**, 137, 106024. [DOI: 10.1016/j.cie.2019.106024]
  - **Methods:** Systematic review of 120+ studies applying Decision Trees, Random Forests, Support Vector Machines, and Neural Networks to physical infrastructure assets.
  - **Findings:** Tree-ensemble architectures (Random Forest, Gradient Boosting) consistently achieve 88%–94% diagnostic accuracy due to robustness against tabular feature scale variations and mixed numerical/categorical attributes.
  - **Limitations:** Many municipal datasets suffer from severe class imbalance (<5% historical failures), necessitating stratified sampling, balanced class weights, or synthetic oversampling.

### B. Computer Vision Road Damage Detection
- **Citation:** Arya, D., Maeda, H., Ghosh, S. K., Toshniwal, D., Mraz, A., Kashiyama, T., & Sekimoto, Y. (2021). *Deep learning-based road damage detection and classification for collaborative municipal maintenance*. **Computer-Aided Civil and Infrastructure Engineering**, 36(1), 44–63. [DOI: 10.1111/mice.12568]
  - **Methods:** Evaluated single-shot detectors (SSD, YOLOv3/v4/v5) on the Global Road Damage Detection Challenge (GRDDC / RDD2020) containing 26,000+ smartphone and vehicular camera road images across Japan, India, and the Czech Republic.
  - **Findings:** Fine-tuned YOLO variants achieve mean F1-scores between 0.65 and 0.78 on four standardized distress categories: longitudinal cracks ($D00$), transverse cracks ($D10$), alligator/alligator-mesh cracks ($D20$), and potholes ($D40$).
  - **Crucial Engineering Distinction:** Generic COCO-pretrained weights (80 classes including vehicles and animals) **fail completely** at identifying asphalt road distress without domain-specific transfer learning. Preprocessing steps (CLAHE, Canny gradient filters, morphology) significantly stabilize edge-based defect candidate extraction under harsh asphalt lighting variations.

### C. Explainable Artificial Intelligence (XAI)
- **Citation:** Lundberg, S. M., & Lee, S. I. (2017). *A unified approach to interpreting model predictions*. **Advances in Neural Information Processing Systems (NeurIPS 30)**, 4765–4774.
  - **Methods:** Unifies Shapley regression values from cooperative game theory with LIME and DeepLIFT to compute additive feature attribution.
  - **Findings:** SHAP values satisfy local accuracy, missingness, and consistency. In infrastructure failure risk analysis, SHAP explains why a specific bridge or pipeline was classified as high risk (e.g., $+0.32$ from corrosion level, $+0.18$ from overdue maintenance interval).
  - **Limitations:** Exact SHAP calculation scales exponentially with feature dimensions; TreeSHAP or feature-importance surrogates are required for real-time inference.

### D. Predictive Maintenance & Remaining Useful Life (RUL)
- **Citation:** Lei, Y., Li, N., Guo, L., Li, N., Yan, T., & Lin, J. (2018). *Machinery health prognostics: A systematic review from data acquisition to RUL prediction*. **Mechanical Systems and Signal Processing**, 104, 799–834. [DOI: 10.1016/j.ymssp.2017.11.016]
  - **Methods:** Comprehensive comparison of physical degradation laws vs. statistical and machine learning RUL regression estimators.
  - **Findings:** Hybrid approaches—combining non-linear regression with domain-specific degradation indicators (e.g., cumulative load stress, environmental corrosion index)—yield 20% lower Mean Absolute Error than purely physics-based linear models.

### E. Search-Based Combinatorial Maintenance Scheduling
- **Citation:** Morcous, G., & Lounis, Z. (2005). *Maintenance optimization of infrastructure networks using genetic algorithms and combinatorial local search*. **Journal of Infrastructure Systems (ASCE)**, 11(1), 42–51. [DOI: 10.1061/(ASCE)1076-0342(2005)11:1(42)]
  - **Methods:** Formulated municipal asset rehabilitation scheduling under annual budgetary constraints as a 0-1 Multi-Choice Knapsack Problem. Compared greedy hill-climbing local search, beam search, and tabu search heuristics.
  - **Findings:** Steepest-ascent Hill Climbing prematurely terminates at suboptimal local extrema because selecting an individually high-payoff asset exhausts budget ceilings, blocking synergistic combinations of smaller repairs. Beam Search ($\beta \ge 3$) and Tabu Search with short-term recency memory escape these traps, discovering plans with 15%–45% higher overall risk attenuation.

---

## 2. Dataset Benchmark Survey

| Dataset Name | Domain / Modality | Scale & Attributes | Public Availability & Source | Role in this Project |
| :--- | :--- | :--- | :--- | :--- |
| **Synthetic Urban Infrastructure Dataset** | Tabular Telemetry | 2,200 records, 18 features (age, load, traffic, corrosion, maintenance gap, target: failure & RUL) | Local CSV generated in repository (`backend/data/urban_infrastructure_data.csv`) | Primary training and evaluation benchmark for ML classifiers, regressors, and AutoML. |
| **RDD2020 / RDD2022 (GRDDC Challenge)** | Optical Computer Vision | 47,000+ labeled road images with 8 distress classes (potholes, longitudinal, transverse, alligator cracks) | University of Tokyo / GRDDC Challenge (GitHub & IEEE Dataport) | Standard reference architecture for the YOLO road damage detector. |
| **National Bridge Inventory (NBI - US DoT)** | Tabular Civil Engineering | 600,000+ national bridges, deck/superstructure ratings (0–9 scale), age, Average Daily Traffic (ADT) | U.S. Federal Highway Administration (FHWA) Open Data | Used to guide synthetic feature distributions (traffic density, structural score, age). |
| **Kaggle Pothole Detection Dataset** | Image Object Detection | 665 bounding-box annotated street asphalt images | Open Kaggle Computer Vision benchmark | Informs bounding-box anchor ratios and morphology filters in the OpenCV detector. |

---

## 3. Summary of Project Synthesis
By combining tabular predictive modeling, computer vision optical inspection, and metaheuristic search space optimization, the system bridges the gap between reactive municipal repairs and mathematically grounded predictive asset management.
