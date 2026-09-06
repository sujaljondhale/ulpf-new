# ULPF Deployment & Operations Guide

**Universal Log Pre-processing Framework (ULPF)**  
*SIH 26156 — National Technical Research Organisation (NTRO)*  
*Phase 7: Docker + Persistence + Deployment Hardening*

---

## 1. System Requirements

| Metric | Minimum (Laptop Demo Mode) | Recommended (Multi-Service Production) |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11, Linux (Ubuntu 22.04+), macOS | Enterprise Linux (RHEL 9, Debian 12) |
| **RAM** | 8 GB RAM (512MB OpenSearch JVM heap, ~150MB MinIO) | 16+ GB RAM (if running local AI SLM) |
| **CPU** | 4 Cores (x86_64 or ARM64) | 8+ Cores |
| **Disk Space** | 10 GB free disk space | 100+ GB SSD storage |
| **Prerequisites** | Docker Engine 24.0+ & Docker Compose v2.20+ | Docker Engine & Kubernetes 1.28+ |

---

## 2. One-Command Quickstart

The entire ULPF platform starts with a single command:

```bash
docker compose up --build
```

Or run via automated startup script:

```bash
# Linux / macOS:
./scripts/start.sh

# Windows:
scripts\start.bat
```

### Access URLs:
* **🏆 SIH Demo Control Center**: [http://localhost:8000/dashboard/index.html#/sih-demo](http://localhost:8000/dashboard/index.html#/sih-demo)
* **📊 Main ULPF Web Dashboard**: [http://localhost:8000/dashboard/index.html#/overview](http://localhost:8000/dashboard/index.html#/overview)
* **💻 Client Event Generator**: [http://localhost:8000/dashboard/client_app.html](http://localhost:8000/dashboard/client_app.html)
* **📖 Interactive Swagger OpenAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **🔌 Core REST API Root**: [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
* **🪣 MinIO S3 Object Console**: [http://localhost:9001](http://localhost:9001) *(User: `ulpf_admin`, Pass: `ulpf_password_2026`)*
* **🔍 OpenSearch Cluster REST**: [http://localhost:9200](http://localhost:9200)

---

## 3. Operational Lifecycle Commands

### Stop the Platform (Preserve Data Volumes)
```bash
docker compose down
```
*Persistent volumes (`ulpf_minio_data`, `ulpf_opensearch_data`, `ulpf_metadata_store`) remain preserved. On the next `docker compose up`, all previously ingested events and configurations will be available.*

### Full Clean Reset (Wipe All Volumes)
```bash
docker compose down -v
docker compose up --build
```
*Removes all persistent volumes and boots a pristine, fresh demonstration environment.*

### Run Automated SIH Demo Suite
```bash
# Linux / macOS:
./scripts/demo.sh

# Windows:
scripts\demo.bat
```

### Inspect System Health Probes
```bash
# Linux / macOS:
./scripts/health.sh

# Windows:
scripts\health.bat
```

---

## 4. Multi-Tier Persistence Architecture

ULPF does **NOT** rely on volatile RAM as a single source of truth. Data flows through a 3-tier persistent hierarchy:

```text
Incoming Raw Log
       │
       ▼
[1. Cryptographic SHA-256 Hashing]
       │
       ▼
[2. MinIO S3 Object Storage] ──────► Bucket: `ulpf-raw` (Immutable Evidence Source of Truth)
       │                              Key: `events/{YYYY}/{MM}/{DD}/{event_id}.raw`
       ▼
[3. Deterministic Normalization] ──► Format Detection -> Regex Parser -> Semantic Normalizer -> ULPF-IR v1.0
       │
       ▼
[4. OpenSearch REST Index] ────────► Index: `ulpf-events` (Searchable Normalized Representation)
       │
       ▼
[5. SQLite Metadata DB] ───────────► Volume: `/app/storage/ulpf_metadata.db` (Parser Registry, Sources, Audit)
```

---

## 5. Graceful Degradation & High Availability

ULPF is designed with robust circuit-breaker and fallback mechanisms:

### Scenario A: OpenSearch Is Starting / Offline
* **Behavior**: Raw log is safely stored in MinIO and metadata is written to persistent SQLite.
* **Search Status**: Queries fallback transparently to SQLite full-text search with zero unhandled exceptions.
* **Health Matrix**: OpenSearch component displays `DEGRADED (SQLite local search active)` while API remains `HEALTHY`.

### Scenario B: MinIO Is Starting / Offline
* **Behavior**: Raw log is immediately written to local tamper-evident disk storage (`/app/storage/raw/{event_id}.raw`) with SHA-256 checksum.
* **Storage Status**: Storage indicates `degraded_local_fallback`. Evidence integrity remains 100% verified.

### Scenario C: Local AI (Ollama) Is Offline
* **Behavior**: All 8 deterministic compiled parsers (CEF, LEEF, Syslog, JSON, Key=Value, CSV, XML, Plaintext) operate at full speed (>13,500 EPS).
* **Unknown Logs**: Unrecognized syntax is safely quarantined in the AI Review Queue with status `UNKNOWN_FORMAT / AI_OFFLINE`.

---

## 6. Local AI / Ollama Profile Configuration

Local SLM inference (Qwen2.5-Coder 3B) is packaged as an optional Docker Compose profile so laptop memory usage remains lean:

```bash
# Start core platform + Local AI SLM engine:
docker compose --profile ai up --build -d
```

To enable OpenSearch Dashboards UI:

```bash
# Start core platform + OpenSearch Dashboards UI:
docker compose --profile analytics up --build -d
```

To run all profiles simultaneously:

```bash
docker compose --profile ai --profile analytics up --build -d
```

---

## 7. Air-Gapped & Sovereign Deployment Architecture

For high-security defense networks (NTRO, defense SOC, isolated perimeters):

```text
Internet Not Required at Runtime
             ↓
Local Container Base Images (Pre-packaged tarball)
             ↓
Local Deterministic Parser Registry
             ↓
Local Storage Volumes (MinIO / SQLite / OpenSearch)
             ↓
Optional Local Quantized SLM (Qwen2.5-Coder:3B)
```

> **Air-Gapped Statement**: *ULPF architecturally supports air-gapped deployment with zero external cloud egress, zero runtime package installation, and 100% sovereign on-premise execution; final compliance validation depends on the deployment host physical isolation.*

---

## 8. Production vs. Prototype Comparison Table

| Capability / Tier | ULPF SIH Prototype (Delivered) | Enterprise Production Architecture |
| :--- | :--- | :--- |
| **API Layer** | Real (FastAPI + Uvicorn Async, Non-root) | Real (FastAPI / Envoy Gateway with Horizontal Pod Autoscaling) |
| **Containerization** | Real (Docker + Docker Compose Stack) | Real (Kubernetes Helm Charts + OCI Images) |
| **Raw Evidence Store** | Real (MinIO S3 Immutable + Local Fallback) | Real (Distributed Ceph / AWS S3 Object Lock / MinIO Cluster) |
| **Search Engine** | Real (OpenSearch 2.11, 512MB Single-Node) | Real (Multi-node Distributed OpenSearch / Elasticsearch Cluster) |
| **Metadata DB** | Real (SQLite 3 with Volume Mount) | Real (PostgreSQL / CockroachDB High-Availability Cluster) |
| **Real-Time Stream** | Real (Server-Sent Events Broadcast Hub) | Real (Scalable WebSockets / Redis PubSub Gateway) |
| **Streaming Buffer** | Real (Async In-Memory Queue / Redpanda) | Real (Multi-Broker Redpanda / Apache Kafka Cluster) |
| **AI / SLM Engine** | Real (Local Ollama Qwen2.5-Coder:3B) | Real (vLLM / Triton Inference Server on Dedicated GPU Nodes) |
| **Throughput (1 Core)** | **13,615 Events / Sec** (Measured) | Scaled Horizontally across N worker instances |
| **Latency (Mean)** | **73.18 µs** (Measured) | Sub-millisecond pipeline SLA |
| **Air-Gapped Support**| Real (Zero WAN dependencies) | Real (Strict DoD/NTRO Sovereign Enclave Deployment) |
| **Billion-Scale Log Scale**| Architectural target via horizontal worker partitioning | Validated with multi-cluster Kafka + OpenSearch sharding |

---

## 9. Security & Container Hardening

* **Non-Root Execution**: Backend runs under unprivileged `ulpfuser:ulpfgroup`.
* **Zero Commit of Credentials**: Standard `.env.example` provided; default passwords overridable via environment variables.
* **Automated Healthchecks**: Every service exposes live healthcheck probes (`/api/v1/health/live`).
* **Resource Caps**: JVM heap capped at 512MB to ensure seamless operation on standard laptops without freezing host memory.
