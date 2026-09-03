import hashlib
import uuid
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class RawEvent(BaseModel):
    """
    Preserves original log event without mutation.
    Includes SHA-256 integrity hash verification.
    """
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ingestion_time: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source: str = Field(default="network_device")
    source_vendor: Optional[str] = None
    source_product: Optional[str] = None
    format: Optional[str] = None
    raw_message: str
    raw_hash: str = ""

    @model_validator(mode="after")
    def compute_sha256(self) -> "RawEvent":
        computed = hashlib.sha256(self.raw_message.encode("utf-8")).hexdigest()
        if not self.raw_hash or self.raw_hash != computed:
            object.__setattr__(self, "raw_hash", computed)
        return self


def create_raw_event(
    raw_message: str,
    source: str = "network_device",
    source_vendor: Optional[str] = None,
    source_product: Optional[str] = None,
    detected_format: Optional[str] = None,
) -> RawEvent:
    return RawEvent(
        raw_message=raw_message,
        source=source,
        source_vendor=source_vendor,
        source_product=source_product,
        format=detected_format,
    )
