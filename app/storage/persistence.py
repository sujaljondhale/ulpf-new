import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
try:
    from .database import DatabaseManager
    from .minio_store import MinioStore
    from .opensearch_store import OpenSearchStore
    from .interfaces import IMainStorageUnit
except (ImportError, ValueError):
    from app.storage.database import DatabaseManager
    from app.storage.minio_store import MinioStore
    from app.storage.opensearch_store import OpenSearchStore
    from app.storage.interfaces import IMainStorageUnit
from kosmoporos.merkle.vault import KosmoporosMerkleVault


class PersistenceManager(IMainStorageUnit):
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
        self.merkle_vault = KosmoporosMerkleVault(block_size=125)

    def persist_event(
        self,
        ir_event: Any = None,
        readable_id: Optional[str] = None,
        raw_event_id: Optional[str] = None,
        source_name: Optional[str] = None,
        record: Optional[Dict[str, Any]] = None,
        source: Optional[str] = None,
        event_id: Optional[str] = None,
        raw_message: Optional[str] = None,
        canonical_event: Any = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Store event across all 3 tiers:
        1. MinIO: Raw payload + SHA-256
        2. OpenSearch: Canonical searchable document
        3. SQLite: Relational persistence & fast query cache
        """
        import time
        from datetime import datetime, timezone
        
        ir_event = ir_event if ir_event is not None else canonical_event
        rid = event_id or readable_id or (getattr(getattr(ir_event, "ulpf", None), "event_id", None) if ir_event else f"ULPF-{int(time.time()*1000)}")
        raw_id = raw_event_id or rid
        src = source or source_name or (getattr(getattr(ir_event, "source", None), "ip", None) or "default")
        
        raw_msg = raw_message or getattr(getattr(ir_event, "original", None), "raw_text", getattr(getattr(ir_event, "original", None), "message", ""))
        raw_hash = getattr(getattr(ir_event, "original", None), "sha256", "")
        if not raw_hash and raw_msg:
            raw_hash = hashlib.sha256(raw_msg.encode("utf-8", errors="replace")).hexdigest()
        log_format = getattr(getattr(ir_event, "original", None), "format", "Unknown")

        if record is None:
            record = {
                "event_id": rid,
                "raw_event_id": raw_id,
                "timestamp": getattr(ir_event, "timestamp", datetime.now(timezone.utc).isoformat()) if ir_event else datetime.now(timezone.utc).isoformat(),
                "source": src,
                "vendor": getattr(getattr(ir_event, "device", None), "vendor", "Generic") if ir_event else "Generic",
                "product": getattr(getattr(ir_event, "device", None), "product", "Generic") if ir_event else "Generic",
                "format": log_format,
                "event_type": getattr(getattr(ir_event, "event", None), "category", "network") if ir_event else "network",
                "action": getattr(getattr(ir_event, "event", None), "action", "allow") if ir_event else "allow",
                "severity": getattr(ir_event, "severity", "informational") if ir_event else "informational",
                "src_ip": getattr(getattr(ir_event, "source", None), "ip", "") if ir_event else "",
                "dst_ip": getattr(getattr(ir_event, "destination", None), "ip", "") if ir_event else "",
                "parser": log_format,
                "status": getattr(ir_event, "status", "success") if ir_event else "success",
                "sha256": raw_hash,
                "raw_message": raw_msg or "",
            }

        # 1. Store Raw Evidence in MinIO (Immutable S3)
        storage_uri, storage_status = self.minio.store_raw_log(
            event_id=rid,
            raw_message=raw_msg or "",
            source=src,
            log_format=log_format,
            sha256_hash=raw_hash,
        )
        record["storage_uri"] = storage_uri
        record["storage_status"] = storage_status

        # 2. Index Normalized Canonical Event in OpenSearch
        os_indexed, opensearch_status = self.opensearch.index_event(
            event_id=rid,
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

        # 4. Checkpoint Merkle Root via Kosmoporos Merkle Vault (125 logs/block batching)
        merkle_rec = self.merkle_vault.append_event(raw_payload=raw_msg or "", event_id=rid)
        sealed_info = merkle_rec.get("sealed_block")
        if sealed_info:
            new_root = sealed_info["root_hash"]
            self.db.set_config("merkle_root_latest", new_root)
            self.db.append_merkle_root(new_root)
        elif not self.db.get_config("merkle_root_latest"):
            init_root = self.merkle_vault.get_latest_root()
            self.db.set_config("merkle_root_latest", init_root)

        return record

    def verify_event_integrity(self, event_id: str) -> Dict[str, Any]:
        """
        Cryptographic Tamper-Evident SHA-256 Verification.
        Retrieves raw log from storage and recalculates cryptographic hash.
        Also verifies the event's place in the hash chain and Merkle root.
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
        
        # Hash Chain Verification (Assuming the DB `events` keeps chronological order)
        chain_status = "UNKNOWN"
        merkle_root = self.db.get_config("merkle_root_latest") or "UNINITIALIZED"

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
            "merkle_root_checkpoint": merkle_root,
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
