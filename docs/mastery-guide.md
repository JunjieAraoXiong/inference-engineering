# Inference Engineering Mastery Guide

This guide synthesizes 10 subagent passes over the book structure, extracted local notes, chapter outlines, figure lists, and Appendix B reading manifest.

The north star: become able to take an inference workload from product requirement to production design, with quantitative tradeoffs for model choice, latency, throughput, hardware, cost, reliability, and optimization technique.

## The Most Valuable Skills

1. Workload framing
   Define the product, modality, user experience, online/offline shape, latency target, throughput target, traffic distribution, quality bar, compliance constraints, and cost ceiling before optimizing anything.

2. Product-specific evals and model selection
   Public leaderboards are only a shortlist. The real skill is building evals from real prompts, hard cases, expected sampling parameters, and product failure modes, then choosing the smallest model that passes.

3. Inference measurement
   Measure TTFT, inter-token latency, tokens/sec/user, tokens/sec/GPU, end-to-end latency, P50/P95/P99, queueing delay, VRAM, GPU utilization, error rate, and cost/token. Avoid averages as the main decision metric.

4. Model mechanics
   Trace tokens through tokenization, prefill, KV cache creation, decode, logits, sampling, and stopping. For non-LLM models, trace the modality-specific pipeline: embeddings, ASR, TTS, diffusion, or video generation.

5. Bottleneck math
   Classify work as compute-bound, memory-bandwidth-bound, interconnect-bound, queue-bound, or client/network-bound. Use arithmetic intensity, ops/byte, prefill/decode split, and KV cache sizing.

6. GPU capacity planning
   Read GPU specs and convert them into serving predictions: VRAM, HBM bandwidth, tensor core precision, NVLink/NVSwitch/InfiniBand topology, MIG/time-slicing, node shape, and GPU-hour economics.

7. Runtime and engine fluency
   Understand the stack from CUDA and PyTorch to ONNX Runtime, TensorRT, vLLM, SGLang, TensorRT-LLM, Triton, and Dynamo. Know what each layer optimizes and what it hides.

8. Optimization technique selection
   Treat quantization, batching, prefix/KV caching, speculative decoding, tensor/expert/pipeline parallelism, and disaggregation as workload-dependent policies, not universal wins.

9. Modality-specific inference
   Do not treat every workload as an LLM. VLMs, embeddings, ASR, TTS, image generation, and video generation each have different units of work, quality metrics, bottlenecks, and serving shapes.

10. Production operations
    Build systems around latency, capacity, reliability, deploy safety, observability, cost, and client experience. Production inference is a control system, not a single fast model server.

## Dependency Graph

Learn in this order:

```text
product use case + SLA + budget
-> evals + model selection
-> model mechanics: tensors, tokens, attention, diffusion, modalities
-> metrics: TTFT, ITL, TPS, throughput, percentiles, queueing
-> bottleneck math: prefill/decode, arithmetic intensity, KV cache
-> hardware: VRAM, HBM bandwidth, tensor cores, interconnect
-> software: CUDA, PyTorch, runtimes, serving engines
-> single-node tuning: batching, quantization, KV cache, prefix caching
-> multi-GPU tuning: TP, EP, PP, topology, disaggregation
-> production systems: containers, autoscaling, routing, deployment, observability
-> platform judgment: expose enough control without unnecessary complexity
```

## Core Mental Models

- Inference is a stack: runtime, infrastructure, and tooling.
- Optimization starts with the workload shape, not the technique.
- Prefill mostly drives TTFT and tends to be compute-heavy.
- Decode mostly drives ITL/TPS and often becomes memory-bandwidth-heavy.
- KV cache is request state, not model weights, and can dominate memory at long context or high batch.
- Batch size trades per-user latency for fleet throughput and cost efficiency.
- Faster is not better if quality regresses. Evals are the guardrail.
- GPU peak FLOPS are not enough. Memory bandwidth, interconnect, scheduler behavior, queueing, and utilization decide the real system.
- Scale changes the problem. A fast single replica becomes autoscaling, routing, capacity, reliability, observability, and client protocol design.

## Quantitative Ideas To Master

- Linear layer: `y = xW + b`
- Attention: `softmax(QK^T / sqrt(d_k))V`
- Hardware ops/byte: `peak_ops_per_second / memory_bandwidth_bytes_per_second`
- Arithmetic intensity: `work / memory_traffic`
- Roofline intuition: below hardware ops/byte is usually memory-bound; above it is usually compute-bound.
- KV cache estimate: `batch * seq_len * layers * 2 * kv_heads * head_dim * bytes_per_value`
- Dedicated GPU cost: `gpu_hours * gpu_hour_price + engineering/ops overhead`
- API cost: `(input_tokens * input_price) + (output_tokens * output_price) + cache/read/write costs`

## Technique Decision Rules

