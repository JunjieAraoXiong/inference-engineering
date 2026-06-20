# Notes: Chapter 5: Techniques

## One-Sentence Thesis

Inference optimization is a set of workload-dependent techniques that trade quality, latency, throughput, memory, cost, and operational complexity.

## Core Ideas

- Quantization reduces precision to lower memory and improve speed, but quality must be measured.
- Speculative decoding tries to generate multiple accepted tokens per target-model step.
- Prefix/KV caching reuses prior computation when requests share stable context.
- Model parallelism spreads a model across GPUs to fit larger weights or improve latency/throughput.
- Disaggregation separates prefill and decode workers when their resource needs differ enough to justify system complexity.
- These techniques interact; one can strengthen or weaken another.

## Mechanisms

- Quantization:
  - start with weights,
  - then activations,
  - consider KV cache if memory pressure matters,
  - treat attention/softmax as higher risk.
- Speculation:
  - draft candidate tokens,
  - validate them with the target model,
  - accept the longest valid prefix,
  - fall back when acceptance is low.
- Caching:
  - stable prefixes allow reuse,
  - cache-aware routing improves hit rate,
  - cache eviction and memory pressure affect tail latency.
- Parallelism:
  - tensor parallelism splits layers across GPUs,
  - expert parallelism maps MoE experts across GPUs,
  - pipeline parallelism divides layers/stages.
- Disaggregation:
  - prefill workers handle prompt processing,
  - decode workers handle token generation,
  - KV transfer cost and queue depth decide whether it is worthwhile.

## Formulas / Quantitative Models

- Quantization value:
  - speed/memory gain must be compared against quality delta.
- Speculation value:
  - useful when accepted tokens per target step outweigh draft overhead.
- Cache value:
  - `shared_prefix_tokens / total_prompt_tokens` is a rough ceiling on benefit.
- Parallelism value:
  - added GPU capacity must beat interconnect overhead and scheduling complexity.

## Tradeoffs

- Quantization improves economics but can damage model behavior in ways generic benchmarks miss.
- Speculation improves per-user decode speed when acceptance is high, but may hurt at high batch or high temperature.
- Caching helps repeated context, but prompt layout and routing determine real hit rate.
- Parallelism can reduce latency or fit large models, but it can be worse than replicas if communication dominates.
- Disaggregation can increase utilization at scale, but adds KV movement, routing policy, and debugging complexity.

## Production Implications

- Run ablation benchmarks. Do not stack five optimizations and guess which one helped.
- Maintain a quality regression suite before quantization or model changes.
- Segment traffic by workload shape: short chat, long RAG, code completion, batch/offline, multimodal, high-temperature generation.
- Build dynamic policies: disable speculation when acceptance falls, route for cache locality when worth it, adjust prefill/decode capacity under load.

## Things To Revisit

- Quantization sweep with quality evals.
- Speculative decoding sweep by batch size, temperature, and draft length.
- Prefix-cache prompt-layout A/B test.
- KV memory/offload experiment.
- Tensor/expert/pipeline parallelism comparison.
- Disaggregated vs colocated serving simulation.
