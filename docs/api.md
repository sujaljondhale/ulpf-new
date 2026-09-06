# ULPF REST API Specification

**Universal Log Pre-processing Framework (ULPF)**  
*SIH 26156 — National Technical Research Organisation (NTRO)*

---

## Base URL
```
http://127.0.0.1:8000
```
Interactive Swagger / OpenAPI UI: `http://127.0.0.1:8000/docs`

---

## 1. System Health & Readiness

### `GET /health`
Liveness check returning overall system health and component statuses.

**Response `200 OK`**:
```json
{
  "status": "healthy",
  "version": "1.0.0-SIH26156",
  "components": {
    "api": "healthy",
    "parsers": "loaded",
    "local_store": "active",
    "opensearch": "simulated_or_connected",
    "ai_engine": "ready_offline"
  }
}
```

---

### `GET /health/ready`
Readiness probe verifying that all core pipelines and deterministic parsers are initialized and ready to ingest events.

**Response `200 OK`**:
```json
{
  "ready": true,
  "loaded_parsers": 7,
  "queue_depth": 0,
  "active_collectors": ["http", "syslog_udp_514", "file_watcher"]
}
```

---

## 2. Core Log Ingestion & Processing

### `POST /process`
Primary high-speed single-log processing endpoint. Executes format detection, parsing, ULPF-IR normalization, and provenance tracking.

**Request**:
```json
{
  "log": "CEF:0|PaloAlto|PAN-OS|10.1|THREAT|vulnerability|9|src=192.168.1.50 dst=10.0.0.1 spt=49152 dpt=80 proto=tcp act=block"
}
```

**Response `200 OK`**:
```json
{
  "status": "success",
  "detection": {
    "format": "CEF",
    "confidence": 0.99,
    "reason": "CEF header pattern detected"
  },
  "normalized_event": {
    "event": {
      "id": "ULPF-2026-9812",
      "timestamp": "2026-09-06T11:45:00.000Z",
      "category": "network",
      "action": "block"
    },
    "source": { "ip": "192.168.1.50", "port": 49152 },
    "destination": { "ip": "10.0.0.1", "port": 80 },
    "network": { "transport": "tcp" },
    "device": { "vendor": "PaloAlto", "product": "PAN-OS" }
  },
  "provenance": {
    "source.ip": {
      "original_field": "src",
      "original_value": "192.168.1.50",
      "parser": "cef",
      "confidence": 1.0
    }
  },
  "raw_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae"
}
```

---

### `POST /detect`
Performs standalone format classification without complete normalization.

**Request**:
```json
{ "log": "<134>1 2026-09-06T11:45:00Z firewall.corp - - - id=firewall proto=udp src=10.1.1.1 dst=8.8.8.8" }
```

**Response `200 OK`**:
```json
{
  "format": "Syslog",
  "confidence": 0.95,
  "reason": "RFC 5424 PRI header detected"
}
```

---

### `POST /parse`
Extracts raw tokenized fields without taxonomy mapping.

---

### `POST /normalize`
Maps structured dictionaries to standard ULPF-IR schemas.

---

## 3. Events & Forensics Integrity

### `GET /api/v1/events`
Query recent events with filtering by vendor, severity, format, or search query.

**Query Parameters**:
* `limit` (default: 50)
* `vendor` (e.g. `Fortinet`, `Cisco`, `Palo Alto`)
* `severity` (e.g. `HIGH`, `CRITICAL`, `LOW`)
* `q` (free-text search)

---

### `POST /api/v1/events/{event_id}/verify-integrity`
Performs cryptographic SHA-256 tamper-evident integrity verification. Recalculates the digest against the stored raw message byte payload.

**Response `200 OK`**:
```json
{
  "event_id": "ULPF-2026-1001",
  "is_valid": true,
  "status": "VERIFIED_TAMPER_EVIDENT",
  "stored_hash": "8f481f185c7c975a8940b5d5d8523c14828b030b42f6381084221a719d3f1107",
  "computed_hash": "8f481f185c7c975a8940b5d5d8523c14828b030b42f6381084221a719d3f1107",
  "byte_length": 142,
  "verified_at": "2026-09-06T11:45:30.120Z",
  "verification_details": "Cryptographic SHA-256 digest matches raw payload byte-for-byte."
}
```

---

## 4. Multi-Vendor Lab & Simulated Devices

### `POST /api/v1/demo/traffic/multivendor`
Generates real-time heterogeneous log streams across 8 enterprise vendors:
* Fortinet FortiGate Firewall
* Cisco Secure Router (IOS-XE)
* Palo Alto Next-Gen Firewall
* Windows Security Event Log
* Linux SSH / Auth Daemon
* Pulse Secure / Ivanti VPN Gateway
* Snort / Suricata Network IDS
* AWS CloudTrail / GuardDuty JSON

**Request**:
```json
{
  "vendor": "all",
  "burst_count": 8,
  "simulate_latency": true
}
```

---

## 5. AI Parser Studio & Unknown Logs

### `GET /api/v1/unknown-logs`
Retrieve logs with confidence score < 0.70 queued for AI onboarding.

### `POST /api/v1/ai/generate-parser`
Infers regex and schema fields for an unknown log format using local SLM.

### `POST /api/v1/ai/approve-parser`
Promotes a verified AI-generated parser into the active deterministic parser registry.

---

## 6. Source Management & Security

### `GET /api/v1/sources`
Lists all monitored IP endpoints with health, EPS, and block status.

### `POST /api/v1/sources/block`
Blocks an offending source IP address from ingesting logs.

**Request**:
```json
{ "ip": "198.51.100.44", "reason": "DDoS log flooding detected" }
```

### `POST /api/v1/sources/unblock`
Restores ingestion for a blocked source IP.
