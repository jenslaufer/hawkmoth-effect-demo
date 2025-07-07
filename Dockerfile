# Dockerfile
FROM python:3.13-slim

RUN pip install --no-cache-dir streamlit polars altair

WORKDIR /app
COPY app.py /app

CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.headless=true", "--server.port=8501", "--server.address=0.0.0.0"]
