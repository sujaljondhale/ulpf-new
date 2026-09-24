# ULPF Codebase Architecture & File Index (`details.md`)

This document provides a comprehensive inventory of all functional source code files, configurations, scripts, and documentation across the Universal Log Pre-processing Framework (ULPF) repository.

> [!NOTE]
> Per configuration rules, sample log files (`*.raw`), binary database stores (`*.db`), and temporary build/cache artifacts (`.pytest_cache`, `__pycache__`, scratch files) have been excluded.

---

## 1. Root Orchestration, Deployment & Environment

| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`start_main.bat`](./start_main.bat) | `start_main.bat` | Windows batch launcher for the Main Core ULPF processing service (FastAPI, collectors, parsers, and dashboard on Port 8000). |
| [`start_testing.bat`](./start_testing.bat) | `start_testing.bat` | Windows batch launcher for the dedicated Testing Web Studio and Network Simulator backend on Port 8050. |
| [`test_pipeline.bat`](./test_pipeline.bat) | `test_pipeline.bat` | Batch script executing the automated regression pipeline (`testing/run_pipeline.py`) with support for `--device-timeout`, `--logs-interval`, and `--fast`. |
| [`docker-compose.yml`](./docker-compose.yml) | `docker-compose.yml` | Multi-container Docker configuration orchestrating FastAPI API, Worker, MinIO S3, OpenSearch, Redpanda Kafka, and Ollama AI services. |
| [`Dockerfile`](./Dockerfile) | `Dockerfile` | Multi-stage production container image for the unified ULPF application. |
| [`Dockerfile.api`](./Dockerfile.api) | `Dockerfile.api` | Dedicated lightweight Docker container specification for the FastAPI API Gateway. |
| [`Dockerfile.worker`](./Dockerfile.worker) | `Dockerfile.worker` | Container specification for background log streaming, parsing, and pipeline worker tasks. |
| [`Dockerfile.ai`](./Dockerfile.ai) | `Dockerfile.ai` | Container specification for AI onboarding and autonomous parser synthesis services. |
| [`pyproject.toml`](./pyproject.toml) | `pyproject.toml` | Build system configuration, package dependencies, Pytest testpaths/pythonpath, and Pyright analyzer settings. |
| [`requirements.txt`](./requirements.txt) | `requirements.txt` | Core Python package dependencies (FastAPI, Uvicorn, Pydantic, PyYAML, Psutil, Requests). |
| [`.env.example`](./.env.example) | `.env.example` | Template environment variable definitions for ports, storage paths, AI API keys, and retention policies. |
| [`.gitignore`](./.gitignore) | `.gitignore` | Specifies intentionally untracked files (caches, virtual environments, raw binaries, SQLite DBs). |
| [`.dockerignore`](./.dockerignore) | `.dockerignore` | Excludes unnecessary local files, caches, and test logs from container build contexts. |
| [`render.yaml`](./render.yaml) | `render.yaml` | Cloud deployment blueprint and service declaration for hosting ULPF on the Render platform. |
| [`README.md`](./README.md) | `README.md` | Master project overview, architectural design summary, key capabilities, and quick-start instructions. |

---

## 2. Main Core Subsystem (`main/`)

### Application Entrypoint & Ingestion Engine
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`run_main.py`](./main/run_main.py) | `main/run_main.py` | Direct executable launcher for the main core service, setting working paths and starting Uvicorn. |
| [`main.py`](./main/app/main.py) | `main/app/main.py` | Core FastAPI application lifecycle manager, registering REST routes, CORS middleware, SSE event streams, and static dashboard files. |
| [`pipeline.py`](./main/app/pipeline.py) | `main/app/pipeline.py` | Central deterministic processing pipeline coordinating format detection, vendor parsing, taxonomy normalization, validation, and storage. |
| [`cli.py`](./main/app/cli.py) | `main/app/cli.py` | Command-line interface tool for offline log ingestion, individual log parsing, and ad-hoc file inspection. |
| [`settings.py`](./main/app/config/settings.py) | `main/app/config/settings.py` | Central application configuration management using Pydantic Settings (ports, directories, retention, AI keys). |

