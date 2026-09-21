import asyncio
from main.app.api.routes import get_analytics_summary, EVENT_LIST
print(f"Events: {len(EVENT_LIST)}")
if EVENT_LIST:
    ev = EVENT_LIST[0]
    print(f"Type: {type(ev)}")
    print(f"Action: {getattr(ev, 'action', 'None')}")
summary = get_analytics_summary()
print(summary['top_threat_formats'])
