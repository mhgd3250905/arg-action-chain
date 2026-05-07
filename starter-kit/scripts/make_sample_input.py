from pathlib import Path
import json

items = [
    {
        "index": 0,
        "created_at": "2026-05-07T08:30:00Z",
        "author": "user_001",
        "content": "导出按钮点击后没有反应，页面提示服务器错误。",
        "url": "https://example.invalid/feedback/1",
    },
    {
        "index": 1,
        "created_at": "2026-05-07T09:10:00Z",
        "author": "user_002",
        "content": "希望批量导入时可以显示每一行失败原因。",
        "url": "https://example.invalid/feedback/2",
    },
]

Path("output").mkdir(exist_ok=True)
Path("tmp").mkdir(exist_ok=True)
Path("output/raw-feedback.json").write_text(
    json.dumps({"total": len(items), "items": items}, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("WROTE output/raw-feedback.json")

