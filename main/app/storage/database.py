import os
import json
import time
import sqlite3
from contextlib import contextmanager
from typing import Dict, Any, List, Optional, Tuple, Generator, Sequence
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings

# Optional PostgreSQL driver (psycopg v3) detection
HAS_PSYCOPG: bool = False
psycopg: Any = None
dict_row: Any = None
try:
    import psycopg  # type: ignore
    from psycopg.rows import dict_row  # type: ignore
    HAS_PSYCOPG = True
except Exception:
    pass


def _to_dict(row: Any) -> Dict[str, Any]:
    if row is None:
        return {}
    if isinstance(row, dict):
        return row
    return dict(row)


def _to_scalar(row: Any, default: Any = 0) -> Any:
    if row is None:
        return default
    if isinstance(row, dict):
        return list(row.values())[0] if row else default
    return row[0]


class DatabaseManager:
    """
    Unified Multi-Backend Database & Persistence Manager.
    Supports:
      1. SQLite (Default zero-config embedded database with WAL mode concurrency)
      2. PostgreSQL (Enterprise SQL database via psycopg v3)
    Provides full DAO repositories for:
      - Events (Canonical records, query indexing, metrics)
      - Sources (Device registry, telemetry, dynamic blocking)
      - Parsers (Synthesized & active parser registry)
      - Audit Logs (Compliance and operation trail)
      - System Config (Key-value platform configuration)
    """

    def __init__(
        self,
        db_path: Optional[str] = None,
        db_type: Optional[str] = None,
        database_url: Optional[str] = None,
    ):
        self.db_type = (db_type or settings.db_type or "sqlite").lower()
        self.database_url = database_url or settings.database_url
        self.db_path = db_path or settings.db_sqlite_path

        # Auto-detect database type from URL scheme if supplied
        if self.database_url:
            if self.database_url.startswith("postgres://") or self.database_url.startswith("postgresql://"):
                self.db_type = "postgres"
            elif self.database_url.startswith("sqlite://"):
                self.db_type = "sqlite"
                self.db_path = self.database_url.replace("sqlite:///", "").replace("sqlite://", "")

        if self.db_type == "sqlite":
            self._ensure_dir()

        self.init_db()

    def _ensure_dir(self):
        if self.db_path and self.db_path != ":memory:":
            try:
                Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def _execute_sql(
        self,
        cursor: Any,
        sql: str,
        params: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Helper to execute SQL with parameterized arguments safely."""
        if params is not None:
            return cursor.execute(sql, tuple(params))
        return cursor.execute(sql)

    @contextmanager
    def get_connection(self) -> Generator[Any, None, None]:
        """Yield database connection with row dictionary mapping and transaction safety."""
        if self.db_type == "postgres" and HAS_PSYCOPG and self.database_url and psycopg is not None:
            pg_kwargs: Dict[str, Any] = {
                "row_factory": dict_row,
                "connect_timeout": int(settings.db_timeout),
            }
            conn = psycopg.connect(self.database_url, **pg_kwargs)  # type: ignore
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
        else:
            self._ensure_dir()
            try:
                conn = sqlite3.connect(self.db_path, timeout=float(settings.db_timeout))
            except sqlite3.OperationalError:
                try:
                    fallback_dir = Path.home() / ".ulpf" / "storage"
                    fallback_dir.mkdir(parents=True, exist_ok=True)
                    self.db_path = str(fallback_dir / "ulpf_metadata.db")
                    conn = sqlite3.connect(self.db_path, timeout=float(settings.db_timeout))
                except Exception:
                    self.db_path = ":memory:"
                    conn = sqlite3.connect(self.db_path, timeout=float(settings.db_timeout))

            conn.row_factory = sqlite3.Row
            # Enable SQLite Write-Ahead Logging (WAL) and synchronous=NORMAL for high throughput
            try:
                conn.execute("PRAGMA journal_mode=WAL;")
                conn.execute("PRAGMA synchronous=NORMAL;")
            except Exception:
                pass
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()

    def init_db(self):
        """Initialize database schema with tables and performance indexes across backends."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 1. Events Table
            if is_pg:
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
            else:
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

            # 2. Performance Indexes
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
                    yaml_spec TEXT,
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
                    expected_format TEXT,
                    status TEXT,
                    is_blocked INTEGER DEFAULT 0,
                    created_at TEXT,
                    last_seen TEXT
                )
            """)

            # Schema migration: ensure existing sqlite databases receive any added columns
            if not is_pg:
                try:
                    cursor.execute("PRAGMA table_info(sources)")
                    existing_cols = {row["name"] if isinstance(row, dict) else row[1] for row in cursor.fetchall()}
                    col_defs = {
                        "name": "TEXT",
                        "source_type": "TEXT",
                        "vendor": "TEXT",
                        "protocol": "TEXT",
                        "address": "TEXT",
                        "expected_format": "TEXT",
                        "status": "TEXT",
                        "is_blocked": "INTEGER DEFAULT 0",
                        "created_at": "TEXT",
                        "last_seen": "TEXT",
                    }
                    for cname, ctype in col_defs.items():
                        if cname not in existing_cols:
                            try:
                                cursor.execute(f"ALTER TABLE sources ADD COLUMN {cname} {ctype}")
                            except Exception:
                                pass
                except Exception:
                    pass

            # 5. Audit Log Table
            if is_pg:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_log (
                        id SERIAL PRIMARY KEY,
                        timestamp TEXT,
                        action TEXT,
                        user_name TEXT,
                        detail TEXT,
                        status TEXT
                    )
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS audit_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        action TEXT,
                        user_name TEXT,
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
            
            # 7. Immutable Merkle Root Ledger
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS merkle_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    root_hash TEXT,
                    created_at TEXT
                )
            """)

    def set_config(self, key: str, value: str) -> bool:
        """Set a key-value configuration setting."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now_str = datetime.now(timezone.utc).isoformat()
                if is_pg:
                    cursor.execute(
                        "INSERT INTO system_config (key, value, updated_at) VALUES (%s, %s, %s) "
                        "ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = EXCLUDED.updated_at",
                        (key, value, now_str)
                    )
                else:
                    cursor.execute(
                        "INSERT OR REPLACE INTO system_config (key, value, updated_at) VALUES (?, ?, ?)",
                        (key, value, now_str)
                    )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to set config {key}: {e}")
            return False

    def append_merkle_root(self, root_hash: str) -> bool:
        """Append a new Merkle Root to the permanent immutable ledger."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now_str = datetime.now(timezone.utc).isoformat()
                if is_pg:
                    cursor.execute(
                        "INSERT INTO merkle_ledger (root_hash, created_at) VALUES (%s, %s)",
                        (root_hash, now_str)
                    )
                else:
                    cursor.execute(
                        "INSERT INTO merkle_ledger (root_hash, created_at) VALUES (?, ?)",
                        (root_hash, now_str)
                    )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to append to merkle ledger: {e}")
            return False

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a key-value configuration setting."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT value FROM system_config WHERE key = {ph}", (key,))
            row = cursor.fetchone()
            return row["value"] if row else default

    # =========================================================================
    # 1. EVENTS REPOSITORY
    # =========================================================================
    def save_event(
        self,
        record: Dict[str, Any],
        ir_json: str = "{}",
        storage_uri: str = "local",
        storage_status: str = "stored",
        opensearch_status: str = "indexed",
    ) -> bool:
        """Insert or replace normalized canonical event."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now_str = datetime.now(timezone.utc).isoformat()
                params = (
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
                    now_str,
                )

                if is_pg:
                    cursor.execute(
                        """
                        INSERT INTO events (
                            event_id, raw_event_id, timestamp, source, vendor, product,
                            format, event_type, action, severity, src_ip, dst_ip,
                            parser, status, sha256, raw_message, ir_json, threat_json,
                            storage_uri, storage_status, opensearch_status, created_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (event_id) DO UPDATE SET
                            raw_event_id = EXCLUDED.raw_event_id,
                            timestamp = EXCLUDED.timestamp,
                            source = EXCLUDED.source,
                            vendor = EXCLUDED.vendor,
                            product = EXCLUDED.product,
                            format = EXCLUDED.format,
                            event_type = EXCLUDED.event_type,
                            action = EXCLUDED.action,
                            severity = EXCLUDED.severity,
                            src_ip = EXCLUDED.src_ip,
                            dst_ip = EXCLUDED.dst_ip,
                            parser = EXCLUDED.parser,
                            status = EXCLUDED.status,
                            sha256 = EXCLUDED.sha256,
                            raw_message = EXCLUDED.raw_message,
                            ir_json = EXCLUDED.ir_json,
                            threat_json = EXCLUDED.threat_json,
                            storage_uri = EXCLUDED.storage_uri,
                            storage_status = EXCLUDED.storage_status,
                            opensearch_status = EXCLUDED.opensearch_status
                        """,
                        params,
                    )
                else:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO events (
                            event_id, raw_event_id, timestamp, source, vendor, product,
                            format, event_type, action, severity, src_ip, dst_ip,
                            parser, status, sha256, raw_message, ir_json, threat_json,
                            storage_uri, storage_status, opensearch_status, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        params,
                    )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to save event {record.get('event_id')}: {e}")
            return False

    def clear_all_events(self) -> bool:
        """Clear all stored events from database."""
        with self.get_connection() as conn:
            cursor: Any = conn.cursor()
            cursor.execute("DELETE FROM events")
            return True

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single event by event_id or raw_event_id."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        with self.get_connection() as conn:
            cursor: Any = conn.cursor()
            if is_pg:
                cursor.execute(
                    "SELECT * FROM events WHERE event_id = %s OR raw_event_id = %s LIMIT 1",
                    (event_id, event_id),
                )
            else:
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
        """Query events with dynamic multi-facet filtering and pagination."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"

        where_clauses: List[str] = []
        params: List[Any] = []

        if source:
            where_clauses.append(f"LOWER(source) = LOWER({ph})")
            params.append(source)
        if vendor:
            where_clauses.append(f"LOWER(vendor) = LOWER({ph})")
            params.append(vendor)
        if format:
            where_clauses.append(f"LOWER(format) = LOWER({ph})")
            params.append(format)
        if severity:
            where_clauses.append(f"LOWER(severity) = LOWER({ph})")
            params.append(severity)
        if action:
            where_clauses.append(f"LOWER(action) = LOWER({ph})")
            params.append(action)
        if status:
            where_clauses.append(f"LOWER(status) = LOWER({ph})")
            params.append(status)
        if search:
            s_param = f"%{search.lower()}%"
            where_clauses.append(
                f"(LOWER(event_id) LIKE {ph} OR "
                f"LOWER(raw_message) LIKE {ph} OR "
                f"LOWER(src_ip) LIKE {ph} OR "
                f"LOWER(dst_ip) LIKE {ph} OR "
                f"LOWER(source) LIKE {ph} OR "
                f"LOWER(vendor) LIKE {ph} OR "
                f"LOWER(format) LIKE {ph} OR "
                f"LOWER(action) LIKE {ph} OR "
                f"LOWER(status) LIKE {ph} OR "
                f"LOWER(sha256) LIKE {ph})"
            )
            params.extend([s_param] * 10)

        where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""
        count_query = f"SELECT COUNT(*) FROM events{where_sql}"
        select_query = f"SELECT * FROM events{where_sql} ORDER BY timestamp DESC, created_at DESC LIMIT {ph} OFFSET {ph}"

        with self.get_connection() as conn:
            cursor: Any = conn.cursor()
            self._execute_sql(cursor, count_query, params)
            res = cursor.fetchone()
            total = _to_scalar(res)

            query_params = list(params) + [limit, offset]
            self._execute_sql(cursor, select_query, query_params)
            rows = cursor.fetchall()

            events = []
            for r in rows:
                d = _to_dict(r)
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
            total_processed = _to_scalar(cursor.fetchone())

            cursor.execute("SELECT COUNT(*) FROM events WHERE status = 'success'")
            success_cnt = _to_scalar(cursor.fetchone())

            cursor.execute("SELECT COUNT(*) FROM events WHERE status = 'unparsed'")
            unparsed_cnt = _to_scalar(cursor.fetchone())

            cursor.execute("SELECT COUNT(*) FROM events WHERE status IN ('error', 'blocked')")
            error_cnt = _to_scalar(cursor.fetchone())

            cursor.execute("SELECT format, COUNT(*) FROM events GROUP BY format")
            rows = cursor.fetchall()
            fmt_dist = {}
            for row in rows:
                k = row[0]
                v = row[1]
                fmt_dist[k or "Unknown"] = v

            cursor.execute("SELECT COUNT(DISTINCT source) FROM events")
            active_sources = _to_scalar(cursor.fetchone())

            return {
                "total_processed": total_processed,
                "success_cnt": success_cnt,
                "unparsed_cnt": unparsed_cnt,
                "error_cnt": error_cnt,
                "fmt_dist": fmt_dist,
                "active_sources": active_sources,
            }

    get_event_stats = get_metrics_summary

    def clear_all_events(self) -> int:
        """Clear event table on demo reset."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events")
            return cursor.rowcount if hasattr(cursor, "rowcount") and cursor.rowcount >= 0 else 0

    # =========================================================================
    # 2. SOURCES REPOSITORY
    # =========================================================================
    def save_source(self, source_data: Dict[str, Any]) -> bool:
        """Insert or update a registered log source."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                sid = source_data.get("source_id") or source_data.get("id")
                name = source_data.get("name") or sid
                stype = source_data.get("source_type") or source_data.get("type", "Network Device")
                vendor = source_data.get("vendor", "Generic")
                protocol = source_data.get("protocol", "Syslog")
                address = source_data.get("address", "127.0.0.1")
                fmt = source_data.get("expected_format") or source_data.get("format", "Generic")
                status = source_data.get("status", "ACTIVE")
                is_blocked = 1 if source_data.get("is_blocked") else 0
                now_str = datetime.now(timezone.utc).isoformat()
                created_at = source_data.get("created_at") or now_str
                last_seen = source_data.get("last_seen") or now_str

                if is_pg:
                    cursor.execute(
                        """
                        INSERT INTO sources (
                            source_id, name, source_type, vendor, protocol, address,
                            expected_format, status, is_blocked, created_at, last_seen
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (source_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            source_type = EXCLUDED.source_type,
                            vendor = EXCLUDED.vendor,
                            protocol = EXCLUDED.protocol,
                            address = EXCLUDED.address,
                            expected_format = EXCLUDED.expected_format,
                            status = EXCLUDED.status,
                            is_blocked = EXCLUDED.is_blocked,
                            last_seen = EXCLUDED.last_seen
                        """,
                        (sid, name, stype, vendor, protocol, address, fmt, status, is_blocked, created_at, last_seen),
                    )
                else:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO sources (
                            source_id, name, source_type, vendor, protocol, address,
                            expected_format, status, is_blocked, created_at, last_seen
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (sid, name, stype, vendor, protocol, address, fmt, status, is_blocked, created_at, last_seen),
                    )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to save source: {e}")
            return False

    def get_source(self, source_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single source by ID."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM sources WHERE source_id = {ph} LIMIT 1", (source_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single event by ID."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM events WHERE event_id = {ph} LIMIT 1", (event_id,))
            row = cursor.fetchone()
            if row:
                d = _to_dict(row)
                if d.get("threat_json"):
                    try:
                        d["threat"] = json.loads(d["threat_json"])
                    except Exception:
                        d["threat"] = None
                return d
            return None

    def downgrade_event(self, event_id: str) -> bool:
        """Mark an event as a false positive by downgrading severity and removing threat details."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            ph = "%s" if is_pg else "?"
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"UPDATE events SET threat_json = NULL, severity = 'info', action = 'allow' WHERE event_id = {ph}",
                    (event_id,)
                )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to downgrade event {event_id}: {e}")
            return False

    def clear_all_sources(self) -> bool:
        """Clear all registered sources from the database on startup."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sources")
                return True
        except Exception:
            return False

    def list_sources(self) -> List[Dict[str, Any]]:
        """Retrieve all registered sources ordered by last seen."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sources ORDER BY last_seen DESC")
            return [dict(r) for r in cursor.fetchall()]

    def update_source_status(self, source_id: str, status: str, is_blocked: int) -> bool:
        """Update source active/blocked status."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE sources SET status = {ph}, is_blocked = {ph} WHERE source_id = {ph}",
                (status, is_blocked, source_id),
            )
            return True

    def delete_source(self, source_id: str) -> bool:
        """Delete source by ID."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM sources WHERE source_id = {ph}", (source_id,))
            return True

    # =========================================================================
    # 3. PARSERS REPOSITORY
    # =========================================================================
    def save_parser(self, parser_data: Dict[str, Any]) -> bool:
        """Save synthesized or approved parser to persistent registry."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now_str = datetime.now(timezone.utc).isoformat()
                params = (
                    parser_data.get("parser_id") or parser_data.get("id"),
                    parser_data.get("name", "Custom Parser"),
                    parser_data.get("format", "custom"),
                    parser_data.get("version", "1.0"),
                    parser_data.get("status", "ACTIVE"),
                    float(parser_data.get("confidence", 0.90)),
                    parser_data.get("author", "ULPF AI Studio"),
                    parser_data.get("description", "Dynamic parser specification"),
                    parser_data.get("code", ""),
                    parser_data.get("yaml_spec", ""),
                    now_str,
                )
                if is_pg:
                    cursor.execute(
                        """
                        INSERT INTO parsers (
                            parser_id, name, format, version, status, confidence,
                            author, description, code, yaml_spec, updated_at
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (parser_id) DO UPDATE SET
                            name = EXCLUDED.name,
                            format = EXCLUDED.format,
                            version = EXCLUDED.version,
                            status = EXCLUDED.status,
                            confidence = EXCLUDED.confidence,
                            author = EXCLUDED.author,
                            description = EXCLUDED.description,
                            code = EXCLUDED.code,
                            yaml_spec = EXCLUDED.yaml_spec,
                            updated_at = EXCLUDED.updated_at
                        """,
                        params,
                    )
                else:
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO parsers (
                            parser_id, name, format, version, status, confidence,
                            author, description, code, yaml_spec, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        params,
                    )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to save parser: {e}")
            return False

    def get_parser(self, parser_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve single parser by parser_id."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM parsers WHERE parser_id = {ph} LIMIT 1", (parser_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_parsers(self) -> List[Dict[str, Any]]:
        """Retrieve all parsers from persistent registry."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM parsers ORDER BY updated_at DESC")
            return [dict(r) for r in cursor.fetchall()]

    def delete_parser(self, parser_id: str) -> bool:
        """Remove parser from persistent registry."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM parsers WHERE parser_id = {ph}", (parser_id,))
            return True

    # =========================================================================
    # 4. AUDIT LOG REPOSITORY
    # =========================================================================
    def record_audit_log(
        self, action: str, user_name: str = "system", detail: str = "", status: str = "SUCCESS"
    ) -> bool:
        """Record operational action for governance and security compliance."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            ph = "%s" if is_pg else "?"
            with self.get_connection() as conn:
                cursor = conn.cursor()
                now_str = datetime.now(timezone.utc).isoformat()
                cursor.execute(
                    f"INSERT INTO audit_log (timestamp, action, user_name, detail, status) VALUES ({ph}, {ph}, {ph}, {ph}, {ph})",
                    (now_str, action, user_name, detail, status),
                )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to record audit log: {e}")
            return False

    def query_audit_logs(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieve recent audit logs with pagination."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM audit_log ORDER BY id DESC LIMIT {ph} OFFSET {ph}",
                (limit, offset),
            )
            return [dict(r) for r in cursor.fetchall()]

    # =========================================================================
    # 5. SYSTEM CONFIG REPOSITORY
    # =========================================================================
    def set_config(self, key: str, value: str) -> bool:
        """Save configuration setting."""
        try:
            is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
            now_str = datetime.now(timezone.utc).isoformat()
            with self.get_connection() as conn:
                cursor = conn.cursor()
                if is_pg:
                    cursor.execute(
                        """
                        INSERT INTO system_config (key, value, updated_at) VALUES (%s, %s, %s)
                        ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = EXCLUDED.updated_at
                        """,
                        (key, value, now_str),
                    )
                else:
                    cursor.execute(
                        "INSERT OR REPLACE INTO system_config (key, value, updated_at) VALUES (?, ?, ?)",
                        (key, value, now_str),
                    )
                return True
        except Exception as e:
            print(f"[DatabaseManager] Failed to set config {key}: {e}")
            return False

    def get_config(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieve configuration setting."""
        is_pg = (self.db_type == "postgres" and HAS_PSYCOPG and self.database_url)
        ph = "%s" if is_pg else "?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT value FROM system_config WHERE key = {ph} LIMIT 1", (key,))
            row = cursor.fetchone()
            if row:
                return _to_scalar(row, default=default)
            return default

    def list_config(self) -> Dict[str, str]:
        """List all system configuration keys and values."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM system_config")
            rows = cursor.fetchall()
            return {r[0]: r[1] for r in rows}

    # =========================================================================
    # 6. HEALTH & TELEMETRY
    # =========================================================================
    def check_health(self) -> Dict[str, Any]:
        """Perform database health check, measuring latency and record counts."""
        start_t = time.perf_counter()
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.execute("SELECT COUNT(*) FROM events")
                event_cnt = _to_scalar(cursor.fetchone())

                cursor.execute("SELECT COUNT(*) FROM sources")
                source_cnt = _to_scalar(cursor.fetchone())

                cursor.execute("SELECT COUNT(*) FROM parsers")
                parser_cnt = _to_scalar(cursor.fetchone())

                elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
                return {
                    "status": "healthy",
                    "backend": self.db_type,
                    "target": self.database_url or self.db_path,
                    "latency_ms": elapsed_ms,
                    "total_records": event_cnt,
                    "table_counts": {
                        "events": event_cnt,
                        "sources": source_cnt,
                        "parsers": parser_cnt,
                    },
                    "persisted": True,
                    "multi_backend_ready": True,
                    "supported_backends": ["sqlite", "postgres" if HAS_PSYCOPG else "postgres (driver ready)"],
                }
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
            return {
                "status": "degraded",
                "backend": self.db_type,
                "target": self.database_url or self.db_path,
                "latency_ms": elapsed_ms,
                "error": str(e),
                "persisted": False,
                "multi_backend_ready": True,
                "supported_backends": ["sqlite", "postgres" if HAS_PSYCOPG else "postgres (driver ready)"],
            }

    @staticmethod
    def test_connection_target(url: str) -> Dict[str, Any]:
        """Test connection to arbitrary database URL without switching active backend."""
        start_t = time.perf_counter()
        if not url:
            return {"status": "error", "message": "No database URL specified"}

        if url.startswith("sqlite://"):
            p = url.replace("sqlite:///", "").replace("sqlite://", "")
            try:
                c = sqlite3.connect(p, timeout=2.0)
                c.execute("SELECT 1")
                c.close()
                elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
                return {"status": "connected", "backend": "sqlite", "latency_ms": elapsed_ms}
            except Exception as e:
                return {"status": "failed", "backend": "sqlite", "error": str(e)}

        elif url.startswith("postgres://") or url.startswith("postgresql://"):
            if not HAS_PSYCOPG or psycopg is None:
                return {
                    "status": "driver_missing",
                    "backend": "postgres",
                    "error": "psycopg module is not installed in the current environment",
                }
            try:
                c = psycopg.connect(url, connect_timeout=3)  # type: ignore
                c.execute("SELECT 1")
                c.close()
                elapsed_ms = round((time.perf_counter() - start_t) * 1000, 2)
                return {"status": "connected", "backend": "postgres", "latency_ms": elapsed_ms}
            except Exception as e:
                return {"status": "failed", "backend": "postgres", "error": str(e)}

        return {"status": "unsupported_scheme", "error": "URL must start with sqlite:// or postgresql://"}
