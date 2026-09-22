# ==============================================================================
# ULPF Testing Simulator & Protocol Testing Hub
# Dedicated testing website, socket probe, and network simulator for ULPF
# ==============================================================================

FROM python:3.12-slim

# Image metadata
LABEL org.opencontainers.image.title="ULPF Testing Simulator Hub" \
      org.opencontainers.image.description="Dedicated testing website and network connection simulator for Universal Log Pre-processing Framework" \
      org.opencontainers.image.version="1.0.0"

# Set environment variables:
# - PYTHONUNBUFFERED=1: Stream logs in real-time without buffering
# - PYTHONDONTWRITEBYTECODE=1: Avoid writing .pyc files
# - PIP_NO_CACHE_DIR=1: Minimize image size
# - PIP_DISABLE_PIP_VERSION_CHECK=1: Suppress upgrade notices
# - TESTING_HOST=0.0.0.0: Bind simulator service across all container interfaces
# - TESTING_PORT=8050: Standard simulator port
# - ULPF_INTERNAL_API_HOST=host.docker.internal: Resolve host machine when probing
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    TESTING_HOST=0.0.0.0 \
    TESTING_PORT=8050 \
    ULPF_INTERNAL_API_HOST=host.docker.internal

# Install system dependencies (curl for healthchecks) and clean up apt cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root system user for secure container execution
RUN groupadd -r appuser && useradd -r -u 1000 -g appuser appuser

# Set working directory
WORKDIR /app

# Install Python dependencies first for optimal Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into container
COPY . .

# Set appropriate permissions for non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose Simulator Web Application Port
EXPOSE 8050

# Healthcheck to monitor web interface and API availability
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/ || exit 1

# Launch the Simulator Hub on port 8050
CMD ["python", "run_testing.py"]
