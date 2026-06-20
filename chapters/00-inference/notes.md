# Notes: Chapter 0: Inference

## One-Sentence Thesis

Inference engineering is the discipline of serving generative models in production by coordinating runtime optimization, infrastructure scaling, and developer-facing tooling.

## Core Ideas

- Training creates model weights; inference turns those weights into a reliable product capability.
- A complete inference system has three layers:
  - Runtime: make one model instance fast and efficient.
  - Infrastructure: scale many instances across clusters, regions, and clouds.
  - Tooling: give engineers the right abstractions to operate the system.
- Runtime techniques include batching, caching, quantization, speculation, parallelism, and disaggregation.
- Infrastructure problems change with scale: one replica, autoscaled replicas, multi-region capacity, then global compute pooling.
- Tooling should balance control and productivity. Too little abstraction slows teams down; too much hides the controls needed for production.

## Mechanisms

- Runtime work improves single-replica performance: kernels, engines, memory layout, batching, and model-specific tricks.
- Infrastructure work handles demand and reliability: autoscaling, routing, capacity, failover, and multi-cloud placement.
- Tooling translates low-level systems into usable workflows: deploy APIs, dashboards, configs, rollbacks, and observability.

## Quantitative Models

- Optimize at the layer that owns the bottleneck:
  - slow token generation: runtime,
  - traffic spikes: autoscaling/routing,
  - regional outage or GPU shortage: infrastructure/capacity,
  - developer mistakes or slow iteration: tooling.
- User-perceived latency is not just model time. It includes client, network, queueing, tokenization, prefill, decode, and postprocessing.

## Tradeoffs

- More abstraction improves speed of development but can hide performance controls.
- More control enables optimization but increases operational burden.
- Runtime wins can be erased by bad routing, cold starts, or queueing.
- Infrastructure reliability often costs money through warm capacity and redundancy.

## Production Implications

- Do not benchmark a model server in isolation and assume production will match it.
- Always ask which layer is responsible for the observed pain: model, engine, GPU, scheduler, network, client, or platform.
- The end goal is not maximum tokens/sec; it is the right quality at the right latency and cost with acceptable reliability.

## Things To Revisit

- Draw the runtime/infrastructure/tooling stack for every system you study.
- For each optimization in later chapters, label which layer it belongs to and what metric it should move.
