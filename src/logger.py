import os

from dataclasses import dataclass
from redis import Redis
from datetime import datetime

@dataclass
class Logger:
    """Class to handle logging to redis database"""
    conn: Redis
    key: str
    
    def __init__(self, key: str):
        self.conn = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True,
            password=os.getenv('REDIS_PASSWORD'),
        )
        self.key = "script:" + key
        
    def log(self, message: str) -> None:
        """
        Log the message to redis database
        """
        message = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + message
        self.conn.rpush(self.key, message)