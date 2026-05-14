#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timezone


def format_time(unix_time):
    if not isinstance(unix_time, int):
        return ""
    return datetime.fromtimestamp(unix_time, timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def main():
    if len(sys.argv) != 3:
        print("usage: render_report.py <hn-topstories.json> <report.md>", file=sys.stderr)
        return 1

    with open(sys.argv[1], encoding="utf-8") as handle:
        data = json.load(handle)

    lines = [
        "# Hacker News Top Stories",
        "",
        f"- 抓取时间：`{data.get('retrieved_at', '')}`",
        f"- 数据来源：{data.get('source_url', '')}",
        f"- 条目数量：{data.get('total', 0)}",
        "",
        "## Stories",
        "",
    ]

    for item in data.get("items", []):
        lines.append(f"### {item.get('rank')}. {item.get('title')}")
        lines.append("")
        lines.append(f"- Score: {item.get('score')}")
        lines.append(f"- Comments: {item.get('descendants')}")
        lines.append(f"- Author: `{item.get('by')}`")
        story_time = format_time(item.get("time"))
        if story_time:
            lines.append(f"- Posted: {story_time}")
        lines.append(f"- URL: {item.get('url')}")
        lines.append(f"- HN: {item.get('hn_url')}")
        lines.append("")

    with open(sys.argv[2], "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")

    print(f"Rendered report -> {sys.argv[2]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