### REST API Layer (`main/app/api/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`routes.py`](./main/app/api/routes.py) | `main/app/api/routes.py` | Primary REST API route definitions (`/ingest`, `/events`, `/sources`, `/threats`, `/export`, `/retention`). |
| [`schemas.py`](./main/app/api/schemas.py) | `main/app/api/schemas.py` | Pydantic validation models and request/response schemas for all API payloads. |
| [`generator.py`](./main/app/api/generator.py) | `main/app/api/generator.py` | Synthetic multi-vendor security event generator (CEF, Syslog, JSON, KV, LEEF) for testing and UI demonstration. |

### Network Collectors & Ingress (`main/app/collectors/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`base.py`](./main/app/collectors/base.py) | `main/app/collectors/base.py` | Abstract base class defining common collector interfaces, lifecycle hooks, and metrics tracking. |
| [`syslog_collector.py`](./main/app/collectors/syslog_collector.py) | `main/app/collectors/syslog_collector.py` | High-throughput UDP (:5140) and TCP (:5141) network syslog listener for real and simulated appliances. |
| [`file_collector.py`](./main/app/collectors/file_collector.py) | `main/app/collectors/file_collector.py` | Directory-watcher collector monitoring local folders (`storage/logs/`) for automated batch file ingestion. |
| [`redpanda_collector.py`](./main/app/collectors/redpanda_collector.py) | `main/app/collectors/redpanda_collector.py` | Streaming consumer integrating with Redpanda / Apache Kafka message brokers for distributed event streams. |
| [`ingress.py`](./main/app/collectors/ingress.py) | `main/app/collectors/ingress.py` | Ingress coordinator accepting incoming datagrams and dispatching to backpressure queues and pipelines. |
| [`queue.py`](./main/app/collectors/queue.py) | `main/app/collectors/queue.py` | In-memory asynchronous backpressure queue managing burst buffers and rate-limiting drop policies. |
| [`source_registry.py`](./main/app/collectors/source_registry.py) | `main/app/collectors/source_registry.py` | Stateful registry tracking connected devices, IP addresses, packet volumes, and connection statuses. |

### Format Detection & Classification (`main/app/detector/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`detector.py`](./main/app/detector/detector.py) | `main/app/detector/detector.py` | Format detection engine evaluating heuristics, header patterns, and confidence scoring. |
| [`format_detector.py`](./main/app/detector/format_detector.py) | `main/app/detector/format_detector.py` | Signature matching for 8 major log standards (CEF, LEEF, Syslog RFC 3164/5424, JSON, KV, CSV, XML). |
| [`models.py`](./main/app/detector/models.py) | `main/app/detector/models.py` | Data structures representing detected format verdicts, confidence scores, and syntax classifications. |

