# Inference Engineering Learning Repo

This repo tracks your study of Philip Kiely's *Inference Engineering* without committing the full book text, page renders, or downloaded papers.

The loop:

1. Run `make bootstrap` after changing the source PDF or repo layout.
2. Run `make extract` to refresh local text extracts and rendered figure pages in `artifacts/`.
3. Read one chapter or section with the local extracts open.
4. Fill the chapter's `notes.md`, `figures.md`, and `questions.md` in your own words.
5. Use `make download-readings` to fetch open arXiv PDFs from Appendix B into `downloads/readings/`.
6. Mark progress in `progress.md`.
7. Commit the notes, progress, manifests, and scripts. Leave `artifacts/` and `downloads/` untracked.

See `docs/learning-loop.md` for the full operating loop and `docs/mastery-guide.md` for the 10-agent synthesis of the highest-value skills and mastery path.

## Layout

- `chapters/`: one folder per book chapter with notes, figures, questions, and chapter-specific reading pointers.
- `appendices/`: glossary and recommended-reading workspaces.
- `readings/`: tracked reading manifest and index generated from Appendix B.
- `scripts/`: repeatable parsing, extraction, download, and progress tools.
- `artifacts/`: ignored local extraction output from the PDF.
- `downloads/`: ignored local copies of public papers/resources.

## Commands

```bash
make bootstrap
make extract
make download-readings
make progress
```

Set a different PDF path when needed:

```bash
make bootstrap PDF="/absolute/path/to/Inference Engineering.pdf"
make extract PDF="/absolute/path/to/Inference Engineering.pdf"
```

## Notes Policy

Keep this repo centered on your understanding:

- Do commit your summaries, mental models, diagrams redrawn in your own words, questions, experiments, and links.
- Do not commit the full PDF, full extracted text, full page renders, or downloaded third-party PDFs unless you have explicit rights to publish them.
- Use short excerpts only when needed for context, then explain them in your own words.
