@echo off
REM ============================================================
REM ULPF Automated Testing & Verification Pipeline Runner (Testing Hub)
REM Executes Pytest suites, Smoke tests, Security tests, Stack verification & Benchmarks
REM ============================================================
cd /d "%~dp0"
echo ============================================================
echo   ULPF AUTOMATED TEST PIPELINE (TESTING HUB)
echo ============================================================
python run_pipeline.py %*
pause
