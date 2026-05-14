#!/usr/bin/env python3
from pathlib import Path


OUTPUT_DIR = Path("output")
FILES = [
    OUTPUT_DIR / "hn-topstories-ids.json",
    OUTPUT_DIR / "hn-topstories.json",
    OUTPUT_DIR / "hn-topstories-report.md",
]


def main():
    if not OUTPUT_DIR.is_dir():
        print("FAIL: output directory missing")
        return 1
    existing = [str(path) for path in FILES if path.exists()]
    if existing:
        print(f"FAIL: stale output files exist: {existing}")
        return 1
    print("OK: cleanup")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
