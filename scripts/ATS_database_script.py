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

NAME="Create ATS Database"
DESCRIPTION="Create database by parsing PDF to IMAGE and extract information using AI"

def execute():
    
    # constants
    FOLDER_NAME="inputs"
    URL="http://192.168.4.128:5000/v1/chat/completions" # http://192.168.4.128:5000/v1/chat/completions

    # create the standardised prompt
    # PROMPT = "Only do this: reply 'Hi!' in JSON format"
    PROMPT = """Role: You are a Data Extraction Specialist. Your task is to analyze a 'Change Implementation' document and extract specific fields into a structured JSON object for database ingestion.

INPUT:
The change implementation document 'typically' has this structure
- Overview
- Benefits/Justification
- Pre-Requisites and Applicability
- Implementation which consists of
- Technical Information: Ignore any details written here
- Proview Information
- Validation
- Verification
- versions (or versions.xml)

INSTRUCTIONS:
1. Analyze the document sections: Overview, Benefits/Justification, Pre-Requisites, Implementation (Proview, Validation, Verification), and Versions.
2. IGNORE any section labeled "Technical Information".
3. Output MUST be valid JSON only. Do not include markdown code blocks (```json), comments, or explanations.
4. If a specific field is missing in the document, use "N/A" for strings, null for objects, or [] for arrays.
5. For "Validations" (which are phrased as questions), rewrite them as declarative sentences.
6. For "Versions" (XML data), copy the content exactly as it appears, preserving all characters.
7. The most important data are pre-requisites, validations, inventory data and versions (XML data).

REQUIRED JSON STRUCTURE:
{
    "overview": "String: Short summary of the document.",
    "jira_ticket": "String: JIRA ID if found, otherwise 'N/A'.",
    "benefits_justification": [
        "String: Bullet point summary of benefits."
    ],
    "pre_requisites_applicability": {
        "manufacturer": "String: (e.g., NCR, DN Series, CINEO or WN)",
        "models": "String: List of models",
        "application": "String: Application context"
    },
    "proview_information": [
        {
            "overview": "String: Proview overview if exists, else 'N/A'",
            "job_names": [
                "String: List of job names"
            ],
            "validations": [
                "String: Validation criteria converted to full sentences"
            ],
            "verifications": [
                {
                    "header": "String: head (or subtitle) of the section",
                    "information": "String: Summary of key details (registries, file checks)",
                    "inventory_data": [
                        "String: Key-value pairs like 'key = value'"
                    ],
                    "versions": [
                        "String: Raw XML version data (do not summarize)"
                    ]
                }
            ]
        }
    ],
    "other_information": [
        "String: Any other key details not captured above"
    ]
}

IMPORTANT: Ensure the output is strictly parseable JSON."""

    # iterate each file in the folder
    output_json = {}
    for filename in os.listdir(os.path.join(os.pardir, FOLDER_NAME)):
        
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
            "stream": False,
            "return_progress": False,
            "reasoning_format": "auto",
            "temperature": 1.0,
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
            "presence_penalty": 1.5,
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
        
        print()
        print(f"Processing: {filename}")
        
        # get the input file
        # filename = "Change_Implemetation_RejectRecycleOFF.pdf"
        input_file = os.path.join(os.pardir, "inputs", filename)

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
            
        print("\tConverted PDF to Images successfully")
            
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
            stream=False
        )

        # stream the response
        if response.status_code == 200:
            
            # get response in JSON format
            data = response.json()

            # get the reasoning content/thinking process
            # print("Reasoning Content")
            # print(data['choices'][0]['message']['reasoning_content'])
            
            # get the actual content
            # print("---")
            # print("Content")
            content = data['choices'][0]['message']['content']
            try:
                json_content = json.loads(content)
                # print(json_content)
                output_json[filename] = json_content # add to overall json output
                
                # write to the file
                with open(os.path.join(os.pardir, "outputs", "output.json"), "w") as fp:
                    json.dump(output_json, fp)
                print("\tWrite to file successful")
            
            except json.decoder.JSONDecodeError as e:
                print("\tFailed to parse content to JSON format")
                
                # write as a text string
                with open(os.path.join(os.pardir, "outputs", f"{filename}.txt"), "w") as f:
                    f.write(content)
            
            finally:
                # print("Completed!")
                response.close()
            