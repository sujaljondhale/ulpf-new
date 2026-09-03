# Architecture Document — Universal Log Pre-processing Framework (ULPF)

**SIH Problem ID:** SIH 26156  
**Organization:** National Technical Research Organisation (NTRO)  
**Deliverable:** 2-Page Executive Architecture Summary

---

## 1. Executive Summary & Problem Context

Modern enterprise and defense networks generate billions of raw log events daily from firewalls, routers, IDPS, WAFs, operating systems, and cloud platforms. These logs arrive in highly fragmented formats (Syslog, CEF, LEEF, JSON, XML, CSV, Key=Value, and unstructured text). 

Legacy SIEM platforms struggle with parser maintenance, vendor lock-in, data loss during transformation, and lack of field-level lineage. **ULPF** is an ultra-fast, vendor-agnostic, loss-less log pre-processing core designed for high-throughput perimeter log ingestion, automated local AI onboarding, and seamless export to **OCSF v1.1.0** and **Elastic Common Schema (ECS v8.x)**.

---

## 2. Overall Pipeline & Component Architecture

```text
                                RAW LOG INGESTION
                                        │
                                        ▼
                       +---------------------------------+
                       | SECURITY & PAYLOAD VALIDATOR    |
                       | Payload limit check (10MB)      |
                       | SHA-256 Integrity Hash          |
                       +----------------┬----------------+
                                        │
                                        ▼
                       +---------------------------------+
                       | DETERMINISTIC FORMAT DETECTOR   |
                       | JSON / XML / CSV / Syslog / CEF |
                       | LEEF / Key=Value / Plaintext    |
                       +----------------┬----------------+
                                        │
                                        ▼
                       +---------------------------------+
                       | PARSER ENGINE & LIFECYCLE REGISTRY|
                       | Built-in & Dynamic Parsers      |
                       | (DRAFT -> ACTIVE -> DEPRECATED) |
                       +----------------┬----------------+
                                        │
                                Known Source Format?
                                 /            \
                               YES             NO (Unparsed Fallback)
                                │              │
                                │              ▼
                                │     LOCAL AI ONBOARDING
                                │     (Ollama Qwen 3B/4B SLM)
                                │              │
                                │     Schema Inference &
                                │     YAML Spec Compiler
                                └──────────────┤
                                               ▼
                                  +------------------------+
                                  | ULPF-IR v1.0 CANONICAL |
                                  | Universal Event Model  |
                                  +-----------┬------------+
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      ▼                                               ▼
             RAW LOG PRESERVATION                               FIELD PROVENANCE
            (100% Lossless Store)                              (Attribution Mapping)
                      │                                               │
                      └───────────────────────┬───────────────────────┘
                                              ▼
                                 +-------------------------+
                                 | CANONICAL EXPORTERS     |
                                 | OCSF v1.1.0 / ECS v8.x  |
                                 +-------------------------+
```

---

## 3. Core Subsystem Specifications

### A. Lossless Ingestion & Integrity (`app/models/raw_event.py`)
- Computes SHA-256 cryptographic hashes for every raw log message upon arrival.
- Preserves raw message text without mutation or truncating unmapped keys.

### B. Format Detector & Parsers (`app/detector/`, `app/parsers/`)
- Deterministic regex & structural parser dispatches: JSON, XML, CSV, Syslog (RFC 3164/5424), CEF, LEEF, Key=Value, and Plaintext fallback.
- Operates at **> 13,600 events/sec per core** without LLM latency overhead on production traffic.

### C. Local AI Unknown Log Onboarding (`app/ai/onboarding.py`)
- Leverages local quantized SLM (**Qwen 3B/4B via Ollama**) running on-device (RTX 4050 6GB GPU).
- Infers syntax structure from 10-100 sample unparsed logs, generates YAML parser specifications, and registers compiled parsers into production 100% offline.

### D. Universal Event Model (ULPF-IR v1.0) & Provenance (`app/models/canonical_event.py`)
- Normalizes logs into canonical taxonomy: `event`, `source`, `destination`, `network`, `device`, `rule`, `user`, `severity`.
- Tracks field-level provenance lineage (`value`, `original_field`, `original_value`, `parser`, `rule`, `confidence`).

### E. Multi-Schema Exporters (`app/exporters/`)
- Dual exporters translate ULPF-IR into **OCSF v1.1.0 (Class 4001 Network Activity)** and **Elastic Common Schema (ECS v8.x)**.

### F. Deployment & Air-Gapped Packaging (`docker-compose.yml`)
- Containerized deployment via Docker (`ulpf-api`, `ulpf-worker`, `ulpf-ai`).
- Zero internet or cloud dependencies; deployable in classified air-gapped networks.
