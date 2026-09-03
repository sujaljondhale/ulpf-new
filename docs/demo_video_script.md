# ULPF — 2-Minute Demo Video Script & Storyboard

**SIH Problem ID:** SIH 26156 (NTRO)  
**Target Duration:** 2 Minutes (120 Seconds)

---

## Video Scene Breakdown

### Scene 1: Problem Statement & Vision (0:00 – 0:20)
- **Visual**: Screen capture of chaotic, multi-vendor raw logs (CEF, Syslog, JSON, Key=Value) flashing rapidly.
- **Voiceover**: "In modern defense and enterprise networks, log ingestion is broken. Millions of heterogeneous events arrive every second in conflicting formats. Security teams waste months building custom parsers. Welcome to ULPF—the Universal Log Pre-processing Framework built for NTRO."

### Scene 2: High-Speed Ingestion & ULPF-IR (0:20 – 0:45)
- **Visual**: Web Dashboard UI (`http://127.0.0.1:8000/dashboard`). Paste a raw CEF firewall log and click **Process Log**.
- **Voiceover**: "ULPF deterministically detects 8 major log formats in microseconds. It generates ULPF-IR v1.0—a universal canonical representation—while preserving raw log data with SHA-256 cryptographic hashes for 100% forensic losslessness."

### Scene 3: Field Provenance & Dual Schema Export (0:45 – 1:10)
- **Visual**: Click **Field Provenance** tab on dashboard, showing visual tree mapping `source.ip <- src`. Toggle to **OCSF Export** and **ECS Export** tabs.
- **Voiceover**: "ULPF tracks field-level provenance for complete transparency—answering where every normalized field came from. It exports seamlessly to OCSF v1.1.0 and Elastic Common Schema out of the box."

### Scene 4: Local AI Unknown Log Onboarding (1:10 – 1:40)
- **Visual**: Paste custom unknown firewall log samples into the **AI Onboarding Studio**. Click **Analyze with Local AI**. Show generated YAML spec, click **Compile**, then **Approve**.
- **Voiceover**: "When an unknown log arrives, ULPF uses an on-device local SLM—Qwen 3B running 100% offline via Ollama. It infers structure, compiles a YAML parser spec, and registers a deterministic production parser in seconds."

### Scene 5: Benchmark & Air-Gapped Docker Conclusion (1:40 – 2:00)
- **Visual**: Show benchmark summary table (13,670+ events/sec, 31MB RAM) and Docker Compose deployment (`docker-compose up -d`).
- **Voiceover**: "ULPF processes over 13,600 events per second with just 31 megabytes of memory. Containerized, air-gapped, and ready for deployment. ULPF: Universal, Lossless, Ultra-Fast."
