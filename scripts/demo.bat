@echo off
REM ==============================================================================
REM ULPF — Automated SIH Demonstration Script for Windows
REM ==============================================================================

set API_BASE=http://localhost:8000/api/v1

echo ======================================================================
echo  [ULPF] RUNNING SIH END-TO-END DEMONSTRATION
echo ======================================================================

echo.
echo [1/5] Checking System Readiness...
curl -s %API_BASE%/health
echo.

echo.
echo [2/5] Triggering Scenario 1: Mixed Enterprise Traffic...
curl -s -X POST %API_BASE%/demo/scenarios/normal
echo.

echo.
echo [3/5] Triggering Scenario 2: Network Security Threats...
curl -s -X POST %API_BASE%/demo/scenarios/security
echo.

echo.
echo [4/5] Triggering Scenario 3: Unknown Vendor Telemetry...
curl -s -X POST %API_BASE%/demo/scenarios/unknown
echo.

echo.
echo [5/5] Ingesting CEF Log via POST /api/v1/ingest...
curl -s -X POST %API_BASE%/ingest -H "Content-Type: application/json" -d "{\"source\": \"Fortinet-Edge\", \"message\": \"CEF:0|Fortinet|FortiGate|7.2.4|32001|traffic:allow|3|src=198.51.100.42 dst=10.0.1.50 spt=54321 dpt=443 proto=tcp act=allow msg=\\\"Outbound TLS Session\\\"\"}"
echo.

echo.
echo ======================================================================
echo  [OK] SIH Demonstration Flow Complete!
echo       Open Dashboard: http://localhost:8000/dashboard/index.html#/sih-demo
echo ======================================================================
