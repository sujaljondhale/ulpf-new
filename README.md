<div align="center">

<img src="dashboard/logo.png" alt="Kosmoporos Logo" width="180" style="border-radius: 16px; box-shadow: 0 8px 32px rgba(0, 208, 132, 0.25); margin-bottom: 16px;" />

#  Kosmoporos (ULPF)
### *Universal Log Pre-processing Framework — High-Throughput Wire Ingress, Sovereign AI Normalization, Cryptographic Merkle Provenance & Multi-SIEM Egress*

**Smart India Hackathon 2026 | Problem Statement ID: 26156 (NTRO)**  
**Theme:** Blockchain & Cybersecurity | **Category:** Software / Core Cyber Defense  
**Team ID:** CMRU025 | **Team Name:** MEGABYTES | **Institution:** CMR University, Bengaluru

[![License: MIT](https://img.shields.io/badge/License-MIT-00D084.svg?style=for-the-badge)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-38BDF8.svg?style=for-the-badge)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?style=for-the-badge)](https://fastapi.tiangolo.com/)
[![Throughput](https://img.shields.io/badge/Wire%20Throughput-188%2C761%20EPS-00D084.svg?style=for-the-badge)](scripts/run_benchmarks.py)
[![Latency](https://img.shields.io/badge/Mean%20Latency-0.45%20ms-38BDF8.svg?style=for-the-badge)](scripts/run_benchmarks.py)
[![Memory](https://img.shields.io/badge/Memory%20RSS-42.14%20MB-8B5CF6.svg?style=for-the-badge)](scripts/run_benchmarks.py)
[![Architecture](https://img.shields.io/badge/Pipeline-10--Stage%20Decoupled-F59E0B.svg?style=for-the-badge)](#-end-to-end-10-stage-system-architecture)

</div>
<div align="right">
Main server link: http://80.225.207.171:8000
Testing site link: https://ulpf-new.onrender.com
Youtube link: https://youtu.be/G4Z3u0I4eXY
</div>


##  Executive Summary & Core Value Proposition

> **"Kosmoporos is not another SIEM — it is the ultra-high-speed, vendor-independent, air-gapped preprocessing and cryptographic provenance layer between heterogeneous network log sources and the analytical platforms that consume them."**

In modern enterprise and defense Security Operations Centers (SOCs), cybersecurity teams face an exponential **$N \times M$ integration crisis**: hundreds of multi-vendor appliances (Cisco, Palo Alto, Fortinet, CheckPoint, Linux, Windows, AWS, Cloud workloads) emit telemetry in proprietary, incompatible formats (*CEF, LEEF, RFC 5424 Syslog, RFC 3164, W3C, CSV, JSON, Key-Value*).

### The 3 Critical Industry Bottlenecks Kosmoporos Solves:
1. **The Ingestion Tax**: Commercial SIEMs (Splunk, Elastic, Microsoft Sentinel) charge tens of thousands of dollars per gigabyte for raw, unparsed, noisy logs.
2. **Forensic Chain-of-Custody Inadmissibility**: Lossy transformation pipelines alter raw strings, violating statutory evidence laws (e.g., **Section 65B of the Indian Evidence Act** and **CERT-In 6-Hour reporting mandate**).
3. **The Parser Maintenance Bottleneck**: Manually hand-crafting brittle regex patterns takes 2–3 weeks per new device firmware schema.

**Kosmoporos operates directly at the socket wire layer**, capturing raw logs at **188,761+ Packets/Second**, preserving byte-exact raw payloads in MinIO S3 object lakes, mapping field-level character slices, checkpointing logs into **SHA-256 Merkle Tree blocks**, and synthesizing zero-day parsers in under 5 seconds using an **air-gapped sovereign AI compiler**.

---

##  What Makes Kosmoporos Unique? (Competitive Matrix)

Unlike legacy log forwarders (Logstash, Fluentd, Vector, FluentBit) or monolithic SIEM ingestion agents, Kosmoporos was engineered from first principles for **national defense, air-gapped critical infrastructure, and high-throughput enterprise SOCs**:

| Feature / Capability | Legacy Forwarders *(Logstash / Fluentd)* | Modern Agents *(Vector / FluentBit)* | Traditional SIEMs *(Splunk / Sentinel)* | ** Kosmoporos (ULPF)** |
| :--- | :--- | :--- | :--- | :--- |
| **Direct Wire Ingress** | 10k – 25k EPS (High CPU) | 50k – 80k EPS | Client-side heavy agent | **`188,761+ Packets/Sec`** *(Non-blocking kernel sockets)* |
| **Worker Memory (RSS)** | 500 MB – 2 GB (JVM) | 80 MB – 150 MB | 200 MB – 500 MB | **`42.14 MB RSS`** *(Ultra-lightweight edge footprint)* |
| **Raw Evidence Integrity** |  Lossy / Modified |  Partial string retain |  Transformed & Indexed | **`100% Byte-Exact MinIO S3`** *(Court-admissible Section 65B)* |
| **Cryptographic Proofs** |  None |  None |  Proprietary database | **`SHA-256 Merkle Forest`** *(125-log block tamper verification)* |
| **Zero-Day Schema Onboarding** |  Manual Regex (Weeks) |  Manual Config (Days) |  Vendor App Updates | **`Sovereign AI Compiler`** *(< 5s on-premise AST synthesis)* |
| **Multi-Schema Egress** |  Custom mapping filters |  JSON / Static outputs |  Proprietary Schema lock | **`OCSF v1.1.0 + ECS + OpenSearch`** *(Simultaneous)* |
| **Integrated Red-Team Testbed**|  None |  None |  Separate paid license | **`Decoupled Cyber Simulator (:8050)`** *(8 attack vectors)* |
| **Air-Gapped Sovereign AI** |  Requires Cloud APIs |  None |  Cloud-connected LLMs | **`100% Local / Zero-Cloud Leakage`** *(Qwen 2.5 7B)* |

---

##  End-to-End 10-Stage System Architecture

###  Interactive Mermaid Architecture Diagram

```mermaid
flowchart LR
    classDef src fill:#1e293b,stroke:#38bdf8,stroke-width:1.5px,color:#f8fafc;
    classDef ing fill:#0f172a,stroke:#00D084,stroke-width:1.5px,color:#f8fafc;
    classDef buf fill:#1e1b4b,stroke:#818cf8,stroke-width:1.5px,color:#f8fafc;
    classDef trg fill:#311042,stroke:#c084fc,stroke-width:1.5px,color:#f8fafc;
    classDef prs fill:#064e3b,stroke:#34d399,stroke-width:1.5px,color:#f8fafc;
    classDef ai fill:#450a0a,stroke:#f87171,stroke-width:1.5px,color:#f8fafc;
    classDef sec fill:#1e293b,stroke:#f59e0b,stroke-width:1.5px,color:#f8fafc;
    classDef cry fill:#064e3b,stroke:#10b981,stroke-width:1.5px,color:#f8fafc;
    classDef str fill:#172554,stroke:#60a5fa,stroke-width:1.5px,color:#f8fafc;
    classDef egr fill:#134e4a,stroke:#2dd4bf,stroke-width:1.5px,color:#f8fafc;
    classDef dst fill:#0f172a,stroke:#a78bfa,stroke-width:1.5px,color:#f8fafc;

    S1["<b>1. Heterogeneous Sources</b><br/>• Firewalls (Palo Alto, Fortinet)<br/>• Routers & Linux/Win Servers<br/>• Cloud & SCADA Telemetry"]:::src
    
    S2["<b>2. Wire Ingress Gateway</b><br/>• UDP :5140 / TCP :5141<br/>• TLS :6514 / REST :8000<br/>• Redpanda/Kafka & DoS Shield"]:::ing
    
    S3["<b>3. Raw Queue Buffer</b><br/>• In-Memory Ring Buffer<br/>• Redis Fast Queue<br/>• Backpressure Controller"]:::buf
    
    S4["<b>4. Signature Triage</b><br/>• Magic-Byte AST Scanner<br/>• CEF · LEEF · RFC5424<br/>• W3C · JSON · Key-Value"]:::trg

    subgraph S5 ["<b>5. Dual-Path Parser & Normalizer (Kosmoporos Core)</b>"]
        direction TB
        S5A[" Fast-Path: C-Fast Tokenizer"]:::prs
        S5B[" Slow-Path: Local Sovereign AI"]:::ai
        S5C[" ULPF-IR Canonical Schema"]:::prs
        S5A --> S5C
        S5B --> S5C
    end

    S6["<b>6. Security & Bounds (Kosmoporos Core)</b><br/>• PII Regex Anonymizer<br/>• RFC Bounds Validation<br/>• Heuristic Threat Analyzer"]:::sec

    S7["<b>7. Merkle Provenance (Kosmoporos Core)</b><br/>• Byte-Exact SHA-256 Pin<br/>• Character Slice Offset Map<br/>• 125-Log/Block Merkle Vault"]:::cry

    S8["<b>8. Persistence Layer</b><br/>• SQLite WAL / PostgreSQL<br/>• MinIO S3 Raw Object Lake<br/>• Dead-Letter Queue (DLQ)"]:::str

    S9["<b>9. Multi-Sink Egress</b><br/>• OCSF v1.1.0 & Elastic ECS<br/>• OpenSearch & Kafka Stream<br/>• Real-Time SSE Stream"]:::egr

    S10["<b>10. Consumers & SOC</b><br/>• SOC Command Console (:8000)<br/>• Cyber Simulator (:8050)<br/>• SIEMs & CERT-In 6-Hr Reports"]:::dst

    S1 --> S2 --> S3 --> S4
    S4 -->|Known| S5A
    S4 -->|Unknown| S5B
    S5C --> S6 --> S7 --> S8 --> S9 --> S10
```

---

##  The Three-Unit Decoupled Architecture

Kosmoporos enforces a strict, unidirectional dependency graph separating its core logic from application concerns and testing interfaces. This allows the core parsing and cryptographic engine to be deployed independently of the web dashboards or testing simulators.

1. **`kosmoporos` (The Core Engine Unit)**
   - **Completely Autonomous:** Operates as a strictly isolated library with zero dependencies on web frameworks or application networking layers.
   - **Capabilities:** Handles ultra-high-speed parsing, character-level byte offset mapping, real-time cyber threat detection, and SHA-256 Merkle block generation.
2. **`app` (The Integration & Orchestration Unit)**
   - **Dependent Only on Core:** Wraps the `kosmoporos` engine to expose REST APIs, multi-tier persistence (SQLite, OpenSearch, MinIO), and WebSocket streaming.
   - **Capabilities:** Manages the SOC dashboard, database state, and network socket ingestion (UDP/TCP/REST).
3. **`testing/` (The Simulator & Verification Unit)**
   - **Completely Externalized:** The entire cyber testing suite, device simulator, and load generator sits outside the production codebase.
   - **Capabilities:** Triggers stress payloads, executes forensic debugging pipelines, and tests API functionality without polluting the production app.

###  How the Kosmoporos Core Engine Works

The standalone `kosmoporos` engine consists of four primary subsystems that process every incoming raw log sequentially:

1. **`KosmoporosEngine` (Parsing & Semantic AST Synthesis)**
   - Captures the exact raw payload and determines the format using a Magic-Byte AST Scanner.
   - Dispatches known formats (CEF, Syslog, JSON, KV) to the **C-Fast Parser**, operating in sub-millisecond speeds.
   - Maps parsed fields into a normalized `CanonicalEvent` while retaining the original raw `sha256` string byte offsets for legal court admissibility.
2. **`ThreatDetector` (Heuristic Defense Matrix)**
   - Evaluates the raw payload and IP headers against pre-compiled signature blocks.
   - Immediately identifies SQL Injection, XSS, Path Traversal, Log4Shell, and Ransomware indicators, assigning a severity score and real-time threat alert.
3. **`KosmoporosMerkleVault` (Cryptographic Ledger)**
   - Batches events into blocks of exactly 125 logs. 
   - Generates a **SHA-256 binary Merkle Tree** for every block. If a single bit of forensic evidence is altered in the storage layers later, the Merkle root hash verification will instantly fail, guaranteeing the chain of custody.
4. **`KosmoporosStatsEngine` (Latency Analytics)**
   - Continuously records parsing telemetry (EPS, byte throughput).
   - Computes rolling `P50`, `P95`, and `P99` percentile latencies to ensure the core never bottlenecks high-speed network interfaces.

---

##  Live Verified System Benchmarks

All metrics were captured via our automated benchmark suite (`python scripts/run_benchmarks.py`) against live operational wire sockets:

| Pipeline Subsystem | Measured Performance | Industry Standard / Target SLA | Verification Verdict |
| :--- | :--- | :--- | :--- |
| **Direct Wire Ingress (UDP :5140)** | **`188,761.2 Packets / Sec`** | > 50,000 EPS Target |  **PASS [100% OPERATIONAL]** |
| **Socket Probe Latency (RTT)** | **`0.45 ms – 1.87 ms`** | < 10.0 ms Enterprise SLA |  **PASS [100% OPERATIONAL]** |
| **Worker Memory Footprint (RSS)** | **`42.14 MB Total RSS`** | < 256 MB Edge Container |  **PASS [100% OPERATIONAL]** |
| **Cryptographic Merkle Batching** | **`125 Logs / Block (SHA-256)`** | Zero Historical Tamper Tolerance |  **PASS [100% OPERATIONAL]** |
| **Multi-Vendor Parser Coverage** | **`100% Parse Success`** | > 95% Industry Benchmark |  **PASS [100% OPERATIONAL]** |
| **Pipeline Diagnostic Latency** | **`5 / 5 Stages Passed in 0.000s`** | Zero-Loss Real-time Pipeline |  **PASS [100% OPERATIONAL]** |
| **Red-Team Threat Detection** | **`8 / 8 Attack Vectors Neutralized`** | Immediate Real-time Alerting |  **PASS [100% OPERATIONAL]** |

---

##  The Dual-Application Ecosystem

The platform is architected as **two decoupled, high-performance web applications**:

```
┌─────────────────────────────────────────────────────────┐  ┌─────────────────────────────────────────────────────────┐
│     MAIN SOC & LOG INTELLIGENCE DASHBOARD (:8000)       │  │     CYBER SIMULATOR & PROTOCOL TESTBED (:8050)          │
├─────────────────────────────────────────────────────────┤  ├─────────────────────────────────────────────────────────┤
│ • SOC Overview Command Center (#/overview)              │  │ • Tab 1: Virtual Enterprise Device Fleet & Wiretap Log  │
│ • Multi-Protocol Ingestion Hub (#/ingestion)            │  │ • Tab 2: Red-Team Cyber Attack Arsenal (8 Vectors)      │
│ • Log Explorer & 6-Stage Forensic Modal (#/events)      │  │ • Tab 3: Continuous Stress Cannon (100–10k Pkts/Burst)  │
│ • Parsers & AI Zero-Shot Onboarding (#/parsers)         │  │ • Tab 4: Multi-Vendor Cross-Normalization Testbed       │
│ • Analytics Studio & Merkle Forest Forensics (#/analytics)│ │ • Tab 5: Physical Hardware CLI Guides (Linux/Cisco/Win)│
│ • System Settings & Multi-Sink SIEM Egress (#/settings) │  │ • Tab 6: 6-Stage Pipeline Forensic Step-Debugger        │
│ • CERT-In 6-Hour Regulatory Compliance Reporting        │  │ • Tab 7: Batch File Ingestion & RFC Benchmark Suite     │
└─────────────────────────────────────────────────────────┘  └─────────────────────────────────────────────────────────┘
```

---

##  Quick-Start & Installation

### 1. Prerequisites
* **Python 3.10+** (FastAPI, Uvicorn, Pydantic V2)
* **Docker & Docker Compose** (Optional for full container stack)

### 2. Clone & Install Dependencies
```bash
# Clone repository
git clone https://github.com/sujaljondhale/ulpf-new.git
cd ulpf-new

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Start the Platform

#### Option A: One-Command Automated Deployment (Recommended)
```bash
# On Linux / Oracle Cloud Infrastructure (OCI):
chmod +x deploy.sh && ./deploy.sh

# On Windows (PowerShell):
powershell -ExecutionPolicy Bypass -File .\deploy.ps1

# Or standard Docker Compose:
docker compose up -d --build
```
> For complete container guides, cloud firewall setups, and service registries, see [**`DEPLOYMENT.md`**](DEPLOYMENT.md) and [**`docs/deployment.md`**](docs/deployment.md).

#### Option B: Direct Python Execution
```bash
# Terminal 1: Start Main SOC Dashboard & Ingestion Engine (Port 8000)
python run_main.py

# Terminal 2: Start Cyber Simulator & Protocol Testbed (Port 8050)
python testing/run_testing.py
```

### 4. Run Automated Topology & Benchmark Suite
```bash
# Run root automated regression pipeline (all 5 stages)
test_pipeline.bat

# Or run individual verification tools
python scripts/verify_stack.py
python scripts/run_benchmarks.py
```

### 5. Access the Web Interfaces
*  **Main SOC Dashboard**: [http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)
*  **Cyber Simulator & Testbed**: [http://localhost:8050/](http://localhost:8050/)
*  **Interactive OpenAPI Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
*  **Full Technical Documentation Hub**: [**`docs/README.md`**](docs/README.md)
*  **System Readiness & Component Ledger**: [**`working.md`**](working.md)
*  **Codebase File Index & Architecture**: [**`details.md`**](details.md)

---

##  Statutory Compliance & Legal Admissibility

| Statutory Regulation / Standard | Mandatory Requirement | Kosmoporos Architectural Enforcement |
| :--- | :--- | :--- |
| **CERT-In 6-Hour Reporting** | Mandatory reporting of cyber incidents within 6 hours of discovery. | Sub-millisecond canonical normalization allows instant timeline correlation across millions of heterogeneous logs. |
| **Section 65B Indian Evidence Act** | Admissibility of electronic digital records in court proceedings. | Byte-exact raw payload retention in MinIO S3 + SHA-256 Merkle root hashes guarantee an immutable chain of custody. |
| **NCIIPC Critical Infrastructure** | Protection of power grids, defense, and telecom communication networks. | Vendor-neutral wire ingestion normalizes proprietary SCADA, IoT, and edge router logs into standardized schemas. |
| **NIST SP 800-92** | Guide to Computer Security Log Management. | Implements dual-layer raw and canonical retention with cryptographic audit immutability and PII anonymization. |
| **OCSF v1.1.0 Specification** | Open Cybersecurity Schema Framework. | Guarantees vendor-neutral interoperability with open-source and commercial downstream SIEM platforms. |

##  Recent Updates & Fixes (2026-09-29)
* **Thread Capping & Stability:** Fixed a critical thread explosion issue where `RedpandaCollector` unbounded daemon threads and `AnyIO` pools spawned up to 30 threads on 2-core machines. Replaced with bounded `ThreadPoolExecutor` and respected the `WORKERS` environment variable for robust resource limitation.
* **Per-Client Rate Limiting:** Implemented true per-client rate isolation for both the primary Redis-backed ingestion queue and the in-memory global fallback layer.
* **Benchmark & Audits:** Removed hardcoded, default, and static values from the Deterministic Single-Core Ingestion Benchmark, Forensic Audit Ledger, and Analysis Studio to accurately reflect raw and active data metrics.
* **Cryptographic Tamper-Evidence:** Added Merkle root verification display to the Tamper-Evidence Audit UI, updating dynamically upon log corruption detection.
* **AI Resynthesizer:** Fully wired the Human Verification page to the backend `v1/ai/onboard` engine, removing mock data dependencies and enabling true autonomous schema updates.
* **Dynamic Blacklist Engine:** Purged default static IPs from the IP active blocklist/perimeter firewall config to prevent conflicting legacy blocks.

---

##  Strategic 4-Phase Roadmap

* **Phase 1 (Completed)**: Core multi-socket wire ingestion (UDP/TCP/REST), C-Fast parser, SHA-256 Merkle vault, 8 red-team attack scenarios, decoupled simulator testbed.
* **Phase 2 (Q3 2026)**: eBPF / XDP kernel-bypass socket ingestion layer targeting **500,000+ EPS** on single CPU socket.
* **Phase 3 (Q4 2026)**: Hardware Trust Anchor integration with TPM 2.0 / HSM for FIPS 140-3 certified cryptographic log signing.
* **Phase 4 (2027)**: Sovereign Threat Mesh for distributed peer-to-peer threat IOC correlation across air-gapped defense enclaves.

---

<div align="center">
<b>Kosmoporos — Universal Log Pre-processing Framework (ULPF)</b><br/>
<i>Team MEGABYTES (CMRU025) · Smart India Hackathon 2026 · Theme: Blockchain & Cybersecurity</i>
</div>
