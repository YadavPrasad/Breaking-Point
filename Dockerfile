# Use Python 3.11 slim
FROM python:3.11-slim

WORKDIR /app

# Install build essentials for packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend
COPY backend/ .

# Copy frontend into container
COPY frontend/ ./frontend

# Copy model artifacts
COPY backend/model_artifacts ./model_artifacts

# Expose port
EXPOSE 8000

# Start app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
