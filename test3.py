import urllib.request
import json

req = urllib.request.Request('http://localhost:8000/api/v1/events')
with urllib.request.urlopen(req) as response:
    events = json.loads(response.read().decode())['events']

threats_by_format = {}

for ev in events:
    sev = str(ev.get("severity", "informational")).lower()
    action = str(ev.get("action", "allow")).lower()
    has_threat = ev.get("threat") is not None
    
    fmt = ev.get("format")
    if not fmt:
        fmt = "Unknown"
        
    if fmt not in threats_by_format:
        threats_by_format[fmt] = 0
        
    if has_threat or action in ["deny", "block"] or sev in ["high", "critical"]:
        print(f"Match: action={action}, sev={sev}, fmt={fmt}")
        threats_by_format[fmt] += 1

print(threats_by_format)
