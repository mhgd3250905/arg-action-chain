#!/usr/bin/env python3
import json
import sys


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main():
    if len(sys.argv) != 3:
        return fail("usage: validate_report.py <report.md> <hn-topstories.json>")

    try:
        with open(sys.argv[1], encoding="utf-8") as handle:
            report = handle.read()
        with open(sys.argv[2], encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        return fail(str(exc))

    if "# Hacker News Top Stories" not in report:
        return fail("missing title")
    if "抓取时间" not in report:
        return fail("missing retrieved time")
    if "数据来源" not in report:
        return fail("missing source")
    if "## Stories" not in report:
        return fail("missing stories section")

    for item in data.get("items", [])[: min(5, len(data.get("items", [])))]:
        if item.get("title") not in report:
            return fail(f"missing item title: {item.get('title')}")

    print("OK: report")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
