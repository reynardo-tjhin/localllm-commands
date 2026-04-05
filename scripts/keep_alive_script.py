from time import sleep
from src.classes import Logger

ID='0012773401804e1aa1dbd57077b51582'
NAME='Keep Alive Script'
DESCRIPTION='Sending Keep Alive events'

def execute():
    
    logger = Logger(ID)
    
    # sending keep alive
    while True:
        logger.log("I'm alive.")
        sleep(2)
