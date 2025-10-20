# Details

## Current best command

- Fits both GPUs
- CUDA0: 11480MiB /  12288MiB
- CUDA1: 11570MiB /  12288MiB

```None
prompt eval time =   22092.13 ms /  3448 tokens (    6.41 ms per token,   156.07 tokens per second)
       eval time =  113740.97 ms /  2519 tokens (   45.15 ms per token,    22.15 tokens per second)
      total time =  135833.11 ms /  5967 tokens
```

```bash
./llama-server  --model ~/Models/OpenAI/gpt-oss-120b-F16.gguf \
                --jinja \
                --host 0.0.0.0 \
                --port 5000 \
                --n-gpu-layers 99 \
                --override-tensor "blk.*.ffn_down_exps.weight=CPU" \
                --override-tensor "blk.*.ffn_gate_exps.weight=CPU" \
                --override-tensor "blk.(0|1|2|3|4|5|6|7|8|9).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(10|11|12|13|14|15|16|17|18|19).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(20|21|22|23|24).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(25|26|27|28|29).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(30|31).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(32).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(33|34|35).ffn_up_exps.weight=CPU" \
                --ctx-size 16384 \
                --flash-attn on \
                --temp 0.1 \
                --top-p 0.9 \
                --top-k 0 \
                --repeat-penalty 1.05
```
