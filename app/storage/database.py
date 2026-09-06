import os
import json
import sqlite3
from contextlib import contextmanager
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings


class DatabaseManager:
    """
    SQLite Metadata & Event Storage Manager.
    Guarantees persistence across container restarts (mounted to persistent volume).
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.db_sqlite_path
        self._ensure_dir()
        self.init_db()

    def _ensure_dir(self):
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        """Initialize database schema with tables and performance indexes."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 1. Events Table (Canonical records & metadata)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    event_id TEXT PRIMARY KEY,
                    raw_event_id TEXT,
                    timestamp TEXT,
                    source TEXT,
                    vendor TEXT,
                    product TEXT,
                    format TEXT,
                    event_type TEXT,
                    action TEXT,
                    severity TEXT,
                    src_ip TEXT,
                    dst_ip TEXT,
                    parser TEXT,
                    status TEXT,
                    sha256 TEXT,
                    raw_message TEXT,
                    ir_json TEXT,
                    threat_json TEXT,
                    storage_uri TEXT,
                    storage_status TEXT,
                    opensearch_status TEXT,
                    created_at TEXT
                )
            """)

            # 2. Indexes for instant multi-facet query filtering
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_source ON events(source)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_format ON events(format)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_severity ON events(severity)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_status ON events(status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_src_ip ON events(src_ip)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_sha256 ON events(sha256)")

            # 3. Parsers Registry Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parsers (
                    parser_id TEXT PRIMARY KEY,
                    name TEXT,
                    format TEXT,
                    version TEXT,
                    status TEXT,
                    confidence REAL,
                    author TEXT,
                    description TEXT,
                    code TEXT,
                    updated_at TEXT
                )
            """)

            # 4. Sources Registry Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    source_id TEXT PRIMARY KEY,
                    name TEXT,
                    source_type TEXT,
                    vendor TEXT,
                    protocol TEXT,
                    address TEXT,
                    status TEXT,
                    is_blocked INTEGER DEFAULT 0,
                    created_at TEXT
                )
            """)

            # 5. Audit Log Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    action TEXT,
                    user TEXT,
                    detail TEXT,
                    status TEXT
                )
            """)

            # 6. System Key-Value Config Table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_config (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT
                )
            """)

            conn.commit()

    def save_event(
        self,
        record: Dict[str, Any],
        ir_json: str = "{}",
        storage_uri: str = "local",
        storage_status: str = "stored",
        opensearch_status: str = "indexed",
    ) -> bool:
        """Insert or replace normalized event and metadata."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO events (
                        event_id, raw_event_id, timestamp, source, vendor, product,
                        format, event_type, action, severity, src_ip, dst_ip,
                        parser, status, sha256, raw_message, ir_json, threat_json,
                        storage_uri, storage_status, opensearch_status, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        record.get("event_id"),
                        record.get("raw_event_id"),
                        record.get("timestamp"),
                        record.get("source"),
                        record.get("vendor"),
                        record.get("product") or record.get("device_name"),
                        record.get("format"),
                        record.get("event_type"),
                        record.get("action"),
                        record.get("severity"),
                        record.get("src_ip"),
                        record.get("dst_ip"),
                        record.get("parser"),
                        record.get("status"),
                        record.get("sha256"),
                        record.get("raw_message"),
                        ir_json,
                        json.dumps(record.get("threat")) if record.get("threat") else None,
                        storage_uri,
                        storage_status,
                        opensearch_status,
                        datetime.now(timezone.utc).isoformat(),
                    ),
                )
                conn.commit()
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to save event {record.get('event_id')}: {e}")
            return False

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single event by event_id or raw_event_id."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM events WHERE event_id = ? OR raw_event_id = ? LIMIT 1",
                (event_id, event_id),
            )
            row = cursor.fetchone()
            if row:
                d = dict(row)
                if d.get("threat_json"):
                    try:
                        d["threat"] = json.loads(d["threat_json"])
                    except Exception:
                        d["threat"] = None
                return d
            return None

    def query_events(
        self,
        source: Optional[str] = None,
        vendor: Optional[str] = None,
        format: Optional[str] = None,
        severity: Optional[str] = None,
        action: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[int, List[Dict[str, Any]]]:
        """Query events with dynamic filters and pagination."""
        query = "SELECT * FROM events WHERE 1=1"
        count_query = "SELECT COUNT(*) FROM events WHERE 1=1"
        params: List[Any] = []

        if source:
            query += " AND LOWER(source) = LOWER(?)"
            count_query += " AND LOWER(source) = LOWER(?)"
            params.append(source)
        if vendor:
            query += " AND LOWER(vendor) = LOWER(?)"
            count_query += " AND LOWER(vendor) = LOWER(?)"
            params.append(vendor)
        if format:
            query += " AND LOWER(format) = LOWER(?)"
            count_query += " AND LOWER(format) = LOWER(?)"
            params.append(format)
        if severity:
            query += " AND LOWER(severity) = LOWER(?)"
            count_query += " AND LOWER(severity) = LOWER(?)"
            params.append(severity)
        if action:
            query += " AND LOWER(action) = LOWER(?)"
            count_query += " AND LOWER(action) = LOWER(?)"
            params.append(action)
        if status:
            query += " AND LOWER(status) = LOWER(?)"
            count_query += " AND LOWER(status) = LOWER(?)"
            params.append(status)
        if search:
            s_param = f"%{search.lower()}%"
            search_clause = """
                AND (
                    LOWER(event_id) LIKE ? OR
                    LOWER(raw_message) LIKE ? OR
                    LOWER(src_ip) LIKE ? OR
                    LOWER(dst_ip) LIKE ? OR
                    LOWER(source) LIKE ? OR
                    LOWER(vendor) LIKE ? OR
                    LOWER(format) LIKE ? OR
                    LOWER(action) LIKE ? OR
                    LOWER(status) LIKE ? OR
                    LOWER(sha256) LIKE ?
                )
            """
            query += search_clause
            count_query += search_clause
            params.extend([s_param] * 10)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]

            query += " ORDER BY timestamp DESC, created_at DESC LIMIT ? OFFSET ?"
            query_params = list(params) + [limit, offset]
            cursor.execute(query, query_params)
            rows = cursor.fetchall()

            events = []
            for r in rows:
                d = dict(r)
                if d.get("threat_json"):
                    try:
                        d["threat"] = json.loads(d["threat_json"])
                    except Exception:
                        d["threat"] = None
                events.append(d)

            return total, events

    def get_all_recent_events(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """Load recent events on application startup to restore in-memory buffer."""
        _, events = self.query_events(limit=limit, offset=0)
        return events

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Calculate aggregated metrics directly from persistent database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM events")
            total_processed = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM events WHERE status = 'success'")
            success_cnt = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM events WHERE status = 'unparsed'")
            unparsed_cnt = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM events WHERE status IN ('error', 'blocked')")
            error_cnt = cursor.fetchone()[0]

            cursor.execute("SELECT format, COUNT(*) FROM events GROUP BY format")
            fmt_dist = {row[0] or "Unknown": row[1] for row in cursor.fetchall()}

            cursor.execute("SELECT COUNT(DISTINCT source) FROM events")
            active_sources = cursor.fetchone()[0]

            return {
                "total_processed": total_processed,
                "success_cnt": success_cnt,
                "unparsed_cnt": unparsed_cnt,
                "error_cnt": error_cnt,
                "fmt_dist": fmt_dist,
                "active_sources": active_sources,
            }

    def clear_all_events(self) -> int:
        """Clear event table on demo reset."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events")
            deleted = cursor.rowcount
            conn.commit()
            return deleted

    def check_health(self) -> Dict[str, Any]:
        """Perform SQLite health check."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.execute("SELECT COUNT(*) FROM events")
                cnt = cursor.fetchone()[0]
                return {
                    "status": "healthy",
                    "path": self.db_path,
                    "total_records": cnt,
                    "persisted": True,
                }
        except Exception as e:
            return {
                "status": "degraded",
                "path": self.db_path,
                "error": str(e),
                "persisted": False,
            }
