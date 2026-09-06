# ULPF Grand Finale: Top 15 Jury Questions & Answers

**Universal Log Pre-processing Framework (ULPF)**  
*SIH 26156 — National Technical Research Organisation (NTRO)*

---

### Q1: What makes ULPF different from Logstash, Vector, or Fluentbit?
**Answer**:
Existing tools are generic log shippers and forwarders. They require engineers to manually write and maintain fragile Grok/regex pipelines for every device type. If an unknown log format arrives, they either drop it or store it as an unparsed blob. Furthermore, standard shippers mutate strings without maintaining cryptographic field-level provenance.

ULPF differs in three fundamental ways:
1. **Automatic Format Agnostic Classification**: Classifies JSON, Syslog, CEF, LEEF, and Key=Value without prior configuration.
2. **Cryptographic Field-Level Provenance**: Every extracted field maintains a verifiable byte-offset and SHA-256 reference back to the immutable raw string for forensic admissibility.
3. **On-Device AI Parser Studio**: Novel or zero-day log formats are automatically parsed using an offline Small Language Model (SLM) with zero cloud dependencies.

---

### Q2: How does ULPF guarantee data integrity and chain of custody?
**Answer**:
Upon raw payload ingress, ULPF immediately computes a SHA-256 cryptographic digest before any parsing occurs:
```python
raw_hash = hashlib.sha256(raw_bytes).hexdigest()
```
The raw string is stored immutably. The normalized ULPF-IR document references this `raw_hash` and tracks exact source field bindings. At any time, an analyst or legal auditor can invoke `POST /api/v1/events/{id}/verify-integrity` to recalculate the digest over the raw store and verify that zero bytes have been tampered with.

---

### Q3: Why does ULPF use a local Small Language Model (SLM) instead of GPT-4 or Claude?
**Answer**:
In national security perimeters (NTRO, defense networks), logs contain highly sensitive data (internal IP subnets, firewall rule IDs, active user credentials, network topology). Sending raw logs to a commercial cloud LLM violates data sovereignty and security regulations.

ULPF runs a local, quantized 3-Billion parameter model (`Qwen2.5-Coder:3B`) completely offline on the host hardware (using CPU or local GPU VRAM). It requires zero internet access, zero API keys, and has zero data leakage risk.

---

### Q4: Does AI slow down the live 12,000 EPS ingestion pipeline?
**Answer**:
**No.** The live processing pipeline is 100% deterministic and operates on compiled regex and C-level string splitters (executing in 73 microseconds). 

The AI Parser Studio runs strictly as an **asynchronous sidecar / control-plane service**. When an unrecognized log format is detected (<0.70 confidence), it is placed in an unknown queue for AI schema synthesis. The high-speed deterministic fast path continues running without blocking. Once approved, the new parser is compiled into the deterministic registry for sub-millisecond execution.

---

### Q5: How do you prevent the AI from "hallucinating" IP addresses or security fields?
**Answer**:
ULPF uses **constrained regex extraction validation**:
1. The AI model is only tasked with producing structural regex patterns and field-binding mappings, NOT the extracted values themselves.
2. The generated parser is executed against the sample log in a sandbox testbench.
3. Extracted fields must pass strict Pydantic V2 schema validation (`IPvAnyAddress`, integer port ranges `1-65535`, standard ISO timestamps). If validation fails, the parser is rejected before human review.

---

### Q6: What is ULPF-IR and how does it relate to OCSF or ECS?
**Answer**:
**ULPF-IR** (Intermediate Representation) is our lightweight canonical event data model designed for high-performance in-memory processing. Because it retains strict taxonomy mappings, ULPF-IR can be exported seamlessly into:
* **OCSF** (Open Cybersecurity Schema Framework - Class 4001 Network Activity)
* **ECS** (Elastic Common Schema)
* **Custom SIEM JSON**

---

### Q7: What happens if OpenSearch or downstream SIEM fails?
**Answer**:
ULPF decouples parsing from dispatch. In containerized mode, Redpanda acts as a persistent streaming buffer. In standalone bare-metal mode, ULPF caches events in an append-only local storage queue. Downstream storage disconnections do not disrupt wire-speed log ingestion.

---

### Q8: How does ULPF handle malformed or corrupted log messages?
**Answer**:
ULPF enforces strict defensive parsing:
* If a log is partially malformed (e.g. valid Syslog header but broken payload), the header is normalized and the body is stored in `unparsed_payload`.
* If a port number is invalid (e.g. `port=999999`), Pydantic validation catches it, assigns `null`, logs a validation warning, and preserves the raw field in provenance.
* The original raw log is always preserved byte-for-byte with status `PARTIAL_PARSE` or `UNPARSED`.

---

### Q9: Can malicious actors exploit ULPF with ReDoS (Regex Denial of Service) attacks?
**Answer**:
ULPF mitigates ReDoS through three layers of defense:
1. **Atomic & Possessive Regular Expressions**: Core parsers avoid nested quantifiers.
2. **Payload Size Caps**: `MAX_LOG_PAYLOAD_BYTES=10485760` (10 MB) rejects oversized payloads at the HTTP/Syslog gateway.
3. **Execution Timeout**: Regex matching runs with strict CPU cycle timeouts.

---

### Q10: How does ULPF scale to 100,000+ Events Per Second?
**Answer**:
* **Scale-Up**: Multi-process Uvicorn workers utilizing all CPU cores (e.g. 8 workers on an 8-core CPU achieve ~95,000 EPS).
* **Scale-Out**: Stateless ULPF worker containers running behind an NGINX/HAProxy load balancer or consuming partitioned topics from Redpanda/Kafka.

---

### Q11: How do you handle log sources sending logs from behind NAT or spoofed IPs?
**Answer**:
ULPF distinguishes between the **Transport Peer IP** (the socket connection IP recorded by the collector) and the **Header Source IP** (the IP declared inside the log payload). Both are preserved independently in the ULPF-IR metadata to allow SOC analysts to correlate proxy chains and detect IP spoofing.

---

### Q12: Can an analyst block malicious or flooding log sources in real-time?
**Answer**:
Yes. The **Log Sources** management module provides real-time IP-level ingestion controls. If a source IP is detected flooding or sending malicious probes, clicking **`[Block Source]`** drops incoming packets from that IP at the gateway before they consume parsing resources.

---

### Q13: What hardware is required to run ULPF in a tactical defense deployment?
**Answer**:
* **Minimum**: 4-core CPU, 4 GB RAM, 2 GB SSD (runs core engine at ~12,000 EPS with quantized CPU SLM).
* **Recommended**: Intel i7 / AMD Ryzen 7, 16 GB RAM, NVIDIA RTX GPU with 6GB VRAM (allows <1s AI parser generation).

---

### Q14: Is ULPF compliant with defense air-gap requirements?
**Answer**:
**Yes, 100%.** ULPF has zero external network calls, zero analytics beacons, zero telemetry, and ships with all dependencies and model weights pre-cacheable on offline media.

---

### Q15: How long does it take for a judge or evaluator to test ULPF?
**Answer**:
Under 3 minutes:
1. Click **`[🎬 Start 3-Minute Demo]`** in the UI.
2. Ingest an 8-vendor burst in the **Multi-Vendor Lab**.
3. Inspect field provenance and verify SHA-256 integrity in **Event Explorer**.
4. Test AI regex generation in the **AI Parser Studio**.
5. Observe the verified 12,594 EPS performance metrics in **System Health**.
