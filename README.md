# localllm-commands

Learning about running local LLMs

## Build

Here is my build specs

- CPU: AMD Ryzen 9 7900 12-Core Processor
- Memory: 2x 48GB 6000MHz DDR5 (via BIOS set to 5600 MHz)
- Graphics Cards: 2x GeForce RTX 3060

## Benchmarks (llama.cpp's llama-bench)

```bash
# SmolLM2-1.7B-Instruct-F16 (Dense model)
./llama-bench --model ~/Models/HuggingFaceTB/SmolLM2-1.7B-Instruct-F16.gguf

# GPT-OSS-20B-F16
./llama-bench --model ~/Downloads/gpt-oss-20b-F16.gguf

# Qwen3-32B-Q4_K_S (Dense model)
./llama-bench --model ~/Models/Qwen/Qwen3-32B-Q4_K_S.gguf \
              --n-gpu-layers 99

# Qwen3-30B-A3B Instruct BF16
./llama-bench --model ~/Models/Qwen/Qwen3-Coder-30B-A3B-Instruct-BF16-00001-of-00002.gguf \
              -ncmoe 99 \
              --n-gpu-layers 99 \
              --flash-attn 1

# Ling-Flash-2.0-Q4_K_M or Ring-flash-2.0-Q4_K_M
./llama-bench --model ~/Models/InclusionAI/Ling-flash-2.0-Q4_K_M.gguf \
              --n-gpu-layers 99 \
              -ncmoe 99 \
              --flash-attn 1

# GPT-OSS-120B-F16
./llama-bench --model ~/Models/OpenAI/gpt-oss-120b-F16.gguf \
              --n-gpu-layers 99 \
              -ncmoe 99 \
              --flash-attn 1

# Hunyuan-A13B-Instruct-Q6_K
./llama-bench --model ~/Models/Tencent/tencent_Hunyuan-A13B-Instruct-Q6_K-00001-of-00002.gguf \
              --n-gpu-layers 99 \
              -ncmoe 99 \
              --flash-attn 1

# GLM-4.5-Air-Q4_K_S
./llama-bench --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf \
              -ncmoe 99 \
              --n-gpu-layers 99 \
              --flash-attn 1
```

| model                          |        size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ----------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 1.7B F16                 |   3.19 GiB  |     1.71 B | CUDA       |  99 |    |           pp512 |      5798.75 ± 10.98 |
| gpt-oss 20B F16                |  12.83 GiB  |    20.91 B | CUDA       |  99 |    |           pp512 |      1922.67 ± 15.30 |
| qwen3 32B Q4_K - Small         |  17.48 GiB  |    32.76 B | CUDA       |  99 |    |           pp512 |        462.98 ± 0.28 |
| qwen3moe 30B.A3B BF16          |  56.89 GiB  |    30.53 B | CUDA       |  99 |  1 |           pp512 |        130.28 ± 1.13 |
| bailingmoe2 100B.A6B Q4_K - Medium |  58.13 GiB |   102.89 B | CUDA    |  99 |  1 |           pp512 |        122.81 ± 1.42 |
| gpt-oss 120B F16               |  60.87 GiB  |   116.83 B | CUDA       |  99 |  1 |           pp512 |        169.31 ± 1.12 |
| hunyuan-moe A13B Q6_K          |  61.75 GiB |    80.39 B | CUDA       |  99 |  1 |           pp512 |         92.76 ± 0.25 |
| glm4moe 106B.A12B Q4_K - Small |  62.27 GiB  |   110.47 B | CUDA       |  99 |  1 |           pp512 |         98.54 ± 0.58 |

| model                          |        size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ----------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| llama 1.7B F16                 |    3.19 GiB |     1.71 B | CUDA       |  99 |    |           tg128 |         89.41 ± 0.03 |
| gpt-oss 20B F16                |   12.83 GiB |    20.91 B | CUDA       |  99 |    |           tg128 |         74.21 ± 0.05 |
| qwen3 32B Q4_K - Small         |   17.48 GiB |    32.76 B | CUDA       |  99 |    |           tg128 |         16.90 ± 0.01 |
| qwen3moe 30B.A3B BF16          |   56.89 GiB |    30.53 B | CUDA       |  99 |  1 |           tg128 |         13.12 ± 0.02 |
| bailingmoe2 100B.A6B Q4_K - Medium |  58.13 GiB |   102.89 B | CUDA    |  99 |  1 |           tg128 |         22.51 ± 0.15 |
| gpt-oss 120B F16               |   60.87 GiB |   116.83 B | CUDA       |  99 |  1 |           tg128 |         18.46 ± 0.06 |
| hunyuan-moe A13B Q6_K          |  61.75 GiB |    80.39 B | CUDA       |  99 |  1 |           tg128 |          6.73 ± 0.01 |
| glm4moe 106B.A12B Q4_K - Small |   62.27 GiB |   110.47 B | CUDA       |  99 |  1 |           tg128 |         10.83 ± 0.07 |

## Others

Used llama.cpp as backend and llama-swap as the interface to swap between models. Running main.py will load all models available in llama-swap and send the prompt to each model. This will give an output file on outputs directory. Currently testing on UI generation using Bootstrap as starter.
