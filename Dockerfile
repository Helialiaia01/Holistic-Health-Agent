FROM python:3.11-slim

WORKDIR /app

COPY requirements-simple.txt .
RUN pip install --no-cache-dir -r requirements-simple.txt

COPY app-simple.py app.py
COPY .env .

EXPOSE 8080

CMD exec gunicorn --bind 0.0.0.0:8080 --workers 2 app:app
