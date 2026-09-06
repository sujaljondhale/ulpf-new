# ==============================================================================
# ULPF — Universal Log Pre-processing Framework
# Production Container Image (FastAPI Backend + Web Dashboard)
# ==============================================================================

FROM python:3.12-slim AS base

# Set environment variables for non-interactive and unbuffered python execution
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    ULPF_ENV=production \
    ULPF_API_HOST=0.0.0.0 \
    ULPF_API_PORT=8000

WORKDIR /app

# Install minimal OS runtime packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root system user for security
RUN groupadd -r ulpfgroup && useradd -r -g ulpfgroup -d /app -s /sbin/nologin ulpfuser

# Create persistent storage directory and set permissions
RUN mkdir -p /app/storage/raw && chown -R ulpfuser:ulpfgroup /app

# Copy application source code
COPY --chown=ulpfuser:ulpfgroup . .

# Switch to non-root user
USER ulpfuser

# Expose API/UI port and Syslog network collector ports
EXPOSE 8000
EXPOSE 5140/udp
EXPOSE 5141

# Docker Healthcheck against liveness endpoint
HEALTHCHECK --interval=20s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/live || exit 1

# Start ULPF Unified API Server & Web Dashboard
# PORT env var is used by Render; defaults to ULPF_API_PORT (8000) on other platforms
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-${ULPF_API_PORT:-8000}}"]
