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
./llama-bench --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf
              --n-gpu-layers 16
```

| model                          |       size |     params | backend    | ngl |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | --------------: | -------------------: |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  16 |           pp512 |        119.72 ± 0.63 |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB |   110.47 B | CUDA       |  16 |           tg128 |          8.59 ± 0.01 |
