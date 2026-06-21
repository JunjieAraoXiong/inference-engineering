# Evals And Model Selection

## My Definition

Model selection is choosing the smallest deployable model that passes product-specific evals with enough margin for production drift.

## Why Public Benchmarks Are Not Enough

Public benchmarks help shortlist models, but product quality depends on real prompts, edge cases, output style, tool behavior, safety constraints, latency, and cost.

## Good Eval Set

- Real production-like prompts.
- Hard examples.
- Common failure modes.
- Domain-specific constraints.
- Expected sampling parameters.
- Regression cases from prior failures.

## Decision Rule

Prefer the smallest and simplest model/deployment that clears the quality bar, latency target, and cost target.

## Failure Mode

Optimizing a large model for speed when a smaller model could have passed the task after prompt work or fine-tuning.

## Production Implication

No quantization, fine-tuning, distillation, model swap, or engine migration is complete until the eval suite passes.
