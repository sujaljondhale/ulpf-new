@echo off
REM ==============================================================================
REM ULPF — Clean Reset Script for Windows
REM ==============================================================================

echo [WARNING] Resetting ULPF environment and wiping volumes...
docker compose down -v

echo [INFO] Rebuilding and starting clean containers...
docker compose up --build -d

echo.
echo [OK] ULPF clean reset complete!
echo      Dashboard: http://localhost:8000/dashboard/index.html#/sih-demo
