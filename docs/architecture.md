# ULPF System Architecture

**Universal Log Pre-processing Framework (ULPF)**  
*SIH 26156 — National Technical Research Organisation (NTRO)*

---

## 1. Executive Summary & Design Philosophy

Perimeter network devices (Firewalls, Routers, IDPS, VPN Concentrators, WAFs) generate multi-gigabyte streams of heterogeneous logs in inconsistent formats: Syslog RFC 3164/5424, ArcSight CEF, IBM QRadar LEEF, Key=Value (Fortinet/CheckPoint), Structured JSON, and unstructured vendor proprietary formats.

Existing SIEM architectures face three critical bottlenecks:
1. **Format Lock-in & Heavy Collectors**: Fragile pipelines (Logstash/Fluentd) requiring high CPU/JVM overhead and complex regex configurations.
2. **Loss of Forensic Evidence**: Normalization transforms often discard raw headers or modify original strings, compromising legal chain of custody.
3. **Handling of Novel Formats**: Unknown log formats are dropped or logged as unparsed raw text without automated schema inference.

**ULPF solves this by decoupling ingestion, normalization, and semantic onboarding into a 100% deterministic, high-throughput pre-processing pipeline backed by an offline AI Parser Studio.**

Furthermore, ULPF strictly decouples the **Core Production Server (`main/`, port 8000)** from the **Testing Simulator Studio (`testing/`, port 8050)** to guarantee that synthetic stress testing never interferes with production telemetry.

---

## 2. High-Level System Architecture Diagram

```
                        [ PERIMETER NETWORK LOG SOURCES ]
           (Firewalls, Routers, VPNs, Cloud Functions, Linux/Windows Hosts)
                                         │
       ┌─────────────────────────────────┼─────────────────────────────────┐
       ▼                                 ▼                                 ▼
[ Syslog UDP :5140 ]             [ Syslog TCP :5141 ]             [ HTTP REST :8000 ]
(RFC 3164 / 5424)               (RFC 5424 Stream)                (POST /api/v1/ingest)
       │                                 │                       (POST /api/v1/upload)
       └─────────────────────────────────┬─────────────────────────────────┘
                                         │
                                         ▼
                         [ 1. RAW EVIDENCE INTEGRITY SEAL ]
                         ├── Compute SHA-256 Digest on Raw Bytes
                         ├── Assign UUID / Event ID (ULPF-2026-xxxx)
                         └── Write to Immutable Raw Store (storage/raw/)
                                         │
                                         ▼
                         [ 2. FOUR-STAGE FORMAT DETECTOR ]
                         ├── Single-Pass Signature & Regex Analysis
                         ├── Confidence Scorer (0.0 to 1.0)
                         └── Fast Dispatch Lookup
                                         │
                      ┌──────────────────┴──────────────────┐
                      ▼                                     ▼
          [ Known Format (≥ 0.70) ]             [ Unknown Format (< 0.70) ]
                      │                                     │
                      ▼                                     ▼
             [ 3. CORE PARSERS ]               [ UNKNOWN QUARANTINE QUEUE ]
             ├── JSON (RFC 8259)               ├── storage/ulpf_unknown.db
             ├── Syslog (RFC 3164/5424)        └── AI Parser Studio (Offline SLM)
             ├── CEF (ArcSight V0-V25)             ├── Auto-Regex Generation
             ├── LEEF (QRadar V1-V2)               ├── Human Validation Diff
             └── Key=Value (Fortinet/Cisco)        └── Dynamic Parser Registry
                      │                                     │
                      └──────────────────┬──────────────────┘
                                         │
                                         ▼
                        [ 4. ULPF-IR CANONICAL ENGINE ]
                        ├── Taxonomy Mapping (Source, Dest, Device, Action)
                        ├── Pydantic V2 Schema Validation
                        └── Field-Level Provenance & Lineage Tracker
                                         │
                                         ▼
                        [ 5. DOWNSTREAM DISPATCH SINK ]
                        ├── SQLite Event Ledger (storage/ulpf_events.db)
                        ├── OpenSearch Analytics (:9200) & Dashboards (:5601)
                        ├── Redpanda / Kafka High-Speed Buffer (:9092)
                        └── MinIO S3 Forensic Object Archive (:9000)
```

---

## 3. The Decoupled Testing Simulator Studio (`testing/`, Port 8050)

To provide enterprise-grade verification without polluting production databases, ULPF runs an independent testing simulator on port `8050`:

