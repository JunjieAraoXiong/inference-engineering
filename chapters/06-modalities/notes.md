# Notes: Chapter 6: Modalities

## One-Sentence Thesis

Each modality changes the unit of inference, the bottleneck, the quality metric, and the serving pipeline, even when it reuses LLM-style infrastructure.

## Core Ideas

- VLMs add visual tokens and preprocessing to an LLM-like serving problem.
- Embeddings are throughput-oriented vector production systems with retrieval quality constraints.
- ASR combines audio preprocessing, chunking, streaming, transcription quality, and sometimes diarization.
- TTS must meet real-time audio constraints and often bottlenecks on audio decoding/vocoder stages.
- Image generation is dominated by denoising steps, attention/GEMM kernels, and quality-speed tradeoffs.
- Video generation is even heavier: temporal coherence, large latent spaces, attention cost, and low batchability.

## Mechanisms

- VLM pipeline:
  - preprocess media,
  - encode visual tokens,
  - run LLM prefill,
  - decode text,
  - optionally combine OCR/ASR side channels.
- Embedding pipeline:
  - chunk data,
  - batch/tokenize,
  - encode,
  - pool/normalize/truncate,
  - write to vector index,
  - retrieve and optionally rerank.
- Voice cascade:
  - VAD,
  - ASR,
  - LLM/RAG/tools,
  - TTS,
  - stream audio.
- Image pipeline:
  - encode prompt/reference/control inputs,
  - denoise latent,
  - decode image,
  - optionally refine/upscale/filter.

## Formulas / Quantitative Models

- ASR long-file performance often uses real-time factor:
  - `processing_time / audio_duration`
- TTS must beat real-time generation:
  - generated audio seconds per wall-clock second should exceed 1 for smooth streaming.
- Image/video cost often scales with:
  - `denoising_steps * denoiser_passes_per_step * resolution/latent_size`

## Tradeoffs

- VLM resolution improves perception but increases visual tokens and prefill cost.
- Embedding dimension improves expressiveness but increases storage, retrieval cost, and index memory.
- ASR chunking improves parallelism but can hurt context, punctuation, and speaker continuity.
- TTS streaming improves UX but complicates buffering and recovery.
- Fewer image denoising steps improve latency but can reduce quality unless trained/scheduled for few-step generation.
- Video generation often gives up batching and needs node-level optimization.

## Production Implications

- Pick metrics per modality, not one universal metric.
- Embedding systems need separate online and offline/backfill paths.
- Voice systems require stage-level tracing because the user feels the whole cascade.
- Image and video generation need quality review loops, not just latency charts.
- Multimodal pipelines should keep stages close together when latency matters.

## Things To Revisit

- Build a modality decision matrix for two target workloads.
- Run a VLM visual-token budget experiment.
- Build an embedding backfill vs online serving design.
- Build a voice cascade latency budget.
- Compare diffusion step count against quality.
