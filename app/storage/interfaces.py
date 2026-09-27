from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple


class ITempStorageUnit(ABC):
    """
    Temporary Storage Unit Interface.
    Acts as a high-throughput staging buffer decoupling network ingress from parsing workers.
    Stores unaltered raw logs with unique IDs.
    """

    @abstractmethod
    def stage_raw_log(
        self,
        event_id: str,
        raw_payload: str,
        source: str = "network_device",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Stage an incoming raw log with its unique ID."""
        pass

    @abstractmethod
    def fetch_next(self, batch_size: int = 100) -> List[Dict[str, Any]]:
        """Fetch staged raw logs for processing."""
        pass

    @abstractmethod
    def ack(self, event_ids: List[str]) -> None:
        """Acknowledge completed processing and purge from staging."""
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, Any]:
        """Return staging queue depth, total staged, and dropped counts."""
        pass


class IMainStorageUnit(ABC):
    """
    Main Storage Unit Interface.
    Designed to store raw logs and parsed logs under the exact same unique event_id.
    """

    @abstractmethod
    def persist_event(
        self,
        event_id: Optional[str] = None,
        raw_message: Optional[str] = None,
        canonical_event: Any = None,
        source: str = "network_device",
        metadata: Optional[Dict[str, Any]] = None,
        ir_event: Any = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Persist both raw log and parsed canonical event correlated with the same ID."""
        pass

    @abstractmethod
    def verify_event_integrity(self, event_id: str) -> Dict[str, Any]:
        """Cryptographically verify raw payload SHA-256 and Merkle hash chain."""
        pass
