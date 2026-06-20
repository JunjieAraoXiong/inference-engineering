# KV Cache

## My Definition

KV cache stores the key and value tensors from previous tokens so decode can avoid recomputing them for the whole context.

## Why It Matters

KV cache is request state. At long context or high batch, it can dominate GPU memory and shape routing, caching, and parallelism decisions.

## Estimate

```text
batch * seq_len * layers * 2 * kv_heads * head_dim * bytes_per_value
```

The `2` is for keys and values.

## Signals

- VRAM usage.
- Cache hit rate.
- Eviction rate.
- TTFT for shared-prefix requests.
- Max batch/context before OOM.

## Failure Mode

Sizing only model weights and forgetting KV cache leads to deployments that fit on paper but fail under realistic context and concurrency.

## Production Implication

KV cache deserves first-class capacity planning, metrics, routing policy, and eviction behavior.
