<<<<<<< HEAD
#!/bin/bash
# ==============================================================================
# ULPF — Subsystem Health Inspection Script
# ==============================================================================

set -e

echo " Inspecting ULPF System Health & Readiness..."
echo ""

if ! curl -s -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo " ULPF API is unreachable at http://localhost:8000."
    echo "   Ensure containers are running with: docker compose ps"
    exit 1
fi

echo "--- /api/v1/health Response ---"
curl -s http://localhost:8000/api/v1/health | python3 -m json.tool || curl -s http://localhost:8000/api/v1/health

echo ""
echo "--- /api/v1/system/readiness Response ---"
curl -s http://localhost:8000/api/v1/system/readiness | python3 -m json.tool || curl -s http://localhost:8000/api/v1/system/readiness
echo ""
=======
#!/bin/bash
# ==============================================================================
# ULPF — Subsystem Health Inspection Script
# ==============================================================================

set -e

echo " Inspecting ULPF System Health & Readiness..."
echo ""

if ! curl -s -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    echo " ULPF API is unreachable at http://localhost:8000."
    echo "   Ensure containers are running with: docker compose ps"
    exit 1
fi

echo "--- /api/v1/health Response ---"
curl -s http://localhost:8000/api/v1/health | python3 -m json.tool || curl -s http://localhost:8000/api/v1/health

echo ""
echo "--- /api/v1/system/readiness Response ---"
curl -s http://localhost:8000/api/v1/system/readiness | python3 -m json.tool || curl -s http://localhost:8000/api/v1/system/readiness
echo ""
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
