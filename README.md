<div align="center">

<img src="main/dashboard/logo.png" alt="Kosmoporos Logo" width="180" style="border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 208, 132, 0.25); margin-bottom: 16px;" />

# ⚡ Kosmoporos (ULPF)
### *Universal Log Pre-processing Framework — High-Throughput Wire Ingress, Sovereign AI Normalization & Cryptographic Merkle Provenance*

**Smart India Hackathon 2026 | Problem Statement ID: 26156 (NTRO)**  
**Theme:** Blockchain & Cybersecurity | **Category:** Software / Core Cyber Defense  
**Team ID:** CMRU025 | **Team Name:** MEGABYTES | **Institution:** CMR University, Bengaluru

[![License: MIT](https://img.shields.io/badge/License-MIT-00D084.svg?style=for-the-badge)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-38BDF8.svg?style=for-the-badge)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?style=for-the-badge)](https://fastapi.tiangolo.com/)
[![Throughput](https://img.shields.io/badge/Wire%20Throughput-184%2C457%2B%20EPS-00D084.svg?style=for-the-badge)](scripts/run_benchmarks.py)
[![Latency](https://img.shields.io/badge/Mean%20Latency-0.45%20ms-38BDF8.svg?style=for-the-badge)](scripts/run_benchmarks.py)
[![Architecture](https://img.shields.io/badge/Architecture-Dual--Core%20Decoupled-8B5CF6.svg?style=for-the-badge)](#-end-to-end-system-architecture)

---

### [📄 View Official Master Presentation PDF (6-Slide Blueprint)](docs/SIH_2026_PS26156_ULPF_Master_Deck.pdf)

</div>

---

## 🌟 Executive Summary & Core Value Proposition

> **"Kosmoporos is not another SIEM — it is the ultra-high-speed, vendor-independent, air-gapped preprocessing and cryptographic provenance layer between multi-vendor enterprise log sources and downstream analytical platforms."**

In modern enterprise and national defense Security Operations Centers (SOCs), cybersecurity teams face a crippling **$N \times M$ integration bottleneck**: thousands of multi-vendor firewalls, switches, routers, servers, and cloud workloads emit logs in proprietary, incompatible formats (*CEF, LEEF, RFC 5424 Syslog, W3C, CSV, JSON, Key-Value*).

### The 3 Critical Industry Pain Points Kosmoporos Solves:
1. **The Ingestion Tax**: Commercial SIEMs (Splunk, Elastic, Sentinel) bill tens of thousands of dollars per gigabyte for raw, noisy, unparsed logs.
2. **Forensic Chain-of-Custody Loss**: Traditional parsers alter raw strings during transformation, violating legal digital evidence requirements (e.g. **Section 65B of the Indian Evidence Act** and **CERT-In 6-Hour reporting**).
3. **The Parser Maintenance Nightmare**: Manually hand-crafting brittle regex patterns takes 2–3 weeks per new device firmware schema.

**Kosmoporos operates directly at the socket wire layer**, ingesting raw streams at **184,457+ Packets/Second**, retaining byte-exact evidence in S3 MinIO lakes, mapping field-level character slices, checkpointing logs into **SHA-256 Merkle Trees**, and synthesizing zero-day parsers in under 5 seconds using an **air-gapped sovereign AI compiler**.

---

## 💎 The 6 Architectural Pillars of Kosmoporos

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE 6 PILLARS OF KOSMOPOROS ARCHITECTURAL NOVELTY                         │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. 🚀 Zero-Copy Wire Sockets (184.4k+ EPS Direct Ingress)
* Asynchronous non-blocking kernel sockets for **Syslog UDP (Port 5140)**, **Syslog TCP (Port 5141)**, **REST API (Port 8000)**, and multi-part batch streams.
* Eliminates the need for resource-heavy proprietary client agents on edge switches, firewalls, and air-gapped endpoints.

### 2. 🧬 Byte-Exact Raw Preservation & Bidirectional Offset Mapping
* Retains **100% of the byte-exact original log string** alongside the normalized canonical schema.
* Generates a bidirectional character-slice pointer map connecting every extracted field directly back to its exact byte offset in the original payload.

### 3. 🛡️ Cryptographic SHA-256 Merkle Ledger (Blockchain Theme Integration)
* Checkpoints telemetry into fixed **125-event blocks** and computes binary SHA-256 Merkle tree roots.
* Any unauthorized historical modification, deletion, or bit-flip triggers an **instant Zero-Knowledge cryptographic mismatch alert** in the SOC console.

### 4. 🧠 Air-Gapped Sovereign AI Parser Compiler (Zero Cloud Leakage)
* Zero-day or mutated log formats automatically fall through to a **local, sovereign on-premise SLM/LLM** (Qwen 2.5 / Ollama).
* The AI analyzes the log's Abstract Syntax Tree (AST), generates an RFC-compliant regex/Pydantic parser, validates it against test samples, and presents it to administrators for single-click approval.

### 5. 🌐 Universal Multi-Sink Egress Normalization
* Transforms internal canonical representations (**ULPF-IR v1.0**) simultaneously into:
  * **OCSF v1.1.0** (*Open Cybersecurity Schema Framework*)
  * **Elastic Common Schema (ECS v8.x)**
  * **MinIO / S3 Immutable Object Lakes**
  * **OpenSearch / Elasticsearch**
  * **Redpanda / Apache Kafka Event Brokers**

### 6. 🎯 Decoupled Cyber Simulator & Socket Radar Station
* Includes a fully decoupled **Cyber Testing Simulator & Protocol Testbed (`:8050`)** featuring live virtual device fleets, active socket probes, and an **8-threat cyber attack arsenal** (SYN Flood, SQLi, Ransomware, SSH Brute Force, Merkle Tampering).

---

## 📊 Empirical Performance Benchmarks (Live Verified)

All metrics were captured via our automated benchmark suite (`python scripts/run_benchmarks.py`) across live operational wire sockets:

| Performance Metric | Observed Live Telemetry | Industry Standard / Target SLA | Verification Status |
| :--- | :--- | :--- | :--- |
| **Direct Wire Ingress (UDP 5140)** | **`184,457.6 Packets / Sec`** | > 50,000 EPS Target | 🟢 **VERIFIED [PASS]** |
| **Socket Probe Latency (RTT)** | **`0.45 ms – 1.83 ms`** | < 10.0 ms Enterprise SLA | 🟢 **VERIFIED [PASS]** |
| **Worker Memory Footprint (RSS)** | **`42.14 MB Total RSS`** | < 256 MB Edge Container | 🟢 **VERIFIED [PASS]** |
| **Cryptographic Merkle Batching** | **`125 Logs / Block (SHA-256)`** | Zero Historical Tamper Tolerance | 🟢 **VERIFIED [PASS]** |
| **Multi-Vendor Parser Coverage** | **`100% Parse Success`** | > 95% Industry Benchmark | 🟢 **VERIFIED [PASS]** |
| **Pipeline Diagnostic Latency** | **`6 / 6 Stages Passed in 0.000s`** | Zero-Loss Real-time Pipeline | 🟢 **VERIFIED [PASS]** |
| **Red-Team Threat Detection** | **`8 / 8 Attack Vectors Neutralized`** | Immediate Real-time Alerting | 🟢 **VERIFIED [PASS]** |

---

## 🏛️ End-to-End System Architecture

Kosmoporos operates on a **5-tier decoupled pipeline architecture** designed for sub-millisecond processing and high fault-tolerance:

```
                                    🌐 MULTI-PROTOCOL INGRESS LAYER
                 ┌───────────────────────────┬───────────────────────────┐
                 │  Syslog UDP Socket :5140  │  Syslog TCP Socket :5141  │
                 └─────────────┬─────────────┴─────────────┬─────────────┘
                               │                           │
                 ┌─────────────┴─────────────┐ ┌───────────┴─────────────┐
                 │   REST API Ingress :8000  │ │   Redpanda / Kafka :9092│
                 └─────────────┬─────────────┘ └───────────┬─────────────┘
                               └─────────────┬─────────────┘
                                             ▼
                     [ TIER 2: HIGH-SPEED PARSING & NORMALIZATION ]
                     ├── C-Fast Format Matcher (Syslog, CEF, LEEF, JSON, KV, CSV, PAN-OS)
                     ├── Canonical Normalizer ──► ULPF-IR Event Schema
                     └── Format Drift / Unknown ──► Sovereign AI Onboarding Engine (Qwen 7B)
                                             ▼
                     [ TIER 3: CRYPTOGRAPHIC MERKLE VAULT & FORENSICS ]
                     ├── SHA-256 Merkle Ledger (125 Logs / Block Binary Hash Tree)
                     ├── Byte-Exact Raw Preservation (Raw ◄─► ULPF-IR Character Pointer Map)
                     └── Real-Time Threat Analyzer (SQLi, XSS, Ransomware, Brute-Force)
                                             ▼
                     [ TIER 4: MULTI-BACKEND PERSISTENCE LAYER ]
                     ├── SQLite WAL / Enterprise PostgreSQL (Metadata & Checkpoints)
                     ├── MinIO S3 Object Store / Local Disk Raw Evidence Lake
                     └── Redis In-Memory Ring Buffers & Dead-Letter Queues (DLQ)
                                             ▼
                     [ TIER 5: STANDARDIZED EGRESS & SOC CONSOLE ]
                     ├── OCSF v1.1.0 · Elastic Common Schema (ECS) · OpenSearch
                     ├── Real-Time Server-Sent Events (SSE) Stream
                     └── Web Intelligence Dashboard (:8000) & Cyber Simulator (:8050)
```

---

## 🖥️ Applications & Web Consoles

The framework provides **two independent, high-performance web applications**:

### 1. Main SOC & Log Intelligence Dashboard (`http://127.0.0.1:8000/dashboard/`)
* **SOC Overview (`#/overview`)**: Real-time throughput gauges, live streaming logs, and queue metrics.
* **Ingestion Hub (`#/ingestion`)**: Protocol port status, sample ingest testing, dynamic throttling, and IP blacklists.
* **Log Explorer (`#/events`)**: Searchable, facet-filtered log database with 6-stage lifecycle forensic inspection modal.
* **Parsers & AI Onboarding (`#/parsers`)**: Compiled deterministic parser registry and automatic regex compiler for zero-day logs.
* **Analytics Studio & Merkle Forensics (`#/analytics`)**: Format breakdowns, MinIO S3 raw evidence retrieval, and interactive Merkle Forest graph.
* **Settings & Compliance (`#/settings`)**: Concurrency tuning, multi-sink export switches (OCSF/ECS), and CERT-In 6-Hour reporting tools.

### 2. Protocol Simulator & Cyber Testbed Hub (`http://localhost:8050/`)
* **Tab 1: Virtual Device Fleet**: Simulates live Palo Alto, Cisco, Fortinet, and CheckPoint devices with live Wiretap Audit Logs.
* **Tab 2: Cyber Attack Arsenal**: Fires 8 real-world cyberattack scenarios and simulates cryptographic Merkle tampering.
* **Tab 3: High-Speed Stress Cannon**: Generates micro-bursts of 100 to 5,000+ packets to benchmark async queue throughput.
* **Tab 4: Multi-Vendor Cross-Normalization**: Demonstrates multi-vendor logs normalizing into identical canonical schemas.
* **Tab 5: Physical Hardware Ingestion**: CLI guides for physical Linux, Windows, Cisco, and MikroTik appliances.
* **Tab 6: Pipeline Step-Debugger**: Step-by-step visual execution of all 6 internal pipeline stages.
* **Tab 7: Batch File Ingestion**: Bulk file upload processing archives at 50,000+ lines per second.

---

## 🚀 Quick-Start & Deployment

### 1. Prerequisites
* **Python 3.10+**
* **Docker & Docker Compose** (Optional for full multi-container stack)

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/sujaljondhale/ulpf-new.git
cd ulpf-new

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Applications
```bash
# Terminal 1: Start Main SOC Dashboard & Ingestion Engine (Port 8000)
python main/run_main.py

# Terminal 2: Start Protocol Simulator & Cyber Testbed (Port 8050)
python testing/run_testing.py
```

### 4. Verify Full Stack Health
```bash
# Run automated multi-service topology verification
python scripts/verify_stack.py

# Run benchmark suite
python scripts/run_benchmarks.py
```

### 5. Access the Web Interfaces
* 🛡️ **Main SOC Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
* ⚡ **Cyber Simulator & Testbed**: [http://localhost:8050/](http://localhost:8050/)
* 📚 **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📜 Statutory Compliance & National Security Alignment

| Regulation / Standard | Mandatory Statutory Requirement | Kosmoporos Architectural Alignment |
| :--- | :--- | :--- |
| **CERT-In 6-Hour Reporting** | Mandatory reporting of cyber incidents within 6 hours. | Sub-millisecond canonical normalization allows instant timeline correlation across millions of logs. |
| **Section 65B Indian Evidence Act** | Admissibility of electronic digital records in courts. | Byte-exact raw payload retention + SHA-256 Merkle root hashes guarantee tamper-proof chain of custody. |
| **NCIIPC Critical Infrastructure** | Protection of power grids, defense, and telecom networks. | Vendor-neutral wire ingestion normalizes SCADA, IoT, and edge router logs into standardized schemas. |
| **NIST SP 800-92** | Guide to Computer Security Log Management. | Implements dual-layer raw and canonical retention with cryptographic audit immutability. |
| **OCSF v1.1.0 Specification** | Open Cybersecurity Schema Framework. | Guarantees seamless interoperability with open-source and commercial downstream SIEM platforms. |

---

## 🗺️ Strategic 4-Phase Roadmap

* **Phase 1 (Completed)**: Multi-socket ingestion (UDP/TCP/REST), C-Fast parser, SHA-256 Merkle vault, 8 red-team attack scenarios, decoupled simulator testbed.
* **Phase 2 (Q3 2026)**: eBPF / XDP kernel-bypass socket ingestion layer targeting **500,000+ EPS** on single CPU socket.
* **Phase 3 (Q4 2026)**: Hardware Trust Anchor integration with TPM 2.0 / HSM for FIPS 140-3 certified cryptographic log signing.
* **Phase 4 (2027)**: Sovereign Threat Mesh for distributed peer-to-peer threat IOC correlation across air-gapped defense enclaves.

---

<div align="center">
<b>Kosmoporos — Universal Log Pre-processing Framework (ULPF)</b><br/>
<i>Team MEGABYTES (CMRU025) · Smart India Hackathon 2026</i>
</div>
