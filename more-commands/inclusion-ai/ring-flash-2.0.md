# Details

## Current Best Command

- Fits both GPUs
- CUDA0: 11524MiB /  12288MiB
- CUDA1: 11196MiB /  12288MiB

```None
prompt eval time =    2441.22 ms /   161 tokens (   15.16 ms per token,    65.95 tokens per second)
       eval time =  349899.35 ms /  8853 tokens (   39.52 ms per token,    25.30 tokens per second)
      total time =  352340.57 ms /  9014 tokens
```

```bash
./llama-server  --model ~/Models/InclusionAI/Ling-flash-2.0-Q4_K_M.gguf \
                --jinja \
                --host 0.0.0.0 \
                --port 5000 \
                --n-gpu-layers 99 \
                --override-tensor "blk.*.ffn_down_exps.weight=CPU" \
                --override-tensor "blk.*.ffn_gate_exps.weight=CPU" \
                --override-tensor "blk.(0|1|2|3|4|5|6|7|8|9).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(10|11|12|13|14|15|16|17|18|19).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(20|21|22|23|24|25).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(26|27|28|29|30|31).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(32|33).ffn_up_exps.weight=CPU" \
                --ctx-size 16384 \
                --flash-attn on \
                --temp 0.1 \
                --top-p 0.9 \
                --top-k 0 \
                --repeat-penalty 1.05
```
