# Latency And Throughput

## My Definition

Latency is what an individual request feels; throughput is how much work the system completes over time. They interact but are not the same metric.

## Key Metrics

- TTFT: time to first token.
- ITL: inter-token latency after the first token.
- Tokens/sec/user: perceived generation speed for one user.
- Tokens/sec/GPU: fleet efficiency.
- End-to-end latency: full request time including client, network, queueing, model, and postprocessing.
- P50/P95/P99: distribution percentiles.

## Mental Model

Batching improves fleet throughput by sharing work, but it can increase individual latency if requests wait too long or batches become too large.

## Failure Mode

Reporting average latency hides the tail. Users complain about p95/p99, not the mean.

## Production Implication

Every benchmark should include percentiles, concurrency, prompt/output distributions, and queueing delay.
