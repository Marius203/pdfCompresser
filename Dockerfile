# Multi-stage build: First stage for React frontend
FROM node:18-slim AS frontend-build

WORKDIR /app/frontend

# Copy package files first for better caching
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY frontend/ ./

# Build with error handling
RUN npm run build && \
    test -f build/index.html || (echo "React build failed" && exit 1)

# Second stage: Python backend
FROM python:3.10-slim AS production

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ghostscript \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with error handling
RUN pip install --no-cache-dir -r requirements.txt && \
    python -c "import flask, flask_cors; print('Dependencies OK')"

# Copy backend files
COPY backend/ ./backend/

# Copy React build from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Verify critical files exist
RUN test -f backend/app.py || (echo "app.py missing" && exit 1) && \
    test -f backend/wsgi.py || (echo "wsgi.py missing" && exit 1) && \
    test -f frontend/build/index.html || (echo "React build missing" && exit 1)

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Change to backend directory
WORKDIR /app/backend

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health', timeout=5)" || exit 1

# Expose port
EXPOSE 5000

# Production Gunicorn configuration
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--worker-class", "sync", \
     "--worker-connections", "1000", \
     "--timeout", "120", \
     "--keepalive", "2", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "100", \
     "--preload", \
     "--log-level", "info", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "wsgi:app"]