threats_by_format = {"Cisco ASA (Syslog)": 0}
format_counts = {"Cisco ASA (Syslog)": 1000}
top_threat_formats = sorted(
    [{"format": k, "count": v} for k, v in threats_by_format.items()], 
    key=lambda x: (x["count"], format_counts.get(x["format"], 0)), 
    reverse=True
)[:5]
print(top_threat_formats)
