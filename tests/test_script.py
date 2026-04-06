import pytest
import pathlib

from src import load_scripts

@pytest.fixture
def script_manager():
    return load_scripts.init_script_manager(
        module_parent_path=pathlib.Path(__file__).parent,
        module_name="test_scripts",
        max_simul_runs=3,
    )

def test_init_script_manager(script_manager):
    """Testing script manager has the right attributes"""
    
    # script manager's attributes
    assert len(script_manager.scripts) == 3
    assert script_manager.max_simul_runs == 3
    assert not script_manager.running_processes
    
    # test script_1
    script_1 = script_manager.scripts.get("0e6a19cc157941e0b56b6a272c6eec71")
    assert script_1 is not None
    assert script_1.script_id == "0e6a19cc157941e0b56b6a272c6eec71"
    assert script_1.name == "Test Script 1"
    assert script_1.description == "Script for Testing No 1"
    
    # test script_2
    script_2 = script_manager.scripts.get("c66d9421757f4051aa2f99b5305cb037")
    assert script_2 is not None
    assert script_2.script_id == "c66d9421757f4051aa2f99b5305cb037"
    assert script_2.name == "Test Script 2"
    assert script_2.description == "Script for Testing No 2"
    
    # test script_3
    script_3 = script_manager.scripts.get("6b84f067aaf34649a5a9a161395b504c")
    assert script_3 is not None
    assert script_3.script_id == "6b84f067aaf34649a5a9a161395b504c"
    assert script_3.name == "Test Script 3"
    assert script_3.description == "Script for Testing No 3"
    
def test_broken_init_script_manager():
    with pytest.raises(AttributeError):
        load_scripts.init_script_manager(
            module_parent_path=pathlib.Path(__file__).parent,
            module_name="missing_ID_script",
            max_simul_runs=3,
        )
        
    with pytest.raises(AttributeError):
        load_scripts.init_script_manager(
            module_parent_path=pathlib.Path(__file__).parent,
            module_name="missing_name_script",
            max_simul_runs=3,
        )
        
    with pytest.raises(AttributeError):
        load_scripts.init_script_manager(
            module_parent_path=pathlib.Path(__file__).parent,
            module_name="missing_description_script",
            max_simul_runs=3,
        )
        
    with pytest.raises(AttributeError):
        load_scripts.init_script_manager(
            module_parent_path=pathlib.Path(__file__).parent,
            module_name="missing_execute_script",
            max_simul_runs=3,
        )