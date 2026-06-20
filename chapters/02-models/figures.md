# Figures: Chapter 2: Models

Use this file to turn each diagram into your own explanation. Rendered page images live in `../../artifacts/book/figure-pages/` after `make extract`.

- [ ] PDF page 45: Figure 2.1: Multi-layer neural networks have one input layer, many hidden layers, and one output layer.
- [ ] PDF page 46: Figure 2.2: In a matmul, the output vector y is the product of an input vector x and a weights matrix W plus a bias vector b.
- [ ] PDF page 47: Figure 2.3: Two matmul equations representing separate layers collapse due to composition of linearity.
- [ ] PDF page 48: Figure 2.4: Activation functions like ReLU are used to break linearity in multi-layer neural networks.
- [ ] PDF page 48: Figure 2.5: Subword tokenization uses one token per common word and punctuation mark, but it splits less common words into multiple tokens.
- [ ] PDF page 50: Figure 2.6: A decode pass generates a logit for each token in the models vocabulary, then normalizes logits to percentages.
- [ ] PDF page 53: Figure 2.7: Transformer block diagram, adapted from Attention Is All You Need (Vaswani et al., 2017).
- [ ] PDF page 54: Figure 2.8: The attention equation, adapted from FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Dao et al., 2022).
- [ ] PDF page 56: Figure 2.9: Mixture of Experts architecture includes both sharding and replicating to take advantage of multi-GPU inference.
- [ ] PDF page 58: Figure 2.10: Diffusion-based models iteratively generate an image from noise, generally over 30 to 50 steps.
- [ ] PDF page 59: Figure 2.11: SDXL architecture pipeline, adapted from SDXL: Improving Latent Diffusion Models for High-Resolution Image Synthesis (Podell et al., 2023).
- [ ] PDF page 64: Figure 2.12: The equation for arithmetic intensity. Where ops:byte was measured on a per-second scale, arithmetic intensity is measured across the execution of a single function or algorithm.
- [ ] PDF page 65: Figure 2.13: A roofl ine chart shows the switch from memory to compute bottleneck based on arithmetic intensity.
- [ ] PDF page 66: Figure 2.14: Standard attention implementation, adapted from FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness (Dao et al., 2022).
- [ ] PDF page 67: Figure 2.15: Memory movement (reads and writes) and compute work for the attention implementation in Figure 2.14.
- [ ] PDF page 67: Figure 2.16: The total memory movement for a kernel is the sum of all reads and writes across the three steps.
- [ ] PDF page 68: Figure 2.17: The total compute for the kernel is the sum of operations across the three steps.
- [ ] PDF page 68: Figure 2.18: The arithmetic intensity of a kernel is the total work (number of compute operations) divided by the memory movement For this example, the arithmetic intensity of 62 is much lower than the H100 GPUs ops:byte ratio of 295. The exact numbers vary by model, sequence length, and hardware, but this example illustrates the general
