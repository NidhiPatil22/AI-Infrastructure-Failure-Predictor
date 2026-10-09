# Version Control & Git Strategy Guide

This document defines the version control, Git workflow, repository hygiene, and release standards for the **AI Urban Infrastructure Failure Predictor**.

---

## 1. Git Initialization & Repository Setup

### Initial Setup Commands
```bash
# Navigate to repository root
cd /path/to/ml_infrastructure_predictor

# Initialize Git repository (if starting fresh)
git init

# Configure user identity
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Set default main branch
git branch -M main

# Link to GitHub remote origin
git remote add origin https://github.com/<your-username>/AI-Infrastructure-Failure-Predictor.git
```

---

## 2. Commit Message Standards (Conventional Commits)

To ensure clarity, auditability, and automated changelog generation, all commits must adhere to the **Conventional Commits** specification:

`<type>(<scope>): <short imperative description>`

### Commit Types:
- `feat`: A new feature (e.g., Computer Vision road damage detector, MLflow integration)
- `fix`: A bug fix (e.g., handling missing asset fields in inference payload)
- `docs`: Documentation updates (e.g., viva questions, reports, README)
- `refactor`: Code restructuring without changing behavior
- `test`: Adding or updating test cases
- `chore`: Build tooling, dependency bumps, or Dockerfile adjustments

### Meaningful Commit Examples:
```bash
git commit -m "feat(cv): integrate OpenCV and YOLO for road damage detection"
git commit -m "feat(optimization): implement Hill Climbing, Beam Search, and Tabu Search"
git commit -m "feat(tracking): integrate MLflow with sqlite backend and metric logging"
git commit -m "feat(automl): benchmark FLAML tabular against manual models"
git commit -m "docs(report): update academic lab report with experimental results"
git commit -m "chore(mlops): add Dockerfile, .dockerignore, and DVC pipeline"
```

---

## 3. Branching Strategy (Git Flow / GitHub Flow)

```
       main  ─────────────────●───────────────────────────●─────► Production Release
                              ▲                           ▲
                              │ Pull Request              │ Pull Request
       develop ───────────────●──────────●────────────────●─────► Staging Integration
                              ▲          ▲
        feature/cv-damage ────┘          │
        feature/search-opt ──────────────┘
```

### Branch Hierarchy:
1. **`main`**: Production-ready, stable codebase. Only accepts peer-reviewed Pull Requests from `develop`.
2. **`develop`**: Central integration branch for upcoming lab milestones.
3. **`feature/*`**: Isolated feature branches for specific laboratory modules:
   - `feature/cv-road-damage`
   - `feature/mlflow-experiment-tracking`
   - `feature/search-space-optimization`
   - `feature/automl-flaml`
   - `feature/docker-mlops`

### Creating and Merging Feature Branches:
```bash
# Create and switch to a feature branch
git checkout -b feature/cv-road-damage

# Work on feature, stage changes, commit
git add backend/app/cv/ streamlit_app.py
git commit -m "feat(cv): add OpenCV morphological distress extractor"

# Push feature branch to remote
git push -u origin feature/cv-road-damage

# Once verified, open a Pull Request into develop/main
```

---

## 4. Repository Hygiene & What NOT to Commit

> **Golden Rule of ML Version Control:**  
> **Commit code, configuration, and small metrics metadata; NEVER commit virtual environments, large binary weights, secret credentials, or temporary logs.**

### Critical Ignored Categories (Managed via `.gitignore`):
1. **Virtual Environments (`.venv/`, `venv/`, `env/`)**: Virtual environments contain OS-specific binaries and must be generated via `requirements.txt`.
2. **Large Model Weights (`*.pt`, `*.pth`, `*.onnx`, `*.h5`)**: Binary checkpoint files bloat the Git tree and degrade clone performance. Use `git-lfs` (Large File Storage) or DVC if versioning binary weights.
3. **Credentials & Secrets (`.env`, `secrets.toml`, `*.pem`)**: API keys and database credentials must never be committed to source control.
4. **Local Databases & Cache (`*.db`, `__pycache__/`, `.pytest_cache/`)**: Transient SQLite databases, compiled bytecodes, and temp files are created locally at runtime.
5. **Experiment Run Dumps (`mlruns/`, `.mlflow/`)**: Raw tracking run folders should be logged to a remote tracking server or tracked via DVC.
