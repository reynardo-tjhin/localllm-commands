import redis
import os

from flask import Flask, g

def get_db() -> redis.Redis:
    if 'db' not in g:
        # g is a special object that is unique for each request
        # it is used to store data that might be accessed by multiple functions
        # during the request.
        # The connection is stored and reused insted of creating a new connection
        # if `get_db` is called a second time in the same request.
        g.db = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True,
            password=os.getenv('REDIS_PASSWORD'),
        )

    return g.db

def close_db(e=None) -> None:
    """
    `close_db` checks if a connection was created by checking if `g.db` was set.
    If the connection exists, it is closed.
    """
    db: redis.Redis = g.pop('db', None)
    
    if (db is not None):
        db.close()
        
def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)