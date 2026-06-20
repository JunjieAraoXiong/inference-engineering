#!/usr/bin/env python3
"""Download open recommended readings into an ignored local folder."""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


USER_AGENT = "inference-engineering-learning-repo/1.0"


def slugify(value: str, max_length: int = 90) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value[:max_length].strip("-") or "reading"


def arxiv_pdf_url(url: str) -> str | None:
    match = re.search(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5})(v[0-9]+)?", url)
    if not match:
        return None
    paper_id = match.group(1) + (match.group(2) or "")
    return f"https://arxiv.org/pdf/{paper_id}.pdf"


def direct_pdf_url(url: str) -> str | None:
    return url if url.lower().split("?", 1)[0].endswith(".pdf") else None


def download(url: str, path: Path, timeout: int) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        data = response.read()
    if path.suffix == ".pdf" and not data.startswith(b"%PDF"):
        raise RuntimeError(f"Expected a PDF, got {content_type or 'unknown content type'}")
    path.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=Path("readings/recommended-readings.json"), type=Path)
    parser.add_argument("--out", default=Path("downloads/readings"), type=Path)
    parser.add_argument("--include-web", action="store_true", help="Also save HTML snapshots for non-PDF web pages.")
    parser.add_argument("--sleep", default=1.0, type=float)
    parser.add_argument("--timeout", default=45, type=int)
    args = parser.parse_args()

    rows = json.loads(args.manifest.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    failed: list[str] = []

    for row in rows:
        url = row["url"]
        target_url = arxiv_pdf_url(url) or direct_pdf_url(url)
        suffix = ".pdf"
        if target_url is None and args.include_web:
            target_url = url
            suffix = ".html"
        if target_url is None:
            row["download_status"] = "skipped_non_direct"
            row.pop("download_url", None)
            row.pop("local_path", None)
            row.pop("download_error", None)
            skipped += 1
            continue

        category = slugify(row["category"])
        title = slugify(row["title"])
        parsed = urlparse(target_url)
        name_hint = Path(parsed.path).name.replace(".pdf", "")
        filename = f"{title or name_hint}{suffix}"
        path = args.out / category / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        row["download_url"] = target_url
        row["local_path"] = str(path)

        if path.exists() and path.stat().st_size > 0:
            row["download_status"] = "downloaded"
            row.pop("download_error", None)
            skipped += 1
            continue

        try:
            print(f"Downloading {target_url}")
            download(target_url, path, args.timeout)
            row["download_status"] = "downloaded"
            row.pop("download_error", None)
            downloaded += 1
            time.sleep(args.sleep)
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            error = str(exc)
            row["download_status"] = "failed"
            row["download_error"] = error
            failed.append(f"{target_url} :: {error}")
            if path.exists() and path.stat().st_size == 0:
                path.unlink()

    args.manifest.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Downloaded: {downloaded}")
    print(f"Skipped: {skipped}")
    print(f"Failed: {len(failed)}")
    if failed:
        failure_path = args.out / "download-failures.txt"
        failure_path.write_text("\n".join(failed) + "\n", encoding="utf-8")
        print(f"Wrote failures to {failure_path}")


if __name__ == "__main__":
    main()
