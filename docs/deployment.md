# ULPF Deployment Guide

---

## Option A — Oracle Cloud VM (Full Production)

> Everything works: Syslog UDP, Syslog TCP, MinIO, OpenSearch, Dashboard, REST API, AI

### Prerequisites
- Oracle Cloud account (free tier — Ampere A1: 4 OCPU, 24 GB RAM is perfect)
- A VM running **Ubuntu 22.04** or **Oracle Linux 8**
- SSH access to the VM

---

### Step 1 — Open Security List Ports (Oracle Cloud Console)

Oracle Cloud blocks all inbound ports by default. You must open them in the Cloud Console **before** the setup script.

```
Oracle Cloud Console
  → Networking
  → Virtual Cloud Networks
  → Your VCN
  → Security Lists
  → Default Security List
  → Add Ingress Rules
```

Add these **Ingress Rules**:

| Source CIDR   | Protocol | Port(s)   | Description               |
|---------------|----------|-----------|---------------------------|
| `0.0.0.0/0`   | TCP      | `8000`    | ULPF Dashboard + REST API |
| `0.0.0.0/0`   | UDP      | `5140`    | Syslog UDP Collector      |
| `0.0.0.0/0`   | TCP      | `5141`    | Syslog TCP Collector      |
| `0.0.0.0/0`   | TCP      | `9001`    | MinIO Console             |
| `0.0.0.0/0`   | TCP      | `9200`    | OpenSearch (restrict if sensitive) |
| `0.0.0.0/0`   | TCP      | `22`      | SSH (already open)        |

---

### Step 2 — Run the Setup Script (SSH into VM)

```bash
# SSH into your Oracle VM
ssh ubuntu@<YOUR_VM_IP>

# Download and run the setup script (one command)
curl -fsSL https://raw.githubusercontent.com/Jayaduran/SIH-/main/scripts/oracle-setup.sh | sudo bash
```

The script will:
1. Install Docker + Docker Compose
2. Configure OS firewall (firewalld / ufw)
3. Clone the ULPF repository to `/opt/ulpf`
4. Create production `.env` file
5. Install systemd service (auto-start on reboot)
6. Start the full stack
7. Verify health check

**Total time: ~3-5 minutes** (Docker image build takes most of that)

---

### Step 3 — Edit Production Password

```bash
sudo nano /opt/ulpf/.env
# Change: MINIO_SECRET_KEY=CHANGE_THIS_PASSWORD_2026
# To something strong, then:
sudo systemctl restart ulpf
```

---

### Step 4 — Verify Everything is Running

```bash
# Check service status
sudo systemctl status ulpf

# Follow live logs
sudo journalctl -u ulpf -f

# Check all containers
cd /opt/ulpf && docker compose ps

# Test API
curl http://localhost:8000/api/v1/health/live
```

---

### Access URLs (replace with your VM IP)

| Service | URL |
|---------|-----|
| ️ Dashboard | `http://<VM_IP>:8000/dashboard/index.html` |
|  API Docs | `http://<VM_IP>:8000/docs` |
| ️ MinIO Console | `http://<VM_IP>:9001` |
|  OpenSearch | `http://<VM_IP>:9200` |
|  Syslog UDP | `<VM_IP>:5140` (UDP) |
|  Syslog TCP | `<VM_IP>:5141` (TCP) |

---

### Useful Management Commands

```bash
# Start / Stop / Restart
sudo systemctl start ulpf
sudo systemctl stop ulpf
sudo systemctl restart ulpf

# Update to latest from GitHub
cd /opt/ulpf && git pull && sudo systemctl restart ulpf

# View container logs
cd /opt/ulpf && docker compose logs -f ulpf-api

# Send test syslog packets to your VM
python scripts/send_syslog.py --host <VM_IP> --port 5140 --protocol udp --count 50
```

---

### Enable AI (if VM has ≥ 16GB RAM)

```bash
sudo nano /opt/ulpf/.env
# Set: AI_ENABLED=true

cd /opt/ulpf
docker compose --profile ai up -d
# Wait ~5 min for model download
docker compose exec ulpf-ai ollama pull qwen2.5-coder:3b
sudo systemctl restart ulpf
```

---

## Option B — Render.com (Demo / Preview)

> Dashboard + REST API + Pipeline work. Syslog UDP/TCP listeners are disabled (Render only supports HTTP). Free tier sleeps after 15 min.

### What Works on Render
-  Web Dashboard
-  REST Ingest API (`POST /api/v1/ingest`)
-  Full parse → normalize → detect pipeline
-  File upload ingestion
-  CEF / Syslog / LEEF / JSON / KV parsers
-  Syslog UDP listener (no raw UDP on Render)
-  Syslog TCP listener (no raw TCP on Render)
-  MinIO (use local storage fallback)
-  OpenSearch (in-memory only)
-  AI/Ollama (no RAM on free tier)

