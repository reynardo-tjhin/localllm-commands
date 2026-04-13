import pytest
import pathlib
import dotenv
import redis
import os

from src import create_app, load_scripts, classes

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    
    # create and load test scripts
    module_parent_path = pathlib.Path(__file__).parent.parent
    module_name = "test_scripts"
    
    # create app
    app = create_app(
        module_parent_path=module_parent_path,
        module_name=module_name,
    )
    
    yield app
    
@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def script_manager():
    """Initialise the script manager before the tests"""
    
    return load_scripts.init_script_manager(
        module_parent_path=pathlib.Path(__file__).parent.parent,
        module_name="test_scripts",
        max_simul_runs=2,
    )
    
@pytest.fixture
def logger():
    """Initialise the logger before the tests"""
    
    # load the environment
    dotenv.load_dotenv()
    return classes.Logger("test")

@pytest.fixture
def script_1_logger():
    """Initialise the script_1 logger before running the tests"""
    
    # load the environment
    dotenv.load_dotenv()
    return classes.Logger("0e6a19cc157941e0b56b6a272c6eec71")

@pytest.fixture
def mock_redis():
    """Initialise redis connection"""
    
    # load the environment
    dotenv.load_dotenv()
    return redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=os.getenv('REDIS_PORT'),
        decode_responses=True,
        password=os.getenv('REDIS_PASSWORD'),
    )