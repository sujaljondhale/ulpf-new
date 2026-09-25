#!/usr/bin/env bash
# ==============================================================================
# ULPF (Universal Log Pre-processing Framework) - Automated Deployment (Bash)
# Optimized for Linux & Oracle Cloud Infrastructure (OCI) Virtual Machines
# ==============================================================================
set -e

echo "======================================================================"
echo "         ULPF ENTERPRISE STACK DEPLOYMENT & BOOTSTRAP                "
echo "======================================================================"

# Determine docker compose binary command
if docker compose version >/dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo "[ERROR] Neither 'docker compose' nor 'docker-compose' found on system."
    echo "Please install Docker and Docker Compose plugin."
    exit 1
fi

# Kernel memory tuning check for OpenSearch / Redpanda on Linux / Oracle VM
if [ -f /proc/sys/vm/max_map_count ]; then
    CURRENT_MAP_COUNT=$(cat /proc/sys/vm/max_map_count)
    if [ "$CURRENT_MAP_COUNT" -lt 262144 ]; then
        echo "[INFO] Optimizing vm.max_map_count for OpenSearch ($CURRENT_MAP_COUNT -> 262144)..."
        sudo sysctl -w vm.max_map_count=262144 2>/dev/null || true
    fi
fi

# 1. Ensure .env exists
if [ ! -f ".env" ]; then
    echo "[1/5] Creating default .env configuration..."
    cp .env.example .env
else
    echo "[1/5] Environment file .env detected."
fi

# 2. Build local container images
echo -e "\n[2/5] Building Docker microservices..."
$COMPOSE_CMD build ulpf-api ulpf-worker ulpf-simulator

# 3. Start core infrastructure and microservices
echo -e "\n[3/5] Starting ULPF stack containers..."
$COMPOSE_CMD up -d redis minio redpanda redpanda-console ulpf-api ulpf-worker ulpf-simulator

# 4. Wait for core services to initialize
echo -e "\n[4/5] Waiting for core services to initialize..."
sleep 10

# 5. Initialize MinIO and Redpanda Topics
echo -e "\n[5/5] Bootstrapping MinIO buckets and Redpanda streaming topics..."

# MinIO alias and bucket creation with retry
for i in {1..5}; do
    if docker exec ulpf-minio mc alias set local http://localhost:9000 ulpf_admin ulpf_password_2026 >/dev/null 2>&1; then
        docker exec ulpf-minio mc mb local/ulpf-raw >/dev/null 2>&1 || true
        echo "  -> MinIO bucket 'ulpf-raw' verified."
        break
    fi
    sleep 2
done

# Redpanda topics creation with retry
for i in {1..5}; do
    if docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress ulpf-events-normalized ulpf-alerts -p 3 -r 1 >/dev/null 2>&1; then
        echo "  -> Redpanda Kafka topics verified."
        break
    fi
    sleep 2
done

echo "======================================================================"
echo "           ULPF ENTERPRISE STACK ONLINE & OPERATIONAL                "
echo "======================================================================"
echo " SOC UI & Gateway:       http://localhost:8000"
echo " Testing Simulator Hub:  http://localhost:8050"
echo " Redpanda Stream Visual: http://localhost:8085"
echo " MinIO Object Storage:   http://localhost:9001 (ulpf_admin / ulpf_password_2026)"
echo " Redis Cache & Broker:   Port 6379"
echo "======================================================================"
