#!/usr/bin/env python3
"""Summarize checkbox progress in markdown files."""

from __future__ import annotations

import re
from pathlib import Path


CHECKBOX_RE = re.compile(r"\[( |x|X)\]")


def count_file(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    total = 0
    done = 0
    for match in CHECKBOX_RE.finditer(text):
        total += 1
        if match.group(1).lower() == "x":
            done += 1
    return done, total


def main() -> None:
    paths = sorted(Path(".").glob("**/*.md"))
    paths = [path for path in paths if not any(part in {"artifacts", "downloads", ".git"} for part in path.parts)]
    grand_done = 0
    grand_total = 0
    for path in paths:
        done, total = count_file(path)
        if total == 0:
            continue
        grand_done += done
        grand_total += total
        pct = (done / total * 100) if total else 0
        print(f"{path}: {done}/{total} ({pct:.0f}%)")
    if grand_total:
        print(f"TOTAL: {grand_done}/{grand_total} ({grand_done / grand_total * 100:.0f}%)")
    else:
        print("No markdown checkboxes found.")


if __name__ == "__main__":
    main()
