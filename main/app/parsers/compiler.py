import re
import yaml
from typing import Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field
from app.models.raw_event import RawEvent
from app.parsers.base import BaseParser, ParseResult


class ParserSpec(BaseModel):
    id: str
    version: str = "1.0"
    vendor: Optional[str] = "Generic"
    product: Optional[str] = "Generic"
    format: str  # "key_value", "regex", "json", "csv", "syslog"
    regex_pattern: Optional[str] = None
    mapping: Dict[str, str] = Field(default_factory=dict)
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)


class CompiledYamlParser(BaseParser):
    """
    Dynamically compiled parser generated from a YAML Parser Specification.
    Executes compiled regex / extraction rules deterministically.
    """

    def __init__(self, spec: ParserSpec):
        self.spec = spec
        self._compiled_regex = re.compile(spec.regex_pattern) if spec.regex_pattern else None

    @property
    def parser_name(self) -> str:
        return self.spec.id

    def parse(self, raw_event: RawEvent) -> ParseResult:
        msg = raw_event.raw_message.strip()
        fields: Dict[str, Any] = {}

        if self.spec.format == "regex" and self._compiled_regex:
            match = self._compiled_regex.search(msg)
            if match:
                fields = match.groupdict()
            else:
                return ParseResult(
                    status="unparsed",
                    parser_name=self.parser_name,
                    fields={},
                    raw_event=raw_event,
                    reason=f"Log message did not match compiled regex pattern for parser {self.spec.id}"
                )
        elif self.spec.format == "key_value":
            # Extract key=value pairs
            kv_pattern = re.compile(r'([a-zA-Z0-9_.-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|(\S+))')
            matches = kv_pattern.findall(msg)
            for key, val_d, val_s, val_u in matches:
                fields[key.strip()] = val_d or val_s or val_u or ""
        else:
            fields = {"raw": msg}

        return ParseResult(
            status="success",
            parser_name=self.parser_name,
            fields=fields,
            raw_event=raw_event
        )


class ParserCompiler:
    """
    Compiles YAML parser specifications into executable CompiledYamlParser instances.
    """

    @staticmethod
    def compile_from_yaml(yaml_content: str) -> Tuple[ParserSpec, CompiledYamlParser]:
        data = yaml.safe_load(yaml_content)
        parser_info = data.get("parser", {})
        input_info = data.get("input", {})
        
        spec = ParserSpec(
            id=parser_info.get("id", "custom_parser"),
            version=str(parser_info.get("version", "1.0")),
            vendor=parser_info.get("vendor", "Generic"),
            product=parser_info.get("product", "Generic"),
            format=input_info.get("format", "key_value"),
            regex_pattern=data.get("regex_pattern"),
            mapping=data.get("mapping", {}),
            confidence=float(data.get("confidence", 0.95)),
        )

        compiled_parser = CompiledYamlParser(spec)
        return spec, compiled_parser
