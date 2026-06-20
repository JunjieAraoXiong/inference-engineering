#!/usr/bin/env python3
"""Create the learning repo structure from the Inference Engineering PDF."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import fitz


CHAPTER_READING_HINTS = {
    "00-inference": ["Architecture", "GPU Infrastructure", "Developer Tools"],
    "01-prerequisites": ["Intelligence Evaluation", "Frontier Open Models"],
    "02-models": ["Architecture", "Inference Optimization Research"],
    "03-hardware": ["GPU Infrastructure"],
    "04-software": ["Developer Tools", "GPU Infrastructure"],
    "05-techniques": ["Inference Optimization Research"],
    "06-modalities": ["Architecture", "Frontier Open Models", "Inference Optimization Research"],
    "07-production": ["GPU Infrastructure", "Developer Tools", "Intelligence Evaluation"],
}

READING_CATEGORIES = {
    "Architecture",
    "Developer Tools",
    "Frontier Open Models",
    "GPU Infrastructure",
    "Inference Optimization Research",
    "Intelligence Evaluation",
}


@dataclass(frozen=True)
class Section:
    level: int
    title: str
    pdf_page: int


@dataclass(frozen=True)
class Chapter:
    slug: str
    title: str
    pdf_start: int
    pdf_end: int
    sections: list[Section]


def ascii_clean(value: str) -> str:
    value = value.replace("\u00a0", " ")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def slugify(value: str) -> str:
    value = ascii_clean(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def is_chapter_title(title: str) -> bool:
    return title.startswith("Chapter ") or title in {"Preface"}


def get_chapters(doc: fitz.Document) -> list[Chapter]:
    toc = [Section(level, ascii_clean(title), page) for level, title, page in doc.get_toc(simple=True)]
    top = [item for item in toc if item.level == 2]
    chapter_tops = [item for item in top if is_chapter_title(item.title)]
    chapters: list[Chapter] = []

    for idx, item in enumerate(chapter_tops):
        next_page = chapter_tops[idx + 1].pdf_page if idx + 1 < len(chapter_tops) else doc.page_count + 1
        if item.title == "Preface":
            slug = "preface"
        else:
            match = re.match(r"Chapter\s+(\d+):\s*(.+)", item.title)
            if not match:
                continue
            number, name = match.groups()
            slug = f"{int(number):02d}-{slugify(name)}"

        sections = [
            section
            for section in toc
            if section.pdf_page >= item.pdf_page
            and section.pdf_page < next_page
            and section.title != item.title
            and section.level > item.level
        ]
        chapters.append(Chapter(slug, item.title, item.pdf_page, next_page - 1, sections))

    return chapters


def extract_figure_captions(doc: fitz.Document) -> list[dict[str, object]]:
    captions: list[dict[str, object]] = []
    for page_index, page in enumerate(doc, start=1):
        lines = [ascii_clean(line) for line in page.get_text("text").splitlines()]
        for idx, line in enumerate(lines):
            if not re.match(r"^Figure\s+[A-Z0-9]+(?:\.\d+)?:", line):
                continue

            caption_parts = [line]
            cursor = idx + 1
            while cursor < len(lines) and len(caption_parts) < 5:
                next_line = lines[cursor]
                if not next_line:
                    break
                if re.match(r"^(Chapter|CHAPTER|Appendix|[0-9]+(\.[0-9]+)*)\b", next_line):
                    break
                caption_parts.append(next_line)
                if next_line.endswith("."):
                    break
                cursor += 1

            caption = ascii_clean(" ".join(caption_parts))
            captions.append({"pdf_page": page_index, "caption": caption})
    return captions


def chapter_for_page(chapters: list[Chapter], page: int) -> Chapter | None:
    for chapter in chapters:
        if chapter.pdf_start <= page <= chapter.pdf_end:
            return chapter
    return None


def extract_readings(doc: fitz.Document) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    category = "General"
    seen: set[tuple[str, str]] = set()

    for page_index in range(doc.page_count):
        page = doc[page_index]
        text = page.get_text("text")
        if "Recommended Reading" not in text and category == "General":
            continue

        blocks = sorted(page.get_text("blocks"), key=lambda block: (block[1], block[0]))
        for block in blocks:
            raw = ascii_clean(block[4])
            if not raw:
                continue
            if raw in READING_CATEGORIES:
                category = raw
                continue
            if "Recommended Reading" in raw and len(raw) < 40:
                continue
            if "http://" not in raw and "https://" not in raw:
                continue

            match = re.search(r"https?://", raw)
            if not match:
                continue

            title = ascii_clean(raw[: match.start()].strip(" ,"))
            url = raw[match.start() :]
            url = re.sub(r"\s+", "", url)
            url = url.strip(".,;:)\"'")
            url = clean_url(url)

            if url == "https://www.baseten.com/blog":
                title = "Baseten Blog"

            if not title:
                title = urlparse(url).netloc

            key = (category, url)
            if key in seen:
                continue
            seen.add(key)
            entries.append(
                {
                    "category": category,
                    "title": title,
                    "url": url,
                    "source_pdf_page": page_index + 1,
                    "download_status": "pending",
                    "notes": "",
                }
            )

    return entries


def clean_url(url: str) -> str:
    replacements = {
        "https://github.com/vipshop/cachedit": "https://github.com/vipshop/cache-dit",
        "https://arxiv.org/abs/2401.04055": "https://arxiv.org/abs/2401.10774",
        "https://github.com/openai/gradeschool-math": "https://github.com/openai/grade-school-math",
        "https://www.goodreads.com/work/editions/10244675-programming-massively-parallelprocessors-a-hands-on-approach": "https://www.goodreads.com/work/editions/10244675-programming-massively-parallel-processors-a-hands-on-approach",
    }
    return replacements.get(url, url)


def write_if_missing(path: Path, content: str) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def chapter_readme(chapter: Chapter) -> str:
    sections = "\n".join(f"- [ ] `{section.title}` (PDF page {section.pdf_page})" for section in chapter.sections)
    if not sections:
        sections = "- [ ] Read and summarize this chapter."

    return f"""# {chapter.title}

