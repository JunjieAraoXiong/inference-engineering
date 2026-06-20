# Notes: Chapter 7: Production

## One-Sentence Thesis

Production inference is a control system around latency, capacity, reliability, cost, deployment safety, observability, and client experience.

## Core Ideas

- A fast model server is not enough; production needs reproducible containers, autoscaling, routing, deployment discipline, observability, cost modeling, and client integration.
- Containers must pin dependencies and match GPU/CUDA/engine compatibility.
- Autoscaling must understand traffic, queueing, cold starts, batch size, and concurrency.
- Routing can depend on region, load, sequence length, KV cache locality, LoRA placement, and priority.
- Multi-cloud and multi-region systems solve capacity and reliability but add operational complexity.
- Client protocol choices affect user-visible latency.

## Mechanisms

- Container release:
  - choose base image,
  - pin dependencies,
  - manage model weights and compiled engines,
  - add health/readiness checks,
  - measure startup.
- Autoscaling:
  - choose signals,
  - set min/max replicas,
  - tune concurrency and batch size,
  - account for cold starts,
  - avoid oscillation.
- Deployment:
  - shadow traffic,
  - canary ramp,
  - monitor p95/p99, errors, queue depth, OOMs, and quality,
  - rollback on predefined thresholds.
- Observability:
  - correlate app, queue, engine, GPU, and client metrics.

## Formulas / Quantitative Models

- End-to-end latency:
  - `client + network + queue + tokenization + prefill + decode + postprocess`
- Dedicated serving cost:
  - `GPU-hours + idle capacity + storage + egress + testing + engineering time`
- Autoscaling target must match batch behavior:
  - underfilled batches waste throughput,
  - overfilled queues hurt tail latency.

## Tradeoffs

- Scale-to-zero saves money but hurts unpredictable low-latency products.
- Warm capacity improves reliability and latency but raises baseline cost.
- Active-active improves resilience but needs routing, data, and capacity discipline.
- Canarying too slowly delays delivery; canarying too fast increases blast radius.
- More observability costs time and storage but reduces debugging time and risk.

## Production Implications

- Benchmark traffic should look like production traffic, including long prompts, burstiness, and cache misses.
- GPU utilization alone is a weak autoscaling signal; include queue depth and latency.
- Rollouts should be autoscaler-aware, or autoscaler lag can masquerade as model regression.
- Cost models must include idle capacity and tail output lengths.
- Measure client overhead; server-only metrics can hide handshake, streaming, and network latency.

## Things To Revisit

- Write a production runbook for one target app.
- Build an autoscaling simulator.
- Build a cost estimator from request logs.
- Compare HTTP streaming, WebSocket, and gRPC for a specific workload.
- Design rollback criteria for model, engine, and prompt changes.
