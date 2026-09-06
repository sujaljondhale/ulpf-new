@echo off
REM ==============================================================================
REM ULPF — Universal Log Pre-processing Framework
REM Startup Automation Script for Windows (Phase 7 Container Stack)
REM ==============================================================================

echo ======================================================================
echo  [ULPF] Starting ULPF Containerized Platform (Docker Stack)
echo ======================================================================

docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker or Docker Compose is not installed or running.
    pause
    exit /b 1
)

echo [1/3] Building and starting ULPF container services...
docker compose up --build -d

echo [2/3] Waiting for services to initialize...
timeout /t 5 /nobreak >nul

echo [3/3] Checking readiness probe...
curl -s -f http://localhost:8000/api/v1/health/ready >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] ULPF Platform is ONLINE and HEALTHY!
) else (
    echo [INFO] Services starting up in background.
)

echo.
echo ======================================================================
echo  ULPF PLATFORM ACCESS URLS
echo ======================================================================
echo   SIH Demo Control Center : http://localhost:8000/dashboard/index.html#/sih-demo
echo   Main Web Dashboard      : http://localhost:8000/dashboard/index.html#/overview
echo   Client Event Generator  : http://localhost:8000/dashboard/client_app.html
echo   Swagger Documentation   : http://localhost:8000/docs
echo   REST API Root           : http://localhost:8000/api/v1
echo   MinIO Object Console    : http://localhost:9001
echo   OpenSearch Search Node  : http://localhost:9200
echo ======================================================================
echo.
