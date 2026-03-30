from time import sleep
from src.logger import Logger

NAME="Keep Alive Script"
DESCRIPTION="test 1"

def execute(index: int):
    
    logger = Logger()
    
    # sending keep alive
    while True:
        logger.log("I'm alive.")
        sleep(2)
