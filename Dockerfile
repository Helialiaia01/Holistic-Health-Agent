FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY app.py .
COPY .env* ./

# Create logs directory
RUN mkdir -p logs

# Cloud Run requires listening on 0.0.0.0:8080
EXPOSE 8080

# Run with gunicorn for production
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 4 --timeout 3600 app:app
