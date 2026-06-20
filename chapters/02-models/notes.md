# Notes: Chapter 2: Models

## One-Sentence Thesis

Model architecture determines inference cost: LLMs generate tokens sequentially, diffusion models denoise over repeated steps, and bottlenecks come from the relationship between compute work and memory movement.

## Core Ideas

- Neural networks are mostly linear algebra plus nonlinear activations.
- Without nonlinear activations, stacked linear layers collapse into one linear transform.
- LLM inference has two main phases:
  - Prefill: process the prompt and create KV cache.
  - Decode: generate one token at a time using prior context.
- Attention is central because it links sequence length, memory traffic, and KV cache.
- MoE models distinguish total parameters from active parameters per token.
- Diffusion models spend inference time across repeated denoising steps, often multiplied by guidance or refinement passes.
- The right optimization depends on whether the workload is compute-bound, memory-bound, or communication-bound.

## Mechanisms

- LLM loop:
  - tokenize prompt,
  - run prefill over prompt tokens,
  - store keys and values in KV cache,
  - decode next token from logits,
  - sample,
  - append token,
  - repeat until stop condition.
- Attention:
  - project hidden states into Q, K, V,
  - compare Q to K,
  - normalize scores,
  - mix V according to attention weights.
- KV cache avoids recomputing past K/V during decode, but consumes memory proportional to context, batch, layers, heads, and dtype.
- Diffusion pipeline:
  - encode conditioning,
  - denoise latent representation for many steps,
  - decode final latent into image/video/audio.

## Formulas / Quantitative Models

- Linear layer: `y = xW + b`
- Attention: `softmax(QK^T / sqrt(d_k))V`
- Hardware ops/byte: `peak_ops_per_second / memory_bandwidth_bytes_per_second`
- Arithmetic intensity: `work / memory_traffic`
- KV cache estimate:
  - `batch * seq_len * layers * 2 * kv_heads * head_dim * bytes_per_value`
- Roofline intuition:
  - arithmetic intensity below hardware ops/byte usually means memory-bound,
  - above it usually means compute-bound.

## Tradeoffs

- Full attention preserves quality and flexibility but scales poorly with long context.
- FlashAttention improves memory movement without changing attention semantics.
- Sliding, linear, compressed, or gated attention changes the algorithm and may change quality.
- MoE can reduce active compute per token, but production batches may activate many experts and create routing/parallelism challenges.
- Fewer diffusion steps reduce latency but can reduce quality unless the model or scheduler is designed for it.

## Production Implications

- Always split benchmarks into prefill and decode when serving LLMs.
- Long context is a memory problem as much as a compute problem.
- Model size is not the only serving variable; active parameters, context length, KV size, and batch shape matter.
- For image/video generation, step count and denoiser efficiency are often more important than token TPS.

## Things To Revisit

- Implement attention from scratch and add KV-cache incremental decode.
- Build a KV cache calculator.
- Recompute arithmetic intensity for several sequence lengths.
- Draw the difference between dense LLM, MoE LLM, diffusion image model, and video model pipelines.
