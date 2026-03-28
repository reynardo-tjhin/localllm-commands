import os

from time import sleep
from datetime import datetime
from redis import Redis

def execute(index: int):
    
    conn = Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        decode_responses=True,
        password=os.getenv('REDIS_PASSWORD'),
    )
    
    # sending keep alive
    while True:
        # output_queue.put(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ",I'm alive.")
        log = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ",I'm alive."
        conn.rpush(str(index), log)
        sleep(2)
