from time import sleep
from src.logger import Logger

NAME="Keep Alive Script"
DESCRIPTION="Sending Keep Alive events"

def execute(index: int):
    
    logger = Logger(str(index))
    
    # sending keep alive
    i = 0
    while i < 10:
        logger.log("I'm alive.")
        sleep(2)
        i += 1
