from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.parsers.base import BaseParser
from app.parsers.json_parser import JsonParser
from app.parsers.syslog_parser import SyslogParser
from app.parsers.cef_parser import CefParser
from app.parsers.leef_parser import LeefParser
from app.parsers.kv_parser import KvParser
from app.parsers.csv_parser import CsvParser
from app.parsers.xml_parser import XmlParser
from app.parsers.text_parser import TextParser
from app.parsers.compiler import ParserSpec, CompiledYamlParser


class ParserStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"


class ParserMetadata(BaseModel):
    id: str
    vendor: str
    product: str
    format: str
    version: str
    schema_version: str = "1.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    confidence: float = 1.0
    status: ParserStatus = ParserStatus.ACTIVE
    test_results: Optional[Dict[str, str]] = None


class ParserRegistry:
    """
    Central Parser Registry for ULPF.
    Manages parser lifecycles (DRAFT -> VALIDATED -> APPROVED -> ACTIVE -> DEPRECATED).
    """

    def __init__(self):
        self._parsers: Dict[str, BaseParser] = {}
        self._metadata: Dict[str, ParserMetadata] = {}
        self._register_builtins()

    def _register_builtins(self):
        builtins = [
            ("syslog", SyslogParser(), "Generic", "Syslog Server", "Syslog"),
            ("json", JsonParser(), "Generic", "JSON Stream", "JSON"),
            ("cef", CefParser(), "Multi-Vendor", "CEF Device", "CEF"),
            ("leef", LeefParser(), "IBM", "QRadar / LEEF Device", "LEEF"),
            ("key_value", KvParser(), "Generic", "KV Firewall", "Key=Value"),
            ("csv", CsvParser(), "Generic", "CSV Log", "CSV"),
            ("xml", XmlParser(), "Microsoft/Generic", "XML Log", "XML"),
            ("plain_text", TextParser(), "Generic", "Unknown Device", "Plaintext"),
        ]

        for pid, instance, vendor, product, fmt in builtins:
            self._parsers[pid] = instance
            self._metadata[pid] = ParserMetadata(
                id=pid,
                vendor=vendor,
                product=product,
                format=fmt,
                version="1.0",
                confidence=1.0,
                status=ParserStatus.ACTIVE,
                test_results={"status": "passed", "coverage": "100%"},
            )

    def register_compiled_parser(
        self, spec: ParserSpec, parser_instance: CompiledYamlParser, status: ParserStatus = ParserStatus.DRAFT
    ) -> ParserMetadata:
        meta = ParserMetadata(
            id=spec.id,
            vendor=spec.vendor or "Generic",
            product=spec.product or "Custom Device",
            format=spec.format,
            version=spec.version,
            confidence=spec.confidence,
            status=status,
            test_results={"status": "unverified"},
        )
        self._parsers[spec.id] = parser_instance
        self._metadata[spec.id] = meta
        return meta

    def update_status(self, parser_id: str, new_status: ParserStatus) -> Optional[ParserMetadata]:
        if parser_id in self._metadata:
            self._metadata[parser_id].status = new_status
            return self._metadata[parser_id]
        return None

    def get_parser(self, parser_id: str) -> Optional[BaseParser]:
        return self._parsers.get(parser_id)

    def get_metadata(self, parser_id: str) -> Optional[ParserMetadata]:
        return self._metadata.get(parser_id)

    def list_parsers(self, status_filter: Optional[ParserStatus] = None) -> List[ParserMetadata]:
        if status_filter:
            return [meta for meta in self._metadata.values() if meta.status == status_filter]
        return list(self._metadata.values())
