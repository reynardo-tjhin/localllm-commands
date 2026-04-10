import pytest
import redis
import os

from src import classes, custom_exceptions

def test_logger_connection_error():
    """Simulate connection error"""
    
    with pytest.raises(custom_exceptions.RedisConnectionError):
        classes.Logger(
            key="test",
            host="127.0.0.1", # assuming redis server is not up in host machine
            port=1234, # random port
            password="random password",
            socket_timeout=0.5, # for testing
            socket_connect_timeout=0.5, # for testing
        )
    
def test_logger_connection(logger):
    """Testing simple logger tests"""
    
    assert logger.key == "script:test"
    
    # create another object to connect to redis database
    r = redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        decode_responses=True,
        password=os.getenv('REDIS_PASSWORD'),
    )
    
    # clean up leftovers
    r.delete('script:test')
    
    # create a log
    logger.log("Hello, World!")
    
    # test
    ls = r.lrange("script:test", 0, -1)
    assert len(ls) is 1
    assert ls[0].split("|")[1] == "Hello, World!"
    
    # push more messages
    logger.log("Another message")
    logger.log("Script is crashing")
    logger.log("Script has ended")
    
    # test
    ls = r.lrange("script:test", 0, -1)
    assert len(ls) is 4
    assert ls[0].split("|")[1] == "Hello, World!"
    assert ls[1].split("|")[1] == "Another message"
    assert ls[2].split("|")[1] == "Script is crashing"
    assert ls[3].split("|")[1] == "Script has ended"
    
    # clean up leftovers
    r.delete('script:test')