---

### Deploy to Render (3 clicks)

#### Method 1 — Auto-Deploy via render.yaml

1. Go to [render.com](https://render.com) → **New** → **Blueprint**
2. Connect your GitHub repo: `Jayaduran/SIH-`
3. Render detects `render.yaml` automatically
4. Click **Apply** → deployment starts

#### Method 2 — Manual Web Service

1. Go to [render.com](https://render.com) → **New** → **Web Service**
2. Connect GitHub repo: `Jayaduran/SIH-`
3. Settings:
   - **Runtime**: Docker
   - **Dockerfile Path**: `./Dockerfile`
   - **Instance Type**: Free
4. Add Environment Variables (see table below)
5. Click **Deploy**

---

### Render Environment Variables

Set these in **Render Dashboard → Your Service → Environment**:

| Variable | Value |
|----------|-------|
| `ULPF_ENV` | `production` |
| `ULPF_DEBUG` | `false` |
| `SYSLOG_UDP_ENABLED` | `false` |
| `SYSLOG_TCP_ENABLED` | `false` |
| `FILE_COLLECTOR_ENABLED` | `true` |
| `FILE_WATCH_DIR` | `/tmp/ulpf-logs` |
| `MAX_EVENTS_PER_SECOND` | `1000` |
| `INGRESS_QUEUE_MAX_SIZE` | `5000` |
| `MINIO_ENDPOINT` | *(leave empty)* |
| `OPENSEARCH_URL` | *(leave empty)* |
| `AI_ENABLED` | `false` |
| `STORAGE_DIR` | `/tmp/ulpf-raw` |
| `DB_SQLITE_PATH` | `/tmp/ulpf-metadata.db` |

> **Note:** On Render free tier, `/tmp` is ephemeral — data resets on each deploy/restart. For persistent demo data use Render's **Starter** plan ($7/month) with a persistent disk.

---

### After Render Deploy

Your app will be live at:
```
https://ulpf-demo.onrender.com/dashboard/index.html
https://ulpf-demo.onrender.com/docs
```

> ️ Free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

---

## Comparison

| Feature | Oracle Cloud VM | Render Free | Local Bare-Metal |
|---------|----------------|-------------|------------------|
| **Cost** | Free (Always Free) | Free (limited) | Free (Local HW) |
| **Sleep** | Never | After 15 min | Never |
| **Syslog UDP 5140** |  Full |  N/A |  Full |
| **Syslog TCP 5141** |  Full |  N/A |  Full |
| **Testing Hub 8050** |  Full |  N/A |  Full |
| **MinIO Storage** |  Persistent |  Ephemeral |  (or local filesystem) |
| **OpenSearch** |  Full |  N/A |  (or in-memory) |
| **AI / Ollama** |  (if RAM ≥ 16GB) |  N/A |  (or offline fallback) |
| **Dashboard** |  |  |  |
| **REST API** |  |  |  |
| **Pipeline** |  Full |  Full |  Full |
| **Custom Domain** | Configure nginx | Included | Local IP / Hostname |
| **Best For** | SIH Live Demo | Public preview link | Local Dev & Rapid Testing |

---

## Option C — Local Bare-Metal Deployment (Windows / Linux)

For local development, testing, and air-gapped lab environments with zero cloud requirements:

### Prerequisites:
* Python 3.10+ (tested through 3.13)
* Dependencies installed: `pip install -r requirements.txt`

### 1. Launch Services:
* **Core Production Server (`:8000`)**:
  ```cmd
  start_main.bat
  ```
  Runs FastAPI worker on `0.0.0.0:8000`, UDP Syslog on `5140`, TCP Syslog on `5141`, and mounts Dashboard at `http://localhost:8000/dashboard/index.html`.

* **Testing Simulator Hub (`:8050`)**:
  ```cmd
  start_testing.bat
  ```
  Runs Testing Hub on `0.0.0.0:8050` (`http://localhost:8050`) for interactive device simulation, attack arsenal, load generation, file upload lab, and remote machine targeting.

* **Run Automated Test Pipeline**:
  ```cmd
  test_pipeline.bat
  ```
  Executes all 5 verification phases (Pytest, Smoke, Security, Stack, Benchmark).

### 2. Accessing from Another Machine:
* In the Testing Hub at `http://<TESTING_HOST>:8050`, use the **Target Machine Controller** to point to the server's IP address:
  - Protocol: `http://` or `https://`
  - Target Host: `192.168.1.50` (or Docker/Cloud IP)
  - Port: `8000`
  - Click ** Ping API** to verify connectivity with real-time latency reporting.

