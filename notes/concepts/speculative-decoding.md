# Speculative Decoding

## My Definition

Speculative decoding uses a cheaper draft process to propose tokens, then validates those tokens with the target model so the system can accept multiple tokens per expensive target pass.

## Why It Helps

It targets decode latency when decode is memory-bandwidth-bound and spare compute is available.

## Signals

- Acceptance rate.
- Accepted tokens per target step.
- Draft overhead.
- ITL.
- Cost/token.

## When It Works Best

- Low or moderate batch size.
- Predictable generation.
- Good draft model or method.
- User-facing latency matters more than maximum fleet throughput.

## Failure Mode

At high temperature, high batch, or low acceptance, speculation can add work without improving latency.

## Production Implication

Speculation should be dynamically enabled or tuned by workload shape, not treated as always-on.
