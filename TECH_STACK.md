# Kosmoporos (ULPF) - Technology Stack

This document outlines the comprehensive technology stack that powers the Universal Log Pre-processing Framework (Kosmoporos), designed for ultra-high throughput, cryptographic provenance, and sovereign AI capabilities.

## 1. Core Languages
- **Python 3.10+**: The primary orchestration, API, and pipeline language.
- **C (C11/C99)**: Used for performance-critical subsystems via `ctypes` bindings, specifically:
  - High-speed parsing (`simd_parser.c`)
  - Cryptographic operations (`sha256.c`)
  - Merkle Tree generation (`merkle_vault.c`)
- **JavaScript (Vanilla)**: Powers the SOC log intelligence dashboard and the cyber protocol simulator testbed.

## 2. Web Framework & API
- **FastAPI (>= 0.110.0)**: Powers the asynchronous REST APIs, WebSocket streaming endpoints, and log ingestion gateways.
- **Uvicorn (>= 0.28.0)**: The lightning-fast ASGI server for handling concurrent HTTP and WebSocket connections.
- **Pydantic (>= 2.6.0)**: Provides strict data validation, canonical event schema enforcement, and type hints for the entire pipeline.
- **Python-Multipart (>= 0.0.32)**: For handling file uploads and form data parsing.

## 3. Storage & Persistence Layer
- **Relational Databases (SQLite / PostgreSQL)**: 
  - **SQLite (WAL Mode)**: Default embedded metadata store for the Kosmoporos core.
  - **PostgreSQL**: Production-grade metadata persistence (managed via `app/storage/database.py`).
- **Object Storage (MinIO)**: S3-compatible high-performance object lake used to store 100% byte-exact raw payloads for cryptographic evidence retention and Section 65B compliance (`app/storage/minio_store.py`).
- **Search & Analytics (OpenSearch)**: Distributed, RESTful search and analytics engine for querying canonical logs, telemetry data, and providing high-speed search across billions of parsed events (`app/storage/opensearch_store.py`).
- **Redis (In-Memory)**: Utilized as a fast queue buffer and backpressure controller during massive ingestion spikes.

## 4. Message Broker & Streaming
- **Redpanda / Kafka**: High-throughput distributed event streaming platform used to ingress wire-speed data and egress to multi-SIEM destinations simultaneously (e.g., streaming OCSF/ECS formats).

## 5. Sovereign AI & Machine Learning
- **Qwen 2.5 7B**: Air-gapped, zero-cloud sovereign local LLM used to dynamically synthesize Abstract Syntax Trees (ASTs) for zero-day/unknown log formats in under 5 seconds.
- **Hugging Face Hub**: Utilized for model management and loading.

## 6. Testing & Benchmarking
- **Pytest (>= 8.0.0)**: The core testing framework for unit tests, system integration tests, and multi-subsystem validations.
- **HTTPX (>= 0.27.0)**: Powers asynchronous HTTP clients in test suites and the cyber protocol simulator.
- **PSUtil (>= 5.9.8)**: Used heavily by the benchmarking and stress-testing scripts (`scripts/run_benchmarks.py`) to measure CPU/Memory RSS metrics in real-time.

## 7. Deployment & Infrastructure
- **Docker & Docker Compose**: The primary deployment architecture allowing decoupled execution of the AI Sidecar, Web Worker, Redpanda, MinIO, and OpenSearch.
- **Shell / PowerShell**: Multi-OS deployment scripts (`deploy.sh` and `deploy.ps1`) for frictionless one-command bootstrapping across Linux (OCI/AWS/Local) and Windows.

## 8. Export Standards & Schemas
- **OCSF v1.1.0** (Open Cybersecurity Schema Framework)
- **ECS** (Elastic Common Schema)