PDF pages: {chapter.pdf_start}-{chapter.pdf_end}

## Reading Checklist

{sections}

## Chapter Loop

1. Read the section once without taking notes.
2. Re-read and fill `notes.md` with your own mental model.
3. Review `figures.md` and redraw important diagrams in your own words.
4. Add unclear terms and follow-up experiments to `questions.md`.
5. Mark the relevant rows in `../../progress.md`.
"""


def notes_template(chapter: Chapter) -> str:
    return f"""# Notes: {chapter.title}

## One-Sentence Thesis

TODO

## Core Ideas

- TODO

## Mechanisms

- TODO

## Formulas / Quantitative Models

- TODO

## Tradeoffs

- TODO

## Production Implications

- TODO

## Things To Revisit

- TODO
"""


def questions_template(chapter: Chapter) -> str:
    return f"""# Questions: {chapter.title}

## Blocking Questions

- [ ] TODO

## Deeper Dives

- [ ] TODO

## Experiments To Run

- [ ] TODO
"""


def figures_markdown(chapter: Chapter, figures: list[dict[str, object]]) -> str:
    rows = [
        figure
        for figure in figures
        if chapter.pdf_start <= int(figure["pdf_page"]) <= chapter.pdf_end
    ]
    if rows:
        lines = "\n".join(
            f"- [ ] PDF page {figure['pdf_page']}: {figure['caption']}" for figure in rows
        )
    else:
        lines = "- [ ] No figures detected for this chapter."

    return f"""# Figures: {chapter.title}

Use this file to turn each diagram into your own explanation. Rendered page images live in `../../artifacts/book/figure-pages/` after `make extract`.

{lines}
"""


def chapter_readings_markdown(chapter: Chapter, readings: list[dict[str, object]]) -> str:
    categories = CHAPTER_READING_HINTS.get(chapter.slug, [])
    lines: list[str] = []
    for category in categories:
        lines.append(f"## {category}")
        category_rows = [entry for entry in readings if entry["category"] == category]
        if not category_rows:
            lines.append("")
            lines.append("- TODO")
            continue
        for entry in category_rows[:12]:
            lines.append(f"- [ ] [{entry['title']}]({entry['url']})")
        lines.append("")

    if not lines:
        lines = ["- TODO"]

    return f"""# Further Reading: {chapter.title}

