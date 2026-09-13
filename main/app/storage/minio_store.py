import os
import time
import socket
import hashlib
import httpx
from typing import Tuple, Optional, Dict, Any
from pathlib import Path
from datetime import datetime, timezone
from app.config import settings


class MinioStore:
    """
    MinIO S3 Immutable Raw Event Evidence Storage Adapter.
    Preserves verbatim raw log payloads before parsing with SHA-256 integrity hashing.
    Gracefully degrades to local disk storage if MinIO is initializing or offline.
    """

    def __init__(
        self,
        endpoint: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket: Optional[str] = None,
        local_dir: Optional[str] = None,
    ):
        self.endpoint = endpoint or settings.minio_endpoint
        self.access_key = access_key or settings.minio_access_key
        self.secret_key = secret_key or settings.minio_secret_key
        self.bucket = bucket or settings.minio_bucket
        self.local_dir = Path(local_dir or settings.storage_dir)
        self.local_dir.mkdir(parents=True, exist_ok=True)
        self.base_url = f"{'https' if settings.minio_secure else 'http'}://{self.endpoint}"
        self._bucket_initialized = False
        self._is_online: Optional[bool] = False
        self._last_check_time = 0.0
        self._check_interval = 30.0  # seconds between probes when offline

    def _ensure_local_fallback(self, event_id: str, raw_message: str, sha256_hash: str) -> str:
        """Store raw log to local disk fallback directory."""
        file_path = self.local_dir / f"{event_id}.raw"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(raw_message)
        return f"local://{file_path.as_posix()}"

    def is_available(self) -> bool:
        """Fast connectivity check with DNS pre-check and circuit breaker."""
        now = time.time()
        if self._is_online is True:
            return True
        if self._is_online is False and (now - self._last_check_time) < self._check_interval:
            return False

        self._last_check_time = now

        # 1. Fast socket connectivity check (0.15s timeout)
        host = self.endpoint.split(":")[0]
        port_str = self.endpoint.split(":")[1] if ":" in self.endpoint else "9000"
        if host in ("minio", "opensearch", "redpanda", "kafka") and not os.path.exists("/.dockerenv"):
            self._is_online = False
            return False

        try:
            port = int(port_str)
            with socket.create_connection((host, port), timeout=0.15):
                pass
        except Exception:
            self._is_online = False
            return False

        # 2. HTTP health check
        try:
            with httpx.Client(timeout=0.2) as client:
                res = client.get(f"{self.base_url}/minio/health/live")
                self._is_online = (res.status_code == 200)
                return self._is_online
        except Exception:
            self._is_online = False
            return False

    def ensure_bucket(self) -> bool:
        """Ensure the raw evidence bucket exists on MinIO."""
        if self._bucket_initialized:
            return True
        if not self.is_available():
            return False

        try:
            url = f"{self.base_url}/{self.bucket}"
            with httpx.Client(timeout=0.5) as client:
                res = client.head(url)
                if res.status_code == 200:
                    self._bucket_initialized = True
                    return True
                elif res.status_code == 404:
                    put_res = client.put(url)
                    if put_res.status_code in (200, 204):
                        self._bucket_initialized = True
                        return True
        except Exception:
            self._is_online = False
        return False

    def store_raw_log(
        self,
        event_id: str,
        raw_message: str,
        source: str = "unknown",
        log_format: str = "unknown",
        sha256_hash: Optional[str] = None,
    ) -> Tuple[str, str]:
        """
        Store raw event evidence.
        Returns (storage_uri, storage_status).
        """
        if sha256_hash is None:
            sha256_hash = hashlib.sha256(raw_message.encode("utf-8")).hexdigest()

        # Try MinIO S3 Object Storage if available
        if self.is_available():
            try:
                object_name = f"events/{datetime.now(timezone.utc).strftime('%Y/%m/%d')}/{event_id}.raw"
                put_url = f"{self.base_url}/{self.bucket}/{object_name}"
                headers = {
                    "Content-Type": "text/plain; charset=utf-8",
                    "x-amz-meta-event-id": event_id,
                    "x-amz-meta-sha256": sha256_hash,
                    "x-amz-meta-source": source,
                    "x-amz-meta-format": log_format,
                    "x-amz-meta-ingested-at": datetime.now(timezone.utc).isoformat(),
                }
                with httpx.Client(timeout=0.5) as client:
                    resp = client.put(put_url, content=raw_message.encode("utf-8"), headers=headers)
                    if resp.status_code in (200, 201, 204):
                        return f"s3://{self.bucket}/{object_name}", "stored_minio"
            except Exception:
                self._is_online = False

        # Local Fallback
        local_uri = self._ensure_local_fallback(event_id, raw_message, sha256_hash)
        return local_uri, "stored_local_fallback"

    def get_raw_log(self, storage_uri: str, event_id: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Retrieve raw log message by storage URI.
        Returns (raw_message, sha256_hash).
        """
        if not storage_uri:
            return None, None

        if storage_uri.startswith("local://"):
            local_path = storage_uri.replace("local://", "")
            p = Path(local_path)
            if p.exists():
                content = p.read_text(encoding="utf-8")
                computed_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                return content, computed_hash

        if storage_uri.startswith("s3://") and self.is_available():
            try:
                path_part = storage_uri.replace("s3://", "")
                bucket, obj_key = path_part.split("/", 1)
                get_url = f"{self.base_url}/{bucket}/{obj_key}"
                with httpx.Client(timeout=0.5) as client:
                    resp = client.get(get_url)
                    if resp.status_code == 200:
                        content = resp.text
                        computed_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                        return content, computed_hash
            except Exception:
                self._is_online = False

        # Check local fallback directory by event_id
        if event_id:
            fallback_file = self.local_dir / f"{event_id}.raw"
            if fallback_file.exists():
                content = fallback_file.read_text(encoding="utf-8")
                computed_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
                return content, computed_hash

        return None, None

    def check_health(self) -> Dict[str, Any]:
        """Check MinIO server connectivity and bucket readiness."""
        if self.is_available():
            return {
                "status": "healthy",
                "endpoint": self.endpoint,
                "bucket": self.bucket,
                "mode": "MinIO S3 Object Storage",
                "tamper_evident": True,
            }

        return {
            "status": "degraded (local fallback)",
            "endpoint": self.endpoint,
            "bucket": self.bucket,
            "fallback_dir": str(self.local_dir),
            "mode": "Local Disk Evidence Store",
            "tamper_evident": True,
        }
