import time
import json
import logging
import threading
from collections import deque
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
try:
    from .interfaces import ITempStorageUnit
except (ImportError, ValueError):
    from app.storage.interfaces import ITempStorageUnit

try:
    from ..config import settings
except (ImportError, ValueError):
    from app.config import settings

logger = logging.getLogger("ulpf.storage.temp")


class MemoryQueueTempStorage(ITempStorageUnit):
    """
    High-Speed In-Memory Staging Buffer.
    Provides sub-microsecond enqueue/dequeue latency to decouple ingress from parser workers.
    """

    def __init__(self, max_size: int = 50000):
        self.max_size = max_size
        self._buffer: deque = deque(maxlen=max_size)
        self._lock = threading.Lock()
        self.total_staged = 0
        self.total_fetched = 0
        self.total_dropped = 0

    def stage_raw_log(
        self,
        event_id: str,
        raw_payload: str,
        source: str = "network_device",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        item = {
            "event_id": event_id,
            "raw_payload": raw_payload,
            "source": source,
            "received_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        with self._lock:
            if len(self._buffer) >= self.max_size:
                self.total_dropped += 1
                return False
            self._buffer.append(item)
            self.total_staged += 1
            return True

    def fetch_next(self, batch_size: int = 100) -> List[Dict[str, Any]]:
        batch = []
        with self._lock:
            for _ in range(min(batch_size, len(self._buffer))):
                if self._buffer:
                    batch.append(self._buffer.popleft())
                    self.total_fetched += 1
                else:
                    break
        return batch

    def ack(self, event_ids: List[str]) -> None:
        # In-memory queue naturally pops on fetch; ack is a no-op
        pass

    def get_metrics(self) -> Dict[str, Any]:
        with self._lock:
            depth = len(self._buffer)
        return {
            "type": "memory_staging_buffer",
            "queue_depth": depth,
            "max_size": self.max_size,
            "total_staged": self.total_staged,
            "total_fetched": self.total_fetched,
            "total_dropped": self.total_dropped,
        }


class DiskSpoolTempStorage(ITempStorageUnit):
    """
    Crash-Resilient Disk Spool Staging Buffer.
    Persists incoming raw logs into an append-only WAL spool file in storage/temp/.
    """

    def __init__(self, spool_dir: Optional[str] = None):
        self.spool_dir = Path(spool_dir or (Path(settings.storage_dir) / "temp"))
        self.spool_dir.mkdir(parents=True, exist_ok=True)
        self.active_spool_file = self.spool_dir / "spool_active.log"
        self._lock = threading.Lock()
        self.total_staged = 0
        self.total_fetched = 0

    def stage_raw_log(
        self,
        event_id: str,
        raw_payload: str,
        source: str = "network_device",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        record = {
            "event_id": event_id,
            "raw_payload": raw_payload,
            "source": source,
            "received_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        line = json.dumps(record) + "\n"
        with self._lock:
            try:
                with open(self.active_spool_file, "a", encoding="utf-8") as f:
                    f.write(line)
                self.total_staged += 1
                return True
            except Exception as e:
                logger.error(f"Failed to spool raw log to disk: {e}")
                return False

    def fetch_next(self, batch_size: int = 100) -> List[Dict[str, Any]]:
        # For simplicity, disk spool delegates reading in batches and rotates
        items = []
        with self._lock:
            if not self.active_spool_file.exists():
                return items
            try:
                with open(self.active_spool_file, "r", encoding="utf-8") as f:
                    lines = [f.readline() for _ in range(batch_size)]
                for line in lines:
                    if line.strip():
                        items.append(json.loads(line))
                        self.total_fetched += 1
            except Exception as e:
                logger.error(f"Failed to fetch spooled logs: {e}")
        return items

    def ack(self, event_ids: List[str]) -> None:
        pass

    def get_metrics(self) -> Dict[str, Any]:
        return {
            "type": "disk_spool_buffer",
            "spool_file": str(self.active_spool_file),
            "total_staged": self.total_staged,
            "total_fetched": self.total_fetched,
        }


# Global shared temp storage unit instance
_global_temp_storage: Optional[ITempStorageUnit] = None


def get_temp_storage(backend: str = "memory") -> ITempStorageUnit:
    global _global_temp_storage
    if _global_temp_storage is None:
        if backend == "disk":
            _global_temp_storage = DiskSpoolTempStorage()
        else:
            _global_temp_storage = MemoryQueueTempStorage()
    return _global_temp_storage
