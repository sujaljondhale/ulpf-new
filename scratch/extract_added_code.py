import re

with open("diff_app.txt", "rb") as f:
    diff_text = f.read().decode("utf-16le", errors="ignore")

lines = diff_text.splitlines()

# Extract only added lines for readability
added_code = []
for line in lines:
    if line.startswith("+") and not line.startswith("+++"):
        added_code.append(line[1:])

with open("scratch/added_code.js", "w") as f:
    f.write("\n".join(added_code))
