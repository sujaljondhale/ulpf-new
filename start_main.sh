#!/usr/bin/env bash
# ==============================================================================
# ULPF Core 1 — Main Worker Ingestion & Normalization Engine
# Starts API, Ingress Listeners (UDP:5140, TCP:5141), and SOC Dashboard (:8000)
# ==============================================================================

echo "======================================================================"
echo " [ULPF CORE 1] Starting Main Worker Platform..."
echo " Dashboard & API: http://localhost:8000/dashboard/index.html#/overview"
echo "======================================================================"

python3 ./main/run_main.py
