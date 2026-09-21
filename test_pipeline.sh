#!/usr/bin/env bash
# ============================================================
# ULPF Automated Testing & Verification Pipeline Runner
# Executes Pytest suites, Smoke tests, Security tests, Stack verification & Benchmarks
# Optional Flags:
#   --fast                    Run smoke, security, and stack tests without full pytest
#   --device-timeout <sec>    Network socket connection/probe timeout (e.g. 2.0)
#   --logs-interval <sec>     Inter-log transmission pacing (e.g. 0.05 for 50ms)
#   --logs-interval-ms <ms>   Inter-log transmission pacing in milliseconds (e.g. 20)
# ============================================================

cd "$(dirname "$0")"

echo "============================================================"
echo "  ULPF AUTOMATED TEST PIPELINE"
echo "  Supports: --device-timeout, --logs-interval, --fast"
echo "============================================================"

python3 testing/run_pipeline.py "$@"
