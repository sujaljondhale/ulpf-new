# ULPF (Universal Log Pre-processing Framework) - Enterprise Deployment Guide

This guide details how to deploy, operate, scale, and monitor the ULPF distributed microservices stack across local workstations, cloud virtual machines (**Oracle Cloud Infrastructure (OCI)**, AWS EC2, Azure, GCP, DigitalOcean), and enterprise container environments.

---

## 1. System Requirements & Architecture

### Minimum Production Specifications
- **CPU**: 2 vCPUs minimum (4+ vCPUs recommended for > 10,000 EPS).
- **Memory**: 4 GB RAM minimum (8 GB+ recommended). *Note: OCI Ampere A1 (4 OCPU / 24 GB RAM) is ideal.*
- **Disk Storage**: 20 GB SSD minimum for raw immutable evidence (MinIO) and WAL streaming logs (Redpanda).
- **OS**: Linux (Ubuntu 20.04/22.04/24.04 LTS, Oracle Linux 8/9, Debian 12, RHEL 9), macOS, or Windows with Docker Desktop (WSL 2).

### Core Microservices Topology
| Container Service | Base Image | Internal Port | Host Port | Role |
| :--- | :--- | :--- | :--- | :--- |
| **`ulpf-api`** | `ulpf-ulpf-api:latest` | `8000`, `5140/udp`, `5141` | `8000`, `5140/udp`, `5141` | Ingestion Gateway, Schema Normalizer, SOC UI |
| **`ulpf-simulator`**| `ulpf-ulpf-simulator:latest` | `8050` | `8050` | Virtual Device Simulator & Testbed Studio |
| **`ulpf-worker`** | `ulpf-ulpf-worker:latest` | Internal | None | Distributed Redpanda Kafka consumer & batch processor |
| **`redpanda`** | `redpandadata/redpanda:v23.3.14`| `9092`, `19092`, `9644` | `9092`, `19092`, `9644` | High-throughput streaming bus (~400MB RAM) |
| **`redpanda-init`**| `redpandadata/redpanda:v23.3.14`| Internal | None | One-shot topic provisioner (ingress, normalized, alerts) |
| **`redpanda-console`**| `redpandadata/console:v2.4.5` | `8080` | `8085` | Live Kafka stream, topic, and partition visualizer |
| **`redis`** | `redis:7.2-alpine` | `6379` | `6379` | High-speed cache, rate limiter & message broker |
| **`minio`** | `minio/minio:latest` | `9000`, `9001` | `9000`, `9001` | S3-compatible raw evidence storage & web console |
| **`opensearch`** | `opensearchproject/opensearch:2.11.1`| `9200` | `9200` | Search & analytics cluster (Optional profile) |
| **`ulpf-ai`** | `ulpf-ai:latest` | `11434` | `11434` | Sovereign local LLM / Ollama engine (Optional profile)|

---

## 2. Fast-Track Deployment

### Option A: Universal Direct Docker Compose (Recommended)
Everything is self-bootstrapping and self-initializing:
```bash
# 1. (Optional) Create .env from template if not already present
cp .env.example .env

# 2. Start the entire microservice stack
docker compose up -d
```
*All images (`alpine/minio:latest-release`, `redis:7.2-alpine`, `redpandadata/redpanda:v23.3.14`, `opensearchproject/opensearch:2.11.1`, and local microservices) pull and build automatically.*
*Redpanda streaming topics (`ulpf-raw-ingress`, `ulpf-events-normalized`, `ulpf-alerts`) and MinIO storage bucket (`ulpf-raw`) are auto-created on startup.*

---

### Option B: Linux / Cloud VM Script (Automated Bash)
```bash
chmod +x deploy.sh
./deploy.sh
```

---

### Option C: Windows (PowerShell)
```powershell
.\deploy.ps1
```

---

## 3. Oracle Cloud Specific Best Practices

### A. Ampere A1 (ARM64) Compatibility
All ULPF microservices and container images (`python:3.12-slim`, `redpandadata/redpanda`, `redpandadata/console`, `redis:7.2-alpine`, `alpine/minio:latest-release`, `opensearchproject/opensearch`) natively provide multi-arch ARM64 / aarch64 images. No code changes or cross-compilation are required when running on Oracle Cloud Ampere A1.

### B. Host OS Firewall & OCI Security Lists
In the Oracle Cloud Console under your VCN Default Security List, add Ingress Rules for:
- TCP: `8000` (SOC UI), `8050` (Simulator), `8085` (Redpanda Console), `9001` (MinIO), `5141` (Syslog TCP)
- UDP: `5140` (Syslog UDP)

