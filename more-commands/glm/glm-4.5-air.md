# Details

## Current best command

- Fits both GPUs
- CUDA0: 11774MiB /  12288MiB
- CUDA1: 11618MiB /  12288MiB

```None
prompt eval time =   35550.72 ms /  3898 tokens (    9.12 ms per token,   109.65 tokens per second)
       eval time =   91104.23 ms /  1147 tokens (   79.43 ms per token,    12.59 tokens per second)
      total time =  126654.95 ms /  5045 tokens
```

```bash
./llama-server --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf
               --jinja
               --host 0.0.0.0
               --port 5000
               --n-gpu-layers 999  # offload all the layers to GPU
               --flash-attn on     # enable flash attention
               --override-tensor "blk.*.ffn_down_exps.weight=CPU"
               --override-tensor "blk.*.ffn_gate_exps.weight=CPU"
               --override-tensor "blk.(0|1|2|3|4|5|6|7|8).ffn_up_exps.weight=CPU"
               --override-tensor "blk.(9).ffn_up_exps.weight=CUDA1"
               --override-tensor "blk.(10|11|12|13|14).ffn_up_exps.weight=CUDA0"
               --override-tensor "blk.(15|16|17|18|19).ffn_up_exps.weight=CUDA1"
               --override-tensor "blk.(20|21|22|23|24).ffn_up_exps.weight=CUDA0"
               --override-tensor "blk.(25|26|27|28|29).ffn_up_exps.weight=CUDA1"
               --override-tensor "blk.(30|31|32|33|34).ffn_up_exps.weight=CUDA0"
               --override-tensor "blk.(35|36|37|38|39).ffn_up_exps.weight=CUDA1"
               --override-tensor "blk.(40|41|42).ffn_up_exps.weight=CUDA0"
               --override-tensor "blk.(43|44|45).ffn_up_exps.weight=CUDA1"
               --ctx-size 16384    # context size
               --temp 0.3
               --top-p 0.9
               --top-k 40
               --repeat-penalty 1.15
```

## Other Command 1

- Offloading all expert layers to CPU
- Context size of 65536
- Command:

```bash
./llama-server --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf
               --jinja
               --host 0.0.0.0
               --port 5000
               --n-gpu-layers 999   # offload all the layers to GPU
               --cpu-moe            # keep all Mixture of Experts (MoE) weights in the CPU
               --flash-attn on      # enable flash attention
               # offload the experts to CPU
               --override-tensor "\.ffn_.*_exps\.weight=CPU"
               --verbose-prompt
               --ctx-size 65536     # context size
               --reasoning-budget 0 # disable thinking
```

## Other Command 2

```bash
./llama-server --model ~/Models/GLM/GLM-4.5-Air-Q4_K_S-00001-of-00002.gguf
               --jinja
               --host 0.0.0.0
               --port 5000
               --n-gpu-layers 999   # offload all the layers to GPU
               --flash-attn on      # enable flash attention
               # offload the experts to CPU
               --override-tensor "\.ffn_.*_exps\.weight=CPU"
               --verbose-prompt
               --ctx-size 65536     # context size
               --cache-type-k q8_0  # kv cache data type for K
               --cache-type-v q8_0  # kv cache data type for V
```
