# ULPF (Universal Log Pre-processing Framework) - Enterprise Deployment Guide

This guide details how to deploy, operate, scale, and monitor the ULPF distributed microservices stack across local workstations, cloud virtual machines (AWS EC2, Azure, GCP, DigitalOcean), and enterprise container environments.

---

## 1. System Requirements & Architecture

### Minimum Production Specifications
- **CPU**: 2 vCPUs minimum (4+ vCPUs recommended for > 10,000 EPS).
- **Memory**: 4 GB RAM minimum (8 GB+ recommended).
- **Disk Storage**: 20 GB SSD minimum for raw immutable evidence (MinIO) and WAL streaming logs (Redpanda).
- **OS**: Linux (Ubuntu 22.04/24.04 LTS, Debian 12, RHEL 9), macOS, or Windows with Docker Desktop (WSL 2).

### Core Microservices Topology
| Container Service | Base Image | Internal Port | Host Port | Role |
| :--- | :--- | :--- | :--- | :--- |
| **`ulpf-api`** | `ulpf-ulpf-api:latest` | `8000`, `5140/udp`, `5141` | `8000`, `5140/udp`, `5141` | Ingestion Gateway, Schema Normalizer, SOC UI |
| **`ulpf-simulator`**| `ulpf-ulpf-simulator:latest` | `8050` | `8050` | Virtual Device Simulator & Testbed Studio |
| **`ulpf-worker`** | `ulpf-ulpf-worker:latest` | Internal | None | Distributed Redpanda Kafka consumer & batch processor |
| **`redpanda`** | `redpandadata/redpanda:v23.3.14`| `9092`, `19092`, `9644` | `9092`, `19092`, `9644` | High-throughput streaming bus (~400MB RAM) |
| **`redpanda-console`**| `redpandadata/console:v2.4.5` | `8080` | `8085` | Live Kafka stream, topic, and partition visualizer |
| **`minio`** | `quay.io/minio/minio:latest` | `9000`, `9001` | `9000`, `9001` | S3-compatible raw evidence storage & web console |
| **`opensearch`** | `opensearchproject/opensearch:2.11.1`| `9200` | `9200` | Search & analytics cluster (Optional profile) |
| **`ulpf-ai`** | `ulpf-ai:latest` | `11434` | `11434` | Sovereign local LLM / Ollama engine (Optional profile)|

---

## 2. Fast-Track Deployment

### Option A: Windows (PowerShell)
Run the automated deployment script in PowerShell from the project root:
```powershell
.\deploy.ps1
```

### Option B: Linux / Cloud VM (Bash)
Make the script executable and execute:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option C: Manual Docker Compose
```bash
# 1. Build local container images
docker compose build ulpf-api ulpf-worker ulpf-simulator

# 2. Start core services in detached background mode
docker compose up -d minio redpanda redpanda-console ulpf-worker ulpf-api ulpf-simulator

# 3. Create MinIO raw evidence bucket
docker exec ulpf-minio mc alias set local http://localhost:9000 ulpf_admin ulpf_password_2026
docker exec ulpf-minio mc mb local/ulpf-raw

# 4. Create Redpanda Kafka streaming topics
docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress ulpf-events-normalized ulpf-alerts -p 3 -r 1
```

---

## 3. Docker Volume Persistence: Why Volumes Are Essential

Docker containers have an ephemeral file system. When a container is restarted, rebuilt, or updated, all files created inside its ephemeral layer are permanently deleted.

ULPF defines persistent named Docker volumes in `docker-compose.yml`:
```yaml
volumes:
  minio_data:
    name: ulpf_minio_data
  redpanda_data:
    name: ulpf_redpanda_data
  ulpf_metadata:
    name: ulpf_metadata_store
  opensearch_data:
    name: ulpf_opensearch_data
```

### Why Each Volume Is Required:
1. **`ulpf_minio_data`**: Stores the raw, immutable S3 log payloads and SHA-256 evidence seals. Ensures regulatory audit compliance (PCI-DSS, SOC 2, HIPAA) across restarts.
2. **`ulpf_redpanda_data`**: Stores commit logs, partition segments, and consumer group offset states. Prevents message loss and reprocessing storms.
3. **`ulpf_metadata_store`**: Stores SQLite metadata, dynamic parser rules, blocked IP blacklists, and forensic analyst audit logs.

