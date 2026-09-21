"""
ULPF Testing & Simulator Backend Service.
Runs on Port 8050 to provide network socket transmission, connection probing,
custom log addition, and serves the dedicated Testing Website.
"""

import sys
import os
import time
import threading
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse

# Silence Windows asyncio ProactorEventLoop WinError 10054 on sudden client socket disconnects
if sys.platform == "win32":
    try:
        from asyncio.proactor_events import _ProactorBasePipeTransport
        _orig_call_connection_lost = getattr(_ProactorBasePipeTransport, "_call_connection_lost", None)

        def _silent_call_connection_lost(self: Any, exc: Any = None):
            try:
                if _orig_call_connection_lost:
                    _orig_call_connection_lost(self, exc)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError, OSError):
                pass

        if _orig_call_connection_lost:
            setattr(_ProactorBasePipeTransport, "_call_connection_lost", _silent_call_connection_lost)
    except Exception:
        pass

# Add testing/ and testing/server to path for flexible execution
SERVER_DIR = Path(__file__).resolve().parent
TESTING_DIR = SERVER_DIR.parent
ROOT_DIR = TESTING_DIR.parent

for p in [SERVER_DIR, TESTING_DIR, ROOT_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Resilient dual-mode imports (supports direct script, uvicorn, IDE language server, and package imports)
try:
    from server.protocol_clients import probe_socket, send_udp_log, send_tcp_log, send_http_log, drop_file_log
    from server.log_generator import get_all_presets, generate_scenario_batch, generate_random_event, generate_device_log
except ImportError:
    try:
        from .protocol_clients import probe_socket, send_udp_log, send_tcp_log, send_http_log, drop_file_log
        from .log_generator import get_all_presets, generate_scenario_batch, generate_random_event, generate_device_log
    except (ImportError, ValueError):
        from protocol_clients import probe_socket, send_udp_log, send_tcp_log, send_http_log, drop_file_log
        from log_generator import get_all_presets, generate_scenario_batch, generate_random_event, generate_device_log


app = FastAPI(
    title="ULPF Network & Log Simulator Hub",
    description="Dedicated testing website and network connection simulator for Universal Log Pre-processing Framework",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory transmission audit log
TRANSMISSION_HISTORY: List[Dict[str, Any]] = []
MAX_HISTORY = 200


class PingRequest(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    protocol: str = "http"  # 'udp', 'tcp', 'http', 'https'
    scheme: str = "http"
    timeout: float = 3.0


class SendLogRequest(BaseModel):
    protocol: str = "udp"  # 'udp', 'tcp', 'http', 'file'
    host: str = "127.0.0.1"
    port: int = 5140
    message: Optional[str] = None
    log: Optional[str] = None
    log_message: Optional[str] = None
    raw_message: Optional[str] = None
    source: str = "Testing-Client"
    vendor: Optional[str] = None
    file_dir: Optional[str] = None
    scheme: str = "http"
    timeout: float = 3.0


class ScenarioRequest(BaseModel):
    scenario: str = "normal"  # 'normal', 'security', 'unknown', 'burst'
    host: str = "127.0.0.1"
    protocol_override: Optional[str] = None  # None, 'udp', 'tcp', 'http'
    api_port: int = 8000
    udp_port: int = 5140
    tcp_port: int = 5141
    scheme: str = "http"
    device_timeout: float = 3.0
    interval_ms: float = 50.0


class TargetStatusRequest(BaseModel):
    host: Optional[str] = "127.0.0.1"
    api_port: Optional[int] = 8000
    udp_port: Optional[int] = 5140
    tcp_port: Optional[int] = 5141
    ollama_port: Optional[int] = 11434
    scheme: Optional[str] = "http"


@app.get("/api/test/target-status")
@app.post("/api/test/target-status")
def get_target_status(
    host: str = "127.0.0.1",
    api_port: int = 8000,
    udp_port: int = 5140,
    tcp_port: int = 5141,
    ollama_port: int = 11434,
    scheme: str = "http",
    req_body: Optional[TargetStatusRequest] = None,
):
    """Check connectivity to Main Worker across HTTP/HTTPS, UDP, TCP, and Local AI ports concurrently."""
    if req_body:
        host = req_body.host or host
        api_port = req_body.api_port or api_port
        udp_port = req_body.udp_port or udp_port
        tcp_port = req_body.tcp_port or tcp_port
        ollama_port = req_body.ollama_port or ollama_port
        scheme = req_body.scheme or scheme
    import concurrent.futures

    # Split-Horizon DNS Translation: When the browser on the host machine requests a probe for 
    # '127.0.0.1' or 'localhost', the completely decoupled simulator backend needs to translate this 
    # to 'host.docker.internal' to route the health check OUT of the simulator container and into 
    # the host machine's exposed ports, acting as an anonymous external client.
    internal_target_host = host
    if internal_target_host in ("127.0.0.1", "localhost"):
        default_internal = "host.docker.internal" if os.path.exists("/.dockerenv") else "127.0.0.1"
        internal_target_host = os.environ.get("ULPF_INTERNAL_API_HOST", default_internal)

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f_http = executor.submit(probe_socket, internal_target_host, api_port, scheme, 1.0)
        f_tcp = executor.submit(probe_socket, internal_target_host, tcp_port, "tcp", 0.5)
        f_udp = executor.submit(probe_socket, internal_target_host, udp_port, "udp", 0.5)
        f_ai = executor.submit(probe_socket, internal_target_host, ollama_port, "tcp", 0.25)

        http_probe = f_http.result()
        tcp_probe = f_tcp.result()
        udp_probe = f_udp.result()
        ai_probe = f_ai.result()

    is_http_up = http_probe.get("status") in ("healthy", "ready", "online")
    is_tcp_up = tcp_probe.get("status") in ("connected", "ready", "online")
    is_ai_up = ai_probe.get("status") in ("connected", "ready", "online", "healthy")

    return {
        "host": host,
        "api_port": api_port,
        "scheme": scheme,
        "version": "1.0.0 Enterprise (Phase 8)",
        "platform": "ULPF Dual-Core Sovereign Telemetry Architecture",
        "ports": {
            "http_api": {
                "port": api_port,
                "protocol": scheme.upper(),
                "status": http_probe.get("status", "offline"),
                "latency_ms": http_probe.get("latency_ms", 0),
                "detail": http_probe.get("detail", "HTTP Ingestion API"),
            },
            "syslog_udp": {
                "port": udp_port,
                "protocol": "UDP",
                "status": udp_probe.get("status", "ready"),
                "latency_ms": udp_probe.get("latency_ms", 0),
                "detail": udp_probe.get("detail", f"UDP socket opened to {host}:{udp_port}"),
            },
            "syslog_tcp": {
                "port": tcp_port,
                "protocol": "TCP",
                "status": tcp_probe.get("status", "disconnected"),
                "latency_ms": tcp_probe.get("latency_ms", 0),
                "detail": tcp_probe.get("detail", f"TCP Syslog Collector on {host}:{tcp_port}"),
            },
            "ai_engine": {
                "port": ollama_port,
                "protocol": "OLLAMA (qwen2.5:7b)",
                "status": "ready" if is_ai_up else "offline",
                "latency_ms": ai_probe.get("latency_ms", 0),
                "detail": "Local Sovereign AI Model Engine (Qwen 7B) active" if is_ai_up else "Optional local AI offline (heuristic regex fallback active)",
            },
        },
        "all_ready": is_http_up,
    }


@app.get("/api/test/presets")
def list_presets():
    """List available multi-vendor log templates and default network ports."""
    return get_all_presets()


@app.post("/api/test/ping")
def ping_target(req: PingRequest):
    """Probe network connection to desired host and port."""
    result = probe_socket(req.host, req.port, req.protocol, timeout=req.timeout)
    return result


@app.post("/api/test/send-log")
def send_log(req: SendLogRequest):
    """
    Transmit custom or generated log over the desired network protocol.
    Supported protocols: UDP, TCP, HTTP REST, File Drop.
    """
    payload_msg = req.message or req.log_message or req.log or req.raw_message or ""
    if not payload_msg or not payload_msg.strip():
        raise HTTPException(status_code=400, detail="Log message payload cannot be empty.")

    proto = (req.protocol or "HTTP").strip().upper()
    receipt: Dict[str, Any] = {}

    if proto == "UDP":
        receipt = send_udp_log(req.host, req.port or 5140, payload_msg, timeout=req.timeout)
    elif proto == "TCP":
        receipt = send_tcp_log(req.host, req.port or 5141, payload_msg, timeout=req.timeout)
    elif proto in ("HTTP", "REST", "API", "HTTPS", "JSON"):
        scheme = getattr(req, "scheme", "http") or ("https" if proto == "HTTPS" else "http")
        port = req.port or 8000
        api_url = f"{scheme}://{req.host}:{port}/api/v1/ingest"
        receipt = send_http_log(api_url, payload_msg, source=req.source, vendor=req.vendor, timeout=req.timeout)
    elif proto == "FILE":
        watch_dir = req.file_dir or str(TESTING_DIR.parent / "main" / "storage" / "logs")
        receipt = drop_file_log(watch_dir, payload_msg)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported protocol: '{req.protocol}'. Choose UDP, TCP, HTTP, or FILE.")

    # Record in history
    record = {
        "id": len(TRANSMISSION_HISTORY) + 1,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "protocol": proto,
        "host": req.host,
        "port": req.port,
        "source": req.source,
        "payload": payload_msg,
        **receipt,
    }
    TRANSMISSION_HISTORY.insert(0, record)
    if len(TRANSMISSION_HISTORY) > MAX_HISTORY:
        TRANSMISSION_HISTORY.pop()

    return receipt


@app.post("/api/test/stream-scenario")
def stream_scenario(req: ScenarioRequest):
    """
    Automated transmission of pre-curated test scenarios across desired network protocols.
    Supports configurable device socket timeout and inter-log sending interval pacing.
    """
    batch = generate_scenario_batch(req.scenario)
    if not batch:
        raise HTTPException(status_code=400, detail=f"Unknown scenario '{req.scenario}'.")

    results = []
    total_bytes = 0
    success_count = 0

    for item in batch:
        proto = (req.protocol_override or item["protocol"]).upper()
        msg = item["message"]
        src = item["source"]

        if proto == "UDP":
            port = req.udp_port or 5140
            r = send_udp_log(req.host, port, msg, timeout=req.device_timeout)
        elif proto == "TCP":
            port = req.tcp_port or 5141
            r = send_tcp_log(req.host, port, msg, timeout=req.device_timeout)
        elif proto in ("HTTP", "REST"):
            port = req.api_port or 8000
            scheme = req.scheme or "http"
            api_url = f"{scheme}://{req.host}:{port}/api/v1/ingest"
            r = send_http_log(api_url, msg, source=src, timeout=req.device_timeout)
        else:
            watch_dir = str(TESTING_DIR.parent / "main" / "storage" / "logs")
            r = drop_file_log(watch_dir, msg)

        if r.get("success"):
            success_count += 1
            total_bytes += r.get("bytes_sent", 0)

        record = {
            "id": len(TRANSMISSION_HISTORY) + 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protocol": proto,
            "host": req.host,
            "source": src,
            "payload": msg,
            **r,
        }
        TRANSMISSION_HISTORY.insert(0, record)
        results.append(r)
        if req.interval_ms > 0:
            time.sleep(req.interval_ms / 1000.0)

    if len(TRANSMISSION_HISTORY) > MAX_HISTORY:
        del TRANSMISSION_HISTORY[MAX_HISTORY:]

    return {
        "status": "success",
        "scenario": req.scenario,
        "total_packets": len(batch),
        "successful_deliveries": success_count,
        "total_bytes_transmitted": total_bytes,
        "interval_ms": req.interval_ms,
        "device_timeout": req.device_timeout,
        "receipts": results,
    }


@app.get("/api/test/history")
def get_history(limit: int = 50):
    """Retrieve transmission log history."""
    return TRANSMISSION_HISTORY[:limit]


@app.get("/api/test/history/export")
def export_history(format: str = "json"):
    """Export transmission history in JSON or CSV format."""
    if format.lower() == "csv":
        import io, csv
        from fastapi.responses import Response
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Timestamp", "Protocol", "Host", "Port", "Source", "Status", "Bytes", "Latency_MS"])
        for r in TRANSMISSION_HISTORY:
            writer.writerow([
                r.get("id"),
                r.get("timestamp"),
                r.get("protocol"),
                r.get("host"),
                r.get("port"),
                r.get("source"),
                "SUCCESS" if r.get("success") else "FAIL",
                r.get("bytes_sent", 0),
                r.get("latency_ms", 0)
            ])
        return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=ulpf_test_audit.csv"})
    return JSONResponse(content={"total": len(TRANSMISSION_HISTORY), "history": TRANSMISSION_HISTORY})


@app.delete("/api/test/history")
def clear_history():
    """Clear transmission log history."""
    global TRANSMISSION_HISTORY
    TRANSMISSION_HISTORY = []
    return {"status": "cleared", "remaining": 0}


# ==============================================================================
# VIRTUAL DEVICE MANAGEMENT & TELEMETRY STREAMING CONTROLLER
# ==============================================================================

class VirtualDeviceConfig(BaseModel):
    id: Optional[str] = None
    name: str = "Edge-Firewall-01"
    vendor: str = "Palo Alto Networks"
    format: str = "palo_alto_panos"  # palo_alto_panos, cisco_asa, fortinet_fortigate, aws_cloudtrail, suricata_eve, syslog, cef, kv, json, leef
    ip: str = "10.0.1.15"
    protocol: str = "TCP"  # UDP, TCP, HTTP, FILE
    port: int = 5141
    interval_ms: float = 100.0  # Pacing / interval in milliseconds
    risk_factor: float = 0.0  # Threat probability 0.0 - 100.0%
    custom_template: Optional[str] = None
    connected: bool = True
    packets_sent: int = 0


VIRTUAL_DEVICES: List[Dict[str, Any]] = [
    {
        "id": "dev-1",
        "name": "PaloAlto-Edge-01",
        "vendor": "Palo Alto Networks",
        "format": "palo_alto_panos",
        "ip": "10.0.1.15",
        "protocol": "TCP",
        "port": 5141,
        "interval_ms": 50.0,
        "risk_factor": 15.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
    {
        "id": "dev-2",
        "name": "FortiGate-Perimeter-02",
        "vendor": "Fortinet",
        "format": "fortinet_fortigate",
        "ip": "10.0.2.40",
        "protocol": "UDP",
        "port": 5140,
        "interval_ms": 100.0,
        "risk_factor": 25.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
    {
        "id": "dev-3",
        "name": "Cisco-ASA-Core-03",
        "vendor": "Cisco",
        "format": "cisco_asa",
        "ip": "172.16.10.1",
        "protocol": "UDP",
        "port": 5140,
        "interval_ms": 150.0,
        "risk_factor": 10.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
    {
        "id": "dev-4",
        "name": "AWS-CloudTrail-Node-04",
        "vendor": "Amazon Web Services",
        "format": "aws_cloudtrail",
        "ip": "198.51.100.44",
        "protocol": "HTTP",
        "port": 8000,
        "interval_ms": 200.0,
        "risk_factor": 30.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
    {
        "id": "dev-5",
        "name": "Suricata-Sensor-05",
        "vendor": "OISF / Suricata",
        "format": "suricata_eve",
        "ip": "192.168.100.55",
        "protocol": "HTTP",
        "port": 8000,
        "interval_ms": 100.0,
        "risk_factor": 50.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
    {
        "id": "dev-6",
        "name": "Linux-Auth-Host-06",
        "vendor": "Linux",
        "format": "syslog",
        "ip": "192.168.100.8",
        "protocol": "TCP",
        "port": 5141,
        "interval_ms": 100.0,
        "risk_factor": 20.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
    {
        "id": "dev-7",
        "name": "Meraki-MR33-AP-07",
        "vendor": "Cisco Meraki",
        "format": "syslog",
        "ip": "192.168.1.50",
        "protocol": "UDP",
        "port": 5140,
        "interval_ms": 250.0,
        "risk_factor": 5.0,
        "custom_template": None,
        "connected": True,
        "packets_sent": 0,
    },
]

STREAM_CONTROLLER = {
    "active_streams": {},  # dev_id -> threading.Thread / flag
    "is_global_streaming": False,
    "lock": threading.Lock(),
}


@app.get("/api/test/devices")
def get_virtual_devices():
    """Retrieve all configured virtual devices."""
    return {"status": "success", "count": len(VIRTUAL_DEVICES), "devices": VIRTUAL_DEVICES}


@app.post("/api/test/devices")
def create_virtual_device(dev: VirtualDeviceConfig):
    """Add a new virtual device to the simulator."""
    new_id = dev.id or f"dev-{int(time.time() * 1000) % 10000}"
    d_dict = dev.model_dump()
    d_dict["id"] = new_id
    VIRTUAL_DEVICES.append(d_dict)
    return {"status": "success", "message": f"Virtual device '{dev.name}' created.", "device": d_dict}


@app.put("/api/test/devices/{dev_id}")
def update_virtual_device(dev_id: str, dev: VirtualDeviceConfig):
    """Update virtual device configurations (format, interval, risk factor, port, protocol, template)."""
    target = next((d for d in VIRTUAL_DEVICES if d["id"] == dev_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Virtual device '{dev_id}' not found")

    target.update({
        "name": dev.name,
        "vendor": dev.vendor,
        "format": dev.format,
        "ip": dev.ip,
        "protocol": dev.protocol.upper(),
        "port": dev.port,
        "interval_ms": dev.interval_ms,
        "risk_factor": dev.risk_factor,
        "custom_template": dev.custom_template,
        "connected": dev.connected,
    })

    return {"status": "success", "message": f"Virtual device '{dev.name}' updated.", "device": target}


@app.delete("/api/test/devices/{dev_id}")
def delete_virtual_device(dev_id: str):
    """Delete a virtual device from the simulator."""
    global VIRTUAL_DEVICES
    if len(VIRTUAL_DEVICES) <= 1:
        raise HTTPException(status_code=400, detail="At least one virtual device must remain in the roster.")
    
    VIRTUAL_DEVICES = [d for d in VIRTUAL_DEVICES if d["id"] != dev_id]
    return {"status": "success", "message": f"Virtual device '{dev_id}' removed.", "remaining": len(VIRTUAL_DEVICES)}


@app.post("/api/test/devices/{dev_id}/send")
def send_device_log_once(dev_id: str, host: str = "127.0.0.1", scheme: str = "http", timeout: float = 3.0):
    """Generate and transmit a log from a specific virtual device based on its configured format and risk factor."""
    dev = next((d for d in VIRTUAL_DEVICES if d["id"] == dev_id), None)
    if not dev:
        raise HTTPException(status_code=404, detail=f"Virtual device '{dev_id}' not found")

    log_msg = generate_device_log(dev)
    proto = dev["protocol"].upper()
    port = dev["port"]
    receipt = {}

    if proto == "UDP":
        receipt = send_udp_log(host, port, log_msg, timeout=timeout)
    elif proto == "TCP":
        receipt = send_tcp_log(host, port, log_msg, timeout=timeout)
    elif proto in ("HTTP", "REST"):
        api_url = f"{scheme}://{host}:{port}/api/v1/ingest"
        receipt = send_http_log(api_url, log_msg, source=dev["name"], vendor=dev["vendor"], timeout=timeout)
    else:
        watch_dir = str(TESTING_DIR.parent / "main" / "storage" / "logs")
        receipt = drop_file_log(watch_dir, log_msg)

    if receipt.get("success"):
        dev["packets_sent"] = dev.get("packets_sent", 0) + 1

    record = {
        "id": len(TRANSMISSION_HISTORY) + 1,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "protocol": proto,
        "host": host,
        "port": port,
        "source": dev["name"],
        "payload": log_msg,
        **receipt,
    }
    TRANSMISSION_HISTORY.insert(0, record)
    if len(TRANSMISSION_HISTORY) > MAX_HISTORY:
        TRANSMISSION_HISTORY.pop()

    return {
        "status": "success" if receipt.get("success") else "error",
        "device_id": dev_id,
        "device_name": dev["name"],
        "log": log_msg,
        "receipt": receipt,
    }


def _device_stream_worker(dev_id: str, host: str, scheme: str):
    """Background worker continuously streaming logs from a virtual device at its configured interval."""
    while STREAM_CONTROLLER["active_streams"].get(dev_id):
        dev = next((d for d in VIRTUAL_DEVICES if d["id"] == dev_id), None)
        if not dev or not dev.get("connected"):
            break

        log_msg = generate_device_log(dev)
        proto = dev["protocol"].upper()
        port = dev["port"]
        r = {}

        try:
            if proto == "UDP":
                r = send_udp_log(host, port, log_msg)
            elif proto == "TCP":
                r = send_tcp_log(host, port, log_msg)
            else:
                api_url = f"{scheme}://{host}:{port}/api/v1/ingest"
                r = send_http_log(api_url, log_msg, source=dev["name"], vendor=dev["vendor"])

            if r.get("success"):
                dev["packets_sent"] = dev.get("packets_sent", 0) + 1
        except Exception:
            pass

        interval = max(0.01, float(dev.get("interval_ms", 100.0)) / 1000.0)
        time.sleep(interval)


@app.post("/api/test/devices/{dev_id}/stream/start")
def start_device_stream(dev_id: str, host: str = "127.0.0.1", scheme: str = "http"):
    """Start continuous log streaming for a specific virtual device."""
    dev = next((d for d in VIRTUAL_DEVICES if d["id"] == dev_id), None)
    if not dev:
        raise HTTPException(status_code=404, detail=f"Virtual device '{dev_id}' not found")

    with STREAM_CONTROLLER["lock"]:
        if STREAM_CONTROLLER["active_streams"].get(dev_id):
            return {"status": "already_streaming", "device_id": dev_id}

        STREAM_CONTROLLER["active_streams"][dev_id] = True
        t = threading.Thread(target=_device_stream_worker, args=(dev_id, host, scheme), daemon=True)
        t.start()

    return {"status": "started", "device_id": dev_id, "interval_ms": dev["interval_ms"]}


@app.post("/api/test/devices/{dev_id}/stream/stop")
def stop_device_stream(dev_id: str):
    """Stop continuous log streaming for a virtual device."""
    with STREAM_CONTROLLER["lock"]:
        STREAM_CONTROLLER["active_streams"][dev_id] = False
    return {"status": "stopped", "device_id": dev_id}


@app.get("/api/test/devices/stream/status")
def get_device_stream_status():
    """Get active streaming status across all virtual devices."""
    active_ids = [k for k, v in STREAM_CONTROLLER["active_streams"].items() if v]
    return {
        "active_stream_count": len(active_ids),
        "streaming_device_ids": active_ids,
        "devices": [
            {
                "id": d["id"],
                "name": d["name"],
                "is_streaming": d["id"] in active_ids,
                "packets_sent": d.get("packets_sent", 0),
                "interval_ms": d.get("interval_ms", 100.0),
                "risk_factor": d.get("risk_factor", 0.0),
            }
            for d in VIRTUAL_DEVICES
        ]
    }


# Curated multi-vendor sample datasets for testing file uploads
SAMPLE_LOG_FILES: Dict[str, Dict[str, Any]] = {
    "palo_alto_traffic.cef": {
        "id": "palo_alto_traffic.cef",
        "name": "Palo Alto Networks PAN-OS Traffic (CEF)",
        "format": "CEF",
        "badge": "CEF / Firewall",
        "description": "5 firewall session records with source/destination IPs, ports, and action verdicts",
        "content": (
            "CEF:0|PaloAltoNetworks|PAN-OS|10.1.0|TRAFFIC|traffic|1|src=10.0.1.25 dst=198.51.100.10 spt=54210 dpt=443 proto=tcp act=allow cn1=120 cn2=450 cs1=Rule-DMZ-Allow\n"
            "CEF:0|PaloAltoNetworks|PAN-OS|10.1.0|TRAFFIC|traffic|4|src=198.51.100.77 dst=10.0.1.5 spt=61200 dpt=22 proto=tcp act=deny cn1=0 cn2=0 cs1=Block-External-SSH\n"
            "CEF:0|PaloAltoNetworks|PAN-OS|10.1.0|TRAFFIC|traffic|1|src=10.0.2.14 dst=8.8.8.8 spt=49200 dpt=53 proto=udp act=allow cn1=65 cn2=120 cs1=DNS-Outbound\n"
            "CEF:0|PaloAltoNetworks|PAN-OS|10.1.0|TRAFFIC|traffic|5|src=192.0.2.88 dst=10.0.4.15 spt=43100 dpt=8080 proto=tcp act=drop cn1=0 cn2=0 cs1=WAF-Default-Drop\n"
            "CEF:0|PaloAltoNetworks|PAN-OS|10.1.0|TRAFFIC|traffic|2|src=10.0.1.50 dst=172.16.0.4 spt=51000 dpt=445 proto=tcp act=allow cn1=512 cn2=1024 cs1=Internal-SMB-Permit\n"
        ),
    },
    "cisco_asa_firewall.log": {
        "id": "cisco_asa_firewall.log",
        "name": "Cisco ASA Firewall Syslog",
        "format": "Syslog",
        "badge": "Syslog / ASA",
        "description": "5 standard Cisco ASA message types (%ASA-4-106023, %ASA-6-302013)",
        "content": (
            "<164>Sep 08 2026 14:15:02 firewall-gw01 %ASA-4-106023: Deny tcp src outside:198.51.100.66/49152 dst inside:10.0.0.15/22 by access-group \"OUTSIDE-IN\" [0x0, 0x0]\n"
            "<166>Sep 08 2026 14:15:03 firewall-gw01 %ASA-6-302013: Built outbound TCP connection 984512 for outside:198.51.100.22/443 (198.51.100.22/443) to inside:10.0.1.10/50211\n"
            "<164>Sep 08 2026 14:15:05 firewall-gw01 %ASA-4-106023: Deny udp src outside:203.0.113.19/5353 dst inside:10.0.2.5/53 by access-group \"OUTSIDE-IN\" [0x0, 0x0]\n"
            "<166>Sep 08 2026 14:15:08 firewall-gw01 %ASA-6-302014: Teardown TCP connection 984512 for outside:198.51.100.22/443 to inside:10.0.1.10/50211 duration 0:00:05 bytes 4820\n"
            "<164>Sep 08 2026 14:15:10 firewall-gw01 %ASA-4-106023: Deny ip src outside:198.51.100.99 dst inside:10.0.0.1 by access-group \"BLACKLIST\" [0x0, 0x0]\n"
        ),
    },
    "suricata_ids_alerts.json": {
        "id": "suricata_ids_alerts.json",
        "name": "Suricata EVE-JSON IDS Alerts",
        "format": "JSON",
        "badge": "EVE-JSON / IDS",
        "description": "5 line-delimited Suricata network intrusion alert events",
        "content": (
            '{"timestamp":"2026-09-08T14:15:20.102Z","event_type":"alert","src_ip":"198.51.100.44","src_port":51230,"dest_ip":"10.0.1.25","dest_port":22,"proto":"TCP","alert":{"action":"blocked","gid":1,"signature_id":2010935,"signature":"ET SCAN Potential SSH Scan","category":"Attempted Information Leak","severity":2}}\n'
            '{"timestamp":"2026-09-08T14:15:21.450Z","event_type":"alert","src_ip":"198.51.100.12","src_port":44120,"dest_ip":"10.0.1.80","dest_port":80,"proto":"TCP","alert":{"action":"allowed","gid":1,"signature_id":2009158,"signature":"ET WEB_SERVER SQL Injection - SELECT","category":"Web Application Attack","severity":1}}\n'
            '{"timestamp":"2026-09-08T14:15:22.012Z","event_type":"dns","src_ip":"10.0.2.14","src_port":53100,"dest_ip":"8.8.8.8","dest_port":53,"proto":"UDP","dns":{"type":"query","rrname":"api.ulpf-core.internal","rrtype":"A"}}\n'
            '{"timestamp":"2026-09-08T14:15:23.890Z","event_type":"alert","src_ip":"203.0.113.88","src_port":39200,"dest_ip":"10.0.1.5","dest_port":443,"proto":"TCP","alert":{"action":"blocked","gid":1,"signature_id":2024101,"signature":"ET EXPLOIT Log4j CVE-2021-44228 JNDI Ingestion","category":"Attempted Administrator Privilege Gain","severity":1}}\n'
            '{"timestamp":"2026-09-08T14:15:25.334Z","event_type":"flow","src_ip":"10.0.0.8","src_port":58200,"dest_ip":"10.0.0.1","dest_port":514,"proto":"UDP","flow":{"bytes_toserver":350,"bytes_toclient":0}}\n'
        ),
    },
    "linux_auth_failures.log": {
        "id": "linux_auth_failures.log",
        "name": "Linux /var/log/auth.log Syslog",
        "format": "Syslog",
        "badge": "Linux / Auth",
        "description": "5 Linux PAM and OpenSSH authentication failure and accepted telemetry entries",
        "content": (
            "Sep 08 14:16:01 edge-server sshd[28410]: Failed password for invalid user admin from 198.51.100.44 port 41200 ssh2\n"
            "Sep 08 14:16:02 edge-server sshd[28412]: Failed password for invalid user root from 198.51.100.44 port 41202 ssh2\n"
            "Sep 08 14:16:04 edge-server sshd[28415]: Failed password for user devops from 198.51.100.44 port 41208 ssh2\n"
            "Sep 08 14:16:08 edge-server sshd[28420]: Accepted publickey for secops from 10.0.1.15 port 55100 ssh2: RSA SHA256:m0+s78Fw\n"
            "Sep 08 14:16:10 edge-server sudo[28430]: secops : TTY=pts/0 ; PWD=/home/secops ; USER=root ; COMMAND=/usr/bin/systemctl status ulpf\n"
        ),
    },
    "scada_modbus_unknown.raw": {
        "id": "scada_modbus_unknown.raw",
        "name": "SCADA Industrial MODBUS Hex (Unknown)",
        "format": "Unknown",
        "badge": "SCADA / Hex Frame",
        "description": "5 proprietary industrial sensor hex frames to verify automated fallback to AI Onboarding & Human Review Queue",
        "content": (
            "[SCADA-MODBUS-HEX] ADDR:0x04 FUNC:0x03 REG:0x1000 LEN:0x0004 DATA:0x00A1 0x00B2 CRC:0x7A1F SENSOR:TURBINE_PRESSURE STATUS:WARNING\n"
            "[SCADA-MODBUS-HEX] ADDR:0x04 FUNC:0x06 REG:0x1002 VAL:0x00FF CRC:0x3C42 SENSOR:TURBINE_VALVE_OVERRIDE OPERATOR:ENG_44\n"
            "[SCADA-MODBUS-HEX] ADDR:0x08 FUNC:0x03 REG:0x2000 LEN:0x0008 DATA:0x01E0 0x01E4 CRC:0x88BC SENSOR:COOLANT_TEMP STATUS:CRITICAL\n"
            "[SCADA-MODBUS-HEX] ADDR:0x08 FUNC:0x05 COIL:0x0010 STAT:ON CRC:0x91AA SENSOR:PUMP_EMERGENCY_SHUTOFF STATUS:TRIPPED\n"
            "[SCADA-MODBUS-HEX] ADDR:0x02 FUNC:0x03 REG:0x0500 LEN:0x0002 DATA:0x0000 0x0000 CRC:0x0000 SENSOR:AUX_POWER STATUS:NORMAL\n"
        ),
    },
}


@app.get("/api/test/sample-files")
def get_sample_files():
    """Returns curated multi-vendor sample log files available for 1-click loading."""
    return [
        {
            "id": k,
            "name": v["name"],
            "format": v["format"],
            "badge": v["badge"],
            "description": v["description"],
            "lines_count": len([l for l in v["content"].splitlines() if l.strip()]),
            "bytes_count": len(v["content"].encode("utf-8")),
            "preview": v["content"][:200] + "...",
            "content": v["content"],
        }
        for k, v in SAMPLE_LOG_FILES.items()
    ]


@app.post("/api/test/upload-file")
async def upload_log_file(
    file: UploadFile = File(...),
    host: str = Form("127.0.0.1"),
    port: int = Form(8000),
    mode: str = Form("http_upload"),  # 'http_upload', 'udp_stream', 'tcp_stream', 'file_drop'
    delay_ms: int = Form(0),
    scheme: str = Form("http"),
):
    """
    Ingests an uploaded raw log file into the ULPF ecosystem via selected transport:
      - 'http_upload': Multipart upload directly to FastAPI /api/v1/upload
      - 'udp_stream': Line-by-line datagram replay across UDP Syslog (port 5140)
      - 'tcp_stream': Line-by-line stream replay across TCP Syslog (port 5141)
      - 'file_drop': Writes file to server watched directory (storage/logs/)
    """
    try:
        content_bytes = await file.read()
        content_str = content_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

    filename = file.filename or "uploaded.log"
    total_bytes = len(content_bytes)
    start_time = time.perf_counter()

    if mode == "http_upload":
        api_url = f"{scheme}://{host}:{port}/api/v1/upload"
        try:
            import httpx
            files = {"file": (filename, content_bytes, "text/plain")}
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(api_url, files=files)

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            if res.status_code == 200:
                data = res.json()
                record = {
                    "id": len(TRANSMISSION_HISTORY) + 1,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "protocol": "FILE_HTTP",
                    "host": host,
                    "port": port,
                    "source": f"file:{filename}",
                    "payload": f"Uploaded '{filename}' ({total_bytes} bytes, {data.get('lines_processed', 0)} lines)",
                    "success": True,
                    "bytes_sent": total_bytes,
                    "latency_ms": latency_ms,
                    "detail": f"File '{filename}' processed: {data.get('success_count', 0)} success, {data.get('unparsed_count', 0)} unparsed",
                }
                TRANSMISSION_HISTORY.insert(0, record)
                if len(TRANSMISSION_HISTORY) > MAX_HISTORY:
                    TRANSMISSION_HISTORY.pop()

                return {
                    "status": "success",
                    "mode": "http_upload",
                    "filename": filename,
                    "bytes_sent": total_bytes,
                    "latency_ms": latency_ms,
                    "lines_processed": data.get("lines_processed", 0),
                    "success_count": data.get("success_count", 0),
                    "unparsed_count": data.get("unparsed_count", 0),
                    "sample_events": data.get("sample_events", []),
                    "server_response": data,
                }
            else:
                return {
                    "status": "error",
                    "mode": "http_upload",
                    "filename": filename,
                    "status_code": res.status_code,
                    "error": res.text,
                    "latency_ms": latency_ms,
                }
        except Exception as e:
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            return {
                "status": "error",
                "mode": "http_upload",
                "filename": filename,
                "error": f"Connection error to {api_url}: {str(e)}",
                "latency_ms": latency_ms,
            }

    elif mode in ("udp_stream", "tcp_stream"):
        lines = [line.strip() for line in content_str.splitlines() if line.strip()]
        stream_success = 0
        stream_failed = 0
        total_streamed_bytes = 0
        target_port = 5140 if mode == "udp_stream" else 5141

        for line in lines:
            if mode == "udp_stream":
                r = send_udp_log(host, target_port, line)
            else:
                r = send_tcp_log(host, target_port, line)

            if r.get("success"):
                stream_success += 1
                total_streamed_bytes += r.get("bytes_sent", 0)
            else:
                stream_failed += 1

            if delay_ms > 0:
                time.sleep(delay_ms / 1000.0)

        latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
        proto_name = "UDP" if mode == "udp_stream" else "TCP"
        record = {
            "id": len(TRANSMISSION_HISTORY) + 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protocol": f"FILE_{proto_name}",
            "host": host,
            "port": target_port,
            "source": f"file:{filename}",
            "payload": f"Streamed '{filename}' ({len(lines)} lines over {proto_name})",
            "success": stream_failed == 0,
            "bytes_sent": total_streamed_bytes,
            "latency_ms": latency_ms,
            "detail": f"Streamed {stream_success}/{len(lines)} lines via {proto_name}:{target_port}",
        }
        TRANSMISSION_HISTORY.insert(0, record)
        if len(TRANSMISSION_HISTORY) > MAX_HISTORY:
            TRANSMISSION_HISTORY.pop()

        return {
            "status": "success",
            "mode": mode,
            "filename": filename,
            "lines_processed": len(lines),
            "success_count": stream_success,
            "failed_count": stream_failed,
            "bytes_sent": total_streamed_bytes,
            "latency_ms": latency_ms,
            "destination": f"{host}:{target_port}",
        }

    elif mode == "file_drop":
        watch_dir = str(TESTING_DIR.parent / "main" / "storage" / "logs")
        target_path = Path(watch_dir) / filename
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content_str)
            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
            lines_count = len([l for l in content_str.splitlines() if l.strip()])
            record = {
                "id": len(TRANSMISSION_HISTORY) + 1,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "protocol": "FILE_DROP",
                "host": "localhost",
                "port": 0,
                "source": f"file:{filename}",
                "payload": f"Dropped '{filename}' into {watch_dir} ({lines_count} lines)",
                "success": True,
                "bytes_sent": total_bytes,
                "latency_ms": latency_ms,
                "detail": f"Wrote file to {target_path.as_posix()}",
            }
            TRANSMISSION_HISTORY.insert(0, record)
            return {
                "status": "success",
                "mode": "file_drop",
                "filename": filename,
                "destination": str(target_path),
                "lines_processed": lines_count,
                "bytes_sent": total_bytes,
                "latency_ms": latency_ms,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to write file drop: {str(e)}")

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported upload mode '{mode}'. Choose 'http_upload', 'udp_stream', 'tcp_stream', or 'file_drop'.")


class BurstRequest(BaseModel):
    count: int = Field(50, ge=1, le=2000)
    protocol: str = "udp"
    host: str = "127.0.0.1"
    port: Optional[int] = None
    rate_limit_eps: Optional[int] = None
    pacing_delay_ms: Optional[int] = None
    interval_ms: Optional[float] = None
    device_timeout: float = 3.0
    source: str = "LoadGen-01"
    scheme: str = "http"


@app.post("/api/test/burst")
def trigger_burst_traffic(req: BurstRequest):
    """
    High-throughput load generator. Emits rapid burst of packets with live performance telemetry.
    Supports configurable device timeout and logs interval pacing.
    """
    proto = req.protocol.upper()
    port = req.port or (5140 if proto == "UDP" else (5141 if proto == "TCP" else 8000))
    t_start = time.perf_counter()
    success_cnt = 0
    err_cnt = 0
    total_bytes = 0
    receipts = []

    # Split-Horizon DNS Translation
    internal_target_host = req.host
    if internal_target_host in ("127.0.0.1", "localhost"):
        internal_target_host = os.environ.get("ULPF_INTERNAL_API_HOST", "host.docker.internal")

    # Calculate inter-packet sleep interval if interval / rate limiting / pacing is requested
    sleep_interval = 0.0
    if req.interval_ms is not None and req.interval_ms >= 0:
        sleep_interval = req.interval_ms / 1000.0
    elif req.pacing_delay_ms and req.pacing_delay_ms > 0:
        sleep_interval = req.pacing_delay_ms / 1000.0
    elif req.rate_limit_eps and req.rate_limit_eps > 0 and req.rate_limit_eps < 1000:
        sleep_interval = 1.0 / req.rate_limit_eps

    for i in range(req.count):
        msg = generate_random_event()
        r = {}
        if proto == "UDP":
            r = send_udp_log(internal_target_host, port, msg, timeout=req.device_timeout)
        elif proto == "TCP":
            r = send_tcp_log(internal_target_host, port, msg, timeout=req.device_timeout)
        else:
            api_url = f"{req.scheme}://{internal_target_host}:{port}/api/v1/ingest"
            r = send_http_log(api_url, msg, source=req.source, timeout=req.device_timeout)

        if r.get("success"):
            success_cnt += 1
            total_bytes += r.get("bytes_sent", len(msg.encode("utf-8")))
        else:
            err_cnt += 1

        if i < 10 or i == req.count - 1:
            receipts.append(r)

        if sleep_interval > 0:
            time.sleep(sleep_interval)

    t_total = time.perf_counter() - t_start
    effective_eps = round(success_cnt / t_total, 2) if t_total > 0 else req.count

    # Add summary entry to history
    record = {
        "id": len(TRANSMISSION_HISTORY) + 1,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "protocol": proto,
        "host": req.host,
        "port": port,
        "source": req.source,
        "payload": f"BURST [{req.count} packets, {effective_eps} EPS]",
        "success": success_cnt > 0,
        "bytes_sent": total_bytes,
        "latency_ms": round(t_total * 1000, 2),
    }
    TRANSMISSION_HISTORY.insert(0, record)
    if len(TRANSMISSION_HISTORY) > MAX_HISTORY:
        del TRANSMISSION_HISTORY[MAX_HISTORY:]

    return {
        "status": "success",
        "protocol": proto,
        "requested": req.count,
        "total_requested": req.count,
        "delivered": success_cnt,
        "failed": err_cnt,
        "elapsed_seconds": round(t_total, 3),
        "effective_eps": effective_eps,
        "total_bytes": total_bytes,
        "sample_receipts": receipts[:5],
    }


# ==============================================================================
# AUTOMATED TEST PIPELINE RUNNER (Integrates run_pipeline.py into Web Hub)
# ==============================================================================

DEFAULT_PIPELINE_STAGES = [
    {"id": "suites", "name": "Pytest Test Suites (13 Suites, 61 Unit Tests)", "status": "idle", "duration": 0.0, "error": None},
    {"id": "smoke", "name": "End-to-End Smoke Test Suite (10 Verification Phases)", "status": "idle", "duration": 0.0, "error": None},
    {"id": "security", "name": "Security & Cyber Resilience Tests (8 Attack Tests)", "status": "idle", "duration": 0.0, "error": None},
    {"id": "stack", "name": "Stack & Subsystem Verification (10 Checks)", "status": "idle", "duration": 0.0, "error": None},
    {"id": "bench", "name": "Ingestion Throughput Benchmark (1,000 Events)", "status": "idle", "duration": 0.0, "error": None},
    {"id": "bench_all", "name": "Comprehensive All-Parsers Benchmark (C + 9 Vendors)", "status": "idle", "duration": 0.0, "error": None},
]

PIPELINE_STATE: Dict[str, Any] = {
    "is_running": False,
    "stage_filter": "all",
    "started_at": None,
    "completed_at": None,
    "total_duration": 0.0,
    "all_passed": None,
    "stages": [dict(s) for s in DEFAULT_PIPELINE_STAGES],
    "logs": [
        "Automated Test Pipeline initialized.",
        "Select a run mode above and click 'Run Test Pipeline' to execute regression verification.",
    ],
}
_pipeline_lock = threading.Lock()


class PipelineRunRequest(BaseModel):
    stage: str = "all"  # 'all', 'fast', 'suites', 'smoke', 'security', 'stack', 'bench', 'bench_all'
    bench_events: int = 1000
    device_timeout: float = 3.0
    logs_interval_ms: float = 10.0


def _run_single_stage(
    stage_dict: Dict[str, Any],
    cmd: List[str],
    cwd: Path,
    device_timeout: float = 3.0,
    logs_interval_ms: float = 10.0
) -> bool:
    stage_dict["status"] = "running"
    stage_dict["duration"] = 0.0
    stage_dict["error"] = None
    t0 = time.time()
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{ROOT_DIR / 'main'}{os.pathsep}{env.get('PYTHONPATH', '')}"
    env["ULPF_DEVICE_TIMEOUT"] = str(device_timeout)
    env["ULPF_LOGS_INTERVAL_MS"] = str(logs_interval_ms)

    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(cwd),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        if proc.stdout:
            for line in iter(proc.stdout.readline, ""):
                if not line:
                    break
                clean_line = line.rstrip()
                if clean_line:
                    with _pipeline_lock:
                        PIPELINE_STATE["logs"].append(clean_line)
                        if len(PIPELINE_STATE["logs"]) > 2000:
                            PIPELINE_STATE["logs"].pop(0)

        proc.wait()
        dur = round(time.time() - t0, 2)
        stage_dict["duration"] = dur
        if proc.returncode == 0:
            stage_dict["status"] = "pass"
            return True
        else:
            stage_dict["status"] = "fail"
            stage_dict["error"] = f"Exit code: {proc.returncode}"
            return False
    except Exception as e:
        dur = round(time.time() - t0, 2)
        stage_dict["duration"] = dur
        stage_dict["status"] = "fail"
        stage_dict["error"] = str(e)
        with _pipeline_lock:
            PIPELINE_STATE["logs"].append(f"[ERROR] {stage_dict['name']}: {e}")
        return False


def _pipeline_worker_thread(
    stage_filter: str,
    bench_events: int,
    device_timeout: float = 3.0,
    logs_interval_ms: float = 10.0
):
    global PIPELINE_STATE

    t_start = time.time()
    active_stages = []

    # Export pipeline-wide configuration to environment for all sub-tools
    os.environ["ULPF_DEVICE_TIMEOUT"] = str(device_timeout)
    os.environ["ULPF_LOGS_INTERVAL_MS"] = str(logs_interval_ms)

    if stage_filter == "fast":
        active_stages = ["smoke", "security", "stack"]
    elif stage_filter in ("suites", "smoke", "security", "stack", "bench", "bench_all"):
        active_stages = [stage_filter]
    else:  # "all"
        active_stages = ["suites", "smoke", "security", "stack", "bench", "bench_all"]

    with _pipeline_lock:
        PIPELINE_STATE["logs"].append("=" * 75)
        PIPELINE_STATE["logs"].append(f"  ULPF AUTOMATED TEST PIPELINE RUN STARTED ({stage_filter.upper()})")
        PIPELINE_STATE["logs"].append(f"  Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        PIPELINE_STATE["logs"].append(f"  Config: Device Timeout={device_timeout}s | Logs Sent Interval={logs_interval_ms}ms")
        PIPELINE_STATE["logs"].append("=" * 75)

    commands = {
        "suites": [sys.executable, "-m", "pytest", "testing/suites/"],
        "smoke": [sys.executable, str(TESTING_DIR / "smoke_test.py")],
        "security": [sys.executable, str(TESTING_DIR / "security" / "security_smoke_test.py")],
        "stack": [sys.executable, str(ROOT_DIR / "scripts" / "verify_stack.py")],
        "bench": [
            sys.executable,
            str(TESTING_DIR / "benchmarks" / "benchmark.py"),
            "--events", str(bench_events),
            "--timeout", str(device_timeout),
            "--interval", str(logs_interval_ms / 1000.0)
        ],
        "bench_all": [
            sys.executable,
            str(TESTING_DIR / "benchmark_all.py"),
        ],
    }

    cwds = {
        "suites": ROOT_DIR,
        "smoke": ROOT_DIR,
        "security": ROOT_DIR,
        "stack": ROOT_DIR,
        "bench": ROOT_DIR,
        "bench_all": ROOT_DIR,
    }

    results = []

    for stage_id in active_stages:
        stage_dict = next((s for s in PIPELINE_STATE["stages"] if s["id"] == stage_id), None)
        if not stage_dict:
            continue

        cmd = commands.get(stage_id)
        cwd = cwds.get(stage_id, ROOT_DIR)
        if not cmd:
            continue

        with _pipeline_lock:
            PIPELINE_STATE["logs"].append(f"\n>>> EXECUTING STAGE: {stage_dict['name']}")

        ok = _run_single_stage(stage_dict, cmd, cwd, device_timeout=device_timeout, logs_interval_ms=logs_interval_ms)
        results.append(ok)

    t_total = round(time.time() - t_start, 2)
    all_ok = all(results) if results else False

    with _pipeline_lock:
        PIPELINE_STATE["is_running"] = False
        PIPELINE_STATE["completed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        PIPELINE_STATE["total_duration"] = t_total
        PIPELINE_STATE["all_passed"] = all_ok
        PIPELINE_STATE["logs"].append("\n" + "=" * 75)
        PIPELINE_STATE["logs"].append(f"  PIPELINE EXECUTION SUMMARY: {'ALL PASSED [OK]' if all_ok else 'FAILED [ERROR]'}")
        PIPELINE_STATE["logs"].append(f"  Total Duration: {t_total}s | Passed: {sum(1 for r in results if r)}/{len(results)}")
        PIPELINE_STATE["logs"].append("=" * 75 + "\n")


@app.post("/api/test/pipeline/run")
def run_test_pipeline(req: PipelineRunRequest):
    """
    Trigger automated test pipeline execution (Pytest, Smoke, Security, Stack, Benchmarks).
    Executes asynchronously in the background.
    """
    global PIPELINE_STATE

    if PIPELINE_STATE["is_running"]:
        return JSONResponse(
            status_code=409,
            content={"status": "running", "message": "Pipeline run is already in progress. Please wait for completion."},
        )

    # Reset stages state
    with _pipeline_lock:
        PIPELINE_STATE["is_running"] = True
        PIPELINE_STATE["stage_filter"] = req.stage
        PIPELINE_STATE["started_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        PIPELINE_STATE["completed_at"] = None
        PIPELINE_STATE["total_duration"] = 0.0
        PIPELINE_STATE["all_passed"] = None
        PIPELINE_STATE["logs"] = []

        active_set = set()
        if req.stage == "fast":
            active_set = {"smoke", "security", "stack"}
        elif req.stage in ("suites", "smoke", "security", "stack", "bench", "bench_all"):
            active_set = {req.stage}
        else:
            active_set = {"suites", "smoke", "security", "stack", "bench", "bench_all"}

        for s in PIPELINE_STATE["stages"]:
            s["status"] = "pending" if s["id"] in active_set else "skipped"
            s["duration"] = 0.0
            s["error"] = None

    t = threading.Thread(
        target=_pipeline_worker_thread,
        args=(req.stage, req.bench_events, req.device_timeout, req.logs_interval_ms),
        daemon=True,
    )
    t.start()

    return {
        "status": "started",
        "stage": req.stage,
        "stages_count": len(active_set),
        "device_timeout": req.device_timeout,
        "logs_interval_ms": req.logs_interval_ms,
        "started_at": PIPELINE_STATE["started_at"],
    }


@app.post("/api/test/benchmark/all")
def run_benchmark_all_direct():
    """Trigger comprehensive all-parsers benchmark suite (C + 9 Vendors + Pipeline)."""
    return run_test_pipeline(PipelineRunRequest(stage="bench_all"))


@app.get("/api/test/pipeline/status")
def get_pipeline_status(offset: int = 0):
    """
    Retrieve current pipeline execution status, stage results, and terminal logs.
    """
    with _pipeline_lock:
        total_logs = len(PIPELINE_STATE["logs"])
        safe_offset = max(0, min(offset, total_logs))
        logs_slice = PIPELINE_STATE["logs"][safe_offset:]

        return {
            "is_running": PIPELINE_STATE["is_running"],
            "stage_filter": PIPELINE_STATE["stage_filter"],
            "started_at": PIPELINE_STATE["started_at"],
            "completed_at": PIPELINE_STATE["completed_at"],
            "total_duration": PIPELINE_STATE["total_duration"],
            "all_passed": PIPELINE_STATE["all_passed"],
            "stages": PIPELINE_STATE["stages"],
            "logs": logs_slice,
            "next_offset": total_logs,
        }


# Mount web interface static directory
WEB_DIR = TESTING_DIR / "web"
if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=str(WEB_DIR), html=True), name="testing_web")

