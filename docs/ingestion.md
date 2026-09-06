# ULPF Ingestion Architecture

**Universal Log Pre-processing Framework — Phase 8: Real Network Log Collectors & Streaming Ingestion**

---

## Overview

ULPF acts as a real preprocessing gateway between enterprise network devices and downstream SIEM/analytics systems:

```
Firewall / Router / VPN / IDS / Proxy
              ↓
      Network Log Collector
     (UDP 5140 | TCP 5141 | REST 8000)
              ↓
        Ingestion Queue
      (rate-limited, backpressured)
              ↓
       Processing Pipeline
     (detect → parse → normalize)
              ↓
     Storage + Analytics
   (MinIO raw | OpenSearch canonical)
```

---

## Collector Components

### 1. Syslog UDP Collector (Port 5140)

**RFC 3164 (BSD Syslog) and RFC 5424 (IETF Structured Syslog)**

Listens on `0.0.0.0:5140` for UDP datagrams from firewalls, routers, switches, and VPN concentrators.

**Characteristics:**
- Non-blocking socket with `select.select()` (0.5s timeout) for clean shutdown
- Handles up to 65,535-byte datagrams
- Decodes with `errors="replace"` — malformed/binary payloads never crash the listener
- Each packet becomes an immutable `RawIngress` object with SHA-256 hash computed before any parsing
- Fires to `IngestionQueue` (backpressured) or direct `event_callback`

**Example RFC 3164:**
```
<34>Oct 11 22:14:15 mymachine su: 'su root' failed for lonvick on /dev/pts/8
```

**Example RFC 5424:**
```
<165>1 2026-09-06T12:34:56.789Z fw.corp FIREWALL 4242 ID47 [origin ip="10.0.0.1"] TCP BLOCKED src=192.168.1.5 dst=8.8.8.8
```

**Testing:**
```bash
python scripts/send_syslog.py --protocol udp --host localhost --port 5140 --count 100 --rate 10
```

---

### 2. Syslog TCP Collector (Port 5141)

**Multi-client stream with newline and octet-count framing**

Listens on `0.0.0.0:5141` for persistent TCP streams from enterprise devices sending continuous syslog streams.

**Characteristics:**
- `select.select()` accept loop with per-client threads
- Per-client receive buffer handles fragmented packets across multiple `recv()` calls
- Supports newline-delimited (`\n`) and octet-counting framing transparently
- Persistent connections remain open until client disconnects or server stops
- Handles `ConnectionResetError` / `socket.timeout` gracefully per client

**Example connection:**
```bash
# Using netcat
echo "<134>1 2026-09-06T12:00:01Z fw01 app1 100 - - TCP test event" | nc localhost 5141
```

**Testing:**
```bash
python scripts/send_syslog.py --protocol tcp --host localhost --port 5141 --count 50 --rate 5
```

---

### 3. Syslog TLS Architecture (Port 6514)

TLS-encrypted syslog support is architecturally prepared. Configuration options:

```ini
SYSLOG_TLS_ENABLED=true
SYSLOG_TLS_PORT=6514
SYSLOG_TLS_CERT_FILE=/certs/server.crt
SYSLOG_TLS_KEY_FILE=/certs/server.key
SYSLOG_TLS_CA_FILE=/certs/ca.crt
```

In the current prototype, UDP (5140) and TCP (5141) collectors are active. TLS wrapping is implemented by passing an `ssl.SSLContext` to the TCP collector's socket.

---

### 4. REST Ingestion API (Port 8000)

**POST /api/v1/ingest**

Submit individual logs via HTTP POST. Supports JSON body or raw text.

**Request (JSON):**
```json
{
  "raw_log": "CEF:0|CheckPoint|Firewall|1|100|Accept|7|src=1.2.3.4 dst=5.6.7.8",
  "vendor": "CheckPoint",
  "product": "FireWall-1",
  "format_hint": "cef",
  "source": "fw-01"
}
```

**Response:**
```json
{
  "status": "success",
  "event_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "raw_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "detected_format": "CEF",
  "forwarded": true
}
```

**POST /api/v1/ingest/batch**

Submit up to 1000 logs in a single request:
```json
{
  "logs": ["log line 1", "log line 2"],
  "source": "batch-client"
}
```

**GET /api/v1/collectors/metrics**

Real-time telemetry for all collectors:
```json
{
  "status": "online",
  "total_received_all_connectors": 15000,
  "total_processed_all_connectors": 14987,
  "syslog_collector": { "udp_listener": {...}, "tcp_listener": {...} },
  "file_collector": { "watched_files_count": 3, ... },
  "ingestion_queue": { "queue_depth": 12, "total_enqueued": 15000, ... }
}
```

---

### 5. File Tail Collector

Monitors a directory for `*.log` files, tails newly appended lines, and tracks byte offsets across restarts.

