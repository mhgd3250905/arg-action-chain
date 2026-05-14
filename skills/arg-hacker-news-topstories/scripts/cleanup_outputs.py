#!/usr/bin/env python3
from pathlib import Path


OUTPUT_DIR = Path("output")
FILES = [
    OUTPUT_DIR / "hn-topstories-ids.json",
    OUTPUT_DIR / "hn-topstories.json",
    OUTPUT_DIR / "hn-topstories-report.md",
]


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for path in FILES:
        if path.exists():
            path.unlink()
    print("Cleaned Hacker News output files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
