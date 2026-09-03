# ULPF — 5-Slide SIH Technical Presentation Content

**SIH Problem ID:** SIH 26156 (NTRO)  
**Project:** Universal Log Pre-processing Framework (ULPF)  
**Category:** Software | Theme: Miscellaneous

---

## Slide 1 — Problem Statement & Enterprise Challenges

### Title: The Enterprise Log Fragmentation Problem
- **Massive Log Heterogeneity**: Modern NTRO/Defense networks ingest billions of logs daily across firewalls, routers, IDPS, WAFs, and cloud apps.
- **Format Chaos**: Data arrives in Syslog, CEF, LEEF, Key=Value, JSON, XML, CSV, and proprietary unstructured strings.
- **SIEM Bottlenecks**: High parser development costs, vendor lock-in, heavy memory consumption (Kafka/Elasticsearch), data truncation, and zero field-level traceability.
- **The Need**: A universal, vendor-neutral, ultra-fast pre-processing core deployable 100% offline in classified air-gapped networks.

---

## Slide 2 — The ULPF Solution & Value Proposition

### Title: Universal Log Pre-processing Framework (ULPF)
- **Universal Format Detection**: Instantly detects 8 log formats deterministically.
- **100% Lossless Storage**: Preserves exact raw log bytes with SHA-256 cryptographic integrity digests.
- **ULPF-IR v1.0 Canonical Model**: Vendor-agnostic intermediate representation.
- **Field-Level Provenance Engine**: Full lineage tracking (`source.ip <- src`, original value, parser, rule, confidence).
- **Dual Schema Exporters**: Out-of-the-box translation to **OCSF v1.1.0** and **Elastic Common Schema (ECS v8.x)**.

---

## Slide 3 — System Architecture & Data Flow

### Title: Architecture & On-Device AI Onboarding Flow
- **High-Speed Ingestion Pipeline**:
  `Raw Log -> Payload Check -> Format Detection -> Parser Selection -> ULPF-IR v1.0 -> Provenance -> OCSF/ECS Exporters`
- **AI-Assisted Unknown Source Onboarding**:
  When unknown logs arrive, local on-device SLM (**Qwen 3B/4B via Ollama**) infers structure from sample logs, generates YAML parser specs, compiles executable parsers, and registers them into production 100% offline.

---

## Slide 4 — Key Engineering Innovations & Air-Gapped Containerization

### Title: Innovation Highlights & Platform Independence
1. **Local Offline AI**: Zero cloud API dependencies; runs quantized Qwen SLM locally on consumer GPU (RTX 4050 6GB VRAM) / CPU.
2. **YAML Parser Compiler**: Compiles human-readable YAML specifications into high-performance executable python parsers.
3. **Parser Lifecycle Management**: 5-stage lifecycle (`DRAFT -> VALIDATED -> APPROVED -> ACTIVE -> DEPRECATED`).
4. **Air-Gapped Docker Packaging**: Packaged via Docker Compose (`docker-compose.yml`) for instant platform-independent deployment on any Linux/Windows server.

---

## Slide 5 — Empirical Benchmarks & Deliverables

### Title: Proven Performance Baseline & SIH Deliverables
- **1,000,000 Event Benchmark Results**:
  - **Throughput**: **13,672 events/sec** (Single core)
  - **Latency**: **73.14 µs** average per event
  - **RAM RSS**: **31.14 MB** total footprint (0 MB memory leak across 1M events)
- **Evaluation Deliverables Included**:
  1. Source Code Repository (`/app`, `/tests`, `/scripts`)
  2. Readme Setup & User Guide (`README.md`)
  3. 2-Page Executive Architecture Summary (`docs/architecture_2page.md`)
  4. Demo Video Script & Storyboard (`docs/demo_video_script.md`)
  5. 5-Slide Presentation Deck (`docs/presentation_5slides.md`)
