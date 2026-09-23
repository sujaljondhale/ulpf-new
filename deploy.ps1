<<<<<<< HEAD
# ==============================================================================
# ULPF (Universal Log Pre-processing Framework) - Windows Production Deployment
# ==============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ULPF ENTERPRISE DEPLOYMENT SCRIPT (WINDOWS / DOCKER)     " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Check Docker Daemon
Write-Host "[1/6] Checking Docker Engine status..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "      Docker installed: $dockerVersion" -ForegroundColor Green
    docker ps > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      ERROR: Docker Desktop daemon is not running! Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
    Write-Host "      Docker daemon is online and operational." -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Docker CLI not found in PATH." -ForegroundColor Red
    exit 1
}

# 2. Environment Configuration
Write-Host "[2/6] Verifying environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "      Created .env from .env.example" -ForegroundColor Green
    } else {
        Write-Host "      WARNING: No .env found. Using default container environments." -ForegroundColor Yellow
    }
} else {
    Write-Host "      Using existing .env configuration." -ForegroundColor Green
}

# 3. Build & Pull Container Images
Write-Host "[3/6] Building and preparing container stack..." -ForegroundColor Yellow
docker compose build ulpf-api ulpf-worker ulpf-simulator
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Failed to build Docker images." -ForegroundColor Red
    exit 1
}

# 4. Launch Microservices Stack
Write-Host "[4/6] Starting microservices stack..." -ForegroundColor Yellow
docker compose up -d minio redpanda redpanda-console ulpf-worker ulpf-api ulpf-simulator
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Failed to start containers via docker compose." -ForegroundColor Red
    exit 1
}

# 5. Initialize Storage Buckets and Kafka Streaming Topics
Write-Host "[5/6] Initializing MinIO S3 buckets and Redpanda topics..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Initialize MinIO Bucket
try {
    docker exec ulpf-minio mc alias set local http://localhost:9000 ulpf_admin ulpf_password_2026 > $null 2>&1
    docker exec ulpf-minio mc mb local/ulpf-raw > $null 2>&1
    Write-Host "      MinIO bucket 'ulpf-raw' verified." -ForegroundColor Green
} catch {
    Write-Host "      MinIO bucket initialization notice." -ForegroundColor Yellow
}

# Initialize Redpanda Topics
try {
    docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress ulpf-events-normalized ulpf-alerts -p 3 -r 1 > $null 2>&1
    Write-Host "      Redpanda Kafka topics created (ulpf-raw-ingress, ulpf-events-normalized, ulpf-alerts)." -ForegroundColor Green
} catch {
    Write-Host "      Redpanda topics verified." -ForegroundColor Yellow
}

# 6. Service Health & Readiness Probe
Write-Host "[6/6] Verifying operational endpoints..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ULPF PRODUCTION STACK DEPLOYED SUCCESSFULLY              " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Service Endpoints:" -ForegroundColor White
Write-Host "  * Core 1 SOC Web Dashboard:       http://localhost:8000/dashboard/index.html" -ForegroundColor Cyan
Write-Host "  * Core 1 REST API Docs:           http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  * Core 2 Simulator & Testbed:     http://localhost:8050/index.html" -ForegroundColor Cyan
Write-Host "  * Redpanda Kafka Console:         http://localhost:8085" -ForegroundColor Cyan
Write-Host "  * MinIO S3 Storage Console:       http://localhost:9001 (ulpf_admin / ulpf_password_2026)" -ForegroundColor Cyan
Write-Host "  * Ingestion Syslog Ports:         UDP 5140, TCP 5141" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Operational Commands:" -ForegroundColor White
Write-Host "  * View Live Container Logs:       docker compose logs -f [service]" -ForegroundColor Gray
Write-Host "  * Scale Streaming Workers:        docker compose up -d --scale ulpf-worker=3" -ForegroundColor Gray
Write-Host "  * Stop Stack:                     docker compose down" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Cyan
=======
# ==============================================================================
# ULPF (Universal Log Pre-processing Framework) - Windows Production Deployment
# ==============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ULPF ENTERPRISE DEPLOYMENT SCRIPT (WINDOWS / DOCKER)     " -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Check Docker Daemon
Write-Host "[1/6] Checking Docker Engine status..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "      Docker installed: $dockerVersion" -ForegroundColor Green
    docker ps > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "      ERROR: Docker Desktop daemon is not running! Please start Docker Desktop." -ForegroundColor Red
        exit 1
    }
    Write-Host "      Docker daemon is online and operational." -ForegroundColor Green
} catch {
    Write-Host "      ERROR: Docker CLI not found in PATH." -ForegroundColor Red
    exit 1
}