### Vendor Parsers (`main/app/parsers/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`base.py`](./main/app/parsers/base.py) | `main/app/parsers/base.py` | Base parser contract and abstract methods for extracting tokenized fields from raw logs. |
| [`cef_parser.py`](./main/app/parsers/cef_parser.py) | `main/app/parsers/cef_parser.py` | Common Event Format parser (ArcSight, Fortinet, Check Point, Palo Alto). |
| [`leef_parser.py`](./main/app/parsers/leef_parser.py) | `main/app/parsers/leef_parser.py` | Log Event Extended Format parser (IBM QRadar, Suricata IDS). |
| [`syslog_parser.py`](./main/app/parsers/syslog_parser.py) | `main/app/parsers/syslog_parser.py` | Standard Syslog parser handling RFC 3164 (BSD) and RFC 5424 (IETF) message headers and payloads. |
| [`json_parser.py`](./main/app/parsers/json_parser.py) | `main/app/parsers/json_parser.py` | High-speed parser for structured JSON logs (AWS CloudTrail, Suricata EVE, Kubernetes). |
| [`kv_parser.py`](./main/app/parsers/kv_parser.py) | `main/app/parsers/kv_parser.py` | Key-value delimiter parser handling quoted strings and nested delimiters (Palo Alto PAN-OS, CheckPoint). |
| [`xml_parser.py`](./main/app/parsers/xml_parser.py) | `main/app/parsers/xml_parser.py` | XML parser extracting security telemetry from Windows Event Logs and application manifests. |
| [`csv_parser.py`](./main/app/parsers/csv_parser.py) | `main/app/parsers/csv_parser.py` | Delimited format parser for comma-separated, tab-separated, and pipe-separated tabular records. |
| [`text_parser.py`](./main/app/parsers/text_parser.py) | `main/app/parsers/text_parser.py` | Unstructured text parser utilizing regex and pattern heuristics for legacy mainframe logs. |
| [`compiler.py`](./main/app/parsers/compiler.py) | `main/app/parsers/compiler.py` | Dynamic JIT parser compilation engine converting declarative regex schemas into executable Python parsers. |
| [`registry.py`](./main/app/parsers/registry.py) | `main/app/parsers/registry.py` | Central parser lookup registry routing detected formats to corresponding parser modules. |

### Normalization & Taxonomy (`main/app/normalization/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`normalizer.py`](./main/app/normalization/normalizer.py) | `main/app/normalization/normalizer.py` | Core transformation engine converting raw parsed tokens into standard ULPF Intermediate Representation (ULPF-IR). |
| [`mappings.py`](./main/app/normalization/mappings.py) | `main/app/normalization/mappings.py` | Exhaustive field-mapping dictionaries translating vendor-specific field names (e.g. `spt`, `src_port`, `source_port`) to canonical names (`src_port`). |
| [`taxonomy.py`](./main/app/normalization/taxonomy.py) | `main/app/normalization/taxonomy.py` | Classification rules normalizing vendor action verdicts (`allow`, `drop`, `block`, `deny`) and severities (`critical`, `high`, `medium`, `low`). |

### Data Models & Provenance (`main/app/models/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`canonical_event.py`](./main/app/models/canonical_event.py) | `main/app/models/canonical_event.py` | Unified, schema-enforced security event data model representing completely normalized records. |
| [`ir.py`](./main/app/models/ir.py) | `main/app/models/ir.py` | Pydantic definition of ULPF Intermediate Representation (ULPF-IR) carrying metadata and normalized attributes. |
| [`provenance.py`](./main/app/models/provenance.py) | `main/app/models/provenance.py` | Legal chain-of-custody model holding SHA-256 cryptographic hashes, ingestion timestamps, and raw byte offsets. |
| [`raw_event.py`](./main/app/models/raw_event.py) | `main/app/models/raw_event.py` | Immutable raw ingested log model preserving original unaltered byte streams for evidentiary compliance. |
| [`taxonomy.py`](./main/app/models/taxonomy.py) | `main/app/models/taxonomy.py` | Enumerations and domain categories for security activities (Authentication, Network Traffic, Malware, Policy). |
| [`api.py`](./main/app/models/api.py) | `main/app/models/api.py` | Internal data transfer models for API requests, batch uploads, and query filtering. |

### AI Model Integration & Parser Synthesis (`main/app/ai/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`onboarding.py`](./main/app/ai/onboarding.py) | `main/app/ai/onboarding.py` | Automated AI parser generator analyzing unrecognized logs and synthesizing executable parser rules for human approval. |
| [`providers.py`](./main/app/ai/providers.py) | `main/app/ai/providers.py` | Multi-provider LLM abstraction layer supporting local Ollama, HuggingFace, OpenAI, Anthropic, and Gemini with automated failover. |

