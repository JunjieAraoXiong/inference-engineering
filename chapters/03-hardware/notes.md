# Notes: Chapter 3: Hardware

## One-Sentence Thesis

Inference hardware decisions are about matching workload bottlenecks to GPU compute, memory capacity, memory bandwidth, and interconnect topology.

## Core Ideas

- GPU specs only matter when mapped to a workload.
- Tensor Cores accelerate matrix operations, but memory bandwidth often dominates decode.
- VRAM sets hard limits on model weights, KV cache, activations, batch size, and context length.
- HBM bandwidth is often the limiting resource for autoregressive decode.
- Interconnect matters once serving crosses GPU boundaries.
- Instance choice includes GPU count, GPU generation, CPU/RAM, local storage, network, provider availability, and price.
- MIG and time-slicing are capacity-partitioning tools with different isolation properties.

## Mechanisms

- Prefill tends to use large matrix operations and can reach higher arithmetic intensity.
- Decode repeatedly streams model weights and KV cache state, often making bandwidth more important than peak FLOPS.
- Tensor parallelism benefits from fast intra-node GPU communication.
- Pipeline or expert parallelism may tolerate slower links better depending on model shape and traffic.
- Multi-node inference adds communication costs that can dominate if topology is ignored.

## Formulas / Quantitative Models

- Model weight memory:
  - `parameter_count * bytes_per_parameter`
- Rough production fit:
  - `weights + KV cache + activations + engine overhead + safety headroom <= VRAM`
- Do not size only to minimum fit. Keep meaningful KV/cache headroom, especially for long context, high batch, adapters, or multimodal workloads.

## Tradeoffs

- Larger GPUs simplify deployment but may be underutilized.
- More small GPUs can improve throughput but add scheduling and communication complexity.
- Full GPUs give performance isolation; MIG gives hardware partitioning; time-slicing increases sharing but weakens isolation.
- Multi-node serving unlocks large models but introduces network and topology constraints.

## Production Implications

- Choose hardware from the workload envelope, not from model size alone.
- Track GPU utilization, HBM utilization, VRAM, queue depth, and token metrics together.
- Benchmark prefill and decode separately to see whether a GPU's compute or bandwidth matters more.
- For multi-GPU deployments, inspect topology before assuming scaling will be linear.

## Things To Revisit

- Build a GPU comparison table for L4, A100, H100/H200, B200/B300.
- Run `nvidia-smi topo -m` on a multi-GPU machine when available.
- Estimate whether a 7B, 70B, and 100B+ model fits under different precisions and context lengths.
