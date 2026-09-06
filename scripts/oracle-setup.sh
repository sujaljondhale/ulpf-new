#!/usr/bin/env bash
# ==============================================================================
# ULPF — Oracle Cloud VM Full Production Setup Script
# Tested on: Oracle Linux 8 / Ubuntu 22.04 (ARM A1 or AMD x86)
# Run as: sudo bash oracle-setup.sh
# ==============================================================================

set -euo pipefail

REPO_URL="https://github.com/Jayaduran/SIH-.git"
APP_DIR="/opt/ulpf"
SERVICE_USER="ulpf"
DOMAIN=""   # Set to your domain/IP, e.g. "ulpf.example.com" or leave blank

echo "========================================================"
echo " ULPF Oracle Cloud VM Setup"
echo "========================================================"

# ── 1. Detect OS ──────────────────────────────────────────
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS"; exit 1
fi
echo "[1/9] Detected OS: $OS"

# ── 2. Install Docker ─────────────────────────────────────
echo "[2/9] Installing Docker..."
if command -v docker &>/dev/null; then
    echo "  Docker already installed: $(docker --version)"
else
    if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
        apt-get update -qq
        apt-get install -y -qq ca-certificates curl gnupg
        install -m 0755 -d /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        chmod a+r /etc/apt/keyrings/docker.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
            > /etc/apt/sources.list.d/docker.list
        apt-get update -qq
        apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin
    elif [[ "$OS" == "ol" || "$OS" == "centos" || "$OS" == "rhel" || "$OS" == "fedora" ]]; then
        dnf install -y -q dnf-plugins-core
        dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        dnf install -y -q docker-ce docker-ce-cli containerd.io docker-compose-plugin
    else
        curl -fsSL https://get.docker.com | bash
    fi
    systemctl enable docker
    systemctl start docker
    echo "  Docker installed: $(docker --version)"
fi

# ── 3. Configure firewall ─────────────────────────────────
echo "[3/9] Configuring firewall..."
if command -v firewall-cmd &>/dev/null; then
    # Oracle Linux / RHEL
    firewall-cmd --permanent --add-port=8000/tcp    # ULPF Dashboard + API
    firewall-cmd --permanent --add-port=5140/udp    # Syslog UDP
    firewall-cmd --permanent --add-port=5141/tcp    # Syslog TCP
    firewall-cmd --permanent --add-port=9000/tcp    # MinIO API
    firewall-cmd --permanent --add-port=9001/tcp    # MinIO Console
    firewall-cmd --permanent --add-port=9200/tcp    # OpenSearch
    firewall-cmd --permanent --add-port=80/tcp      # HTTP (optional nginx)
    firewall-cmd --permanent --add-port=443/tcp     # HTTPS (optional)
    firewall-cmd --reload
    echo "  firewalld rules applied"
elif command -v ufw &>/dev/null; then
    # Ubuntu
    ufw allow 8000/tcp
    ufw allow 5140/udp
    ufw allow 5141/tcp
    ufw allow 9000/tcp
    ufw allow 9001/tcp
    ufw allow 9200/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    echo "  ufw rules applied"
fi
echo ""
echo "  !! IMPORTANT: Also open these ports in Oracle Cloud Security List:"
echo "  !! Dashboard: https://cloud.oracle.com → Networking → VCN → Security Lists"
echo "  !! Add Ingress rules for: TCP 8000, UDP 5140, TCP 5141, TCP 9001"

# ── 4. Create service user ────────────────────────────────
echo "[4/9] Creating service user '$SERVICE_USER'..."
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -m -s /bin/bash "$SERVICE_USER"
    usermod -aG docker "$SERVICE_USER"
fi

# ── 5. Clone / update repository ─────────────────────────
echo "[5/9] Cloning ULPF repository..."
if [ -d "$APP_DIR/.git" ]; then
    echo "  Updating existing repo..."
    cd "$APP_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$APP_DIR"
    cd "$APP_DIR"
fi
chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

# ── 6. Create production .env ─────────────────────────────
echo "[6/9] Creating production .env file..."
if [ ! -f "$APP_DIR/.env" ]; then
    cat > "$APP_DIR/.env" <<'ENV'
