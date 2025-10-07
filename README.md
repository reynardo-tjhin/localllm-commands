# localllm-commands

Learning about running local LLMs

## Build

Here is my build specs

- CPU: AMD Ryzen 9 7900 12-Core Processor
- Memory: 2x 48GB 6000MHz DDR5
- Graphics Cards: 2x GeForce RTX 3060

## Benchmarks (llama.cpp's llama-bench)

```bash
./llama-bench --model ~/Models/HuggingFaceTB/SmolLM2-1.7B-Instruct-Q4_K_M.gguf
```

| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 1.7B Q4_K - Medium         | 1005.01 MiB |     1.71 B | CUDA       |  99 |           pp512 |     5491.76 ± 162.18 |
| llama 1.7B Q4_K - Medium         | 1005.01 MiB |     1.71 B | CUDA       |  99 |           tg128 |        218.94 ± 0.51 |

```bash
./llama-bench --model ~/Models/HuggingFaceTB/SmolLM2-1.7B-Instruct-F16.gguf
```

| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| llama 1.7B F16                   |   3.19 GiB |     1.71 B | CUDA       |  99 |           pp512 |      5798.75 ± 10.98 |
| llama 1.7B F16                   |   3.19 GiB |     1.71 B | CUDA       |  99 |           tg128 |         89.41 ± 0.03 |

```bash
./llama-bench --model ~/Downloads/gpt-oss-20b-F16.gguf
```

| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| gpt-oss 20B F16                |  12.83 GiB |    20.91 B | CUDA       |  99 |           pp512 |      1922.67 ± 15.30 |
| gpt-oss 20B F16                |  12.83 GiB |    20.91 B | CUDA       |  99 |           tg128 |         74.21 ± 0.05 |

```bash
# offloading the maximum number of layers possible within the total number of VRAM to GPU
# no tweaking, max no of layers can be offloaded to GPU = 16 layers
./llama-bench --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf \
              --n-gpu-layers 16
```

| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  16 |           pp512 |        119.72 ± 0.63 |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  16 |           tg128 |          8.59 ± 0.01 |

```bash
# offloading all the attention layers to GPU
# offloading all the expert layers to CPU
./llama-bench --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf \
              --n-gpu-layers 99 \
              --override-tensor "\.ffn_.*_exps\.weight=CPU"
```

| model                          |       size |     params | backend    | ngl | ot                    |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------------- | --------------: | -------------------: |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  99 | \.ffn_.*_exps\.weight=CPU |           pp512 |         96.41 ± 0.65 |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  99 | \.ffn_.*_exps\.weight=CPU |           tg128 |         10.75 ± 0.04 |

```bash
# enable flash attention
# offload all expert layers to CPU
./llama-bench --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf \
              -ncmoe 99 \
              --n-gpu-layers 99 \
              --flash-attn 1
```

| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  99 |  1 |           pp512 |         98.54 ± 0.58 |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  99 |  1 |           tg128 |         10.83 ± 0.07 |

```bash
./llama-bench --model ~/Models/OpenAI/gpt-oss-120b-F16.gguf \
              --n-gpu-layers 99 \
              -ncmoe 99 \
              --flash-attn 1
```

| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| gpt-oss 120B F16               |  60.87 GiB |   116.83 B | CUDA       |  99 |  1 |           pp512 |        169.31 ± 1.12 |
| gpt-oss 120B F16               |  60.87 GiB |   116.83 B | CUDA       |  99 |  1 |           tg128 |         18.46 ± 0.06 |

```bash
./llama-bench --model ~/Models/Qwen/Qwen3-32B-Q4_K_S.gguf \
              --n-gpu-layers 99
```

| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| qwen3 32B Q4_K - Small         |  17.48 GiB |    32.76 B | CUDA       |  99 |           pp512 |        462.98 ± 0.28 |
| qwen3 32B Q4_K - Small         |  17.48 GiB |    32.76 B | CUDA       |  99 |           tg128 |         16.90 ± 0.01 |
