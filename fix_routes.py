import sys

with open("/Users/sujal/Downloads/ulpf-s/ulpf/main/app/api/routes.py", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    new_lines.append(line)
    if 'passed = sum(1 for s in steps if s["status"] == "PASS")' in line:
        break

new_code = """        return {
            "overall_status": "PASSED" if passed == len(steps) else "WARNING",
            "passed": passed,
            "total": len(steps),
            "steps": steps,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    return await run_in_threadpool(run_sync_suite)

@router.get("/api/v1/analytics/summary")
def get_analytics_summary():
    \"\"\"Return aggregated analytics data for the Analytics Studio dashboard.\"\"\"
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "informational": 0}
    source_counts = {}
    format_counts = {}
    threats_by_format = {}
    
    # Analyze the last 1000 events in memory
    recent_events = EVENT_LIST[:1000]
    
    for ev in recent_events:
        if isinstance(ev, dict):
            # Severity
            sev = str(ev.get("severity", "informational")).lower()
            
            # Action and Threat
            action = str(ev.get("action", "allow")).lower()
            has_threat = ev.get("threat") is not None
            
            # Source IPs
            src_val = ev.get("source")
            if isinstance(src_val, dict):
                src = src_val.get("ip", "Unknown")
            elif isinstance(src_val, str):
                src = src_val
            else:
                src = ev.get("source_device", "Unknown")
            
            if not src:
                src = "Unknown"
            
            # Formats
            fmt = ev.get("format")
            if not fmt:
                orig_dict = ev.get("original", {})
                if isinstance(orig_dict, dict):
                    fmt = orig_dict.get("format", "Unknown")
                else:
                    fmt = "Unknown"
                
        else:
            # Severity
            sev = str(getattr(ev, "severity", "informational")).lower()
            
            # Action and Threat
            action = str(getattr(ev, "action", "allow")).lower()
            has_threat = getattr(ev, "threat", None) is not None
            
            # Source IPs
            src_val = getattr(ev, "source", None)
            if hasattr(src_val, "ip"):
                src = getattr(src_val, "ip", "Unknown")
            elif isinstance(src_val, str):
                src = src_val
            else:
                src = getattr(ev, "source_device", "Unknown")
            if not src:
                src = "Unknown"
            
            # Formats
            fmt = getattr(ev, "format", None)
            if not fmt:
                orig_obj = getattr(ev, "original", None)
                fmt = getattr(orig_obj, "format", "Unknown") if orig_obj else "Unknown"

        # Update counts
        if sev in severity_counts:
            severity_counts[sev] += 1
        else:
            severity_counts["informational"] += 1
            
        if not src:
            src = "Unknown"
        source_counts[src] = source_counts.get(src, 0) + 1
        
        if not fmt:
            fmt = "Unknown"
        format_counts[fmt] = format_counts.get(fmt, 0) + 1
        
        if fmt not in threats_by_format:
            threats_by_format[fmt] = 0
        
        # Threat logs by format (matches frontend filtering logic)
        if has_threat or action in ["deny", "block"] or sev in ["high", "critical"]:
            threats_by_format[fmt] += 1
            
    top_sources = sorted([{"ip": k, "count": v} for k, v in source_counts.items()], key=lambda x: x["count"], reverse=True)[:5]
    top_formats = sorted([{"format": k, "count": v} for k, v in format_counts.items()], key=lambda x: x["count"], reverse=True)[:5]
    top_threat_formats = sorted(
        [{"format": k, "count": v} for k, v in threats_by_format.items()], 
        key=lambda x: (x["count"], format_counts.get(x["format"], 0)), 
        reverse=True
    )[:5]
    
    # Extract real EPS from the global throughput monitor
    base_eps = 0
    try:
        base_eps = float(global_throughput_monitor.get_stats().get("avg_eps_10s", 0))
    except:
        pass
        
    return {
        "severity_distribution": severity_counts,
        "top_sources": top_sources,
        "top_formats": top_formats,
        "top_threat_formats": top_threat_formats,
        "live_eps": base_eps,
        "processing_rate": f"{base_eps} logs/sec",
        "total_analyzed": len(recent_events)
    }

@router.get("/api/v1/analytics/minio-stats")
def get_minio_stats():
    \"\"\"Return health and storage insights for the MinIO raw evidence bucket.\"\"\"
    return persistence_manager.minio.check_health()

@router.get("/api/v1/analytics/evidence/{event_id}")
def get_raw_evidence(event_id: str):
    \"\"\"Retrieve raw byte-for-byte evidence and SHA-256 hash from MinIO.\"\"\"
    ev = EVENT_STORE.get(event_id)
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found in memory")
    
    if isinstance(ev, dict):
        storage_uri = ev.get("storage_uri", "")
        original = ev.get("original", {})
    else:
        storage_uri = getattr(ev, "storage_uri", "")
        original = getattr(ev, "original", {})
        
    content, sha256 = persistence_manager.minio.get_raw_log(storage_uri, event_id=event_id)
    
    if not content:
        if isinstance(original, dict):
            content = original.get("raw_text", "RAW CONTENT UNAVAILABLE")
            sha256 = original.get("sha256", "HASH UNAVAILABLE")
        elif hasattr(original, "raw_text"):
            content = getattr(original, "raw_text", "RAW CONTENT UNAVAILABLE")
            sha256 = getattr(original, "sha256", "HASH UNAVAILABLE")
        else:
            content = "RAW CONTENT UNAVAILABLE"
            sha256 = "HASH UNAVAILABLE"
            
    return {
        "event_id": event_id,
        "raw_content": content,
        "sha256_hash": sha256,
        "tamper_verified": True if content and "UNAVAILABLE" not in sha256 else False,
        "parsed_event": ev if isinstance(ev, dict) else (getattr(ev, "model_dump", lambda: vars(ev))())
    }

@router.post("/api/v1/ai/reanalyze-threat/{event_id}")
def ai_reanalyze_threat(event_id: str):
    \"\"\"
    Verify if a flagged threat is a true positive or a benign false positive.
    Downgrades the threat if verified as benign.
    \"\"\"
    ev = EVENT_STORE.get(event_id)
    if not ev:
        # Try database
        ev = persistence_manager.db.get_event(event_id)
        if not ev:
            raise HTTPException(status_code=404, detail="Event not found.")
            
    threat = ev.get("threat")
    if not threat:
        return {"status": "success", "is_threat": False, "reasoning": "Log does not have a threat tag."}
        
    threat_type = threat.get("threat_type", "Unknown Threat")
    raw_msg = ev.get("original", {}).get("raw") or ev.get("raw_message") or str(ev)
    
    result = ai_engine.reanalyze_threat(raw_message=raw_msg, parsed_threat=threat_type)
    
    if not result.get("is_threat", True):
        # Downgrade in memory
        ev.pop("threat", None)
        if "ulpf" in ev and "threat" in ev["ulpf"]:
            ev["ulpf"].pop("threat", None)
        ev["severity"] = "info"
        if ev.get("action") in ("deny", "block"):
            ev["action"] = "allow"
        
        # Downgrade in database
        persistence_manager.db.downgrade_event(event_id)
        
    return {"status": "success", "result": result, "event_id": event_id}
"""

with open("/Users/sujal/Downloads/ulpf-s/ulpf/main/app/api/routes.py", "w") as f:
    f.writelines(new_lines)
    f.write(new_code)
