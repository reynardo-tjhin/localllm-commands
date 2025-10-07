# Performance

## Commands

### Command 1

- Offloading all expert layers to CPU
- Context size of 65536
- Speed/Performance:

```none
prompt eval time =   99729.10 ms /  3176 tokens (   31.40 ms per token,    31.85 tokens per second)
eval time =  674500.35 ms /  2865 tokens (  235.43 ms per token,     4.25 tokens per second)
total time =  774229.46 ms /  6041 tokens
```

- Command:

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