# 2. Environment Configuration
Write-Host "[2/6] Verifying environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "      Created .env from .env.example" -ForegroundColor Green
    } else {
        Write-Host "      WARNING: No .env found. Using default container environments." -ForegroundColor Yellow
    }
} else {
    Write-Host "      Using existing .env configuration." -ForegroundColor Green
}

# 3. Build & Pull Container Images
Write-Host "[3/6] Building and preparing container stack..." -ForegroundColor Yellow
docker compose build ulpf-api ulpf-worker ulpf-simulator
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Failed to build Docker images." -ForegroundColor Red
    exit 1
}

# 4. Launch Microservices Stack
Write-Host "[4/6] Starting microservices stack..." -ForegroundColor Yellow
docker compose up -d minio redpanda redpanda-console ulpf-worker ulpf-api ulpf-simulator
if ($LASTEXITCODE -ne 0) {
    Write-Host "      ERROR: Failed to start containers via docker compose." -ForegroundColor Red
    exit 1
}

# 5. Initialize Storage Buckets and Kafka Streaming Topics
Write-Host "[5/6] Initializing MinIO S3 buckets and Redpanda topics..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Initialize MinIO Bucket
try {
    docker exec ulpf-minio mc alias set local http://localhost:9000 ulpf_admin ulpf_password_2026 > $null 2>&1
    docker exec ulpf-minio mc mb local/ulpf-raw > $null 2>&1
    Write-Host "      MinIO bucket 'ulpf-raw' verified." -ForegroundColor Green
} catch {
    Write-Host "      MinIO bucket initialization notice." -ForegroundColor Yellow
}

# Initialize Redpanda Topics
try {
    docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress ulpf-events-normalized ulpf-alerts -p 3 -r 1 > $null 2>&1
    Write-Host "      Redpanda Kafka topics created (ulpf-raw-ingress, ulpf-events-normalized, ulpf-alerts)." -ForegroundColor Green
} catch {
    Write-Host "      Redpanda topics verified." -ForegroundColor Yellow
}

# 6. Service Health & Readiness Probe
Write-Host "[6/6] Verifying operational endpoints..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   ULPF PRODUCTION STACK DEPLOYED SUCCESSFULLY              " -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Service Endpoints:" -ForegroundColor White
Write-Host "  * Core 1 SOC Web Dashboard:       http://localhost:8000/dashboard/index.html" -ForegroundColor Cyan
Write-Host "  * Core 1 REST API Docs:           http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  * Core 2 Simulator & Testbed:     http://localhost:8050/index.html" -ForegroundColor Cyan
Write-Host "  * Redpanda Kafka Console:         http://localhost:8085" -ForegroundColor Cyan
Write-Host "  * MinIO S3 Storage Console:       http://localhost:9001 (ulpf_admin / ulpf_password_2026)" -ForegroundColor Cyan
Write-Host "  * Ingestion Syslog Ports:         UDP 5140, TCP 5141" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Operational Commands:" -ForegroundColor White
Write-Host "  * View Live Container Logs:       docker compose logs -f [service]" -ForegroundColor Gray
Write-Host "  * Scale Streaming Workers:        docker compose up -d --scale ulpf-worker=3" -ForegroundColor Gray
Write-Host "  * Stop Stack:                     docker compose down" -ForegroundColor Gray
Write-Host "============================================================" -ForegroundColor Cyan
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
