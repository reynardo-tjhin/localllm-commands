import os

from time import sleep
from datetime import datetime
from redis import Redis

NAME="Simple Script"
DESCRIPTION="Simple Script"

def execute(index: int):
    
    conn = Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        decode_responses=True,
        password=os.getenv('REDIS_PASSWORD'),
    )
    
    return None
