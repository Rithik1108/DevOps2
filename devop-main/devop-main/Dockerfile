# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY monitor.py .

# Create directory for logs and results
RUN mkdir -p /app/logs /app/results

# Set permissions
RUN chmod +x monitor.py

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash monitor && \
    chown -R monitor:monitor /app
USER monitor

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('https://httpbin.org/status/200', timeout=5)" || exit 1

# Default command
CMD ["python", "monitor.py"]