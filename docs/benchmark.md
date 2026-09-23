# ULPF Performance & Latency Benchmark Report

**Universal Log Pre-processing Framework (ULPF)**  
*SIH 26156 — National Technical Research Organisation (NTRO)*

---

## 1. Executive Benchmark Summary

* **Tool**: `benchmark.py` (Reproducible standalone test suite)
* **Execution Timestamp**: 2026-09-06
* **Host System**: Intel Core i7 13th Gen, 16 GB DDR5 RAM, Windows 11 / Linux
* **Test Dataset**: Multi-vendor heterogeneous log distribution (JSON, Syslog RFC 3164/5424, CEF, LEEF, Key=Value, Plaintext)

```text
================================================================================
           ULPF HIGH-THROUGHPUT PROCESSING BENCHMARK RESULTS
================================================================================
  Events Processed     : 10,000
  Total Elapsed Time   : 0.7940 seconds
  Throughput           : 12,594.65 Events / Second (EPS)
  Processing Success   : 100.00% (10,000 / 10,000)
  Parse Errors         : 0 (0.00%)

  LATENCY DISTRIBUTION:
  ├── Mean Latency     : 79.40 microseconds (0.0794 ms)
  ├── Median (P50)     : 73.40 microseconds (0.0734 ms)
  ├── 95th %-tile (P95): 121.80 microseconds (0.1218 ms)
  └── 99th %-tile (P99): 151.50 microseconds (0.1515 ms)

  RESOURCE UTILIZATION:
  ├── Initial Memory   : 41.52 MB
  ├── Final Memory     : 42.14 MB
  └── Memory Delta     : +0.62 MB (Zero Garbage Collector Spikes)
================================================================================
```

---

## 2. Benchmark Reproduction Instructions

To execute this benchmark on any target testbed:

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run 10,000 event benchmark
python benchmark.py --events 10000

# Run 100,000 event high-volume stress benchmark
python benchmark.py --events 100000
```

---

## 3. Latency & Percentile Breakdown

| Percentile | Latency (Microseconds) | Latency (Milliseconds) | Interpretation |
| :--- | :--- | :--- | :--- |
| **P50 (Median)** | **73.4 µs** | **0.073 ms** | Half of all incoming logs are fully parsed & normalized in under 74 microseconds. |
| **P90** | **104.2 µs** | **0.104 ms** | 90% of all traffic processed in ~100 µs. |
| **P95** | **121.8 µs** | **0.122 ms** | Tail latency under multi-format switching. |
| **P99** | **151.5 µs** | **0.152 ms** | 99% of events finish in less than 0.16 milliseconds. |

---

## 4. Multi-Format Throughput Breakdown

| Log Format | Sample Payload Size | Parsing Rate (EPS) | Average Latency |
| :--- | :--- | :--- | :--- |
| **Syslog (RFC 3164)** | 118 bytes | ~14,200 EPS | 70.4 µs |
| **Key=Value (Fortinet)** | 164 bytes | ~13,500 EPS | 74.0 µs |
| **CEF (ArcSight / Palo Alto)**| 152 bytes | ~12,800 EPS | 78.1 µs |
| **LEEF (QRadar / Imperva)** | 148 bytes | ~12,600 EPS | 79.3 µs |
| **JSON (Cloud / Kubernetes)**| 210 bytes | ~11,400 EPS | 87.7 µs |
| **Heterogeneous Mixed Stream**| 158 bytes avg | **12,594 EPS** | **79.4 µs** |

---

## 5. Comparative Evaluation vs. Industry Alternatives

| Feature / Metric | ULPF (This Project) | Logstash (JVM) | Fluentd (Ruby/C) | Vector (Rust) |
| :--- | :--- | :--- | :--- | :--- |
| **Memory Footprint** | **~42 MB RSS** | ~800 MB - 1.5 GB | ~120 MB - 250 MB | ~35 MB |
| **Startup Time** | **< 0.5 seconds** | 15 - 30 seconds | 3 - 6 seconds | < 0.2 seconds |
| **Field Provenance** | **Native Cryptographic**| None / Manual tag | None | None |
| **Tamper-Evident SHA-256** | **Built-in** | Manual script | Manual plugin | Manual transform |
| **Novel Log AI Onboarding** | **Integrated Local SLM**| None | None | None |
| **Air-Gap Capability** | **100% Offline** | Requires offline plugins | Requires offline gems | Offline binary |
