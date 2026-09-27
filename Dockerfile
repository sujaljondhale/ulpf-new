# ==============================================================================
# ULPF Testing Simulator & Protocol Testing Hub
# Production Container Image for Cloud Deployment (Testing Site)
# ==============================================================================

FROM python:3.12-slim AS base

# Set environment variables for non-interactive and unbuffered python execution
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    TESTING_HOST=0.0.0.0 \
    TESTING_PORT=8050 \
    PYTHONPATH=/app/main:/app/testing:/app

WORKDIR /app

# Install minimal OS runtime packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create deterministic non-root system user for security
RUN groupadd -r -g 10001 appgroup && useradd -r -u 10001 -g appgroup appuser

# Create persistent storage directories and set permissions
RUN mkdir -p /app/storage/raw /app/storage/logs && chown -R appuser:appgroup /app

# Copy application source code
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Expose Simulator Web Application Port
EXPOSE 8050

# Docker Healthcheck against testing web root
HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=5 \
    CMD curl -f -s http://127.0.0.1:${PORT:-8050}/ || exit 1

# Launch the Simulator Web Application & API Hub
CMD ["sh", "-c", "python testing/run_testing.py"]
