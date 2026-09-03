"""
Standard field lookup dictionaries mapping vendor and format specific key names
to canonical ULPF Network Taxonomy fields.
"""

TAXONOMY_FIELD_MAPPINGS = {
    "source.ip": [
        "src", "src_ip", "source_ip", "sourceIp", "sip", "srcip", "src_addr",
        "c-ip", "ClientIP", "source.ip", "src_host", "src_ip_addr"
    ],
    "source.port": [
        "spt", "src_port", "source_port", "sourcePort", "sport", "srcport",
        "c-port", "ClientPort", "source.port"
    ],
    "destination.ip": [
        "dst", "dst_ip", "dest_ip", "destination_ip", "destinationIp", "dip",
        "dstip", "dst_addr", "s-ip", "ServerIP", "destination.ip", "dst_host"
    ],
    "destination.port": [
        "dpt", "dst_port", "dest_port", "destination_port", "destinationPort",
        "dport", "dstport", "s-port", "ServerPort", "destination.port"
    ],
    "network.protocol": [
        "proto", "protocol", "app_proto", "service", "app", "application",
        "network.protocol"
    ],
    "network.transport": [
        "transport", "trans_proto", "network.transport", "ip_proto"
    ],
    "event.action": [
        "action", "act", "outcome", "status", "event.action", "disposition",
        "result", "firewall_action"
    ],
    "event.type": [
        "event_type", "type", "cat", "category", "event.type", "log_type"
    ],
    "event.category": [
        "category", "cat", "event.category", "class"
    ],
    "event.id": [
        "SignatureID", "EventID", "event_id", "id", "event.id", "sig_id"
    ],
    "event.time": [
        "time", "timestamp", "date", "event_time", "event.time", "@timestamp"
    ],
    "device.vendor": [
        "DeviceVendor", "Vendor", "vendor", "dev_vendor", "device.vendor", "make"
    ],
    "device.product": [
        "DeviceProduct", "Product", "product", "dev_product", "device.product", "model"
    ],
    "device.hostname": [
        "hostname", "shost", "dhost", "host", "device.hostname", "syslog_host", "node"
    ],
    "rule.name": [
        "rule", "rule_name", "policy", "policy_name", "rule.name", "filter_name"
    ],
    "rule.id": [
        "rule_id", "policy_id", "rule.id", "filter_id"
    ],
    "user.name": [
        "user", "usr", "username", "suser", "duser", "user_name", "user.name", "account"
    ],
    "severity": [
        "Severity", "severity", "priority", "sev", "log_level", "pri"
    ],
}
