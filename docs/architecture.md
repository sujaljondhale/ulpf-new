## Single-PC Simultaneous Deployment (16 GB RAM / 6 GB VRAM)

ULPF can run **all microservices simultaneously on a single development PC** (Intel i7 13th Gen, RTX 4050 GPU, 16 GB RAM) by applying lightweight memory tuning:

| Container Service | Role / Purpose | Host RAM | GPU VRAM | Port |
| :--- | :--- | :--- | :--- | :--- |
| **`ulpf-api`** | Core FastAPI Engine & Web Dashboard | ~35 MB | 0 MB | `8000` |
| **`ulpf-ai`** | Local SLM (Ollama + Qwen 3B Q4) | ~250 MB | ~2.2 GB | `11434` |
| **`redpanda`** | Event Streaming Buffer (C++ Kafka API) | ~400 MB | 0 MB | `9002` |
| **`minio`** | Immutable Raw Log Object Storage (S3 API) | ~150 MB | 0 MB | `9000` / `9001` |
| **`opensearch`** | Normalized Event Indexing (512MB Heap) | ~800 MB | 0 MB | `9200` |
| **`opensearch-dashboards`**| Analytics & SIEM Dashboard Console | ~350 MB | 0 MB | `5601` |
| **Windows OS Overhead** | Operating System & System Services | ~6,500 MB | ~500 MB | - |
| **TOTAL SYSTEM RAM** | **100% Operational Simultaneously** | **~8.5 GB / 16 GB** | **~2.7 GB / 6 GB** | - |


```text
NETWORK / PERIMETER DEVICES (Firewalls, Routers, IDS/IPS, WAF, Proxy)
                           │
                           ▼
                  +-----------------+
                  | Ingestion Layer |
                  +--------┬--------+
                           │
                           ▼
             +---------------------------+
             | Format Detector           |
             | JSON / XML / CSV          |
             | Syslog / CEF / LEEF       |
             | Key=Value / Plain text    |
             +-------------┬-------------+
                           │
                           ▼
             +---------------------------+
             | Parser Engine / Registry  |
             | Deterministic Parsers     |
             +-------------┬-------------+
                           │
                    Known Source?
                     /         \
                   YES          NO
                    │            │
                    │            ▼
                    │    AI Onboarding Engine
                    │    (Local SLM Qwen 3B/4B)
                    │            │
                    │    Schema Inference &
                    │    Parser Spec Generation
                    │            │
                    │    Compiler & Registry
                    └────────────┤
                                 ▼
                     +-----------------------+
                     | ULPF-IR v1.0 Model    |
                     | Universal Canonical   |
                     +-----------┬-----------+
                                 │
                   ┌─────────────┴─────────────┐
                   ▼                           ▼
            RAW EVENT STORE           FIELD PROVENANCE
             (SHA-256 Hash)            (Attribution)
                   │                           │
                   └─────────────┬─────────────┘
                                 ▼
                    +--------------------------+
                    | Schema Exporters         |
                    | OCSF v1.1.0 / ECS v8.x   |
                    +--------------------------+
```
