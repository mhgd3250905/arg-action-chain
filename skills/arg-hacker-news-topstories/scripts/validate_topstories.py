#!/usr/bin/env python3
import json
import re
import sys


def fail(message):
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main():
    if len(sys.argv) != 2:
        return fail("usage: validate_topstories.py <hn-topstories.json>")

    try:
        with open(sys.argv[1], encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception as exc:
        return fail(f"invalid json: {exc}")

    if data.get("source") != "hacker-news-topstories":
        return fail("invalid source")
    if data.get("source_url") != "https://hacker-news.firebaseio.com/v0/topstories.json":
        return fail("invalid source_url")
    if not isinstance(data.get("items"), list):
        return fail("items must be a list")
    if data.get("total") != len(data["items"]):
        return fail("total mismatch")
    if len(data["items"]) < 1:
        return fail("no top stories")

    ranks = set()
    ids = set()
    for item in data["items"]:
        rank = item.get("rank")
        item_id = item.get("id")
        if not isinstance(rank, int) or rank < 1:
            return fail("invalid rank")
        if rank in ranks:
            return fail("duplicate rank")
        ranks.add(rank)
        if not isinstance(item_id, int):
            return fail(f"invalid id at rank {rank}")
        if item_id in ids:
            return fail(f"duplicate id at rank {rank}")
        ids.add(item_id)
        if not str(item.get("title", "")).strip():
            return fail(f"empty title at rank {rank}")
        if not re.match(r"^https?://", str(item.get("url", ""))):
            return fail(f"invalid url at rank {rank}")
        if not isinstance(item.get("score"), int):
            return fail(f"invalid score at rank {rank}")
        if not isinstance(item.get("descendants"), int):
            return fail(f"invalid descendants at rank {rank}")

    print(f"OK: {len(data['items'])} items")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
