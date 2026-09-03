from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LogInputRequest(BaseModel):
    log: str = Field(..., description="Raw log message string")
    source: Optional[str] = "network_device"


class SamplesInputRequest(BaseModel):
    sample_logs: List[str] = Field(..., description="10-100 sample unparsed log strings")


class GenerateParserRequest(BaseModel):
    yaml_spec: str = Field(..., description="YAML parser specification string")


class ApproveParserRequest(BaseModel):
    parser_id: str = Field(..., description="Parser ID to approve")


class DetectResponse(BaseModel):
    format: str
    confidence: float
    reason: str


class ParseResponse(BaseModel):
    status: str
    format: str
    raw_hash: str
    extracted_fields: Dict[str, Any]
    reason: Optional[str] = None


class NormalizeResponse(BaseModel):
    status: str
    normalized_event: Dict[str, Any]
    provenance: Dict[str, Any]
    unmapped: Dict[str, Any]


class ProcessResponse(BaseModel):
    status: str
    detection: DetectResponse
    canonical_event: Dict[str, Any]
    provenance: Dict[str, Any]
    ocsf_export: Dict[str, Any]
    ecs_export: Dict[str, Any]
    raw_hash: str
    reason: Optional[str] = None
