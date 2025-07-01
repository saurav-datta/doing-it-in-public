import json
import pandas as pd
import tempfile
import os
from os import system

# Sample data
data = [
    {"id": 1, "name": "Alice", "score": 85},
    {"id": 2, "name": "Bob", "score": 90},
    {"id": 3, "name": "Charlie", "score": 78}
]

# Write to temporary .jsonl file
with tempfile.NamedTemporaryFile(mode="w+", suffix=".jsonl", delete=False) as tmp_file:
    for record in data:
        tmp_file.write(json.dumps(record) + "\n")
    tmp_file_path = tmp_file.name

print("== Read temp file ==")
with open(tmp_file_path, 'r') as fh:
    for line in fh.readlines():
        print(line.strip())

# Read into pandas
df = pd.read_json(tmp_file_path, lines=True)
print("== print df ==")
print(df)

# Clean up
os.remove(tmp_file_path)
print("done")
