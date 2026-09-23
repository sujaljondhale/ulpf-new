@echo off
REM ==============================================================================
REM ULPF — Stop Script for Windows
REM ==============================================================================

echo [ULPF] Stopping ULPF containers...
docker compose down

echo.
echo [OK] All ULPF containers stopped.
echo [INFO] Persistent data volumes are preserved.
echo        Run scripts\start.bat to resume.
