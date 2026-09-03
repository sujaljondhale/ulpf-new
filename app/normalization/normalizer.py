from typing import Dict, Any, Tuple, Optional
from app.normalization.taxonomy import NetworkTaxonomy
from app.normalization.mappings import TAXONOMY_FIELD_MAPPINGS
from app.models.provenance import ProvenanceRecord


class SemanticNormalizer:
    """
    Normalizes vendor/format-specific extracted fields into the canonical NetworkTaxonomy
    and tracks field-level provenance. Preserves unmapped fields into a dedicated dictionary.
    """

    def _find_field(self, extracted: Dict[str, Any], candidates: list) -> Optional[Tuple[str, Any]]:
        for cand in candidates:
            if cand in extracted and extracted[cand] is not None:
                return cand, extracted[cand]

        # Case-insensitive search fallback
        lowered = {k.lower(): (k, v) for k, v in extracted.items() if v is not None}
        for cand in candidates:
            if cand.lower() in lowered:
                orig_k, orig_v = lowered[cand.lower()]
                return orig_k, orig_v

        return None

    def normalize(
        self, extracted_fields: Dict[str, Any], parser_name: str, confidence: float = 1.0
    ) -> Tuple[NetworkTaxonomy, Dict[str, ProvenanceRecord], Dict[str, Any]]:
        taxonomy = NetworkTaxonomy()
        provenance: Dict[str, ProvenanceRecord] = {}
        mapped_keys = set()

        # 1. Source IP
        res = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["source.ip"])
        if res:
            orig_k, orig_v = res
            taxonomy.source.ip = str(orig_v)
            provenance["source.ip"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="ip_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 2. Source Port
        res = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["source.port"])
        if res:
            orig_k, orig_v = res
            try:
                val_int = int(orig_v)
                taxonomy.source.port = val_int
                provenance["source.port"] = ProvenanceRecord(
                    value=val_int,
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    rule="port_mapping",
                    confidence=confidence,
                )
            except (ValueError, TypeError):
                pass
            mapped_keys.add(orig_k)

        # 3. Destination IP
        res = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["destination.ip"])
        if res:
            orig_k, orig_v = res
            taxonomy.destination.ip = str(orig_v)
            provenance["destination.ip"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="ip_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 4. Destination Port
        res = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["destination.port"])
        if res:
            orig_k, orig_v = res
            try:
                val_int = int(orig_v)
                taxonomy.destination.port = val_int
                provenance["destination.port"] = ProvenanceRecord(
                    value=val_int,
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    rule="port_mapping",
                    confidence=confidence,
                )
            except (ValueError, TypeError):
                pass
            mapped_keys.add(orig_k)

        # 5. Network Protocol & Transport
        res = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["network.protocol"])
        if res:
            orig_k, orig_v = res
            val_str = str(orig_v).lower()
            if val_str in ["tcp", "udp", "icmp"]:
                taxonomy.network.transport = val_str
                provenance["network.transport"] = ProvenanceRecord(
                    value=val_str,
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    rule="transport_mapping",
                    confidence=confidence,
                )
            else:
                taxonomy.network.protocol = val_str
                provenance["network.protocol"] = ProvenanceRecord(
                    value=val_str,
                    original_field=orig_k,
                    original_value=orig_v,
                    parser=parser_name,
                    rule="proto_mapping",
                    confidence=confidence,
                )
            mapped_keys.add(orig_k)

        res_trans = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["network.transport"])
        if res_trans:
            orig_k, orig_v = res_trans
            taxonomy.network.transport = str(orig_v).lower()
            provenance["network.transport"] = ProvenanceRecord(
                value=str(orig_v).lower(),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="transport_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 6. Event Action
        res_act = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["event.action"])
        if res_act:
            orig_k, orig_v = res_act
            taxonomy.event.action = str(orig_v).lower()
            provenance["event.action"] = ProvenanceRecord(
                value=str(orig_v).lower(),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="action_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 7. Device Vendor / Product / Hostname
        res_v = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["device.vendor"])
        if res_v:
            orig_k, orig_v = res_v
            taxonomy.device.vendor = str(orig_v)
            provenance["device.vendor"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="vendor_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        res_p = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["device.product"])
        if res_p:
            orig_k, orig_v = res_p
            taxonomy.device.product = str(orig_v)
            provenance["device.product"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="product_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        res_h = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["device.hostname"])
        if res_h:
            orig_k, orig_v = res_h
            taxonomy.device.hostname = str(orig_v)
            provenance["device.hostname"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="hostname_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 8. Rule Name & ID
        res_rn = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["rule.name"])
        if res_rn:
            orig_k, orig_v = res_rn
            taxonomy.rule.name = str(orig_v)
            provenance["rule.name"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="rule_name_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        res_ri = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["rule.id"])
        if res_ri:
            orig_k, orig_v = res_ri
            taxonomy.rule.id = str(orig_v)
            provenance["rule.id"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="rule_id_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 9. User Name
        res_u = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["user.name"])
        if res_u:
            orig_k, orig_v = res_u
            taxonomy.user.name = str(orig_v)
            provenance["user.name"] = ProvenanceRecord(
                value=str(orig_v),
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="user_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # 10. Severity
        res_s = self._find_field(extracted_fields, TAXONOMY_FIELD_MAPPINGS["severity"])
        if res_s:
            orig_k, orig_v = res_s
            taxonomy.severity = orig_v
            provenance["severity"] = ProvenanceRecord(
                value=orig_v,
                original_field=orig_k,
                original_value=orig_v,
                parser=parser_name,
                rule="severity_mapping",
                confidence=confidence,
            )
            mapped_keys.add(orig_k)

        # Preserve any unmapped extracted fields
        unmapped = {k: v for k, v in extracted_fields.items() if k not in mapped_keys and not k.startswith("_")}

        return taxonomy, provenance, unmapped
