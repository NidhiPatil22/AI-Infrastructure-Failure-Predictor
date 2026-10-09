# Multi-Stage / Production Dockerfile for AI Urban Infrastructure Failure Predictor
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8501

# Install essential system dependencies (libgl1 for OpenCV, build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libgomp1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency specifications first for layer caching
COPY backend/requirements.txt /app/backend/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt && \
    pip install --no-cache-dir streamlit opencv-python-headless ultralytics mlflow flaml xgboost lightgbm networkx scipy

# Copy application source code
COPY . /app

# Ensure sample images and database directories exist
RUN python -c "from backend.app.cv.road_damage_detector import generate_sample_road_images; generate_sample_road_images('/app/backend/data/sample_road_images')"

# Expose ports:
# 8501 for Streamlit primary application
# 8000 for optional FastAPI REST service
EXPOSE 8501 8000

# Default entrypoint runs Streamlit
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
