import pytest
import pathlib

from src import create_app, load_scripts

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    
    # create and load test scripts
    module_parent_path = pathlib.Path(__file__).parent
    module_name = "scripts"
    
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
