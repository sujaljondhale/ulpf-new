<<<<<<< HEAD
@echo off
REM ============================================================
REM ULPF Automated Testing & Verification Pipeline Runner
REM Executes Pytest suites, Smoke tests, Security tests, Stack verification & Benchmarks
REM Optional Flags:
REM   --fast                    Run smoke, security, and stack tests without full pytest
REM   --device-timeout <sec>    Network socket connection/probe timeout (e.g. 2.0)
REM   --logs-interval <sec>     Inter-log transmission pacing (e.g. 0.05 for 50ms)
REM   --logs-interval-ms <ms>   Inter-log transmission pacing in milliseconds (e.g. 20)
REM ============================================================
cd /d "%~dp0"
echo ============================================================
echo   ULPF AUTOMATED TEST PIPELINE
echo   Supports: --device-timeout, --logs-interval, --fast
echo ============================================================
python testing\run_pipeline.py %*
pause
=======
@echo off
REM ============================================================
REM ULPF Automated Testing & Verification Pipeline Runner
REM Executes Pytest suites, Smoke tests, Security tests, Stack verification & Benchmarks
REM Optional Flags:
REM   --fast                    Run smoke, security, and stack tests without full pytest
REM   --device-timeout <sec>    Network socket connection/probe timeout (e.g. 2.0)
REM   --logs-interval <sec>     Inter-log transmission pacing (e.g. 0.05 for 50ms)
REM   --logs-interval-ms <ms>   Inter-log transmission pacing in milliseconds (e.g. 20)
REM ============================================================
cd /d "%~dp0"
echo ============================================================
echo   ULPF AUTOMATED TEST PIPELINE
echo   Supports: --device-timeout, --logs-interval, --fast
echo ============================================================
python testing\run_pipeline.py %*
pause
>>>>>>> 3831b7383e78d54d129d8499c87cadb87be6e6c0
