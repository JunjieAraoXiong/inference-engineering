# Quantization

## My Definition

Quantization reduces numerical precision to improve memory use, bandwidth pressure, throughput, or cost.

## Good Order Of Operations

1. Establish baseline quality and performance.
2. Quantize weights.
3. Consider activations.
4. Consider KV cache if memory pressure matters.
5. Be cautious with attention/softmax.
6. Run product-specific regression evals.

## Signals

- VRAM reduction.
- TTFT/ITL improvement.
- Tokens/sec/GPU.
- Quality delta.
- Cost/token.

## Failure Mode

A quantized model can pass generic benchmarks while failing product-specific edge cases.

## Production Implication

Quantization is not complete until quality, latency, memory, and cost are measured together.
