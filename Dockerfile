# Multi-stage build: First stage for React frontend
FROM node:18-slim AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build the React app
RUN npm run build

# Second stage: Python backend with React build
FROM python:3.10-slim

# Install system dependencies including Ghostscript
RUN apt-get update && apt-get install -y \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend files
COPY backend/ ./backend/

# Copy the React build from the previous stage
COPY --from=frontend-build /app/frontend/build ./frontend/build

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Change to backend directory
WORKDIR /app/backend

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]