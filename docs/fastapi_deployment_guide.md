# FastAPI Production Deployment & Serving Guide

While **Streamlit** acts as the primary interactive laboratory front-end for human practitioners, the system also incorporates a fully functional **FastAPI** backend for headless, microservice, or enterprise integration.

---

## 1. Architecture Comparison: Streamlit vs. FastAPI

| Attribute | Streamlit Application (`streamlit_app.py`) | FastAPI Microservice (`backend/app/main.py`) |
| :--- | :--- | :--- |
| **Primary Use Case** | Visual dashboards, live demonstrations, interactive laboratory exploration | Machine-to-machine REST API, automated IoT sensor ingest, CI/CD integration |
| **User Interface** | Built-in reactive Python UI widgets | Auto-generated OpenAPI / Swagger UI & ReDoc |
| **Throughput** | Moderate (optimized for concurrent dashboard users) | High (asynchronous ASGI event loop via Starlette and Uvicorn) |
| **Integration** | Standalone browser application | React, Vue, mobile apps, or municipal ERP / SCADA backends |

---

## 2. Running FastAPI Locally

### Step 1: Activate Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### Step 2: Launch Uvicorn ASGI Server
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Server endpoints will be live at `http://localhost:8000`.

---

## 3. Interactive Documentation
FastAPI automatically generates interactive API documentation:
- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 4. Key REST Endpoints & Payloads

### A. Health Check
- **Route:** `GET /api/health`
- **Response:**
```json
{
  "status": "ok",
  "message": "AI Urban Infrastructure Failure Predictor backend is running."
}
```

### B. Single Asset Risk & RUL Prediction
- **Route:** `POST /api/predict`
- **Sample Request Body:**
```json
{
  "asset_id": "BRIDGE-NORTH-04",
  "asset_type": "Bridge",
  "zone": "North",
  "material": "Concrete",
  "age_years": 24.5,
  "traffic_density": 78.0,
  "average_load": 135.0,
  "annual_rainfall": 1950.0,
  "average_temperature": 26.5,
  "maintenance_count": 4,
  "days_since_maintenance": 280,
  "days_since_inspection": 210,
  "structural_score": 42.0,
  "corrosion_level": 64.0,
  "previous_failures": 2,
  "usage_intensity": 82.0
}
```
- **Sample Response Body:**
```json
{
  "asset_id": "BRIDGE-NORTH-04",
  "asset_type": "Bridge",
  "zone": "North",
  "failure_probability": 0.8842,
  "risk_level": "HIGH",
  "remaining_useful_life": 8.42,
  "priority": "P1 - Critical",
  "recommendation": "Immediate inspection and preventive maintenance required.",
  "failure_probability_percent": "88.42%"
}
```

### C. Computer Vision Road Damage Analysis
- **Route:** `POST /api/cv/detect-damage`
- **Request Type:** `multipart/form-data` with `file: <road_image.jpg>`
- **Response:** Bounding boxes, class labels (`Pothole`, `Longitudinal Crack`), Road Damage Index (0-100), and base64-encoded annotated image.

### D. Search Space Maintenance Scheduling Optimization
- **Route:** `POST /api/optimization/compare`
- **Request Body:**
```json
{
  "budget_limit": 50000.0,
  "capacity_limit": 160.0
}
```
- **Response:** Side-by-side execution metrics and selected asset plans for Hill Climbing, Beam Search, and Tabu Search.

---

## 5. Production Serving Recommendations

For high-concurrency production deployments:
```bash
# Production multi-worker execution via Gunicorn + Uvicorn workers
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```
- Place behind **Nginx** reverse proxy for SSL termination, request buffering, and rate limiting.
- Containerize using the provided root `Dockerfile`.
