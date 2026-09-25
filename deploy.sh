#!/usr/bin/env bash
# ==============================================================================
# ULPF (Universal Log Pre-processing Framework) - Automated Deployment (Bash)
# ==============================================================================
set -e

echo "======================================================================"
echo "         ULPF ENTERPRISE STACK DEPLOYMENT & BOOTSTRAP                "
echo "======================================================================"

# 1. Ensure .env exists
if [ ! -f ".env" ]; then
    echo "[1/5] Creating default .env configuration..."
    cp .env.example .env
else
    echo "[1/5] Environment file .env detected."
fi

# 2. Build local container images
echo -e "\n[2/5] Building Docker microservices..."
docker compose build ulpf-api ulpf-worker ulpf-simulator

# 3. Start core infrastructure and microservices
echo -e "\n[3/5] Starting ULPF stack containers..."
docker compose up -d redis minio redpanda redpanda-console ulpf-api ulpf-worker ulpf-simulator

# 4. Wait for core services to initialize
echo -e "\n[4/5] Waiting for services to initialize..."
sleep 10

# 5. Initialize MinIO and Redpanda Topics
echo -e "\n[5/5] Bootstrapping MinIO buckets and Redpanda streaming topics..."
docker exec ulpf-minio mc alias set local http://localhost:9000 ulpf_admin ulpf_password_2026 2>/dev/null || true
docker exec ulpf-minio mc mb local/ulpf-raw 2>/dev/null || true
docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress ulpf-events-normalized ulpf-alerts -p 3 -r 1 2>/dev/null || true

echo "======================================================================"
echo "           ULPF ENTERPRISE STACK ONLINE & OPERATIONAL                "
echo "======================================================================"
echo " SOC UI & Gateway:       http://localhost:8000"
echo " Testing Simulator Hub:  http://localhost:8050"
echo " Redpanda Stream Visual: http://localhost:8085"
echo " MinIO Object Storage:   http://localhost:9001 (ulpf_admin / ulpf_password_2026)"
echo " Redis Cache & Broker:   Port 6379"
echo "======================================================================"
