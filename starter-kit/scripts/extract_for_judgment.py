import json
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

data = json.loads(src.read_text(encoding="utf-8"))
items = [
    {
        "index": item["index"],
        "created_at": item.get("created_at", ""),
        "author": item.get("author", ""),
        "content": item.get("content", ""),
    }
    for item in data.get("items", [])
]

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"WROTE {dst}")

