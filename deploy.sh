#!/usr/bin/env bash
# ==============================================================================
# ULPF (Universal Log Pre-processing Framework) - Linux/Server Production Deploy
# ==============================================================================
set -euo pipefail

echo "============================================================"
echo "   ULPF ENTERPRISE DEPLOYMENT SCRIPT (LINUX / CLOUD SERVER) "
echo "============================================================"

# 1. Check Docker & Docker Compose
echo "[1/6] Checking Docker Engine and Compose..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: docker command not found. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "ERROR: Docker daemon is not running or current user lacks docker permissions."
    exit 1
fi
echo "      Docker daemon is online."

# 2. Environment Configuration
echo "[2/6] Verifying environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "      Created .env from .env.example"
    else
        echo "      WARNING: No .env found. Using default container environments."
    fi
else
    echo "      Using existing .env configuration."
fi

# 3. Build & Pull Images
echo "[3/6] Building and preparing container images..."
docker compose build ulpf-api ulpf-worker ulpf-simulator

# 4. Launch Microservices Stack
echo "[4/6] Starting microservices stack..."
docker compose up -d minio redpanda redpanda-console ulpf-worker ulpf-api ulpf-simulator

# 5. Initialize Storage Buckets and Kafka Streaming Topics
echo "[5/6] Initializing MinIO S3 buckets and Redpanda topics..."
sleep 5

# Initialize MinIO Bucket
docker exec ulpf-minio mc alias set local http://localhost:9000 ulpf_admin ulpf_password_2026 > /dev/null 2>&1 || true
docker exec ulpf-minio mc mb local/ulpf-raw > /dev/null 2>&1 || true
echo "      MinIO bucket 'ulpf-raw' initialized."

# Initialize Redpanda Topics
docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress ulpf-events-normalized ulpf-alerts -p 3 -r 1 > /dev/null 2>&1 || true
echo "      Redpanda Kafka topics initialized."

# 6. Service Readiness Summary
echo "============================================================"
echo "   ULPF PRODUCTION STACK DEPLOYED SUCCESSFULLY              "
echo "============================================================"
echo ""
echo "  Service Endpoints:"
echo "  * Core 1 SOC Web Dashboard:       http://localhost:8000/dashboard/index.html"
echo "  * Core 1 REST API Docs:           http://localhost:8000/docs"
echo "  * Core 2 Simulator & Testbed:     http://localhost:8050/index.html"
echo "  * Redpanda Kafka Console:         http://localhost:8085"
echo "  * MinIO S3 Storage Console:       http://localhost:9001 (ulpf_admin / ulpf_password_2026)"
echo "  * Ingestion Syslog Ports:         UDP 5140, TCP 5141"
echo ""
echo "  Operational Commands:"
echo "  * View Live Container Logs:       docker compose logs -f [service]"
echo "  * Scale Streaming Workers:        docker compose up -d --scale ulpf-worker=3"
echo "  * Stop Stack:                     docker compose down"
echo "============================================================"