### Storage, Database & Audit Ledger (`main/app/storage/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`database.py`](./main/app/storage/database.py) | `main/app/storage/database.py` | SQLite metadata database management, schema auto-migration, event queries, and source record persistence. |
| [`persistence.py`](./main/app/storage/persistence.py) | `main/app/storage/persistence.py` | Raw log persistence engine writing immutable `.raw` archive files with SHA-256 hash indexing and time-based retention pruning. |
| [`minio_store.py`](./main/app/storage/minio_store.py) | `main/app/storage/minio_store.py` | Cold object storage interface archiving compressed raw logs to MinIO / AWS S3 buckets. |
| [`opensearch_store.py`](./main/app/storage/opensearch_store.py) | `main/app/storage/opensearch_store.py` | Hot search indexer streaming canonical events to OpenSearch / Elasticsearch for sub-second threat querying. |

### Validation & Exporters (`main/app/validation/` & `main/app/exporters/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`validator.py`](./main/app/validation/validator.py) | `main/app/validation/validator.py` | Integrity validator verifying IP syntax, timestamp validity, and required field completeness. |
| [`base.py`](./main/app/exporters/base.py) | `main/app/exporters/base.py` | Abstract exporter interface for transforming and exporting normalized events. |
| [`ocsf.py`](./main/app/exporters/ocsf.py) | `main/app/exporters/ocsf.py` | Open Cybersecurity Schema Framework (OCSF v1.1) mapping engine and JSON exporter. |
| [`ecs.py`](./main/app/exporters/ecs.py) | `main/app/exporters/ecs.py` | Elastic Common Schema (ECS v8.x) mapping engine and JSON exporter. |
| [`redpanda_exporter.py`](./main/app/exporters/redpanda_exporter.py) | `main/app/exporters/redpanda_exporter.py` | Kafka publisher streaming dual-packaged (OCSF + ECS) events to Redpanda topics. |
| [`forwarder.py`](./main/app/exporters/forwarder.py) | `main/app/exporters/forwarder.py` | Real-time TCP/UDP/HTTP forwarder replicating normalized events to external SIEMs and datalakes. |

---

## 3. Main Enterprise Dashboard (`main/dashboard/`)

| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`index.html`](./main/dashboard/index.html) | `main/dashboard/index.html` | Core Enterprise Security Control Center single-page application structure, navigation bar, and modal skeletons. |
| [`app.js`](./main/dashboard/app.js) | `main/dashboard/app.js` | Main client-side router, SSE real-time stream listener, chart renderers, custom log injector, device manager, and `#/testing` suite view. |
| [`style.css`](./main/dashboard/style.css) | `main/dashboard/style.css` | Comprehensive cybersecurity theme styling supporting Nord Dark and Snow Light modes, responsive grids, and tables. |
| [`client_app.html`](./main/dashboard/client_app.html) | `main/dashboard/client_app.html` | Lightweight standalone test harness for client browser ping and manual log submission. |
| [`client_app.js`](./main/dashboard/client_app.js) | `main/dashboard/client_app.js` | Client-side scripting for standalone browser ingestion testing. |

---

## 4. Testing Architecture & Network Simulator (`testing/`)

