import requests
import json

# run llama-swap in server
# ./llama-swap-linux-amd64 --config config.yaml --listen 0.0.0.0:8080

# currently three models are supported
# GLM 4.5 Air            Q_4_K_S
# GPT OSS 120B           FP16
# Qwen3 Coder 30B A3B    BF16

# rough idea
URL="http://192.168.4.128:8080/upstream/gpt-oss-120b-f16/v1/chat/completions"

def main():
    
    # build the request payload
    payload = {
        "messages": [
            {
                "role": "user",
                "content": "Hi!"
            }
        ],
        "stream": False,
        "reasoning_format": "auto",
        "temperature": 0.8,
        "max_tokens": -1,
        "dynatemp_range": 0,
        "dynatemp_exponent": 1,
        "top_k": 40,
        "top_p": 0.95,
        "min_p": 0.05,
        "xtc_probability": 0,
        "xtc_threshold": 0.1,
        "typ_p": 1,
        "repeat_last_n": 64,
        "repeat_penalty": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "dry_multiplier": 0,
        "dry_base": 1.75,
        "dry_allowed_length": 2,
        "dry_penalty_last_n": -1,
        "samplers": [
            "top_k",
            "typ_p",
            "top_p",
            "min_p",
            "temperature"
        ],
        "timings_per_token": True
    }

    # send the request
    response = requests.post(
        url=URL,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
        },
        data=json.dumps(payload),
        timeout=30,
    )

    # show the result
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Reponse status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
