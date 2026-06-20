# Production Inference

## My Definition

Production inference is operating model serving as a reliable, observable, cost-controlled user-facing system.

## Core Components

- Reproducible container.
- Pinned dependencies.
- Serving engine.
- Router and queue.
- Autoscaler.
- Health checks.
- Metrics and logs.
- Canary and rollback process.
- Cost model.
- Client protocol.

## Signals

- P95/P99 end-to-end latency.
- Queue depth.
- Error rate.
- Replica startup time.
- GPU utilization and VRAM.
- TTFT and ITL.
- Cost per successful request.

## Failure Mode

A canary with too few warm replicas can make autoscaler lag look like model regression.

## Production Implication

Every model change should include deploy safety, observability, rollback criteria, and cost impact.