### Test Pipeline, Simulator Server & Network Clients
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`run_pipeline.py`](./testing/run_pipeline.py) | `testing/run_pipeline.py` | Unified automated verification pipeline executing Pytest suites, smoke tests, security tests, stack checks, and benchmarks with `--device-timeout` and `--logs-interval` configuration. |
| [`run_testing.py`](./testing/run_testing.py) | `testing/run_testing.py` | Standalone CLI entrypoint launching the Testing Hub server and network simulator on Port 8050. |
| [`sim_server.py`](./testing/server/sim_server.py) | `testing/server/sim_server.py` | Dedicated FastAPI simulation backend service (Port 8050) exposing socket probing, live scenario streaming, burst load generation, and pipeline status APIs. |
| [`protocol_clients.py`](./testing/server/protocol_clients.py) | `testing/server/protocol_clients.py` | Low-level raw network socket drivers (`send_udp_log`, `send_tcp_log`, `send_http_log`, `probe_socket`) with configurable socket timeouts. |
| [`log_generator.py`](./testing/server/log_generator.py) | `testing/server/log_generator.py` | Multi-vendor log generation library creating realistic packets for Cisco, Palo Alto, Fortinet, Suricata, Linux, and SCADA protocols. |
| [`smoke_test.py`](./testing/smoke_test.py) | `testing/smoke_test.py` | 10-phase end-to-end integration test validating API reachability, format detection, normalization, hashing, and state reset. |
| [`simulate_live_feed.py`](./testing/simulate_live_feed.py) | `testing/simulate_live_feed.py` | Continuous background simulator generating random multi-vendor network telemetry streams. |

### Benchmarks & Security Resilience Testing
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`benchmark.py`](./testing/benchmarks/benchmark.py) | `testing/benchmarks/benchmark.py` | High-throughput deterministic performance benchmark measuring EPS, P50/P95/P99 latency, and RAM delta with configurable inter-log interval pacing. |
| [`security_smoke_test.py`](./testing/security/security_smoke_test.py) | `testing/security/security_smoke_test.py` | Cyber resilience test suite executing 8 attack vectors: SQLi, XSS, directory traversal, oversized payloads, invalid IPs, YAML attacks, and prompt injection. |

### Pytest Verification Test Suites (`testing/suites/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`test_device_and_retention.py`](./testing/suites/test_device_and_retention.py) | `testing/suites/test_device_and_retention.py` | Unit tests for offset-aware datetime retention, device connection update APIs, socket timeout enforcement, and log interval pacing. |
| [`test_pipeline.py`](./testing/suites/test_pipeline.py) | `testing/suites/test_pipeline.py` | Integration tests verifying end-to-end flow through the `UlpfPipeline` class across diverse formats. |
| [`test_parsers.py`](./testing/suites/test_parsers.py) | `testing/suites/test_parsers.py` | Exhaustive unit tests for all 8 deterministic vendor parsers (CEF, LEEF, Syslog, JSON, KV, CSV, XML, Text). |
| [`test_detector.py`](./testing/suites/test_detector.py) | `testing/suites/test_detector.py` | Unit tests validating format detection accuracy and confidence scoring across standard formats. |
| [`test_normalizer.py`](./testing/suites/test_normalizer.py) | `testing/suites/test_normalizer.py` | Tests verifying field transformation, IP validation, timestamp normalization, and severity mappings. |
| [`test_api.py`](./testing/suites/test_api.py) | `testing/suites/test_api.py` | REST API endpoint tests testing `/api/v1/ingest`, `/api/v1/events`, and filtering parameters. |
| [`test_network_collectors.py`](./testing/suites/test_network_collectors.py) | `testing/suites/test_network_collectors.py` | Tests for live network listeners on UDP and TCP syslog socket ports. |
| [`test_collectors_and_forwarding.py`](./testing/suites/test_collectors_and_forwarding.py) | `testing/suites/test_collectors_and_forwarding.py` | Tests validating ingress buffer queues and real-time SIEM forwarding. |
| [`test_exporters.py`](./testing/suites/test_exporters.py) | `testing/suites/test_exporters.py` | Tests validating schema compliance for downstream OCSF v1.1 and ECS v8.x export formats. |
| [`test_redpanda.py`](./testing/suites/test_redpanda.py) | `testing/suites/test_redpanda.py` | Integration tests verifying topic publishing and consuming over Redpanda Kafka brokers. |
| [`test_ai_and_compiler.py`](./testing/suites/test_ai_and_compiler.py) | `testing/suites/test_ai_and_compiler.py` | Tests verifying dynamic parser compilation and JIT loading of synthesized parsing rules. |
| [`test_ai_intelligence.py`](./testing/suites/test_ai_intelligence.py) | `testing/suites/test_ai_intelligence.py` | Tests verifying AI MITRE ATT&CK mapping, Sigma rule generation, and OpenSearch query synthesis. |
| [`test_database_and_ai_integration.py`](./testing/suites/test_database_and_ai_integration.py) | `testing/suites/test_database_and_ai_integration.py` | Tests for SQLite database metadata persistence and AI onboarding review queue workflows. |
| [`test_persistence_and_restart.py`](./testing/suites/test_persistence_and_restart.py) | `testing/suites/test_persistence_and_restart.py` | Tests verifying state recovery, crash resilience, and SHA-256 deduplication across restarts. |
| [`test_security_and_edge_cases.py`](./testing/suites/test_security_and_edge_cases.py) | `testing/suites/test_security_and_edge_cases.py` | Edge-case fuzz testing on malformed datagrams, truncated headers, and boundary conditions. |

