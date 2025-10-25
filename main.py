import requests
import json

from playwright.sync_api import sync_playwright, Page

# run llama-swap in server
# ./llama-swap-linux-amd64 --config config.yaml --listen 0.0.0.0:8080

# models
NO_OF_MODELS=3
models = [
    "glm4.5-air",
    "gpt-oss-120b-f16",
    "qwen3-coder-30b-a3b",
]

def get_model_status(page: Page, model_id: int) -> str:

    # get the status using the css selector
    model_status_css_selector = f"tr.hover\\:bg-secondary-hover:nth-child({model_id}) > td:nth-child(3) > span:nth-child(1)"
    page.wait_for_selector(model_status_css_selector, state="visible")
    model_status = page.locator(model_status_css_selector).inner_text()

    return model_status

def get_model_name(page: Page, model_id: int) -> str:

    # get the status using the css selector
    model_name_css_selector = f"tr.hover\\:bg-secondary-hover:nth-child({model_id}) > td:nth-child(1) > a:nth-child(1)"
    page.wait_for_selector(model_name_css_selector, state="visible")
    model_name = page.locator(model_name_css_selector).inner_text()

    return model_name


def load_unload_model(page: Page, model_id: int, action: str = ['load', 'unload']):
    print("INFO - load/Unload the model")
    model_load_unload_css_selector = f"tr.hover\\:bg-secondary-hover:nth-child({model_id}) > td:nth-child(2) > button:nth-child(1)"
    page.click(model_load_unload_css_selector)

    if (action == "load"):
        while (get_model_status(page, model_id) != "ready"):
            # do nothing
            pass
        print("INFO - model successfully loaded")

    elif (action == "unload"):
        while (get_model_status(page, model_id) != "stopped"):
            # do nothing
            pass
        print("INFO - model successfully unloaded")
    else:
        print("ERROR - action undefined")


def send_single_prompt(prompt: str, link: str, filename: str) -> None:
    """
    Send a prompt to the link provided
    Output the results to "outputs" folder
    """
    # build the payload request
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}"
            }
        ]
    }
    # send the request
    print("INFO - sending the request to the URL")
    response = requests.post(
        url=link,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
        },
        data=json.dumps(payload),
    )
    # write to desired file
    if response.status_code == 200:
        print("INFO - request successful; writing to outputs folder")
        data = response.json()
        file = open(f"./outputs/{filename}", "w")
        # file.write(str(data))
        
        print(type(data))
        print(data)

        file.close()
        print("INFO - write file successful")
    else:
        print("ERROR - request failed")
        print(f"ERROR - Reponse status code: {response.status_code}")
        print(f"ERROR - Response text: {response.text}")


def main():
    with sync_playwright() as p:

        print("INFO - launching a new chromium browser")
        browser = p.chromium.launch(headless=False)

        print("INFO - launching a new page")
        page = browser.new_page()

        # go to the page
        print("INFO - go to the link 'http://192.168.4.128:8080/ui/models'")
        page.goto("http://192.168.4.128:8080/ui/models")

        # load the first model
        print("INFO - loading the first model")
        load_unload_model(page, 1, action='load')
        
        # send prompt
        model_name = get_model_name(page, 1)
        link = "http://192.168.4.128:8080/upstream/"+model_name+"/v1/chat/completions"
        
        print(f"INFO - model name: {model_name}")
        send_single_prompt("Hi!", link, f"{model_name}.txt")
        
        # unload model
        load_unload_model(page, 1, action='unload')

        browser.close()

if __name__ == "__main__":
    main()
