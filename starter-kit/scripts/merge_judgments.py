import json
import sys
from pathlib import Path

raw_path = Path(sys.argv[1])
judgment_path = Path(sys.argv[2])
out_path = Path(sys.argv[3])

raw = json.loads(raw_path.read_text(encoding="utf-8"))
judgments = json.loads(judgment_path.read_text(encoding="utf-8"))
by_index = {item["index"]: item for item in judgments}

items = []
for item in raw.get("items", []):
    judgment = by_index.get(item["index"])
    if not judgment:
        continue
    if judgment["relevant"] == "no":
        continue
    items.append(
        {
            **item,
            "relevant": judgment["relevant"],
            "category": judgment["category"],
            "severity": judgment["severity"],
            "summary": judgment["summary"],
        }
    )

out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(
    json.dumps({"total": len(items), "items": items}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(f"WROTE {out_path}")

