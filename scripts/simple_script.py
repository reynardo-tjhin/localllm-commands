import os

from time import sleep
from datetime import datetime
from redis import Redis
from uuid import uuid4

ID='c2881c0619f84a96811e52f53c6b9eb9'
NAME='Simple Script'
DESCRIPTION='Simple Script'

def execute(index: int):
    
    conn = Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        decode_responses=True,
        password=os.getenv('REDIS_PASSWORD'),
    )
    
    return None
