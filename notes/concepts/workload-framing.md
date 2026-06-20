# Workload Framing

## My Definition

Workload framing is the process of turning a product idea into measurable inference requirements.

## Questions To Answer

- Is the workload online, offline, or mixed?
- Is the user waiting synchronously, streaming, or submitting a batch job?
- What are the expected input and output lengths?
- What are the P50/P95/P99 latency targets?
- What quality failures are unacceptable?
- What is the cost ceiling?
- What data, region, or compliance constraints exist?

## Why It Matters

The same model can need different deployments for chat, code completion, long-context RAG, embeddings backfill, voice agents, and image generation.

## Signals

- Traffic distribution.
- Sequence length distribution.
- Concurrency.
- Required latency percentiles.
- Quality eval pass rate.
- Cost per successful request.

## Failure Mode

Picking a model or GPU before defining the workload usually creates expensive optimization work that does not move the product metric.

## Production Implication

The first artifact for any inference project should be a workload brief, not a benchmark.
