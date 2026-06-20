# GPU Roofline

## My Definition

The roofline model compares the compute required by an operation to the memory traffic it creates, then predicts whether compute or memory bandwidth is the likely limit.

## Formulas

```text
hardware_ops_per_byte = peak_ops_per_second / memory_bandwidth_bytes_per_second
arithmetic_intensity = work / memory_traffic
```

If arithmetic intensity is below the hardware ops/byte ratio, the workload is usually memory-bound. If it is above, it is usually compute-bound.

## Why It Matters

Peak FLOPS alone do not tell you serving performance. A GPU with huge compute can still be limited by HBM bandwidth during decode.

## Failure Mode

Buying more FLOPS for a memory-bound workload can raise cost without improving user-visible latency.

## Production Implication

Hardware selection should include compute, memory bandwidth, VRAM, interconnect, and workload arithmetic intensity.
