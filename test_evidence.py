original = {"format": "JSON", "message": "hello world", "sha256": "abcdef"}
content = original.get("raw_text", original.get("message", original.get("raw", "RAW CONTENT UNAVAILABLE")))
print("Content:", content)
