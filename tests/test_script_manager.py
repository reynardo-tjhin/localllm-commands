import pytest
import pathlib
import time

from src import load_scripts, custom_exceptions, classes

def test_init_script_manager(script_manager):
    """Testing script manager has the right attributes"""
    
    # script manager's attributes
    assert len(script_manager.scripts) == 3
    assert script_manager.max_simul_runs == 2
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
    """Test with scripts with missing details: ID, name, description and execute function"""
    
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
        
def test_add_script(script_manager):
    """Testing add scripts"""
    
    # Test 1: None script
    with pytest.raises(TypeError):
        script_manager.add_script(None)
        
    # Test 2: duplicate script
    with pytest.raises(custom_exceptions.DuplicateScriptError):
        from test_scripts import test_script_1
        
        script_manager.add_script(classes.Script(
            script_id=test_script_1.ID,
            name=test_script_1.NAME,
            description=test_script_1.DESCRIPTION,
            execute_fn=test_script_1.execute,
        ))
        
def test_start_end_simple_script(script_manager):
    """Testing starting the script"""
    
    # just a keep alive script
    # that runs indefinitely that sleeps every 5 seconds
    script_id = "0e6a19cc157941e0b56b6a272c6eec71"
    
    # start the script - test_script_1
    new_process = script_manager.start_script(script_id)
    
    # give some time for the process to start
    time.sleep(0.5)
    
    # check whether it's running
    assert new_process is not None
    assert len(script_manager.running_processes) == 1
    assert script_manager.running_processes.get(script_id).is_alive()
    
    # stop the script
    ended_process = script_manager.end_script(script_id)
    
    # give some time to terminate the process
    time.sleep(0.1)
    
    # check whether it's stopped
    assert ended_process is not None
    assert new_process == ended_process
    assert len(script_manager.running_processes) == 0
    assert ended_process.is_alive() is False
    assert ended_process.exitcode == -15

def test_start_end_two_scripts(script_manager):
    """Testing running two scripts at the same time"""
    
    # scripts
    script_id_1 = "0e6a19cc157941e0b56b6a272c6eec71"
    script_id_2 = "c66d9421757f4051aa2f99b5305cb037"
    
    # start both script
    script_1_process = script_manager.start_script(script_id_1)
    time.sleep(0.5) # break to let the process starts fully

    script_2_process = script_manager.start_script(script_id_2)
    time.sleep(0.5) # break to let the process starts fully
    
    # check the scripts processes
    assert script_1_process is not None
    assert script_2_process is not None
    assert script_1_process.is_alive()
    
    # script 2 is a very fast script
    assert script_2_process.is_alive() is False
    
    assert len(script_manager.running_processes) == 2
    assert script_1_process is script_manager.running_processes.get(script_id_1)
    assert script_2_process is script_manager.running_processes.get(script_id_2)
    
    # wait for script 2 to finish
    time.sleep(0.5)
    
    # remains the same because no calls to update the internals of the script manager
    assert len(script_manager.running_processes) == 2

    # stop script 1
    # performs __refresh() that updates the internals of script_manager
    script_manager.end_script(script_id_1)
    
    # wait for script 2 to be terminated
    time.sleep(0.5)

    # check the script manager
    assert len(script_manager.running_processes) == 0
    assert script_1_process.is_alive() is False