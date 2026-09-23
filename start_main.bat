<<<<<<< HEAD
@echo off
REM ==============================================================================
REM ULPF Core 1 — Main Worker Ingestion & Normalization Engine
REM Starts API, Ingress Listeners (UDP:5140, TCP:5141), and SOC Dashboard (:8000)
REM ==============================================================================

echo ======================================================================
echo  [ULPF CORE 1] Starting Main Worker Platform...
echo  Dashboard ^& API: http://localhost:8000/dashboard/index.html#/overview
echo ======================================================================

python .\main\run_main.py
pause
=======
@echo off
REM ==============================================================================
REM ULPF Core 1 — Main Worker Ingestion & Normalization Engine
REM Starts API, Ingress Listeners (UDP:5140, TCP:5141), and SOC Dashboard (:8000)
REM ==============================================================================

echo ======================================================================
echo  [ULPF CORE 1] Starting Main Worker Platform...
echo  Dashboard ^& API: http://localhost:8000/dashboard/index.html#/overview
echo ======================================================================

python .\main\run_main.py
pause
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
