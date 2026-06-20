# Figures: Chapter 4: Software

Use this file to turn each diagram into your own explanation. Rendered page images live in `../../artifacts/book/figure-pages/` after `make extract`.

- [ ] PDF page 99: Figure 4.1: Example CUDA kernel doubles each value in an array. Ordinarily, on a CPU, this function would run in linear time, with each ele- ment in the array being doubled sequentially. But on a GPU, thousands of elements can be processed simultaneously, making this function much more efficient.
- [ ] PDF page 103: Figure 4.2: Kernel fusion reduces reads and writes between memory and compute within a GPU.
- [ ] PDF page 104: Figure 4.3: A basic neural network in PyTorch, adapted from the PyTorch documentation.
- [ ] PDF page 109: Figure 4.4: vLLM inference example on eight GPUs. vLLM is pip-installable and provides official Docker images with pre-bun- dled dependencies and support for various hardware architectures.
- [ ] PDF page 110: Figure 4.5: SGLang inference example on eight GPUs.
- [ ] PDF page 112: Figure 4.6: TensorRT-LLM inference example on eight GPUs. The best way to install TensorRT-LLM is by running it via one of NVIDIAs official Docker containers
- [ ] PDF page 116: Figure 4.7: A kernel profi ler shows you how long each operation within a kernel takes to execute, revealing bottlenecks.
