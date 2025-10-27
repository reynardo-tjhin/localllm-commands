# Details

## Current Best Command

- Fits both GPUs
- CUDA0: 11444MiB /  12288MiB
- CUDA1: 11092MiB /  12288MiB

```None
prompt eval time =    4119.96 ms /   196 tokens (   21.02 ms per token,    47.57 tokens per second)
       eval time =  208331.87 ms /  1691 tokens (  123.20 ms per token,     8.12 tokens per second)
      total time =  212451.83 ms /  1887 tokens
```

```bash
./llama-server  --model ~/Models/Tencent/tencent_Hunyuan-A13B-Instruct-Q6_K-00001-of-00002.gguf \
                --jinja \
                --host 0.0.0.0 \
                --port 5000 \
                --n-gpu-layers 99 \
                --override-tensor "blk.*.ffn_down_exps.weight=CPU" \
                --override-tensor "blk.*.ffn_gate_exps.weight=CPU" \
                --override-tensor "blk.(0|1|2|3|4|5|6|7|8|9).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(10|11|12|13|14|15|16|17|18|19).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(20|21).ffn_up_exps.weight=CUDA0" \
                --override-tensor "blk.(22|23|24).ffn_up_exps.weight=CUDA1" \
                --override-tensor "blk.(25|26|27|28|29|30|31|32|33).ffn_up_exps.weight=CPU" \
                --ctx-size 16384 \
                --flash-attn on \
                --temp 0.1 \
                --top-p 0.9 \
                --top-k 0 \
                --repeat-penalty 1.05
```