### Testing Web Studio UI (`testing/web/`)
| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`index.html`](./testing/web/index.html) | `testing/web/index.html` | Dedicated testing studio web interface (Port 8050) providing virtual device management, attack arsenal, load generator, port radar, and pipeline controls. |
| [`simulator.js`](./testing/web/simulator.js) | `testing/web/simulator.js` | Frontend controller for virtual device telemetry streaming, socket ping probing, attack dispatch, and live pipeline execution tracking. |
| [`style.css`](./testing/web/style.css) | `testing/web/style.css` | Cyber lab dark theme styles, audit tables, radar indicators, and diagnostic console feeds. |

---

## 5. Operational & Diagnostic Scripts (`scripts/`)

| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`verify_stack.py`](./scripts/verify_stack.py) | `scripts/verify_stack.py` | Comprehensive 10-check integration probe testing Docker containers, FastAPI, MinIO, OpenSearch, Redpanda, and AI. |
| [`run_worker.py`](./scripts/run_worker.py) | `scripts/run_worker.py` | Standalone background worker process for distributed log ingestion and normalization. |
| [`test_device_send.py`](./scripts/test_device_send.py) | `scripts/test_device_send.py` | Command-line testing utility to send custom single or batch UDP/TCP/HTTP logs to ULPF. |
| [`test_million_logs.py`](./scripts/test_million_logs.py) | `scripts/test_million_logs.py` | Stress-testing script firing up to 1,000,000 synthetic log records to measure long-term stability and throughput. |
| [`test_wifi_logs.py`](./scripts/test_wifi_logs.py) | `scripts/test_wifi_logs.py` | Test generator simulating Cisco Meraki, Aruba, and Ubiquiti wireless 802.11 association/disassociation logs. |
| [`send_syslog.py`](./scripts/send_syslog.py) | `scripts/send_syslog.py` | Fast UDP syslog socket client for quick manual packet injection on Port 5140. |
| [`generate_report_pdf.py`](./scripts/generate_report_pdf.py) | `scripts/generate_report_pdf.py` | Automated report compiler generating forensic compliance and security incident PDF summaries. |
| [`start.bat`](./scripts/start.bat) / [`start.sh`](./scripts/start.sh) | `scripts/start.bat`, `scripts/start.sh` | Shell scripts to launch all local services. |
| [`stop.bat`](./scripts/stop.bat) / [`stop.sh`](./scripts/stop.sh) | `scripts/stop.bat`, `scripts/stop.sh` | Shell scripts to gracefully terminate running ULPF processes. |
| [`reset.bat`](./scripts/reset.bat) / [`reset.sh`](./scripts/reset.sh) | `scripts/reset.bat`, `scripts/reset.sh` | Scripts resetting demonstration state, clearing SQLite databases, and wiping temporary archives. |
| [`health.bat`](./scripts/health.bat) / [`health.sh`](./scripts/health.sh) | `scripts/health.bat`, `scripts/health.sh` | Quick health and port availability checking scripts. |
| [`demo.bat`](./scripts/demo.bat) / [`demo.sh`](./scripts/demo.sh) | `scripts/demo.bat`, `scripts/demo.sh` | Automated demonstration scenario triggers for live hackathon evaluation. |
| [`entrypoint_ai.sh`](./scripts/entrypoint_ai.sh) | `scripts/entrypoint_ai.sh` | Docker container entrypoint for bootstrapping local Ollama models in isolated deployments. |
| [`oracle-setup.sh`](./scripts/oracle-setup.sh) | `scripts/oracle-setup.sh` | Infrastructure setup and provisioning script for Oracle Cloud Infrastructure (OCI) instances. |

