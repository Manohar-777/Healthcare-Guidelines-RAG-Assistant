# Healthcare RAG Assistant - Docker Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY corpus/ ./corpus/
COPY scripts/ ./scripts/
COPY evaluation/ ./evaluation/
COPY streamlit_app.py .
COPY test_api.py .

# Create directories for models and index
RUN mkdir -p models index

# Expose ports
EXPOSE 9070 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:9070/ || exit 1

# Build index on startup (downloads model automatically)
# Then start server
CMD python scripts/pipeline.py && \
    uvicorn app.server:app --host 0.0.0.0 --port 9070