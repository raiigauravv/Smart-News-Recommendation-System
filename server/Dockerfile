# Multi-stage build for smaller image size (cost optimization)
FROM python:3.11-slim as builder
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app /app/app
COPY ../utils /app/utils
COPY ../dataset /app/dataset

# Create startup script for Azure App Service
RUN echo '#!/bin/bash\nuvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}' > /app/startup.sh
RUN chmod +x /app/startup.sh

# Azure App Service runs on dynamic port
EXPOSE ${PORT:-8000}

# Use startup script
CMD ["/app/startup.sh"]