import requests

from bs4 import BeautifulSoup
from src.classes import Logger

ID='c2881c0619f84a96811e52f53c6b9eb9'
NAME='Simple Script'
DESCRIPTION='Simple Script that scrapes the quotes website'

def execute():
        
    logger = Logger(ID)

    for page_no in range(1, 11):
        
        logger.log(f"Page {page_no}: Sending a GET request")
        r = requests.get(
            url=f"https://quotes.toscrape.com/page/{page_no}/",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
            }
        )
        response_text = r.text
        logger.log(f"Page {page_no}: GET request completed")
        
        logger.log(f"Page {page_no}: Finding all the quotes")
        bs = BeautifulSoup(response_text, features="html.parser")
        for span in bs.find_all("span", class_="text"):
            # print(span.text[1:-1])
            logger.log(f"Page {page_no}: {span.text[1:-1]}")
            
        logger.log(f"Page {page_no}: Completed")
    
    return None

if (__name__ == "__main__"):
    execute()