# Notes: Chapter 4: Software

## One-Sentence Thesis

The inference software stack turns model architecture and GPU hardware into a serving system through kernels, frameworks, runtimes, engines, benchmarking, and profiling.

## Core Ideas

- CUDA is the low-level execution layer for NVIDIA GPUs.
- PyTorch is productive but may not expose the best inference performance by default.
- Inference engines optimize batching, memory management, KV cache, scheduling, and kernels.
- vLLM, SGLang, TensorRT-LLM, Triton, and Dynamo each sit at different points in the performance/control/complexity tradeoff.
- Model formats and compilation paths matter: Hugging Face weights, safetensors, ONNX, TensorRT engines, and engine-specific build artifacts.
- Profiling connects user-visible latency to kernel timelines, memory copies, synchronization, and scheduler behavior.

## Mechanisms

- Kernel fusion reduces memory reads/writes by combining operations.
- CUDA graphs reduce launch overhead for repeated static execution patterns.
- Continuous batching lets engines interleave requests token-by-token.
- PagedAttention-style memory management improves KV cache allocation and reduces fragmentation.
- TensorRT-LLM and related runtimes can compile and specialize execution for NVIDIA hardware.

## Formulas / Quantitative Models

- Benchmark by workload shape:
  - prompt length,
  - output length,
  - concurrency,
  - batch size,
  - context window,
  - precision,
  - engine settings.
- Split latency:
  - `queue + tokenization + prefill + decode + sampling + detokenization + network`

## Tradeoffs

- Transformers baseline is easiest to reason about but usually slower.
- vLLM is a practical first production engine for LLM serving.
- SGLang adds strong structured generation and serving capabilities.
- TensorRT-LLM can deliver high NVIDIA-specific performance but adds build and compatibility complexity.
- Compilation and specialized engines can improve speed but reduce portability and increase operational surface area.

## Production Implications

- Do not compare engines with toy prompts only.
- Pin driver, CUDA, model revision, engine version, quantization, and workload parameters.
- Warm up before measuring.
- Use profiler traces when metrics say "slow" but not "why."
- Verify correctness and quality after engine changes, not just latency.

## Things To Revisit

- Serve the same small model with Transformers and vLLM.
- Add SGLang or TensorRT-LLM comparison when hardware allows.
- Create a benchmark report with TTFT, ITL, throughput, VRAM, and percentiles.
- Learn PyTorch Profiler first, then Nsight Systems for kernel timelines.
