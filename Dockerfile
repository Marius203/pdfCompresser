# Multi-stage build: First stage for React frontend
FROM node:18-slim AS frontend-build

WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code and build
COPY frontend/ ./
RUN npm run build

# Second stage: Python backend
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ghostscript && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY backend/ ./backend/

# Copy React build from previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Change to backend directory
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "300", "wsgi:app"]