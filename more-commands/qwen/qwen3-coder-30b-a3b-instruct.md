# Details

To achieve optimal performance, we recommend the following settings:

1. Sampling Parameters: We suggest using temperature=0.7, top_p=0.8, top_k=20, repetition_penalty=1.05.
2. Adequate Output Length: We recommend using an output length of 65,536 tokens for most queries, which is adequate for instruct models.

## Command 1

```bash
./llama-server  --model ~/Models/Qwen/Qwen3-Coder-30B-A3B-Instruct-BF16-00001-of-00002.gguf \
                --jinja \
                --host 0.0.0.0 \
                --port 5000 \
                --n-gpu-layers 99 \
                --override-tensor "blk.*.ffn_down_exps.weight=CPU" \
                --override-tensor "blk.*.ffn_gate_exps.weight=CPU" \
                --ctx-size 16384 \
                --cache-type-k q8_0 \
                --cache-type-k q8_0 \
                --flash-attn on \
                --temp 0.7 \
                --top-p 0.8
                --top-k 20 \
                --repeat-penalty 1.05
```