### Backing Up Volumes:
```bash
# Backup MinIO raw storage volume
docker run --rm -v ulpf_minio_data:/data -v $(pwd):/backup alpine tar czf /backup/minio_backup.tar.gz /data

# Restore MinIO raw storage volume
docker run --rm -v ulpf_minio_data:/data -v $(pwd):/backup alpine sh -c "cd /data && tar xzf /backup/minio_backup.tar.gz --strip 1"
```

---

## 4. How to Test and Operate MinIO & Redpanda Consoles

### A. Testing the Redpanda Kafka Streaming Console
- **Console URL**: [http://localhost:8085](http://localhost:8085)
- **What to do in Redpanda Console**:
  1. **Topics Tab**: Click `Topics` to inspect the 3 core pipelines: `ulpf-raw-ingress`, `ulpf-events-normalized`, and `ulpf-alerts`.
  2. **Partitions**: Verify that partition 0, 1, and 2 are in `Clean` and `Healthy` states.
  3. **Consumer Groups Tab**: Click `Consumer Groups` -> View `ulpf-workers`. Monitor the `Lag` column (should be 0 under steady state).
  4. **Messages Tab**: Click on `ulpf-raw-ingress` -> `Messages` -> Inspect streaming log packets in real time.
- **Testing via CLI**:
  ```bash
  # Send a test streaming log packet
  echo '{"raw":"CEF:0|Test|Firewall|1.0|drop|Drop|High|src=192.168.1.55"}' | docker exec -i ulpf-redpanda rpk topic produce ulpf-raw-ingress

  # Read message from the stream
  docker exec ulpf-redpanda rpk topic consume ulpf-raw-ingress -n 1
  ```

### B. Testing the MinIO S3 Raw Storage Console
- **Console URL**: [http://localhost:9001](http://localhost:9001)
- **Default Credentials**: Username: `ulpf_admin` | Password: `ulpf_password_2026`
- **What to do in MinIO Console**:
  1. **Buckets Tab**: Open `Buckets` -> Locate `ulpf-raw`.
  2. **Object Browser**: Browse objects stored hierarchically by date: `events/YYYY/MM/DD/[event_id].raw`.
  3. **Forensic Metadata**: Select any `.raw` file and click `Metadata`. Verify the immutable `x-amz-meta-sha256` integrity hash, source IP, and ingestion timestamp.
  4. **Retention Policies**: Configure object locking or retention rules for legal hold if required.
- **Testing via CLI**:
  ```bash
  # List all objects in bucket
  docker exec ulpf-minio mc ls local/ulpf-raw --recursive
  ```

---

## 5. Horizontal Scale-Out (High-Load Tuning)

When incoming traffic surges past 25,000 events per second, scale out the distributed parsing workers with zero downtime:
```bash
docker compose up -d --scale ulpf-worker=4
```
Redpanda will automatically rebalance the 3+ partitions across all 4 worker instances.

---

## 6. Cloud Production Deployment with Nginx Reverse Proxy (SSL/TLS)

For public server deployment (e.g. AWS EC2, DigitalOcean), place Nginx in front of ULPF with HTTPS:

```nginx
# /etc/nginx/sites-available/ulpf.conf
server {
    listen 80;
    server_name soc.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name soc.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/soc.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/soc.yourdomain.com/privkey.pem;

    # Core 1 SOC Web Dashboard & API
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket / Server-Sent Events (SSE) support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Redpanda Stream Console (Secured path or separate subdomain)
    location /streams/ {
        proxy_pass http://127.0.0.1:8085/;
        proxy_set_header Host $host;
    }
}
```

---

## 7. Operational Troubleshooting

| Symptom | Cause | Solution |
| :--- | :--- | :--- |
| `port is already allocated` | Host process occupying port 8000/8050 | Check `netstat -ano \| findstr :8000` (Windows) or `lsof -i :8000` (Linux) and stop the conflicting process. |
| `ulpf-worker` not consuming | Redpanda topic does not exist | Run `docker exec ulpf-redpanda rpk topic create ulpf-raw-ingress`. |
| MinIO upload fails | Bucket `ulpf-raw` not initialized | Run `docker exec ulpf-minio mc mb local/ulpf-raw`. |
| Memory limit warning | Docker Desktop RAM setting too low | Allocate at least 4 GB RAM in Docker Desktop -> Settings -> Resources. |
