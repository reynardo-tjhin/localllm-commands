# Details

## Command 1

- Offloading all expert layers to CPU
- Context size of 65536
- Command:

```bash
./llama-server --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf
               --jinja
               --host 0.0.0.0
               --port 5000
               --n-gpu-layers 999    # offload all the layers to GPU
               --cpu-moe            # keep all Mixture of Experts (MoE) weights in the CPU
               --flash-attn on      # enable flash attention
               # offload the experts to CPU
               --override-tensor "\.ffn_.*_exps\.weight=CPU"
               --verbose-prompt
               --ctx-size 65536     # context size
               --reasoning-budget 0 # disable thinking
```

## Command 2

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
               --cache-type-k q8_0  # kv cache data type for K
               --cache-type-v q8_0  # kv cache data type for V
```