**Configuration:**
```ini
FILE_WATCH_DIR=/app/storage/logs
```

**Behavior:**
- Scans `watch_dir` for `*.log` files every ~1 second
- Tracks file offset (byte position) per file
- **Rotation detection:** If current file size < last known offset, or inode changes → reset offset to 0
- Each new line becomes a `RawIngress(connector_type="file_tail")` event
- Files can be added dynamically at runtime via `collector.watch_file(path)`

---

## RawIngress Data Model

Every log event from any transport is immediately wrapped in a `RawIngress` object:

```python
class RawIngress(BaseModel):
    event_id: str           # UUID (auto-generated)
    connector_type: str     # "syslog_udp" | "syslog_tcp" | "rest" | "file_tail"
    source: str             # "client_ip:port" or "file:/path/app.log"
    received_at: str        # ISO-8601 UTC timestamp
    raw_text: str           # Verbatim original log (NEVER modified)
    raw_sha256: str         # SHA-256 of raw_text (auto-computed)
    transport_metadata: dict  # Protocol-specific metadata
    vendor_hint: str        # Optional: "Cisco", "Palo Alto"
    product_hint: str       # Optional: "ASA", "PAN-OS"
    format_hint: str        # Optional: "cef", "leef", "syslog"
```

> **Forensic guarantee:** `raw_text` is stored exactly as received, byte-for-byte, before any decoding, parsing, or normalization step. SHA-256 is computed from this verbatim content.

---

## Ingestion Queue & Backpressure

The `IngestionQueue` buffers events between network collectors and the processing pipeline.

**Parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_size` | 50,000 | Maximum queue depth before backpressure |
| `max_eps` | 25,000 | Maximum events/second (sliding window) |
| `worker_count` | 2 | Worker threads consuming from queue |

**Rate limiting algorithm:** Sliding 1-second window. Events exceeding `max_eps` are dropped with reason `RATE_LIMIT_EXCEEDED`. Full queue drops with `QUEUE_FULL_BACKPRESSURE`.

**Metrics (`GET /api/v1/collectors/metrics → ingestion_queue`):**
```json
{
  "queue_depth": 42,
  "max_queue_size": 50000,
  "max_eps_limit": 25000,
  "total_enqueued": 100000,
  "total_processed": 99958,
  "total_dropped_rate_limit": 0,
  "total_dropped_backpressure": 42
}
```

---

## Source Registry

The `SourceRegistry` tracks all connected network devices:

```
GET /api/v1/sources
POST /api/v1/sources/{source_id}/block
```

Each source record includes:
- `source_id`, `name`, `vendor`, `protocol`, `address`
- `events_received`, `events_per_sec`, `last_seen`
- `status`: `ACTIVE | READY | BLOCKED`
- `is_blocked`: Toggle to accept/deny events from this source

---

## Docker Port Mappings

```yaml
# docker-compose.yml
ulpf-api:
  ports:
    - "8000:8000"       # HTTP API + Web Dashboard
    - "5140:5140/udp"   # Syslog UDP (RFC 3164 / RFC 5424)
    - "5141:5141"       # Syslog TCP (persistent streams)
```

After `docker compose up --build`:

| Service | URL |
|---------|-----|
| Dashboard | http://localhost:8000/dashboard/index.html |
| API Docs | http://localhost:8000/docs |
| Syslog UDP | `udp://localhost:5140` |
| Syslog TCP | `tcp://localhost:5141` |
| MinIO Console | http://localhost:9001 |
| OpenSearch | http://localhost:9200 |

---

## Network Traffic Simulator

```bash
# Send 100 UDP syslog events at 10 EPS
python scripts/send_syslog.py --protocol udp --host localhost --port 5140 --count 100 --rate 10

# Send TCP stream burst
python scripts/send_syslog.py --protocol tcp --host localhost --port 5141 --count 500 --rate 50

# Send multi-vendor mix
python scripts/send_syslog.py --vendor cisco --count 50
python scripts/send_syslog.py --vendor palo_alto --count 50
python scripts/send_syslog.py --vendor suricata --count 50
```

---

## Scale-Out: Redpanda / Kafka Mode

For production deployments exceeding 25,000 EPS, ULPF can be configured to publish `RawIngress` objects to a Redpanda/Kafka topic instead of the local queue:

```ini
REDPANDA_BROKERS=redpanda:9092
REDPANDA_TOPIC=ulpf-raw-ingress
```

When `REDPANDA_BROKERS` is set, the `IngestionQueue` publishes to Kafka instead of the local in-process queue. Multiple ULPF worker instances can then consume from the same topic for horizontal scaling.

---

## Testing

```bash
# Unit + integration tests (10 tests covering all collectors)
pytest tests/test_network_collectors.py -v

# Full suite (53 tests)
pytest

# Live network simulator
python scripts/send_syslog.py --count 200 --rate 20
```
