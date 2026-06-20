# Figures: Chapter 7: Production

Use this file to turn each diagram into your own explanation. Rendered page images live in `../../artifacts/book/figure-pages/` after `make extract`.

- [ ] PDF page 183: Figure 7.1: Docker containers are composed of layers, from a base image up to an ephemeral, writable top layer.
- [ ] PDF page 184: Figure 7.2: Requirements should be pinned to exact versions to prevent future changes from breaking inference containers.
- [ ] PDF page 186: Figure 7.3: Without autoscaling, inference systems waste resources during traffic lulls and miss SLAs during traffic spikes.
- [ ] PDF page 186: Figure 7.4: A strong autoscaling system for inference matches resources to demand. Autoscaling systems use Kubernetes, an open-source container orches- tration system, along with a cluster-level system for provisioning and deal- locating compute. Kubernetes can run one or more replicas of a model container, each on its own instance. An instance includes the GPUs and
- [ ] PDF page 187: Figure 7.5: Kubernetes clusters have a single control plane that orchestrates multiple workers.
- [ ] PDF page 189: Figure 7.6: Static batching sets a fi xed batch size and waits for the batch to fi ll before beginning inference, leading to long wait times for early requests.
- [ ] PDF page 189: Figure 7.7: Dynamic batching adds a cutoff time after which a batch is run whether or not it is full.
- [ ] PDF page 190: Figure 7.8: Continuous batching operates at the token level, switching in new requests as old requests fi nish.
- [ ] PDF page 191: Figure 7.9: Each step in the cold start process adds to the overall timeline. Unless you have a pool of warm nodes that youre fl exing between mod- els, GPU procurement speed is mostly a function of your cloud provider.
- [ ] PDF page 195: Figure 7.10: Independent component scaling gives each model access to appropriate resources and individual scaling.
- [ ] PDF page 196: Figure 7.11: A multi-cloud approach extends the idea of control and workload planes to a multi-cluster, multi-region system.
- [ ] PDF page 199: Figure 7.12: Root cause of failures when training Llama 3, adapted from The Llama 3 Herd of Models (Grattafi ori et al., 2024).
- [ ] PDF page 202: Figure 7.13: Iteratively shifting traffic over to the new deployment prevents multiple issues during inference service updates.
- [ ] PDF page 204: Figure 7.14: An equation for estimating the total cost of using per-token APIs in a product.
- [ ] PDF page 204: Figure 7.15: An equation for estimating the total cost of using dedicated deployments in a product.
- [ ] PDF page 206: Figure 7.16: On-server inference time is just a fraction of the end-to-end latency for a given request.
- [ ] PDF page 208: Figure 7.17: One-time HTTP requests and responses are a good fi t for use cases like text chat, but not for continuous streaming.
- [ ] PDF page 208: Figure 7.18: WebSockets establish a continuous connection for unstructured data like audio streams.
- [ ] PDF page 209: Figure 7.19: gRPC establishes a continuous connection for well-defi ned service-to- service communication.
