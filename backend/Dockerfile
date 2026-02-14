# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory for FAISS
RUN mkdir -p data

# Expose port (Cloud Run will inject PORT env var)
ENV PORT=8080

# Run the application
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT}
