from typing import Dict, Any, Tuple, Optional
from app.models.taxonomy import (
    NetworkTaxonomy,
    EventDetails,
    SourceDetails,
    DestinationDetails,
    NetworkDetails,
    DeviceDetails,
    RuleDetails,
    UserDetails,
)
from app.models.ir import FieldProvenance


class SemanticNormalizer:
    """
    Semantic Normalizer for ULPF.
    Maps extracted vendor/format fields to the Canonical Network Security Taxonomy
    and maintains field-level provenance.
    """

    FIELD_MAPPINGS: Dict[str, list] = {
        "source.ip": ["src", "src_ip", "source_ip", "sourceIp", "sip", "srcip", "src_addr", "source.ip"],
        "source.port": ["spt", "src_port", "source_port", "sourcePort", "sport", "srcport", "source.port"],
        "destination.ip": ["dst", "dst_ip", "dest_ip", "destination_ip", "destinationIp", "dip", "dstip", "dst_addr", "destination.ip"],
        "destination.port": ["dpt", "dst_port", "dest_port", "destination_port", "destinationPort", "dport", "dstport", "destination.port"],
        "network.protocol": ["proto", "protocol", "app_proto", "service", "network.protocol"],
        "network.transport": ["transport", "trans_proto", "network.transport"],
        "event.action": ["action", "act", "outcome", "status", "event.action"],
        "event.type": ["event_type", "type", "cat", "event.type"],
        "event.category": ["category", "cat", "event.category"],
        "event.id": ["SignatureID", "EventID", "event_id", "id", "event.id"],
        "event.time": ["time", "timestamp", "date", "event_time", "event.time"],
        "device.vendor": ["DeviceVendor", "Vendor", "vendor", "dev_vendor", "device.vendor"],
        "device.product": ["DeviceProduct", "Product", "product", "dev_product", "device.product"],
        "device.hostname": ["hostname", "shost", "dhost", "host", "device.hostname"],
        "rule.name": ["rule", "rule_name", "policy", "policy_name", "rule.name"],
        "rule.id": ["rule_id", "policy_id", "rule.id"],
        "user.name": ["user", "usr", "username", "suser", "duser", "user_name", "user.name"],
        "severity": ["Severity", "severity", "priority", "sev"],
    }

    def _find_field(self, extracted_fields: Dict[str, Any], candidates: list) -> Optional[Tuple[str, Any]]:
        """Look up candidate field names in extracted fields (case-insensitive search fallback)."""
        for cand in candidates:
            if cand in extracted_fields and extracted_fields[cand] is not None:
                return cand, extracted_fields[cand]

        # Case-insensitive fallback
        lowered_fields = {k.lower(): (k, v) for k, v in extracted_fields.items() if v is not None}
        for cand in candidates:
            if cand.lower() in lowered_fields:
                orig_key, val = lowered_fields[cand.lower()]
                return orig_key, val

        return None

    def normalize(self, extracted_fields: Dict[str, Any], parser_name: str) -> Tuple[NetworkTaxonomy, Dict[str, FieldProvenance]]:
        taxonomy = NetworkTaxonomy()
        provenance: Dict[str, FieldProvenance] = {}

        # 1. Source IP
        res = self._find_field(extracted_fields, self.FIELD_MAPPINGS["source.ip"])
        if res:
            orig_k, orig_v = res
            taxonomy.source.ip = str(orig_v)
            provenance["source.ip"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 2. Source Port
        res = self._find_field(extracted_fields, self.FIELD_MAPPINGS["source.port"])
        if res:
            orig_k, orig_v = res
            try:
                taxonomy.source.port = int(orig_v)
                provenance["source.port"] = FieldProvenance(
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    confidence=1.0
                )
            except (ValueError, TypeError):
                pass

        # 3. Destination IP
        res = self._find_field(extracted_fields, self.FIELD_MAPPINGS["destination.ip"])
        if res:
            orig_k, orig_v = res
            taxonomy.destination.ip = str(orig_v)
            provenance["destination.ip"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 4. Destination Port
        res = self._find_field(extracted_fields, self.FIELD_MAPPINGS["destination.port"])
        if res:
            orig_k, orig_v = res
            try:
                taxonomy.destination.port = int(orig_v)
                provenance["destination.port"] = FieldProvenance(
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    confidence=1.0
                )
            except (ValueError, TypeError):
                pass

        # 5. Network Protocol & Transport
        res = self._find_field(extracted_fields, self.FIELD_MAPPINGS["network.protocol"])
        if res:
            orig_k, orig_v = res
            val_str = str(orig_v).lower()
            if val_str in ["tcp", "udp", "icmp"]:
                taxonomy.network.transport = val_str
                provenance["network.transport"] = FieldProvenance(
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    confidence=1.0
                )
            else:
                taxonomy.network.protocol = val_str
                provenance["network.protocol"] = FieldProvenance(
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    confidence=1.0
                )

        res_trans = self._find_field(extracted_fields, self.FIELD_MAPPINGS["network.transport"])
        if res_trans:
            orig_k, orig_v = res_trans
            taxonomy.network.transport = str(orig_v).lower()
            provenance["network.transport"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 6. Event Details
        res_act = self._find_field(extracted_fields, self.FIELD_MAPPINGS["event.action"])
        if res_act:
            orig_k, orig_v = res_act
            taxonomy.event.action = str(orig_v).lower()
            provenance["event.action"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_type = self._find_field(extracted_fields, self.FIELD_MAPPINGS["event.type"])
        if res_type:
            orig_k, orig_v = res_type
            taxonomy.event.type = str(orig_v)
            provenance["event.type"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_cat = self._find_field(extracted_fields, self.FIELD_MAPPINGS["event.category"])
        if res_cat:
            orig_k, orig_v = res_cat
            taxonomy.event.category = str(orig_v)
            provenance["event.category"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_id = self._find_field(extracted_fields, self.FIELD_MAPPINGS["event.id"])
        if res_id:
            orig_k, orig_v = res_id
            taxonomy.event.id = str(orig_v)
            provenance["event.id"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_time = self._find_field(extracted_fields, self.FIELD_MAPPINGS["event.time"])
        if res_time:
            orig_k, orig_v = res_time
            taxonomy.event.time = str(orig_v)
            provenance["event.time"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 7. Device Details
        res_dev_v = self._find_field(extracted_fields, self.FIELD_MAPPINGS["device.vendor"])
        if res_dev_v:
            orig_k, orig_v = res_dev_v
            taxonomy.device.vendor = str(orig_v)
            provenance["device.vendor"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_dev_p = self._find_field(extracted_fields, self.FIELD_MAPPINGS["device.product"])
        if res_dev_p:
            orig_k, orig_v = res_dev_p
            taxonomy.device.product = str(orig_v)
            provenance["device.product"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_dev_h = self._find_field(extracted_fields, self.FIELD_MAPPINGS["device.hostname"])
        if res_dev_h:
            orig_k, orig_v = res_dev_h
            taxonomy.device.hostname = str(orig_v)
            provenance["device.hostname"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 8. Rule Details
        res_rule_n = self._find_field(extracted_fields, self.FIELD_MAPPINGS["rule.name"])
        if res_rule_n:
            orig_k, orig_v = res_rule_n
            taxonomy.rule.name = str(orig_v)
            provenance["rule.name"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        res_rule_i = self._find_field(extracted_fields, self.FIELD_MAPPINGS["rule.id"])
        if res_rule_i:
            orig_k, orig_v = res_rule_i
            taxonomy.rule.id = str(orig_v)
            provenance["rule.id"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 9. User Details
        res_usr = self._find_field(extracted_fields, self.FIELD_MAPPINGS["user.name"])
        if res_usr:
            orig_k, orig_v = res_usr
            taxonomy.user.name = str(orig_v)
            provenance["user.name"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        # 10. Severity
        res_sev = self._find_field(extracted_fields, self.FIELD_MAPPINGS["severity"])
        if res_sev:
            orig_k, orig_v = res_sev
            taxonomy.severity = str(orig_v)
            provenance["severity"] = FieldProvenance(
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                confidence=1.0
            )

        return taxonomy, provenance
