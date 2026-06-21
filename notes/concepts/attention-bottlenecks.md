# Attention Bottlenecks

## My Definition

Attention bottlenecks come from comparing tokens to other tokens and moving the resulting tensors through memory.

## Core Formula

```text
softmax(QK^T / sqrt(d_k))V
```

## Mental Model

Attention is both math and memory traffic. FlashAttention-style kernels are powerful because they reduce memory movement while preserving exact attention semantics.

## Bottleneck Questions

- Is this prefill or decode?
- What is the sequence length?
- What is the head dimension?
- How much data is read/written?
- Is the algorithm memory-bound or compute-bound?

## Failure Mode

Saying "attention is quadratic" is incomplete. Prefill and decode behave differently because KV cache changes what is recomputed.

## Production Implication

Choose attention optimizations based on phase, context length, precision, and quality tolerance.
