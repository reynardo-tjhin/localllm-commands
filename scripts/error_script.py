import traceback

from src.classes import Logger

ID='c3c5d945d8bd4a22b323c971090f7aaa'
NAME='Error Script'
DESCRIPTION='Script that goes to an error state'

def execute():
    logger = Logger(ID)
    
    try:
        a = [0, 1, 2, 3, 4, "five"]
        for i in a:
            i += 6
            
    except TypeError as e:
        logger.log("[ERROR]: " + traceback.format_exc())
        logger.log("[ERROR]: " + str(e))
        # print(traceback.format_exc())
        # print(e)
        
if (__name__ == "__main__"):
    execute()