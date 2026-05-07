import json
import sys
from collections import Counter
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])

data = json.loads(src.read_text(encoding="utf-8"))
items = data.get("items", [])
categories = Counter(item["category"] for item in items)

lines = [
    "# Feedback Report",
    "",
    f"Total: {len(items)}",
    "",
    "## Category Breakdown",
    "",
]

for category, count in sorted(categories.items()):
    lines.append(f"- {category}: {count}")

lines.extend(["", "## Items", ""])

for item in items:
    lines.append(
        f"- [{item['severity']}] {item['category']}: {item['summary']} ({item.get('url','')})"
    )

dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"WROTE {dst}")