---

## 6. Technical Documentation & Architecture Specifications (`docs/`)

| File Name | Location | Use / Purpose |
| :--- | :--- | :--- |
| [`architecture.md`](./docs/architecture.md) | `docs/architecture.md` | Comprehensive system architecture document detailing the decoupled Core vs Testing Hub layout and data flow. |
| [`api.md`](./docs/api.md) | `docs/api.md` | Complete REST API specification detailing request parameters, response structures, and sample curl calls. |
| [`testing.md`](./docs/testing.md) | `docs/testing.md` | Complete guide to the testing suite, network simulator, automated pipeline execution, and timeout/interval configurations. |
| [`ai-integration.md`](./docs/ai-integration.md) | `docs/ai-integration.md` | Guide to AI onboarding, parser synthesis, threat reasoning, and multi-provider configuration (Ollama, OpenAI, Gemini). |
| [`ingestion.md`](./docs/ingestion.md) | `docs/ingestion.md` | Guide covering high-throughput network ingestion, backpressure queues, and syslog configuration. |
| [`deployment.md`](./docs/deployment.md) | `docs/deployment.md` | Guide for deploying ULPF with Docker Compose, Kubernetes, and bare-metal environments. |
| [`air-gapped-deployment.md`](./docs/air-gapped-deployment.md) | `docs/air-gapped-deployment.md` | Architecture and offline container procedures for secure, isolated defense networks without internet access. |
| [`evidence.md`](./docs/evidence.md) | `docs/evidence.md` | Legal evidence and forensic chain-of-custody documentation explaining raw log immutability and SHA-256 hashing. |
| [`ulpf-ir.md`](./docs/ulpf-ir.md) | `docs/ulpf-ir.md` | Formal specification of the ULPF Intermediate Representation schema standard. |
| [`benchmark.md`](./docs/benchmark.md) | `docs/benchmark.md` | Reproducible benchmark methodology, hardware environments, EPS metrics, and latency percentiles. |
| [`data-flow.md`](./docs/data-flow.md) | `docs/data-flow.md` | Step-by-step trace of a log datagram from socket arrival to parsing, normalization, indexing, and export. |
| [`limitations.md`](./docs/limitations.md) | `docs/limitations.md` | Architectural boundaries, edge-case assumptions, and Phase 2 enhancement roadmap. |
| [`judge-questions.md`](./docs/judge-questions.md) | `docs/judge-questions.md` | Curated technical FAQ and defense briefing addressing hackathon evaluation criteria. |
| [`demo-script.md`](./docs/demo-script.md) | `docs/demo-script.md` | 3-minute structured live demonstration walkthrough script. |
| [`demo_video_script.md`](./docs/demo_video_script.md) | `docs/demo_video_script.md` | Screenplay and narration script for video demonstration recordings. |
| [`presentation_5slides.md`](./docs/presentation_5slides.md) | `docs/presentation_5slides.md` | Executive 5-slide pitch presentation summarizing problem, solution, architecture, and impact. |
| [`architecture_2page.md`](./docs/architecture_2page.md) | `docs/architecture_2page.md` | Condensed 2-page executive architectural briefing document. |
