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

---

## 2. High-Level Architecture Diagram

```
                             [ RAW INGESTION LAYER ]
                                        │
           ┌────────────────────────────┼───────────────────────────┐
           ▼                            ▼                           ▼
    [ Syslog UDP/TCP 514 ]     [ HTTP REST /process ]     [ Batch File Uploader ]
           │                            │                           │
           └────────────────────────────┬───────────────────────────┘
                                        │
                                        ▼
                         [ 1. RAW INTEGRITY PRESERVER ]
                         ├── Compute SHA-256 Digest
                         ├── Assign UUID4 & Ingestion Timestamp
                         └── Write to Immutable Raw Store
                                        │
                                        ▼
                         [ 2. DETERMINISTIC DETECTOR ]
                         ├── Regex Structure & Signature Matching
                         ├── Confidence Scorer (0.0 to 1.0)
                         └── Fast Dispatch Table
                                        │
                      ┌─────────────────┴─────────────────┐
                      ▼                                   ▼
          [ Known Format (≥0.70) ]            [ Unknown Format (<0.70) ]
                      │                                   │
                      ▼                                   ▼
             [ 3. CORE PARSERS ]                 [ AI PARSER ONBOARDING ]
             ├── JSON (Flattened)                ├── Vector Pattern Match
             ├── Syslog (RFC 3164/5424)          ├── Local SLM (Qwen2.5-Coder)
             ├── CEF (ArcSight V0-V25)           ├── Auto-Regex Generation
             ├── LEEF (QRadar V1-V2)             ├── Interactive Testbench
             └── Key=Value (Fortinet/Cisco)      └── Dynamic Parser Registry
                      │                                   │
                      └─────────────────┬─────────────────┘
                                        │
                                        ▼
                         [ 4. ULPF-IR CANONICAL ENGINE ]
                         ├── Taxonomy Mapping (Source, Dest, Device, Action)
                         ├── Pydantic V2 Schema Validation
                         └── Field-Level Provenance & Lineage Tracker
                                        │
                                        ▼
                         [ 5. DOWNSTREAM DISPATCH SINK ]
                         ├── OpenSearch / Elasticsearch Indexing
                         ├── OCSF / ECS Standard Formats
                         ├── Redpanda / Kafka High-Speed Buffer
                         └── MinIO S3 Object Archive
```

---

## 3. Core Architectural Subsystems

### 3.1 Raw Ingestion & Tamper-Evident Integrity
* **Module**: `app/models/raw.py`, `app/api/routes.py`
* **Invariant**: The original raw string is **never modified, truncated, or re-encoded**.
* **Integrity Guarantee**: A SHA-256 cryptographic digest is computed across the raw byte payload upon arrival. Field-level provenance retains references to the exact slice and raw hash, establishing verifiable chain of custody for digital forensics.

### 3.2 Deterministic Format Detection
* **Module**: `app/detector/format_detector.py`
* **Throughput**: Single-pass regex evaluation with zero external network lookups.
* **Supported Formats**:
  * `JSON`: RFC 8259 JSON validation (`confidence: 1.0`)
  * `CEF`: ArcSight standard header `CEF:\d+\|` (`confidence: 0.99`)
  * `LEEF`: QRadar header `LEEF:\d+(\.\d+)?\|` (`confidence: 0.99`)
  * `Syslog`: RFC 3164 BSD `<PRI>` and RFC 5424 structured headers (`confidence: 0.90 - 0.95`)
  * `Key=Value`: Multiple `key=value` token pairs (`confidence: 0.70 - 0.95`)
  * `Plaintext / Unrecognized`: Fallback to AI Parser Studio (`confidence: 0.20`)

### 3.3 The Universal Intermediate Representation (ULPF-IR)
* **Module**: `app/models/ir.py`, `app/models/taxonomy.py`
* All heterogeneous inputs are transformed into a canonical, schema-validated structure:
  * **Event Metadata**: `id`, `timestamp`, `category`, `action`, `severity`
  * **Network Coordinates**: `source.ip`, `source.port`, `destination.ip`, `destination.port`, `protocol`
  * **Device Attribution**: `device.vendor`, `device.product`, `device.hostname`
  * **Security Context**: `rule.id`, `rule.name`, `threat.name`, `user.name`
  * **Field Provenance**: Source field name, extracted value, parser name, and confidence per attribute.

### 3.4 On-Device AI Parser Studio (Offline & Sovereign)
* **Module**: `app/ai/`, `app/parsers/`
* **Engine**: Local Small Language Model (SLM) — `Qwen2.5-Coder 3B` / `Llama-3-8B-Instruct` via Ollama.
* **Function**: When an unfamiliar or proprietary log format is received, the AI Parser Studio extracts sample patterns, generates optimized Python regex extractors, presents an interactive human-in-the-loop validation diff, and registers the parser into the live runtime engine without system restarts.
* **Security**: Operates 100% offline with zero cloud API keys, protecting classified telemetry.

### 3.5 Storage & Streaming Topology
* **Local Mode (Default)**: In-memory circular buffer with fast file persistence for low-footprint single-node deployments (< 100 MB RAM).
* **Distributed Mode (Docker Compose)**:
  * **Ingestion Buffer**: Redpanda (C++ Kafka API, ~400MB RAM)
  * **Raw Forensic Store**: MinIO S3 Object Storage (~150MB RAM)
  * **Search & Analytics**: OpenSearch 2.11 (512MB JVM Heap)
  * **SIEM Dashboards**: OpenSearch Dashboards on port 5601

---

## 4. Hardware & Resource Footprint

| Component | Minimum Specification | Recommended Specification |
| :--- | :--- | :--- |
| **CPU** | 4 Cores (x86_64 / ARM64) | 8+ Cores (Intel i7 13th Gen / AMD Ryzen 7) |
| **System RAM** | 4 GB | 16 GB |
| **Disk Space** | 2 GB free SSD | 20 GB NVMe SSD |
| **GPU / VRAM** | CPU Only (Quantized SLM) | NVIDIA RTX 4050 6GB VRAM (for <1s AI parser generation) |
| **Network** | Offline / Air-Gapped | Isolated Management VLAN |
