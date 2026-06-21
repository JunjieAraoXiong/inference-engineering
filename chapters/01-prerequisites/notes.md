# Notes: Chapter 1: Prerequisites

## One-Sentence Thesis

Before optimizing inference, define the product constraints, quality bar, latency budget, cost target, and model-selection process.

## Core Ideas

- Optimization without a target is wasted effort.
- The first decision is the workload shape: online vs offline, consumer vs B2B, streaming vs batch, predictable vs bursty.
- Model choice should be driven by product-specific evals, not only public benchmarks.
- The best model is often the smallest model that clears the quality bar with margin.
- Fine-tuning, distillation, and quantization all require regression evals because speed or specialization can damage quality.
- Latency must be described precisely: TTFT, inter-token latency, total response time, and percentiles mean different things.

## Mechanisms

- Product scoping creates the operating envelope:
  - quality threshold,
  - model candidates,
  - target latency percentiles,
  - throughput target,
  - traffic distribution,
  - cost ceiling,
  - compliance constraints.
- Evals turn subjective quality into an engineering loop.
- Cost modeling compares shared API token cost against dedicated GPU-hour cost, utilization, and engineering overhead.

## Formulas / Quantitative Models

- API cost:
  - `input_tokens * input_price + output_tokens * output_price + cache/read/write costs`
- Dedicated cost:
  - `gpu_hours * hourly_price + idle_capacity + storage + networking + engineering/ops time`
- Useful latency split:
  - `client + network + queue + tokenization + prefill + decode + postprocess`
- Percentiles matter because production users feel the tail, not the mean.

## Tradeoffs

- Shared APIs are faster for iteration and uncertain demand.
- Dedicated deployments make sense when scale, custom models, latency control, uptime, or data/compliance requirements justify fixed cost.
- Larger models may improve quality but increase latency, VRAM, serving complexity, and cost.
- Smaller models plus fine-tuning can beat larger general models for constrained domains.

## Production Implications

- Define evals before changing model precision, model size, prompts, or serving engine.
- Benchmark with realistic prompt lengths, output lengths, sampling parameters, and burst patterns.
- Treat P95/P99 as first-class requirements for user-facing systems.
- Separate user-perceived TPS from fleet throughput; both are called "TPS" in casual conversation, but they answer different questions.

## Things To Revisit

- Build a product brief for one target application.
- Create a small eval set with obvious cases, hard cases, and expected failure modes.
- Keep a cost spreadsheet that compares API and dedicated serving over weekly traffic.