| Technique | Use when | Defer when | Main metrics |
| --- | --- | --- | --- |
| Quantization | You need lower memory, better throughput, or more KV headroom and have quality evals. | Quality is fragile or evals are missing. | Quality delta, VRAM, TTFT, ITL, TPS, cost/token. |
| Speculative decoding | Decode is memory-bound, batch is low/moderate, and spare compute exists. | Batch is high, acceptance is low, temperature is high, or throughput matters more than per-user latency. | Acceptance rate, ITL, accepted tokens/step, cost/token. |
| Prefix/KV caching | Requests share long stable prefixes: system prompts, RAG scaffolds, code context, repeated media. | User-specific tokens appear early or cache-aware routing is absent. | Cache hit rate, TTFT, KV memory pressure, eviction rate. |
| Model parallelism | Model weights plus KV cache do not fit comfortably or large-model latency needs more GPUs. | More replicas would improve throughput more cheaply. | VRAM headroom, interconnect bandwidth, user TPS, aggregate TPS. |
| Disaggregation | Large model, high volume, long prefill-heavy traffic, and enough scale to justify complexity. | Small models, low traffic, short prompts, or high prefix-cache hit rate. | TTFT, prefill queue depth, decode TPS, KV transfer time, P:D utilization. |

## Modality-Specific Guide

| Modality | Unit of work | Main bottleneck | Skills to learn |
| --- | --- | --- | --- |
| LLM text | Tokens | Prefill compute, decode memory bandwidth, KV cache | TTFT, ITL, batching, KV cache, attention kernels, sampling. |
| VLM | Visual tokens plus text tokens | Visual prefill, long context, KV growth | Image/video preprocessing, visual token budgets, downsampling, prefix caching. |
| Embeddings | Vectors | Throughput, batching, vector index cost | Pooling, normalization, Matryoshka dimensions, ANN retrieval, MTEB-style evals. |
| ASR | Audio chunks/files | Chunking, streaming latency, orchestration | VAD, Whisper-style inference, chunk parallelism, timestamp stitching, diarization. |
| TTS | Audio stream | Real-time decode, audio decoder/vocoder | TTFB, first sentence latency, streaming, voice/prosody controls, safety. |
| Image generation | Denoising steps | Compute-heavy denoiser and attention kernels | Diffusion, CFG, schedulers, few-step distillation, TensorRT/SGLang Diffusion. |
| Video generation | Frames/latent video | Attention-heavy, often batch-size-one, multi-GPU | Context parallelism, attention quantization, temporal coherence, node-level profiling. |

## Practice Projects

1. Product brief
   Pick one target app. Define users, modality, traffic shape, quality evals, SLOs, cost ceiling, and deployment mode.

2. Transformer mechanics notebook
   Implement attention in NumPy or PyTorch, add a causal mask, then add KV-cache incremental decode and verify outputs against full attention for the next token.

3. Bottleneck calculator
   Build a small calculator for arithmetic intensity, KV cache memory, model weight memory, and GPU fit.

4. Serving benchmark
   Serve the same small model with a simple Transformers baseline and a production engine such as vLLM or SGLang. Compare prompt length, output length, concurrency, batch size, TTFT, ITL, VRAM, and throughput.

5. Quantization and quality report
   Compare baseline precision against one or more quantized modes. Track speed, memory, and product-specific eval quality.

6. Prefix-cache experiment
   A/B prompt layouts where shared context appears before or after user-specific tokens. Measure cache hit rate and TTFT.

7. Hardware selection memo
   Compare at least three GPU or instance choices for the target workload. Estimate weights, KV cache, headroom, batch capacity, interconnect need, and cost.

8. Modality decision matrix
   Design two non-text pipelines, such as VLM and ASR/TTS. Include quality metrics, serving pipeline, bottlenecks, and failure modes.

9. Production runbook
   Specify container build, dependency pinning, health checks, autoscaling signals, canary rollout, rollback criteria, alerts, dashboards, and cost model.

10. Capstone architecture
    Present a full inference system: model choice, eval suite, hardware, serving engine, optimization techniques, autoscaling, routing, observability, cost, and client protocol.

## Operational Checklists

Product and model gate:

- Is the workload online, offline, or mixed?
- Is the UX streaming, synchronous, async, or batch?
- What are P50/P95/P99 latency targets?
- What are expected input/output lengths and outliers?
- What is the cost ceiling per request, user, and month?
- What compliance or region constraints exist?
- What eval set proves the model is good enough?
- What is the smallest model that passes with margin?

Benchmark gate:

- Use production-like prompts, sequence lengths, sampling params, and traffic bursts.
- Separate prefill, decode, queueing, tokenization, network, and client overhead.
- Warm up before timing.
- Report percentiles, not just means.
- Change one variable at a time.
- Verify quality after every speed optimization.

Production gate:

