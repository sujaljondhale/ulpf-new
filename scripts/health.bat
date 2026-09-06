@echo off
REM ==============================================================================
REM ULPF — Subsystem Health Inspection Script for Windows
REM ==============================================================================

echo [ULPF] Inspecting System Health & Readiness...
echo.

curl -s http://localhost:8000/api/v1/health
echo.
echo.
curl -s http://localhost:8000/api/v1/system/readiness
echo.
