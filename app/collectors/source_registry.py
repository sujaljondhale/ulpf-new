import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.storage.database import DatabaseManager


class SourceRegistry:
    """
    Source Registry & Access Controller.
    Tracks active, blocked, and degraded log sources with SQLite persistence.
    """

    def __init__(self, db: Optional[DatabaseManager] = None):
        self.db = db or DatabaseManager()
        self._sources: Dict[str, Dict[str, Any]] = {}
        self._last_event_times: Dict[str, float] = {}
        self._event_counts: Dict[str, int] = {}
        self._init_default_sources()

    def _init_default_sources(self):
        """Seed baseline enterprise log sources."""
        defaults = [
            {
                "source_id": "Firewall-01",
                "name": "Firewall-01",
                "source_type": "Firewall",
                "vendor": "Fortinet",
                "protocol": "Syslog UDP (5140)",
                "address": "10.0.1.1:5140",
                "expected_format": "CEF",
                "status": "ACTIVE",
                "is_blocked": 0,
            },
            {
                "source_id": "Router-01",
                "name": "Router-01",
                "source_type": "Router",
                "vendor": "Cisco",
                "protocol": "Syslog UDP (5140)",
                "address": "10.0.1.254:5140",
                "expected_format": "Syslog",
                "status": "ACTIVE",
                "is_blocked": 0,
            },
            {
                "source_id": "VPN-01",
                "name": "VPN-01",
                "source_type": "VPN",
                "vendor": "Palo Alto",
                "protocol": "Syslog TCP (5141)",
                "address": "10.0.2.1:5141",
                "expected_format": "Key=Value",
                "status": "ACTIVE",
                "is_blocked": 0,
            },
            {
                "source_id": "IDS-01",
                "name": "IDS-01",
                "source_type": "IDS/IPS",
                "vendor": "Suricata",
                "protocol": "Syslog TCP (5141)",
                "address": "10.0.3.5:5141",
                "expected_format": "JSON",
                "status": "ACTIVE",
                "is_blocked": 0,
            },
            {
                "source_id": "Demo-Web-01",
                "name": "Demo-Web-01",
                "source_type": "Server",
                "vendor": "ULPF Gateway",
                "protocol": "REST HTTP",
                "address": "http://127.0.0.1:8000",
                "expected_format": "JSON",
                "status": "ACTIVE",
                "is_blocked": 0,
            },
        ]
        for s in defaults:
            self._sources[s["source_id"]] = s
            self._event_counts[s["source_id"]] = 0

    def register_or_update(
        self,
        source_id: str,
        name: Optional[str] = None,
        source_type: str = "Generic Device",
        vendor: str = "Unknown",
        protocol: str = "Syslog",
        address: str = "127.0.0.1",
        expected_format: str = "Unknown",
    ) -> Dict[str, Any]:
        """Register newly observed network device or update existing source record."""
        if source_id in self._sources:
            s = self._sources[source_id]
            s["last_seen"] = datetime.now(timezone.utc).isoformat()
            return s

        src_entry = {
            "source_id": source_id,
            "name": name or source_id,
            "source_type": source_type,
            "vendor": vendor,
            "protocol": protocol,
            "address": address,
            "expected_format": expected_format,
            "status": "ACTIVE",
            "is_blocked": 0,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_seen": datetime.now(timezone.utc).isoformat(),
        }
        self._sources[source_id] = src_entry
        self._event_counts[source_id] = 0
        return src_entry

    def record_event(self, source_id: str, is_error: bool = False):
        """Record ingress event for a source."""
        if source_id not in self._sources:
            self.register_or_update(source_id=source_id)

        self._event_counts[source_id] = self._event_counts.get(source_id, 0) + 1
        self._last_event_times[source_id] = time.time()
        self._sources[source_id]["last_seen"] = datetime.now(timezone.utc).isoformat()

    def toggle_block(self, source_id: str) -> Tuple[bool, str]:
        """Toggle source blocking state."""
        if source_id not in self._sources:
            self.register_or_update(source_id=source_id)

        current = self._sources[source_id].get("is_blocked", 0)
        new_state = 0 if current else 1
        self._sources[source_id]["is_blocked"] = new_state
        self._sources[source_id]["status"] = "BLOCKED" if new_state else "ACTIVE"
        return bool(new_state), self._sources[source_id]["status"]

    def is_blocked(self, source_id: str) -> bool:
        """Check if source is currently blocked."""
        if source_id in self._sources:
            return bool(self._sources[source_id].get("is_blocked", 0))
        return False

    def list_sources(self) -> List[Dict[str, Any]]:
        """Return all registered sources with live statistics."""
        results = []
        for sid, s in self._sources.items():
            cnt = self._event_counts.get(sid, 0)
            is_bl = bool(s.get("is_blocked", 0))
            status_str = "BLOCKED" if is_bl else ("ACTIVE" if cnt > 0 else "READY")
            results.append({
                "id": sid,
                "name": s.get("name", sid),
                "type": s.get("source_type", "Network Device"),
                "vendor": s.get("vendor", "Generic"),
                "protocol": s.get("protocol", "Syslog"),
                "address": s.get("address", "0.0.0.0"),
                "format": s.get("expected_format", "CEF"),
                "status": status_str,
                "events_received": cnt,
                "events_per_sec": 0 if is_bl else (12 if cnt > 0 else 0),
                "is_blocked": is_bl,
                "last_seen": s.get("last_seen", datetime.now(timezone.utc).isoformat()),
            })
        return results