```
   [ ULPF TESTING SIMULATOR HUB (Port 8050) ]
   ├── Tab 1: Virtual Devices (Palo Alto, Fortinet, Cisco, Linux, Windows)
   ├── Tab 2: Cyber Threat & Attack Arsenal (6 Cyber Attack Scenarios)
   ├── Tab 3: High-Throughput Load Generator (Stress bursts & EPS radar)
   ├── Tab 4: Server Health & Port Radar (Socket probes across 8000/5140/5141)
   ├── Tab 5: Real Device Guides, Settings & Transmission Audit Ledger
   ├── Tab 6: Automated Test Pipeline Runner (test_pipeline.bat web runner)
   └── Tab 7: Multi-Transport File Uploader Lab (HTTP, UDP, TCP, File Drop)
                       │
                       ▼
       [ TARGET MACHINE CONTROLLER & SMART URL PARSER ]
       ├── Target IP / Host (e.g. 192.168.1.50, ulpf.cloud, 127.0.0.1)
       ├── Protocol Scheme (http:// or https://)
       ├── Configurable API Port, Syslog UDP, and TCP Ports
       └── Backend Proxy (/api/test/target-status) Bypassing Browser CORS
                       │
                       ▼ (Socket Dispatches)
   [ PRODUCTION SERVER (Local Machine, Remote LAN, Docker, or Cloud VM) ]
```

---

## 4. Core Architectural Subsystems

### 4.1 Raw Ingestion & Tamper-Evident Integrity
* **Module**: `main/app/collector/`, `main/app/models/raw.py`
* **Invariant**: The original raw string is **never modified, truncated, or re-encoded**.
* **Integrity Guarantee**: A SHA-256 cryptographic digest is computed directly across the raw byte payload upon socket arrival. Field-level provenance retains references to the exact slice and raw hash, establishing verifiable chain of custody for digital forensics.
* **Storage Location**: `main/storage/raw/ULPF-YYYYMMDD-HHMMSS-xxxx.raw`.

### 4.2 Deterministic Format Detection
* **Module**: `main/app/detector/format_detector.py`
* **Throughput**: Single-pass regex evaluation with zero external network lookups.
* **Supported Formats**:
  * `JSON`: RFC 8259 JSON validation (`confidence: 1.0`)
  * `CEF`: ArcSight standard header `CEF:\d+\|` (`confidence: 0.99`)
  * `LEEF`: QRadar header `LEEF:\d+(\.\d+)?\|` (`confidence: 0.99`)
  * `Syslog`: RFC 3164 BSD `<PRI>` and RFC 5424 structured headers (`confidence: 0.90 - 0.95`)
  * `Key=Value`: Multiple `key=value` token pairs (`confidence: 0.70 - 0.95`)
  * `Unknown / Proprietary`: Fallback to AI Parser Studio (`confidence: < 0.70`)

### 4.3 The Universal Intermediate Representation (ULPF-IR)
* **Module**: `main/app/models/ir.py`, `main/app/normalization/`
* All heterogeneous inputs are transformed into a canonical, schema-validated structure:
  * **Event Metadata**: `id`, `timestamp`, `category`, `action`, `severity`
  * **Network Coordinates**: `source.ip`, `source.port`, `destination.ip`, `destination.port`, `protocol`
  * **Device Attribution**: `device.vendor`, `device.product`, `device.hostname`
  * **Security Context**: `rule.id`, `rule.name`, `threat.name`, `user.name`
  * **Field Provenance**: Source field name, extracted value, parser name, and confidence per attribute.

### 4.4 On-Device AI Parser Studio (Offline & Sovereign)
* **Module**: `main/app/ai/`
* **Engine**: Local Small Language Model (SLM) — `deepseek-r1:1.5b` / `llama3.2:1b` / `qwen2.5-coder` via Ollama or built-in offline heuristic synthesizer.
* **Function**: Infers field delimiters, generates regex extractors, and dynamically registers parsers for unknown logs into the live runtime engine without system restarts.
* **Security**: Operates 100% offline with zero cloud API keys, protecting classified telemetry.

### 4.5 Storage & Streaming Topology
* **Local Mode (Default Bare-Metal)**:
  * Raw evidence store in `main/storage/raw/`
  * SQLite relational canonical events in `main/storage/ulpf_events.db`
  * Unknown logs queue in `main/storage/ulpf_unknown.db`
  * Watched folder in `main/storage/logs/`
* **Distributed Mode (Docker Compose)**:
  * **Ingestion Buffer**: Redpanda (C++ Kafka API, ~400MB RAM)
  * **Raw Forensic Store**: MinIO S3 Object Storage (~150MB RAM)
  * **Search & Analytics**: OpenSearch 2.11 (512MB JVM Heap)
  * **SIEM Dashboards**: OpenSearch Dashboards on port 5601

---

## 5. Hardware & Resource Footprint

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **CPU** | 4 Cores (x86_64 / ARM64) | 8+ Cores (Intel i7 / AMD Ryzen 7) |
| **System RAM** | 4 GB | 16 GB |
| **Disk Space** | 2 GB free SSD | 20 GB NVMe SSD |
| **GPU / VRAM** | CPU Only (Quantized SLM) | NVIDIA RTX (for <1s AI parser generation) |
| **Network** | Offline / Air-Gapped | Isolated Management VLAN |