- Dependencies are pinned.
- Image build and startup are measured.
- Model weights and compiled engine cache strategy are explicit.
- Autoscaling uses workload-aware signals, not only GPU utilization.
- Queue depth, backpressure, and priority behavior are visible.
- Canary and rollback criteria are predefined.
- Dashboards connect application traces, server metrics, queue metrics, and GPU metrics.
- Cost is modeled over weekly traffic, including idle capacity and engineering overhead.

## Reading Spine

Do not try to read all Appendix B items linearly. Use this spine first.

Phase 1: evals and model choice

- Baseten Blog
- Evals for AI Engineers
- MMLU, HumanEval, MTEB, SWE-Bench
- Llama, Qwen, DeepSeek, Mistral, Gemma model hubs

Phase 2: model mechanics

- Deep Learning or Deep Learning with Python as a reference
- Attention is All You Need
- Language Models Are Few-Shot Learners
- BERT and Sentence-BERT
- Outrageously Large Neural Networks
- The Llama 3 Herd of Models

Phase 3: modalities

- Denoising Diffusion Probabilistic Models
- High-Resolution Image Synthesis with Latent Diffusion Models
- DiT and SDXL
- CLIP, BLIP-2, Visual Instruction Tuning
- Robust Speech Recognition via Large-Scale Weak Supervision

Phase 4: hardware and kernels

- GPU Glossary
- NVIDIA H100 and Blackwell technical briefs
- Programming Massively Parallel Processors
- CUDA by Example and CUDA C++ Programming Guide
- cuBLAS, CUTLASS, DeepGEMM, NVLink, InfiniBand

Phase 5: serving software

- PyTorch Performance Tuning Guide
- PyTorch Profiler
- Transformers and Diffusers
- ONNX Runtime and TensorRT
- vLLM, SGLang, TensorRT-LLM, Triton, Dynamo

Phase 6: optimization

- FlashAttention, FlashAttention-2/3, FlashInfer
- LLM.int8, GPTQ, SmoothQuant, AWQ
- Fast Inference from Transformers via Speculative Decoding
- Medusa, EAGLE, Lookahead Decoding
- PagedAttention, LMCache, CacheBlend
- Megatron-LM, Ring Attention, context parallelism
- Beyond the Buzz: A Pragmatic Take on Inference Disaggregation

Phase 7: production systems

- Designing Data-Intensive Applications
- Kubernetes Documentation
- Site Reliability Engineering
- SemiAnalysis

## 10-Week Plan

| Week | Focus | Portfolio artifact | Mastery signal |
| --- | --- | --- | --- |
| 1 | Chapters 0-1: stack, product constraints, evals, metrics | `portfolio/01-inference-product-brief.md` | You can turn an app idea into quality, latency, throughput, cost, and deployment constraints. |
| 2 | Chapter 2 part 1: tensors, tokenization, LLM loop, transformer blocks | `portfolio/02-transformer-mechanics.md` | You can trace a prompt through prefill, KV cache, decode, logits, and sampling. |
| 3 | Chapter 2 part 2: attention, MoE, diffusion, arithmetic intensity | `portfolio/03-bottleneck-calculator.md` | You can classify bottlenecks quantitatively. |
| 4 | Chapter 3: GPU architecture and instance choice | `portfolio/04-hardware-selection-memo.md` | You can choose hardware from workload constraints, not just model size. |
| 5 | Chapter 4: CUDA, PyTorch, runtimes, inference engines, profiling | `portfolio/05-serving-benchmark.md` | You can benchmark and explain what an inference engine changed. |
| 6 | Chapter 5 part 1: quantization and speculative decoding | `portfolio/06-optimization-quality-report.md` | You can optimize while protecting quality. |
| 7 | Chapter 5 part 2: caching, long context, parallelism, disaggregation | `portfolio/07-serving-architecture-options.md` | You can choose cache, TP/EP/PP, or disaggregation from measured constraints. |
| 8 | Chapter 6: modalities | `portfolio/08-modality-decision-matrix.md` | You can design non-text pipelines with the right metrics and bottleneck assumptions. |
| 9 | Chapter 7: production systems | `portfolio/09-production-runbook.md` | You can operate an inference service, not just run a model. |
| 10 | Capstone | `portfolio/10-capstone-inference-system.md` | You can defend a complete inference architecture in a closed-book design review. |

## Mastery Criteria

You have mastered the book when you can:

- Explain every chapter thesis in one sentence.
- Redraw the important figures from memory in your own words.
- Given a workload, estimate model fit, KV cache memory, bottleneck class, hardware need, and cost drivers.
- Build a benchmark that separates prefill, decode, queueing, tokenization, network, and client overhead.
- Choose between model size, quantization, batching, caching, parallelism, and disaggregation with explicit tradeoffs.
- Design a production inference service with deployment, rollback, observability, autoscaling, capacity, cost, and client protocol choices.
- Defend the capstone architecture in a 30-minute review using repo notes, experiments, and portfolio artifacts as evidence.
