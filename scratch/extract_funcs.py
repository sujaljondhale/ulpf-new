import re

with open("diff_app.txt", "rb") as f:
    diff_text = f.read().decode("utf-16le", errors="ignore")

added_funcs = set()
for line in diff_text.splitlines():
    if line.startswith("+") and not line.startswith("+++"):
        match = re.search(r'function\s+([a-zA-Z0-9_]+)\s*\(', line)
        if match:
            added_funcs.add(match.group(1))

with open("scratch/added_funcs.txt", "w") as f:
    f.write("\n".join(sorted(added_funcs)))
