#!/usr/bin/env python3
"""Extract local-only book text and render figure pages."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import fitz


def ascii_clean(value: str) -> str:
    value = value.replace("\u00a0", " ")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return value.strip()


def figure_pages(doc: fitz.Document) -> set[int]:
    pages: set[int] = set()
    for page_index, page in enumerate(doc, start=1):
        if re.search(r"\bFigure\s+[A-Z0-9]+(?:\.\d+)?:", page.get_text("text")):
            pages.add(page_index)
    return pages


def write_text_extracts(doc: fitz.Document, out_dir: Path) -> None:
    pages_dir = out_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for page_index, page in enumerate(doc, start=1):
        text = ascii_clean(page.get_text("text"))
        (pages_dir / f"page-{page_index:03d}.txt").write_text(text + "\n", encoding="utf-8")


def render_pages(doc: fitz.Document, pages: set[int], out_dir: Path, dpi: int) -> None:
    render_dir = out_dir / "figure-pages"
    render_dir.mkdir(parents=True, exist_ok=True)
    matrix = fitz.Matrix(dpi / 72, dpi / 72)
    for page_number in sorted(pages):
        pix = doc[page_number - 1].get_pixmap(matrix=matrix, alpha=False)
        pix.save(render_dir / f"page-{page_number:03d}.png")


def write_manifest(doc: fitz.Document, pages: set[int], out_dir: Path, pdf: Path) -> None:
    manifest = {
        "source_pdf": str(pdf),
        "page_count": doc.page_count,
        "figure_pages": sorted(pages),
        "text_dir": "pages",
        "figure_page_dir": "figure-pages",
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--out", default=Path("artifacts/book"), type=Path)
    parser.add_argument("--dpi", default=180, type=int)
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")

    doc = fitz.open(args.pdf)
    args.out.mkdir(parents=True, exist_ok=True)
    pages = figure_pages(doc)
    write_text_extracts(doc, args.out)
    render_pages(doc, pages, args.out, args.dpi)
    write_manifest(doc, pages, args.out, args.pdf)
    print(f"Wrote text for {doc.page_count} pages to {args.out / 'pages'}.")
    print(f"Rendered {len(pages)} figure pages to {args.out / 'figure-pages'}.")


if __name__ == "__main__":
    main()
