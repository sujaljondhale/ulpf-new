#!/bin/bash
# ==============================================================================
# ULPF — Universal Log Pre-processing Framework
# Startup Automation Script (Production Container Stack)
# ==============================================================================

set -e

echo "======================================================================"
echo " 🚀 Starting ULPF Containerized Platform (Phase 7 Deployment)"
echo "======================================================================"

# 1. Check Docker & Compose availability
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed or not in PATH."
    exit 1
fi

if ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not available."
    exit 1
fi

# 2. Build and start core services (API, MinIO, OpenSearch)
echo "📦 Building and starting core container services..."
docker compose up --build -d

# 3. Wait for API and storage health readiness
echo "⏳ Waiting for ULPF API and storage engines to become ready..."
MAX_RETRIES=30
RETRY_COUNT=0
READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s -f http://localhost:8000/api/v1/health/ready > /dev/null 2>&1; then
        READY=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT+1))
    sleep 2
done

if [ "$READY" = true ]; then
    echo "✅ All ULPF services are ONLINE and HEALTHY!"
else
    echo "⚠️ Warning: Startup timed out waiting for ready state, but containers are running."
fi

# 4. Display Access URLs
echo ""
echo "======================================================================"
echo " 🌐 ULPF PLATFORM ACCESS URLS"
echo "======================================================================"
echo "  🏆 SIH Demo Control Center : http://localhost:8000/dashboard/index.html#/sih-demo"
echo "  📊 Main ULPF Web Dashboard : http://localhost:8000/dashboard/index.html#/overview"
echo "  💻 Client Event Generator  : http://localhost:8000/dashboard/client_app.html"
echo "  📖 Interactive Swagger Docs: http://localhost:8000/docs"
echo "  🔌 Core REST API Root      : http://localhost:8000/api/v1"
echo "  🪣 MinIO S3 Object Console : http://localhost:9001 (User: ulpf_admin)"
echo "  🔍 OpenSearch Cluster REST : http://localhost:9200"
echo "======================================================================"
echo ""