If you are on an Ubuntu OCI image, ensure host iptables allows inbound traffic:
```bash
sudo iptables -I INPUT 6 -p tcp -m multiport --dports 8000,8050,8085,9000,9001,5141 -j ACCEPT
sudo iptables -I INPUT 6 -p udp --dport 5140 -j ACCEPT
```

### C. OpenSearch Memory and `vm.max_map_count`
If using OpenSearch on Linux, ensure `vm.max_map_count` is set:
```bash
sudo sysctl -w vm.max_map_count=262144
```

### D. Managing ULPF with Systemd on OCI
```bash
# Check status
sudo systemctl status ulpf

# Stop stack
sudo systemctl stop ulpf

# Start stack
sudo systemctl start ulpf

# Restart stack
sudo systemctl restart ulpf

# View live container logs
docker compose logs -f ulpf-api
```

---

## 4. Docker Volume Persistence: Why Volumes Are Essential

Docker containers have an ephemeral file system. When a container is restarted, rebuilt, or updated, all files created inside its ephemeral layer are permanently deleted.

ULPF defines persistent named Docker volumes in `docker-compose.yml`:
```yaml
volumes:
  minio_data:
    name: ulpf_minio_data
  redpanda_data:
    name: ulpf_redpanda_data
  redis_data:
    name: ulpf_redis_data
  ulpf_metadata:
    name: ulpf_metadata_store
  opensearch_data:
    name: ulpf_opensearch_data
```

### Why Each Volume Is Required:
1. **`ulpf_minio_data`**: Stores raw, immutable S3 log payloads and SHA-256 evidence seals. Ensures regulatory audit compliance (PCI-DSS, SOC 2, HIPAA) across restarts.
2. **`ulpf_redpanda_data`**: Stores commit logs, partition segments, and consumer group offset states. Prevents message loss and reprocessing storms.
3. **`ulpf_metadata_store`**: Stores SQLite metadata, dynamic parser rules, blocked IP blacklists, and forensic analyst audit logs.
4. **`ulpf_redis_data`**: Persists Redis AOF write logs for cached rate limits and active session states.

---

## 5. How to Test and Operate Consoles

### A. Testing the Redpanda Kafka Streaming Console
- **Console URL**: `http://<VM_IP>:8085` (Local: `http://localhost:8085`)
- **Key Operations**:
  1. **Topics Tab**: Inspect `ulpf-raw-ingress`, `ulpf-events-normalized`, and `ulpf-alerts`.
  2. **Partitions**: Verify that partitions 0, 1, and 2 are in `Clean` and `Healthy` states.
  3. **Consumer Groups**: Monitor `ulpf-workers` lag.
  4. **Messages**: Live streaming log packet inspection.

### B. Testing the MinIO S3 Raw Storage Console
- **Console URL**: `http://<VM_IP>:9001` (Local: `http://localhost:9001`)
- **Default Credentials**: Username: `ulpf_admin` | Password: `ulpf_password_2026`
- **Key Operations**:
  1. **Buckets**: Open `ulpf-raw`.
  2. **Object Browser**: Inspect events partitioned by date: `events/YYYY/MM/DD/[event_id].raw`.
  3. **Integrity Metadata**: Check `x-amz-meta-sha256` hash seal.

---

## 6. Horizontal Scale-Out (High-Load Tuning)

When incoming traffic surges past 25,000 events per second, scale out the distributed parsing workers with zero downtime:
```bash
docker compose up -d --scale ulpf-worker=4
```
Redpanda will automatically rebalance the partitions across all 4 worker instances.

---

## 7. Operational Troubleshooting

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| Cannot connect from browser to VM IP | OCI Security List or host firewall blocking ports | Ensure VCN Security List has Ingress rules for TCP 8000, 8050, 8085, 9001. Open host iptables / firewalld ports. |
| OpenSearch exits with code 137 / fatal error | `vm.max_map_count` is too low | Run `sudo sysctl -w vm.max_map_count=262144`. |
| Out of memory (OOM) during build on 1GB VM | Swap space not configured | Create swap: `sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`. |
| `ulpf-worker` not consuming | Redpanda topic does not exist | Run `docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress`. |
| MinIO upload fails | Bucket `ulpf-raw` not initialized | Auto-initialized by `ulpf-api` on startup or run `curl -X PUT http://localhost:9000/ulpf-raw`. |
| Simulator socket probe fails to resolve API | Linux Docker split-horizon DNS | Ensured `extra_hosts` and `ULPF_INTERNAL_API_HOST=ulpf-api` are set in `docker-compose.yml`. |
