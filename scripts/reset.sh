#!/bin/bash
# ==============================================================================
# ULPF — Clean Reset Script
# Wipes all Docker volumes and boots a clean demonstration environment
# ==============================================================================

set -e

echo "⚠️ WARNING: Performing full clean reset (wiping all persistent volumes)..."
docker compose down -v

echo "📦 Rebuilding and starting clean environment..."
docker compose up --build -d

echo "⏳ Waiting for service readiness..."
sleep 6

echo ""
echo "✅ ULPF clean reset complete! Fresh demonstration environment ready."
echo "   Dashboard: http://localhost:8000/dashboard/index.html#/sih-demo"
