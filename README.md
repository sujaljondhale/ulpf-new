# Universal Log Pre-processing Framework (ULPF)

**SIH Problem ID:** SIH 26156 (NTRO)  
**Theme:** Cybersecurity & High-Throughput Log Pre-processing  
**Status:** Phase 7 — Docker + Persistence + Deployment Hardening

---

## 1. What is ULPF?

**ULPF (Universal Log Pre-processing Framework)** is a vendor-independent preprocessing and normalization layer positioned between heterogeneous enterprise log sources and downstream analytics systems (OpenSearch, OCSF, ECS, SIEMs).

It preserves raw evidence, creates a common internal event representation (**ULPF-IR**), maintains cryptographic field-level provenance, assists onboarding of unknown formats with local AI, and provides standardized outputs to multiple downstream consumers.

---

## 🚀 One-Command Containerized Deployment

The complete ULPF platform (API, Dashboard, MinIO Raw Storage, OpenSearch Normalized Index, SQLite Metadata) runs with a single command:

```bash
docker compose up --build
```

### Automation Scripts

| Action | Linux / macOS | Windows | Description |
| :--- | :--- | :--- | :--- |
| **Start Stack** | `./scripts/start.sh` | `scripts\start.bat` | Starts all containers, waits for health, prints URLs |
| **Stop Stack** | `./scripts/stop.sh` | `scripts\stop.bat` | Gracefully stops services preserving volumes |
| **Clean Reset** | `./scripts/reset.sh` | `scripts\reset.bat` | Wipes volumes (`docker compose down -v`) and boots clean |
| **Health Check** | `./scripts/health.sh` | `scripts\health.bat` | Inspects real live health probes across subsystems |
| **Run SIH Demo** | `./scripts/demo.sh` | `scripts\demo.bat` | Ingests multi-vendor logs and verifies pipeline |

---

## 🌐 Platform URLs

* 🏆 **SIH Demo Control Center**: [http://localhost:8000/dashboard/index.html#/sih-demo](http://localhost:8000/dashboard/index.html#/sih-demo)
* 📊 **Main Web Dashboard**: [http://localhost:8000/dashboard/index.html#/overview](http://localhost:8000/dashboard/index.html#/overview)
* 💻 **Client Event Generator**: [http://localhost:8000/dashboard/client_app.html](http://localhost:8000/dashboard/client_app.html)
* 📖 **Interactive Swagger OpenAPI**: [http://localhost:8000/docs](http://localhost:8000/docs)
* 🔌 **REST API Root**: [http://localhost:8000/api/v1](http://localhost:8000/api/v1)
* 🪣 **MinIO S3 Object Console**: [http://localhost:9001](http://localhost:9001) *(User: `ulpf_admin`, Pass: `ulpf_password_2026`)*
* 🔍 **OpenSearch Node**: [http://localhost:9200](http://localhost:9200)

---

## 3. How Does It Work?

```text
                  MANY SOURCES
       Firewall     Router     VPN     WAF
          │           │         │       │
          ↓           ↓         ↓       ↓
       Syslog        JSON      CEF     LEEF
          │           │         │       │
          └───────────┼─────────┴───────┘
                      ↓
                     ULPF
      (Raw Preservation ➔ Detect ➔ Parse ➔ Validate)
                      ↓
                   ULPF-IR
     (Canonical Intermediate Representation & Provenance)
                      ↓
             ┌────────┼────────┐
             ↓        ↓        ↓
           OCSF      ECS      SIEM / OpenSearch

      Preserve → Understand → Normalize → Trace → Deliver
```

1. **Preserve**: The incoming log is hashed with SHA-256 and preserved byte-for-byte in MinIO S3 object storage before transformation.
2. **Understand**: The format is classified deterministically (confidence ≥ 0.95) and structured tokens are extracted.
3. **Normalize**: Vendor fields are mapped to canonical semantic security taxonomy (**ULPF-IR v1.0**) and validated with Pydantic V2.
4. **Trace**: Field-level provenance is recorded, linking normalized attributes back to raw byte offsets and source keys.
5. **Deliver**: The canonical event is indexed in OpenSearch, persisted in SQLite, and exported simultaneously to OCSF v1.1.0, ECS v8.x, and downstream SIEM sinks.

---

## 4. Multi-Tier Persistence Architecture

* **MinIO (`ulpf-raw` bucket)**: Persistent raw log evidence store. Every incoming log is hashed with SHA-256 and stored verbatim.
* **OpenSearch (`ulpf-events` index)**: High-performance searchable canonical representation.
* **SQLite (`storage/ulpf_metadata.db`)**: Persistent database for parsers, log sources, audit trails, and restart recovery.
* **Restart Resilience**: After `docker compose restart`, all previously ingested events and configurations remain intact and searchable.

---

## ⚡ Performance Benchmark (10,000 Events)

Reproducible CLI benchmark run: `python benchmark.py --events 10000`

* **Throughput**: **13,615.15 Events / Second (EPS)** (Single CPU Core)
* **Processing Latency (P50 Median)**: **70.00 microseconds (0.0700 ms)**
* **Processing Latency (Mean)**: **73.18 microseconds (0.0732 ms)**
* **Processing Latency (P95)**: **89.20 microseconds (0.0892 ms)**
* **Processing Latency (P99)**: **142.80 microseconds (0.1428 ms)**
* **Parse Success Rate**: **100.00%** (10,000 / 10,000, 0 errors)
* **Process Memory Delta**: **+0.54 MB**

---

## 🔒 Security & Defense Air-Gap Guarantees

* **100% Offline & Sovereign**: Operates strictly within air-gapped secure enclaves with zero external cloud telemetry, zero API keys, and zero tracking.
* **Tamper-Evident Provenance**: Recalculates SHA-256 hash on-demand against stored raw messages to detect any modification.
* **Active Threat Defense**: Includes real-time IP source blocking to mitigate DDoS log flooding and rogue injection attacks.
* **Non-Root Execution**: Runs under unprivileged `ulpfuser` in container environment.

---

## 📁 Technical Documentation Index

* 📘 [Architecture Specification](docs/architecture.md) — Comprehensive technical design & component breakdown
* 🚢 [Deployment & Operations Guide](docs/deployment.md) — Bare-metal, Docker Compose, and air-gapped setup
* 🔄 [Data Flow & Lifecycle](docs/data-flow.md) — Byte-level trace from wire ingress to downstream sinks
* 🌐 [REST API Reference](docs/api.md) — OpenAPI endpoint schemas, payloads, and response status codes
* 🎬 [3-Minute Live Jury Script](docs/demo-script.md) — Presenter script and timing guide for SIH evaluation
* 📊 [Performance Benchmark Report](docs/benchmark.md) — Complete methodology, latency percentiles, and hardware baseline
* ❓ [Top 15 Jury Q&A Guide](docs/judge-questions.md) — Direct, technically rigorous answers to evaluation questions
* 🛡️ [Engineering Scope & Limitations](docs/limitations.md) — Honest evaluation of prototype boundaries and production roadmap

---

## 👥 Authors & Acknowledgments

* **Project**: Universal Log Pre-processing Framework (ULPF)
* **Problem Statement**: SIH 26156 (NTRO)
* **License**: Apache 2.0 (Open Source for National Security Research)
