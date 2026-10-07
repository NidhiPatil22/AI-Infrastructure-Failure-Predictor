# AI Urban Infrastructure Failure Predictor — Frontend

React + Vite interface for the existing FastAPI backend. All displayed model results come from the backend; fields and charts not returned by its API are identified as unavailable instead of being simulated.

## Run locally

1. Start the FastAPI backend from `backend/` on port `8000`.
2. In this folder, install packages once with `npm install`.
3. Start Vite with `npm run dev`.
4. Open the local URL printed by Vite.

Set `VITE_API_URL` in `.env` if the backend is hosted somewhere other than `http://localhost:8000`.

## Backend routes used

- `GET /api/health`
- `GET /api/dashboard`
- `POST /api/predict`
- `GET /api/analytics`
- `GET /api/infrastructure`

The backend does not currently return full per-asset analytics, raw failure-by-type or failure-by-zone counts, feature importance, PCA coordinates, or full infrastructure records. The UI reports these gaps explicitly.
