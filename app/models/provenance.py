from typing import Any, Optional
from pydantic import BaseModel, Field


class ProvenanceRecord(BaseModel):
    """
    Field-level provenance record answering:
    Where did this normalized canonical field come from?
    """
    value: Any
    original_field: str
    original_value: Any
    parser: str
    rule: Optional[str] = "direct_mapping"
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
