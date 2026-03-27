import redis
import os

from flask import Flask, g

def get_db():
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
        # sqlite3.Row tells the connection to return rows that behave like dicts.
        # This allows accessing the columns by name.
        # g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    `close_db` checks if a connection was created by checking if `g.db` was set.
    If the connection exists, it is closed.
    """
    db: redis.Redis = g.pop('db', None)
    
    if (db is not None):
        db.close()
        
def init_app(app: Flask):
    app.teardown_appcontext(close_db)