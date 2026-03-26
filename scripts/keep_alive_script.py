from multiprocessing import Queue
from time import sleep
from datetime import datetime

def execute(output_queue: Queue):
    
    # sending keep alive
    while True:
        output_queue.put(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ",I'm alive.")
        sleep(2)
