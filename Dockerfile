# Dockerfile
FROM python:3.13-slim

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --no-cache-dir streamlit numpy matplotlib

# Create app directory
WORKDIR /app
COPY app.py /app


# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.headless=true", "--server.port=8501", "--server.address=0.0.0.0"]
