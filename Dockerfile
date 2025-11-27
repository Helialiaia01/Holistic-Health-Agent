FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY app.py .
COPY .env .

# Create logs directory
RUN mkdir -p logs

# Cloud Run listens on 0.0.0.0:8080
EXPOSE 8080

# Run with gunicorn
CMD exec gunicorn --bind 0.0.0.0:8080 --workers 2 --worker-class sync --timeout 300 app:app
