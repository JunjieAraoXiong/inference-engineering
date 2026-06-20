# Learning Loop

The goal is to turn the book and its recommended readings into durable working knowledge, not just collect PDFs.

## Workflow Pattern

Use a sequential loop with a quality gate:

1. Parse: extract page text, figure pages, chapter boundaries, and Appendix B links.
2. Segment: place each chapter into its own folder with section checklists.
3. Read: work through one section at a time.
4. Explain: write the idea in your own words in `notes.md`.
5. Diagram: use `figures.md` plus local page renders to redraw or narrate the diagrams.
6. Drill: add questions, formulas, experiments, and confusions to `questions.md`.
7. Expand: read the chapter's `further-reading.md` queue and update reading notes.
8. Synthesize: update `progress.md` and commit the learning artifact.
9. Review: open a PR so the repo history stays inspectable.

The quality gate is simple: do not mark a section done until you can explain the mechanism, the bottleneck or tradeoff, and one production implication without quoting the book.

## Daily Cadence

For each session:

1. Pick one unchecked section from a chapter `README.md`.
2. Read the extracted page text in `artifacts/book/pages/` or the original PDF.
3. Inspect matching diagrams in `artifacts/book/figure-pages/`.
4. Add your own summary, at least one question, and any relevant formula or mental model.
5. Check off the section and figure rows you actually understood.
6. Run `make progress`.
7. Commit and open a PR for the notes from that session.

## Reading Strategy

Appendix B resources are grouped by topic. The downloader fetches directly available PDFs, especially arXiv papers, and leaves everything else as links.

For papers:

- Read the abstract, introduction, method diagram, and results table first.
- Write the claim in one sentence.
- Connect it to a chapter concept.
- Record what changes in production if the paper's method works.
- Record whether the method is research-only, library-supported, or production-ready.

For tools and documentation:

- Identify the abstraction the tool provides.
- Record the main configuration knobs.
- Note failure modes, observability hooks, and deployment constraints.

## PR Rule

Every meaningful learning increment should be a PR:

- One chapter section, one paper note, or one experiment per PR is ideal.
- Keep generated local artifacts out of git.
- Treat the PR description as the session summary.
- A separate human approval is still needed for review; the author should not approve their own PR.
