# Prefill And Decode

## My Definition

Prefill processes the prompt and builds KV cache. Decode generates new tokens one at a time using the cache.

## Why It Matters

The two phases stress hardware differently. Prefill tends to be more compute-heavy; decode often becomes memory-bandwidth-heavy.

## Signals

- Prefill latency drives TTFT.
- Decode latency drives ITL and perceived streaming speed.
- Prompt length mostly pressures prefill.
- Output length mostly pressures decode duration.

## Optimization Implications

- Long prompts: improve prefill, chunking, prefix caching, disaggregation, or prompt layout.
- Slow streaming: improve decode, batching policy, memory bandwidth, speculation, or quantization.

## Failure Mode

Using one total latency number hides which phase is broken.

## Production Implication

Measure and dashboard prefill and decode separately.
