from app.api.routes import get_raw_evidence, EVENT_LIST
ev = EVENT_LIST[0]
eid = ev["event_id"]
print(f"Testing event ID: {eid}")
print(get_raw_evidence(eid))
