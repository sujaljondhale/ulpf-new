# ULPF Intermediate Representation (ULPF-IR v1.0) Specification

## Overview
ULPF-IR is a versioned, vendor-agnostic canonical representation designed specifically for perimeter security network logs.

## JSON Schema Example
```json
{
  "ulpf": {
    "schema_version": "1.0",
    "event_id": "46b7eac0-7a8c-46ee-8799-1b786d24a626"
  },
  "event": {
    "category": "network",
    "type": "connection",
    "action": "allow",
    "time": "2026-09-02T12:00:00Z"
  },
  "source": {
    "ip": "10.10.1.5",
    "port": 51522
  },
  "destination": {
    "ip": "8.8.8.8",
    "port": 443
  },
  "network": {
    "transport": "tcp",
    "protocol": "https"
  },
  "device": {
    "vendor": "CheckPoint",
    "product": "FireWall-1",
    "hostname": "fw-edge-01"
  },
  "rule": {
    "name": "Allow-HTTPS-Outbound"
  },
  "severity": "Low",
  "original": {
    "format": "CEF",
    "message": "CEF:0|CheckPoint|...",
    "sha256": "6310e073c672a97293228556587904746a5b244d4e7cfc1d0563c6c0bf619e19"
  },
  "provenance": {
    "source.ip": {
      "value": "10.10.1.5",
      "original_field": "src",
      "original_value": "10.10.1.5",
      "parser": "cef",
      "confidence": 1.0
    }
  },
  "unmapped": {}
}
```
