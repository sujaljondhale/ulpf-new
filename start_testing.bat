@echo off
REM ==============================================================================
REM ULPF Core 2 — Protocol Simulator & Testing Hub Website
REM Starts Network Connection Simulator, Custom Log Studio, and Testbed (:8050)
REM ==============================================================================

echo ======================================================================
echo  [ULPF CORE 2] Starting Protocol Simulator ^& Testing Website...
echo  Testing Hub: http://localhost:8050/
echo ======================================================================

python .\testing\run_testing.py
pause
