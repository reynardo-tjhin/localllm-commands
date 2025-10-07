# localllm-commands

Learning about running local LLMs

## Build

Here is my build specs

- CPU: AMD Ryzen 9 7900 12-Core Processor
- Memory: 2x 48GB 6000MHz DDR5
- Graphics Cards: 2x GeForce RTX 3060

## Models and Its Commands

### GLM 4.5 Air

- Quantization Type: Q4_K_S
- Backend: llama.cpp
- Commands used:

```bash
./llama-server --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf
               --jinja
               --host 0.0.0.0
               --port 5000
               -n-gpu-layers 999    # offload all the layers to GPU
               --flash-attn on      # enable flash attention
               # offload the experts to CPU
               --override-tensor "\.ffn_.*_exps\.weight=CPU"
               --verbose-prompt
               --ctx-size 65536     # context size
               --cache-type-k q8_0  # KV cache quantization type
```
