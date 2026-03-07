#############################################
#  README.md
#
#  Script for ATS
#  
#  Situation: ATS uses change implementation documents before releasing to test team
#             for further testing/before releasing to PROD environment.
#             There are many change implementation documents that have important details.
#             It is a painful process to open them in MS word and read through the
#             document.
#  Solution: Therefore, this script will read through the folder with all the 
#            documents. Send them to an AI with OCR and image capabilities, and ask
#            the AI to create a JSON output. Then, we will create a simple web interface
#            with the database.
#############################################
import requests
import os
import base64
import json

from io import BytesIO
from pdf2image import convert_from_path

# constants
FOLDER_NAME="TODO"
URL="http://192.168.4.128:5000/v1/chat/completions" # http://192.168.4.128:5000/v1/chat/completions

# create the standardised prompt
# PROMPT = "Do nothing and only respond me with a 'Hi!'"
PROMPT = """I need you to list
- the summary description
- the deploy and copy jobs (they have *_D_* as the deploy job and *_C_* as the copy job)
- reboot required: yes/no
- pre-requisites: what's the application pre-requisites?
- versions.xml

Answer without any explanation!
And answer ONLY in JSON format!"""

# construct the payload
payload = {
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": PROMPT,
                },
            ]
        }
    ],
    "stream": True,
    "return_progress": True,
    "reasoning_format": "auto",
    "temperature": 0.6,
    "max_tokens": -1,
    "dynatemp_range": 0,
    "dynatemp_exponent": 1,
    "top_k": 20,
    "top_p": 0.95,
    "min_p": 0,
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
        "penalties",
        "dry",
        "top_n_sigma",
        "top_k",
        "typ_p",
        "top_p",
        "min_p",
        "xtc",
        "temperature"
    ],
    "timings_per_token": True,
}

# get the input file
input_file = os.path.join(os.curdir, "inputs", "Change_Implemetation_RejectRecycleOFF.pdf")

# convert PDF to images
images = convert_from_path(input_file, dpi=300, fmt="png")
for image in images:
    
    # convert to Base64
    buffered = BytesIO()
    image.save(buffered, format='PNG')
    base64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
    # construct the image payload
    img_payload = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/png;base64,{base64_img}"
        }
    }
    payload.get("messages")[0].get("content").append(img_payload)
    
# DEBUG: dump the payload
# with open(os.path.join(os.curdir, "outputs", "test.json"), "w") as f:
#     json.dump(payload, f, indent=2)
    
    

# create the request
response = requests.post(
    url=URL,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
    },
    json=payload,
    stream=True
)

# stream the response
if response.status_code == 200:
    for line in response.iter_lines():
        if line:
            try:
                decoded_line = line.decode('utf-8')
                decoded_line = json.loads(decoded_line[6:])
                # print(decoded_line['choices'][0])
                
                if (decoded_line['choices'][0]['delta'].get('reasoning_content')):
                    print(decoded_line['choices'][0]['delta']['reasoning_content'], end="", flush=True)
                    
                if (decoded_line['choices'][0]['delta'].get('content')):
                    print(decoded_line['choices'][0]['delta']['content'], end="", flush=True)

            except json.decoder.JSONDecodeError as e:
                # import traceback
                # traceback.print_exc()
                # print(e)
                continue
                
            finally:
                continue

response.close()