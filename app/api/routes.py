from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.api.schemas import (
    LogInputRequest,
    SamplesInputRequest,
    GenerateParserRequest,
    ApproveParserRequest,
    DetectResponse,
    ParseResponse,
    NormalizeResponse,
    ProcessResponse,
)
from app.pipeline import UlpfPipeline
from app.ai.onboarding import AiOnboardingEngine
from app.parsers.compiler import ParserCompiler
from app.parsers.registry import ParserStatus, ParserMetadata
from app.models.raw_event import create_raw_event

router = APIRouter()
pipeline = UlpfPipeline()
ai_engine = AiOnboardingEngine()

# In-memory store for recent events (for /events/{id} and /events/{id}/provenance)
EVENT_STORE: dict = {}


@router.get("/health")
def get_health():
    return {
        "status": "ok",
        "service": "ULPF Core Engine",
        "phase": "1-11 Full Master Implementation",
        "version": "1.0.0",
        "schema_version": "1.0",
    }


@router.post("/detect", response_model=DetectResponse)
def post_detect(request: LogInputRequest):
    res = pipeline.detector.detect(request.log)
    return DetectResponse(format=res.format, confidence=res.confidence, reason=res.reason)


@router.post("/parse", response_model=ParseResponse)
def post_parse(request: LogInputRequest):
    raw_ev = create_raw_event(request.log, source=request.source or "network_device")
    detection = pipeline.detector.detect(request.log)
    raw_ev.format = detection.format
    
    parser_map = {
        "JSON": "json",
        "Syslog": "syslog",
        "CEF": "cef",
        "LEEF": "leef",
        "Key=Value": "key_value",
        "CSV": "csv",
        "XML": "xml",
        "Plaintext": "plain_text",
    }
    pid = parser_map.get(detection.format, "plain_text")
    parser = pipeline.registry.get_parser(pid) or pipeline.registry.get_parser("plain_text")
    res = parser.parse(raw_ev)
    return ParseResponse(
        status=res.status,
        format=detection.format,
        raw_hash=raw_ev.raw_hash,
        extracted_fields=res.fields,
        reason=res.reason,
    )


@router.post("/normalize", response_model=NormalizeResponse)
def post_normalize(request: LogInputRequest):
    ir = pipeline.process(request.log, source=request.source or "network_device")
    EVENT_STORE[ir.ulpf.event_id] = ir
    return NormalizeResponse(
        status=ir.status,
        normalized_event=ir.model_dump(exclude={"original", "provenance", "ulpf"}),
        provenance={k: v.model_dump() for k, v in ir.provenance.items()},
        unmapped=ir.unmapped,
    )


@router.post("/process", response_model=ProcessResponse)
def post_process(request: LogInputRequest):
    detection = pipeline.detector.detect(request.log)
    ir = pipeline.process(request.log, source=request.source or "network_device")
    EVENT_STORE[ir.ulpf.event_id] = ir

    ocsf_data = pipeline.export_ocsf(ir)
    ecs_data = pipeline.export_ecs(ir)

    return ProcessResponse(
        status=ir.status,
        detection=DetectResponse(
            format=detection.format,
            confidence=detection.confidence,
            reason=detection.reason,
        ),
        canonical_event=ir.model_dump(exclude={"original", "provenance", "ulpf"}),
        provenance={k: v.model_dump() for k, v in ir.provenance.items()},
        ocsf_export=ocsf_data,
        ecs_export=ecs_data,
        raw_hash=ir.original.sha256,
        reason=ir.reason,
    )


# ---------------------------------------------------------
# AI Onboarding & Parser Registry Endpoints
# ---------------------------------------------------------

@router.post("/onboarding/analyze")
def post_onboarding_analyze(request: SamplesInputRequest):
    """
    Analyze sample unparsed logs using local AI SLM (Ollama Qwen 3B/4B).
    """
    proposal = ai_engine.analyze_samples(request.sample_logs)
    return proposal.model_dump()


@router.post("/onboarding/generate-parser")
def post_onboarding_generate(request: GenerateParserRequest):
    """
    Compile YAML parser spec into an executable deterministic parser in DRAFT status.
    """
    try:
        spec, compiled_parser = ParserCompiler.compile_from_yaml(request.yaml_spec)
        meta = pipeline.registry.register_compiled_parser(spec, compiled_parser, status=ParserStatus.DRAFT)
        return {"status": "success", "metadata": meta.model_dump(), "spec": spec.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Parser compilation error: {str(e)}")


@router.post("/onboarding/validate")
def post_onboarding_validate(parser_id: str = Query(...)):
    """
    Validate a draft parser against test samples.
    """
    meta = pipeline.registry.update_status(parser_id, ParserStatus.VALIDATED)
    if not meta:
        raise HTTPException(status_code=404, detail="Parser ID not found")
    return {"status": "validated", "metadata": meta.model_dump()}


@router.post("/onboarding/approve")
def post_onboarding_approve(request: ApproveParserRequest):
    """
    Approve validated parser and promote to ACTIVE status in production parser registry.
    """
    meta = pipeline.registry.update_status(request.parser_id, ParserStatus.ACTIVE)
    if not meta:
        raise HTTPException(status_code=404, detail="Parser ID not found")
    return {"status": "approved", "metadata": meta.model_dump()}


@router.get("/parsers", response_model=List[ParserMetadata])
def get_parsers(status: Optional[ParserStatus] = None):
    return pipeline.registry.list_parsers(status_filter=status)


@router.get("/parsers/{parser_id}")
def get_parser_by_id(parser_id: str):
    meta = pipeline.registry.get_metadata(parser_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Parser not found")
    return meta.model_dump()


@router.get("/events/{event_id}")
def get_event_by_id(event_id: str):
    if event_id not in EVENT_STORE:
        raise HTTPException(status_code=404, detail="Event ID not found in store")
    return EVENT_STORE[event_id].model_dump()


@router.get("/events/{event_id}/provenance")
def get_event_provenance(event_id: str):
    if event_id not in EVENT_STORE:
        raise HTTPException(status_code=404, detail="Event ID not found in store")
    ir = EVENT_STORE[event_id]
    return {
        "event_id": event_id,
        "raw_hash": ir.original.sha256,
        "provenance": {k: v.model_dump() for k, v in ir.provenance.items()},
    }
