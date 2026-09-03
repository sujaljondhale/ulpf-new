import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from app.config import settings
from app.parsers.compiler import ParserSpec, ParserCompiler


class AiAnalysisProposal(BaseModel):
    format: str
    vendor: str = "Unknown"
    product: str = "Unknown"
    detected_fields: List[str]
    suggested_mappings: Dict[str, str]
    confidence: float
    regex_pattern: Optional[str] = None
    yaml_spec: str


class AiOnboardingEngine:
    """
    AI-Assisted Log Onboarding Engine.
    Leverages local quantized SLM (e.g. Qwen 3B/4B via Ollama) to analyze unparsed sample logs,
    propose taxonomy mappings, and generate parser specifications without cloud dependencies.
    """

    def __init__(self, ollama_url: str = settings.ollama_host, model: str = settings.ai_model_name):
        self.ollama_url = ollama_url
        self.model = model

    def analyze_samples(self, sample_logs: List[str]) -> AiAnalysisProposal:
        """
        Analyze 10-100 unparsed sample logs and propose a structural parser spec.
        Uses local Ollama if available; falls back to deterministic heuristic pattern analysis.
        """
        if not sample_logs:
            raise ValueError("At least 1 sample log required for AI analysis.")

        # Try local Ollama inference
        try:
            return self._call_ollama(sample_logs)
        except Exception:
            # Fallback heuristic analysis engine
            return self._heuristic_analysis(sample_logs)

    def _call_ollama(self, sample_logs: List[str]) -> AiAnalysisProposal:
        prompt = f"""You are a cybersecurity log engineer. Analyze these sample network security logs:
{json.dumps(sample_logs[:5], indent=2)}

Extract the structure and output ONLY a JSON object with this exact key structure:
{{
  "format": "key_value",
  "vendor": "CheckPoint",
  "product": "Firewall",
  "detected_fields": ["src", "dst", "spt", "dpt", "action"],
  "suggested_mappings": {{
    "src": "source.ip",
    "dst": "destination.ip",
    "spt": "source.port",
    "dpt": "destination.port",
    "action": "event.action"
  }},
  "confidence": 0.95
}}
"""
        req_data = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.ollama_url}/api/generate",
            data=req_data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            response_text = data.get("response", "{}")
            parsed_json = json.loads(response_text)

            format_val = parsed_json.get("format", "key_value")
            vendor = parsed_json.get("vendor", "CustomVendor")
            product = parsed_json.get("product", "CustomDevice")
            mappings = parsed_json.get("suggested_mappings", {})
            conf = float(parsed_json.get("confidence", 0.90))

            yaml_str = self._build_yaml_str(
                parser_id=f"{vendor.lower()}_{product.lower()}_v1",
                vendor=vendor,
                product=product,
                fmt=format_val,
                mappings=mappings,
                conf=conf,
            )

            return AiAnalysisProposal(
                format=format_val,
                vendor=vendor,
                product=product,
                detected_fields=list(mappings.keys()),
                suggested_mappings=mappings,
                confidence=conf,
                yaml_spec=yaml_str,
            )

    def _heuristic_analysis(self, sample_logs: List[str]) -> AiAnalysisProposal:
        """Deterministic pattern inference fallback when local LLM server is not running."""
        sample = sample_logs[0]
        detected_fields = []
        mappings = {}
        fmt = "key_value"

        # Heuristic detection of key=value pairs
        kv_matches = re.findall(r'([a-zA-Z0-9_.-]+)=', sample)
        if kv_matches:
            detected_fields = list(set(kv_matches))
            for f in detected_fields:
                fl = f.lower()
                if fl in ["src", "src_ip", "source_ip", "sip"]:
                    mappings[f] = "source.ip"
                elif fl in ["dst", "dst_ip", "dest_ip", "dip"]:
                    mappings[f] = "destination.ip"
                elif fl in ["spt", "src_port", "sport"]:
                    mappings[f] = "source.port"
                elif fl in ["dpt", "dst_port", "dport"]:
                    mappings[f] = "destination.port"
                elif fl in ["act", "action", "status"]:
                    mappings[f] = "event.action"
                elif fl in ["proto", "protocol"]:
                    mappings[f] = "network.transport"

        parser_id = "ai_onboarded_device_v1"
        yaml_str = self._build_yaml_str(
            parser_id=parser_id,
            vendor="InferredVendor",
            product="InferredDevice",
            fmt=fmt,
            mappings=mappings,
            conf=0.92,
        )

        return AiAnalysisProposal(
            format=fmt,
            vendor="InferredVendor",
            product="InferredDevice",
            detected_fields=detected_fields,
            suggested_mappings=mappings,
            confidence=0.92,
            yaml_spec=yaml_str,
        )

    def _build_yaml_str(
        self, parser_id: str, vendor: str, product: str, fmt: str, mappings: Dict[str, str], conf: float
    ) -> str:
        data = {
            "parser": {
                "id": parser_id,
                "version": "1.0",
                "vendor": vendor,
                "product": product,
            },
            "input": {
                "format": fmt,
            },
            "confidence": conf,
            "mapping": mappings,
        }
        import yaml
        return yaml.dump(data, sort_keys=False)
