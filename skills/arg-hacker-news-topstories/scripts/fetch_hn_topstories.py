#!/usr/bin/env python3
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


TOPSTORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"


def load_json(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "arg-hacker-news-topstories/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return json.loads(response.read().decode(charset))


def normalize_item(raw, rank):
    url = raw.get("url") or f"https://news.ycombinator.com/item?id={raw.get('id')}"
    return {
        "rank": rank,
        "id": raw.get("id"),
        "title": raw.get("title", ""),
        "url": url,
        "hn_url": f"https://news.ycombinator.com/item?id={raw.get('id')}",
        "score": raw.get("score", 0),
        "by": raw.get("by", ""),
        "time": raw.get("time"),
        "descendants": raw.get("descendants", 0),
        "type": raw.get("type", ""),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--ids-output", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--sleep", type=float, default=0.05)
    args = parser.parse_args()

    try:
        story_ids = load_json(TOPSTORIES_URL)
        if not isinstance(story_ids, list):
            raise ValueError("topstories endpoint did not return a list")

        items = []
        for rank, item_id in enumerate(story_ids[: args.limit], start=1):
            raw = load_json(ITEM_URL.format(item_id=item_id))
            if isinstance(raw, dict) and raw.get("type") == "story" and raw.get("title"):
                items.append(normalize_item(raw, rank))
            time.sleep(args.sleep)
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        print(f"FETCH_FAILED: {exc}", file=sys.stderr)
        return 1

    normalized = {
        "source": "hacker-news-topstories",
        "source_url": TOPSTORIES_URL,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "total": len(items),
        "items": items,
    }

    with open(args.ids_output, "w", encoding="utf-8") as handle:
        json.dump(story_ids[: args.limit], handle, ensure_ascii=False, indent=2)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(normalized, handle, ensure_ascii=False, indent=2)

    print(f"Fetched {normalized['total']} Hacker News top stories")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
