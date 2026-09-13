import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from app.storage.database import DatabaseManager
from app.storage.minio_store import MinioStore
from app.storage.opensearch_store import OpenSearchStore


class PersistenceManager:
    """
    Master Storage & Persistence Coordinator.
    Architecture:
      MINIO        -> Immutable Raw Evidence Source of Truth (S3 Object)
      OPENSEARCH   -> Searchable Normalized Canonical Representation
      SQLITE DB    -> Persistent Metadata, Sources, Parsers, & Restart Cache
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.minio = MinioStore()
        self.opensearch = OpenSearchStore()

    def persist_event(
        self,
        ir_event: Any,
        readable_id: str,
        raw_event_id: str,
        source_name: str,
        record: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Store event across all 3 tiers:
        1. MinIO: Raw payload + SHA-256
        2. OpenSearch: Canonical searchable document
        3. SQLite: Relational persistence & fast query cache
        """
        raw_message = getattr(ir_event.original, "message", "") or record.get("raw_message", "")
        raw_hash = getattr(ir_event.original, "sha256", "") or record.get("sha256", "")
        log_format = getattr(ir_event.original, "format", "Unknown")

        # 1. Store Raw Evidence in MinIO (Immutable S3)
        storage_uri, storage_status = self.minio.store_raw_log(
            event_id=readable_id,
            raw_message=raw_message,
            source=source_name,
            log_format=log_format,
            sha256_hash=raw_hash,
        )
        record["storage_uri"] = storage_uri
        record["storage_status"] = storage_status

        # 2. Index Normalized Canonical Event in OpenSearch
        os_indexed, opensearch_status = self.opensearch.index_event(
            event_id=readable_id,
            document=record,
        )
        record["opensearch_status"] = opensearch_status

        # 3. Store in SQLite Database for persistent state across restarts
        ir_json = "{}"
        try:
            if hasattr(ir_event, "model_dump_json"):
                ir_json = ir_event.model_dump_json()
            elif hasattr(ir_event, "json"):
                ir_json = ir_event.json()
        except Exception:
            pass

        self.db.save_event(
            record=record,
            ir_json=ir_json,
            storage_uri=storage_uri,
            storage_status=storage_status,
            opensearch_status=opensearch_status,
        )

        return record

    def verify_event_integrity(self, event_id: str) -> Dict[str, Any]:
        """
        Cryptographic Tamper-Evident SHA-256 Verification.
        Retrieves raw log from storage and recalculates cryptographic hash.
        """
        event_record = self.db.get_event(event_id)
        if not event_record:
            return {
                "event_id": event_id,
                "integrity_status": "NOT_FOUND",
                "match": False,
                "error": f"Event {event_id} not found in persistent storage",
            }

        storage_uri = event_record.get("storage_uri", "")
        stored_hash = event_record.get("sha256", "")
        raw_message, computed_hash = self.minio.get_raw_log(storage_uri, event_id=event_id)

        if raw_message is None:
            raw_message = event_record.get("raw_message", "")
            computed_hash = hashlib.sha256(raw_message.encode("utf-8")).hexdigest()

        is_valid = (stored_hash == computed_hash)

        return {
            "event_id": event_id,
            "integrity_status": "INTEGRITY_VERIFIED" if is_valid else "INTEGRITY_MISMATCH",
            "stored_hash": stored_hash,
            "calculated_hash": computed_hash,
            "algorithm": "SHA-256",
            "tamper_evident": True,
            "match": is_valid,
            "storage_uri": storage_uri,
            "storage_status": event_record.get("storage_status"),
            "evidence_length_bytes": len(raw_message.encode("utf-8")) if raw_message else 0,
        }

    def get_storage_health(self) -> Dict[str, Any]:
        """Return health status of MinIO, OpenSearch, and SQLite."""
        minio_health = self.minio.check_health()
        opensearch_health = self.opensearch.check_health()
        db_health = self.db.check_health()

        return {
            "minio": minio_health,
            "opensearch": opensearch_health,
            "sqlite": db_health,
        }

    def load_startup_events(self) -> List[Dict[str, Any]]:
        """Load persistent events on system boot to restore cache."""
        return self.db.get_all_recent_events(limit=1000)

    def clear_all_events(self) -> int:
        """Clear persistent event database on demo reset."""
        return self.db.clear_all_events()
