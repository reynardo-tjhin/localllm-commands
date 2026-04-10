import pytest
import pathlib
import dotenv

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