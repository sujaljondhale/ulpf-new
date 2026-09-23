# ULPF 3-Minute Live Jury Demo Script

**Universal Log Pre-processing Framework (ULPF)**  
*SIH 26156 — National Technical Research Organisation (NTRO)*

---

##  Overview & Timing

| Step | Duration | Target Screen | Core Message |
| :--- | :--- | :--- | :--- |
| **1. The Problem** | 0:00 - 0:30 | **Multi-Vendor Lab** | Perimeter devices output 8+ incompatible formats. Current SIEMs choke. |
| **2. Deterministic Pipeline** | 0:30 - 1:00 | **Multi-Vendor Lab** | ULPF unifies all 8 formats into one canonical schema at 12,000+ EPS. |
| **3. Forensic Provenance** | 1:00 - 1:30 | **Event Explorer** | 100% field traceability and cryptographic SHA-256 tamper evidence. |
| **4. Unknown Log AI Onboarding** | 1:30 - 2:15 | **AI Parser Onboarding** | Zero-downtime parser creation using local, offline SLM. |
| **5. Parser Testbench & Schema** | 2:15 - 2:45 | **Parser Testbench** | Live regex verification and instant dynamic promotion. |
| **6. Health & Performance Proof** | 2:45 - 3:00 | **System Health** | Measured 12,594 EPS, 73µs P50 latency, 100% offline & air-gapped. |

---

##  Step-by-Step Script

### Step 1: Multi-Vendor Ingestion (0:00 - 0:30)
* **Action**: In the top header bar, click **`[ Start 3-Minute Demo]`** (or navigate to `Processing → Multi-Vendor Lab`).
* **Click**: Click **` Ingest Heterogeneous Burst (8 Vendors)`**.
* **Say**:
  > *"Judges, in national security perimeters, every vendor outputs logs differently—Cisco uses Syslog, Palo Alto uses CEF, IBM uses LEEF, Fortinet uses Key=Value, and AWS uses JSON. Watch as we ingest all 8 disparate vendor streams simultaneously into ULPF."*

---

### Step 2: Canonical Normalization Proof (0:30 - 1:00)
* **Action**: Point to the **Comparison Matrix** table below the generator.
* **Point out**:
  * Show that `Source IP`, `Dest IP`, `Action`, and `Severity` are 100% normalized across Fortinet, Cisco, Palo Alto, Linux, and Windows.
* **Say**:
  > *"Notice that despite vastly different raw formats, every single event is instantly transformed into our canonical ULPF-IR schema without dropping a single byte of evidence."*

---

### Step 3: Forensic Traceability & SHA-256 Verification (1:00 - 1:30)
* **Action**: Navigate to `Explorer → Event Explorer` (or click Next Step in the demo guide).
* **Action**: Click the **`[Inspect]`** button on any Fortinet or Palo Alto event.
* **Action**: Scroll down to the **Tamper-Evident Integrity** card and click **` Verify SHA-256 Integrity`**.
* **Say**:
  > *"For digital forensics and legal admissibility, ULPF never modifies the raw log. We compute a cryptographic SHA-256 hash upon ingress. Notice the field provenance graph showing exactly which raw byte slice populated which normalized field."*

---

### Step 4: Unknown Log Handling & AI Parser Studio (1:30 - 2:15)
* **Action**: Navigate to `AI Engine → AI Parser Onboarding`.
* **Action**: Click on the pending proprietary log (e.g., Industrial SCADA / Custom Microservice log).
* **Action**: Click **` Generate Dynamic Parser (Local AI)`**.
* **Say**:
  > *"When a novel or zero-day device format arrives, traditional SIEMs drop it or fail. ULPF routes it to our sovereign, offline AI Parser Studio powered by an on-device Small Language Model. It automatically infers the regex pattern and field bindings in seconds."*

---

### Step 5: Parser Testbench & Promotion (2:15 - 2:45)
* **Action**: Review the generated regex, then click **` Approve & Register Parser`**.
* **Action**: Navigate to `AI Engine → Parser Registry` to show the newly activated parser running deterministically.
* **Say**:
  > *"The human analyst reviews the diff and approves it. The parser is instantly registered into the live deterministic engine with zero restarts and zero downtime."*

---

### Step 6: Verified Benchmarks & System Health (2:45 - 3:00)
* **Action**: Navigate to `System → System Health`.
* **Say**:
  > *"ULPF processes over 12,500 events per second with a P50 latency of just 73 microseconds on standard hardware, with zero cloud dependencies. It is 100% offline, air-gap ready, and engineered for high-consequence defense perimeters."*
