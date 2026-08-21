#!/usr/bin/env python3
"""Build competitor JSON array from JSONL file."""
import json, sys

items = []
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                pass

print(json.dumps(items))