# ULPF Production Environment — Oracle Cloud VM
ULPF_ENV=production
ULPF_DEBUG=false
ULPF_API_HOST=0.0.0.0
ULPF_API_PORT=8000

# Syslog Collectors
SYSLOG_UDP_ENABLED=true
SYSLOG_UDP_HOST=0.0.0.0
SYSLOG_UDP_PORT=5140
SYSLOG_TCP_ENABLED=true
SYSLOG_TCP_HOST=0.0.0.0
SYSLOG_TCP_PORT=5141
SYSLOG_TLS_ENABLED=false

# File Collector
FILE_COLLECTOR_ENABLED=true
FILE_WATCH_DIR=/app/storage/logs

# Ingestion Queue
MAX_EVENTS_PER_SECOND=25000
INGRESS_QUEUE_MAX_SIZE=50000

# MinIO (change these passwords!)
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=ulpf_admin
MINIO_SECRET_KEY=CHANGE_THIS_PASSWORD_2026
MINIO_BUCKET=ulpf-raw
MINIO_SECURE=false

# OpenSearch
OPENSEARCH_URL=http://opensearch:9200
OPENSEARCH_INDEX=ulpf-events

# Storage
STORAGE_DIR=/app/storage/raw
DB_SQLITE_PATH=/app/storage/ulpf_metadata.db

# AI (disable if VM RAM < 8GB)
AI_ENABLED=false
OLLAMA_URL=http://ulpf-ai:11434
OLLAMA_MODEL=qwen2.5-coder:3b
ENV
    chown "$SERVICE_USER:$SERVICE_USER" "$APP_DIR/.env"
    echo "  .env created at $APP_DIR/.env"
    echo "  ** EDIT $APP_DIR/.env and change the MinIO password! **"
else
    echo "  .env already exists, skipping."
fi

# ── 7. Install systemd service ────────────────────────────
echo "[7/9] Installing systemd service..."
cat > /etc/systemd/system/ulpf.service <<SERVICE
[Unit]
Description=ULPF Universal Log Pre-processing Framework
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStartPre=/usr/bin/docker compose pull --ignore-pull-failures
ExecStart=/usr/bin/docker compose up --build --remove-orphans
ExecStop=/usr/bin/docker compose down
Restart=on-failure
RestartSec=10s
TimeoutStartSec=120s
TimeoutStopSec=60s
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ulpf

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl enable ulpf
echo "  systemd service 'ulpf' installed and enabled on boot"

# ── 8. Start ULPF ─────────────────────────────────────────
echo "[8/9] Starting ULPF stack (this takes 2-3 minutes)..."
cd "$APP_DIR"
sudo -u "$SERVICE_USER" docker compose up --build -d
echo "  Services starting in background..."

# ── 9. Wait and verify ────────────────────────────────────
echo "[9/9] Waiting for API to be ready..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:8000/api/v1/health/live &>/dev/null; then
        echo "  ✓ ULPF API is UP!"
        break
    fi
    sleep 5
    echo "  Waiting... ($((i*5))s)"
done

VM_IP=$(curl -sf http://checkip.amazonaws.com 2>/dev/null || hostname -I | awk '{print $1}')

echo ""
echo "========================================================"
echo " ULPF is LIVE on Oracle Cloud VM!"
echo "========================================================"
echo ""
echo " Dashboard:      http://$VM_IP:8000/dashboard/index.html"
echo " API Docs:       http://$VM_IP:8000/docs"
echo " MinIO Console:  http://$VM_IP:9001  (login: ulpf_admin)"
echo " OpenSearch:     http://$VM_IP:9200"
echo " Syslog UDP:     $VM_IP:5140 (UDP)"
echo " Syslog TCP:     $VM_IP:5141 (TCP)"
echo ""
echo " Manage with:"
echo "   sudo systemctl start ulpf"
echo "   sudo systemctl stop ulpf"
echo "   sudo systemctl status ulpf"
echo "   sudo journalctl -u ulpf -f"
echo ""
echo " Update to latest:"
echo "   cd $APP_DIR && git pull && sudo systemctl restart ulpf"
echo ""
echo " !! Don't forget to open Security List ports in Oracle Cloud Console !!"
echo "========================================================"
