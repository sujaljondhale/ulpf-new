# ==============================================================================
# ULPF — Universal Log Pre-processing Framework
# Dedicated Main SOC Backend & Dashboard Container Image (for VM / Host Deployment)
# ==============================================================================

FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    ULPF_ENV=production \
    ULPF_API_HOST=0.0.0.0 \
    ULPF_API_PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd -r ulpfgroup && useradd -r -g ulpfgroup -d /app -s /sbin/nologin ulpfuser
RUN mkdir -p /app/storage/raw && chown -R ulpfuser:ulpfgroup /app

COPY --chown=ulpfuser:ulpfgroup main/ .

USER ulpfuser

EXPOSE 8000
EXPOSE 5140/udp
EXPOSE 5141

HEALTHCHECK --interval=20s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/live || exit 1

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-${ULPF_API_PORT:-8000}} --no-access-log"]
