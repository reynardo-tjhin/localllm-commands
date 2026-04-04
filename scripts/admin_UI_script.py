import requests
import json

from playwright.sync_api import sync_playwright, Page

# generate the ID by calling `uuid.uuid4().hex`
ID='d38134b0435f4d2392c953f6160e9e64'
NAME='Generate Admin UI Script'
DESCRIPTION='Create Admin UI using different local AI models'

# run llama-swap in server
# ./llama-swap-linux-amd64 --config config.yaml --listen 0.0.0.0:8080

def execute():
    
    PROMPT="""Role: You are a Senior Front end Engineer
Library: Bootstrap, HTML & CSS and Jinja (with Flask as backend)
Task: Create an admin dashboard interface for your Flask-based movie service and user service with the below specifications. You DO NOT need to implement the backend! Just the Frontend!
Current movie database structure:
-- for movies
CREATE TABLE "movie" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	"imdb_rating"	REAL,
	"rotten_tomatoes_rating"	INTEGER,
	"metacritic_rating"	INTEGER,
	"release_date"	TEXT NOT NULL,
	"media_location"	TEXT NOT NULL UNIQUE,
	"poster_location"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
-- genre table for movies
CREATE TABLE "genre" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT NOT NULL,
	PRIMARY KEY("id")
);
-- relationship table between movie and genre
CREATE TABLE "movie_genre" (
	"movie_id"	TEXT NOT NULL,
	"genre_id"	TEXT NOT NULL,
	PRIMARY KEY("movie_id","genre_id"),
	FOREIGN KEY("genre_id") REFERENCES "genre" ON DELETE CASCADE,
	FOREIGN KEY("movie_id") REFERENCES "movie" ON DELETE CASCADE
);
-- for users
CREATE TABLE "user" (
	"id"	TEXT NOT NULL UNIQUE, -- str(uuid.uuid4())
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"is_admin"	TEXT NOT NULL, -- True/False
	PRIMARY KEY("id")
);
Backend Integration:
- The route to movies management: {{ url_for('admin.movies') }}
- The route to user management: {{ url_for('admin.user') }} (not done)
- More management will be made, but not in the current version
Dashboard Structure:
- Header with navigation menu and user profile
- Sidebar navigation with main menu items for:
  - Movie management
  - User management
  - Settings
- Main content area with grid system for dashboard components
  - Dashboard Components: (for the components, you don't have to worry backend as I am an expert!)
    - Key metrics cards showing movie statistics (total movies, active users, ratings average)
    - Charts and graphs for data visualization (genre distribution, user activity trends, movie popularity)
    - Not really sure what to add here (just be creative!)
Functionality:
- Responsive design that works on desktop and mobile devices
- Dark/light theme toggle option (based on your existing Flask templates)
Visual Design:
- Clean, professional aesthetic with appropriate spacing
- Consistent color scheme matching your choice of theme
- Typography hierarchy for readability
- Icons for visual cues (based on your existing Flask templates)
- appropriate use of white space and borders"""
    

    # models
    NO_OF_MODELS=6
    models = [
        "glm4.5-air",
        "gpt-oss-120b-f16",
        "hunyuan-a13b-instruct",
        "ling-flash-2.0",
        "qwen3-coder-30b-a3b",
        "ring-flash-2.0",
    ]

    def get_model_status(page: Page, model_id: int) -> str:
        """
        Get the status of the model
        """
        # get the status using the css selector
        model_status_css_selector = f"tr.hover\\:bg-secondary-hover:nth-child({model_id}) > td:nth-child(3) > span:nth-child(1)"
        page.wait_for_selector(model_status_css_selector, state="visible")
        model_status = page.locator(model_status_css_selector).inner_text()

        return model_status

    def get_model_name(page: Page, model_id: int) -> str:
        """
        Get the name of the model
        """

        # get the status using the css selector
        model_name_css_selector = f"tr.hover\\:bg-secondary-hover:nth-child({model_id}) > td:nth-child(1) > a:nth-child(1)"
        page.wait_for_selector(model_name_css_selector, state="visible")
        model_name = page.locator(model_name_css_selector).inner_text()

        return model_name


    def load_unload_model(page: Page, model_id: int, action: str = ['load', 'unload']):
        """
        Load or unload a model based on the model_id and the action given
        """
        print(f"INFO - {action} the model")
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
        Send a prompt to the link provided.
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
            # write to file
            with open(f"./outputs/{filename}", "w", encoding="utf-16") as f:
                f.write(data['choices'][0]['message']['content'])
                print("INFO - write file successful")
        else:
            print("ERROR - request failed")
            print(f"ERROR - Reponse status code: {response.status_code}")
            print(f"ERROR - Response text: {response.text}")



    # get the prompt from a file
    prompt = PROMPT
    print(f"INFO - prompt: {prompt}")

    # run playwright
    with sync_playwright() as p:

        print("INFO - launching a new chromium browser")
        browser = p.chromium.launch(headless=True)

        print("INFO - launching a new page")
        page = browser.new_page()

        # go to the page
        print("INFO - go to the link 'http://192.168.4.128:8080/ui/models'")
        page.goto("http://192.168.4.128:8080/ui/models")

        for index in range(1, NO_OF_MODELS+1):
            # load the first model
            print(F"INFO - loading the model no {index}")
            load_unload_model(page, index, action='load')
            
            # send prompt
            model_name = get_model_name(page, model_id=index)
            link = "http://192.168.4.128:8080/upstream/"+model_name+"/v1/chat/completions"
            
            print(f"INFO - model name: {model_name}")
            send_single_prompt(prompt, link, f"{model_name}.txt")
            
            # unload model
            load_unload_model(page, index, action='unload')

        browser.close()
