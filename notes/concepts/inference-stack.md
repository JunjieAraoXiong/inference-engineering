# Inference Stack

## My Definition

The inference stack is the set of systems that turn model weights into a reliable product feature. It has three layers: runtime, infrastructure, and tooling.

## Why It Matters

A model can be fast in a notebook and still fail in production because queueing, cold starts, routing, autoscaling, or client overhead dominate the user experience.

## Layers

- Runtime: kernels, model execution, batching, KV cache, precision, serving engine.
- Infrastructure: replicas, clusters, routing, autoscaling, regions, capacity, reliability.
- Tooling: deployment workflow, metrics, logs, rollbacks, configs, developer interface.

## Signals

- Runtime: TTFT, ITL, tokens/sec/GPU, VRAM, GPU utilization.
- Infrastructure: queue depth, cold-start time, p95/p99, regional failover, replica availability.
- Tooling: deploy frequency, rollback speed, incident debugging time, config errors.

## Failure Mode

Optimizing the runtime while ignoring queueing or cold starts can make benchmark numbers look better while users still see slow responses.

## Production Implication

Every performance investigation should start by locating the responsible layer before choosing an optimization.
