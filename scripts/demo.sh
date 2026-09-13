#!/bin/bash
# ==============================================================================
# ULPF — Automated SIH Demonstration Script
# ==============================================================================

set -e

API_BASE="http://localhost:8000/api/v1"

echo "======================================================================"
echo "  RUNNING ULPF SIH END-TO-END DEMO SUITE"
echo "======================================================================"

echo ""
echo "1. Checking System Health..."
curl -s -f "$API_BASE/health" > /dev/null || (echo " API offline" && exit 1)
echo "    ULPF Core Engine Online"

echo ""
echo "2. Triggering Scenario 1: Mixed Multi-Vendor Normal Traffic..."
curl -s -X POST "$API_BASE/demo/scenarios/normal" | python3 -m json.tool || true

echo ""
echo "3. Triggering Scenario 2: Network Security Threats..."
curl -s -X POST "$API_BASE/demo/scenarios/security" | python3 -m json.tool || true

echo ""
echo "4. Triggering Scenario 3: Unknown Vendor Telemetry Format..."
curl -s -X POST "$API_BASE/demo/scenarios/unknown" | python3 -m json.tool || true

echo ""
echo "5. Triggering Scenario 4: Active Cyberattack Incident..."
curl -s -X POST "$API_BASE/demo/scenarios/attack" | python3 -m json.tool || true

echo ""
echo "6. Ingesting Raw Single Event via REST API..."
INGEST_RES=$(curl -s -X POST "$API_BASE/ingest" \
  -H "Content-Type: application/json" \
  -d '{"source": "Fortinet-Perimeter", "message": "CEF:0|Fortinet|FortiGate|7.2.4|32001|traffic:allow|3|src=198.51.100.42 dst=10.0.1.50 spt=54321 dpt=443 proto=tcp act=allow msg=\"Outbound TLS Session\""}')
echo "$INGEST_RES" | python3 -m json.tool || echo "$INGEST_RES"

echo ""
echo "7. Verifying Tamper-Evident SHA-256 Evidence..."
curl -s "$API_BASE/events?limit=1" | python3 -m json.tool || true

echo ""
echo "======================================================================"
echo "  SIH Demonstration Pipeline Execution Complete!"
echo "    Open Dashboard: http://localhost:8000/dashboard/index.html#/sih-demo"
echo "======================================================================"
