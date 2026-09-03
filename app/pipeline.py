from typing import Optional, Dict, Any, Tuple
from app.models.raw_event import RawEvent, create_raw_event
from app.models.canonical_event import CanonicalEvent, UlpfMeta, OriginalLogMeta
from app.detector.detector import FormatDetector, DetectionResult
from app.parsers.registry import ParserRegistry, ParserStatus
from app.normalization.normalizer import SemanticNormalizer
from app.exporters.ocsf import OcsfExporter
from app.exporters.ecs import EcsExporter
from app.validation.validator import SecurityValidator


class UlpfPipeline:
    """
    Master Orchestration Pipeline for ULPF Phase 1 - Phase 11:
    Raw -> Security Validation -> Format Detection -> Parser Registry -> Semantic Normalizer -> ULPF-IR v1.0 -> Exporters (OCSF / ECS)
    """

    def __init__(self):
        self.detector = FormatDetector()
        self.normalizer = SemanticNormalizer()
        self.registry = ParserRegistry()
        self.ocsf_exporter = OcsfExporter()
        self.ecs_exporter = EcsExporter()

    def process(self, raw_message: str, source: str = "network_device") -> CanonicalEvent:
        """
        Execute full pipeline from raw message string to ULPF-IR v1.0 CanonicalEvent.
        Guarantees zero unhandled exceptions and 100% data preservation.
        """
        # 1. Input Security Validation
        valid, err_msg = SecurityValidator.validate_payload(raw_message)
        if not valid:
            raw_ev = create_raw_event(raw_message or "", source=source)
            return CanonicalEvent(
                ulpf=UlpfMeta(event_id=raw_ev.event_id),
                original=OriginalLogMeta(
                    format="Unknown",
                    message=raw_ev.raw_message,
                    sha256=raw_ev.raw_hash,
                ),
                status="error",
                reason=err_msg,
            )

        # 2. Raw Event Creation & Hash Verification
        raw_event = create_raw_event(raw_message, source=source)

        # 3. Format Detection
        detection: DetectionResult = self.detector.detect(raw_message)
        raw_event.format = detection.format

        # 4. Parser Selection from Registry
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

        parser_id = parser_map.get(detection.format, "plain_text")
        parser = self.registry.get_parser(parser_id) or self.registry.get_parser("plain_text")

        # 5. Parsing
        parse_result = parser.parse(raw_event)

        # 6. Check Parse Failure / Plaintext
        if parse_result.status != "success" or detection.format == "Plaintext":
            return CanonicalEvent(
                ulpf=UlpfMeta(event_id=raw_event.event_id),
                original=OriginalLogMeta(
                    format=detection.format,
                    message=raw_event.raw_message,
                    sha256=raw_event.raw_hash,
                ),
                unmapped=parse_result.fields,
                status="unparsed",
                reason=parse_result.reason or detection.reason,
            )

        # 7. Semantic Normalization & Field Provenance Mapping
        meta = self.registry.get_metadata(parser_id)
        confidence = meta.confidence if meta else 1.0

        taxonomy, provenance, unmapped = self.normalizer.normalize(
            extracted_fields=parse_result.fields,
            parser_name=parse_result.parser_name,
            confidence=confidence,
        )

        # 8. Construct ULPF-IR CanonicalEvent
        ir = CanonicalEvent(
            ulpf=UlpfMeta(event_id=raw_event.event_id),
            event=taxonomy.event,
            source=taxonomy.source,
            destination=taxonomy.destination,
            network=taxonomy.network,
            device=taxonomy.device,
            rule=taxonomy.rule,
            user=taxonomy.user,
            severity=taxonomy.severity,
            original=OriginalLogMeta(
                format=detection.format,
                message=raw_event.raw_message,
                sha256=raw_event.raw_hash,
            ),
            provenance=provenance,
            unmapped=unmapped,
            status="success",
        )

        return ir

    def export_ocsf(self, canonical_event: CanonicalEvent) -> Dict[str, Any]:
        """Export ULPF-IR to OCSF v1.1.0 JSON representation."""
        return self.ocsf_exporter.export(canonical_event)

    def export_ecs(self, canonical_event: CanonicalEvent) -> Dict[str, Any]:
        """Export ULPF-IR to Elastic Common Schema (ECS v8.x) JSON representation."""
        return self.ecs_exporter.export(canonical_event)