The full manifest is in `../../readings/recommended-readings.json`. This chapter starts with the most relevant categories.

{chr(10).join(lines).rstrip()}
"""


def readings_readme(readings: list[dict[str, object]]) -> str:
    by_category: dict[str, list[dict[str, object]]] = {}
    for entry in readings:
        by_category.setdefault(str(entry["category"]), []).append(entry)

    parts = [
        "# Recommended Readings",
        "",
        "Generated from Appendix B. Open arXiv papers can be downloaded with:",
        "",
        "```bash",
        "make download-readings",
        "```",
        "",
        "The downloader stores files under `downloads/readings/`, which is intentionally ignored by git.",
        "",
    ]
    for category, rows in by_category.items():
        parts.append(f"## {category}")
        parts.append("")
        for row in rows:
            parts.append(f"- [ ] [{row['title']}]({row['url']})")
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def progress_markdown(chapters: list[Chapter]) -> str:
    rows = [
        "| Chapter | Read | Notes | Figures | Questions | Further Reading |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for chapter in chapters:
        rows.append(f"| [{chapter.title}](chapters/{chapter.slug}/) | [ ] | [ ] | [ ] | [ ] | [ ] |")
    rows.extend(
        [
            "| [Appendix A: Inference Glossary](appendices/glossary/) | [ ] | [ ] | n/a | [ ] | n/a |",
            "| [Appendix B: Recommended Reading](appendices/recommended-reading/) | [ ] | [ ] | n/a | [ ] | [ ] |",
        ]
    )
    return "# Progress\n\n" + "\n".join(rows) + "\n"


def write_repo(pdf: Path) -> None:
    doc = fitz.open(pdf)
    chapters = get_chapters(doc)
    figures = extract_figure_captions(doc)
    readings = extract_readings(doc)

    Path("chapters").mkdir(exist_ok=True)
    Path("appendices/glossary").mkdir(parents=True, exist_ok=True)
    Path("appendices/recommended-reading").mkdir(parents=True, exist_ok=True)
    Path("readings").mkdir(exist_ok=True)
    Path("scripts").mkdir(exist_ok=True)

    for chapter in chapters:
        base = Path("chapters") / chapter.slug
        write_if_missing(base / "README.md", chapter_readme(chapter))
        write_if_missing(base / "notes.md", notes_template(chapter))
        write_if_missing(base / "questions.md", questions_template(chapter))
        write_text(base / "figures.md", figures_markdown(chapter, figures))
        write_text(base / "further-reading.md", chapter_readings_markdown(chapter, readings))

    write_if_missing(
        Path("appendices/glossary/README.md"),
        "# Appendix A: Inference Glossary\n\nUse this folder to build your own glossary entries and examples.\n",
    )
    write_if_missing(
        Path("appendices/glossary/notes.md"),
        "# Glossary Notes\n\n| Term | My definition | Example | Related chapter |\n| --- | --- | --- | --- |\n",
    )
    write_if_missing(
        Path("appendices/recommended-reading/README.md"),
        "# Appendix B: Recommended Reading\n\nUse this folder to prioritize, summarize, and connect the recommended resources back to the chapters.\n",
    )
    write_if_missing(
        Path("appendices/recommended-reading/notes.md"),
        "# Recommended Reading Notes\n\n## Reading Queue\n\n- [ ] TODO\n\n## Synthesis\n\n- TODO\n",
    )
    write_text(Path("readings/README.md"), readings_readme(readings))
    write_text(Path("readings/recommended-readings.json"), json.dumps(readings, indent=2) + "\n")
    write_if_missing(Path("progress.md"), progress_markdown(chapters))

    print(f"Created {len(chapters)} chapter folders.")
    print(f"Detected {len(figures)} figure captions.")
    print(f"Extracted {len(readings)} recommended-reading entries.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    args = parser.parse_args()
    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")
    write_repo(args.pdf)


if __name__ == "__main__":
    main()
