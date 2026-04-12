"""
Search for script modules
"""
import importlib
import pathlib
import sys
import pkgutil

from .classes import Script, ScriptManager
from .custom_exceptions import ScriptIDAlreadyExists

def init_script_manager(
        module_parent_path: pathlib.Path,
        module_name: str,
        max_simul_runs: int = 4,
    ) -> ScriptManager:
    """Initialise script manager. Imports the 'module_name' from the 'module_parent_path'.
    The modules must have the Script's metadata like name, description, ID and execute
    function.
    
    :param module_parent_path: the parent path of where the scripts are located
    :param module_name: the name of the directory that contains all the scripts
    :param max_simul_runs: the parameter for how many scripts that can run at a time
    """
    # add the path to sys.path
    sys.path.append(str(module_parent_path))
    
    # import the module by name
    module = importlib.import_module(module_name)
    
    # pop off the path
    sys.path.pop()
    
    # create new event manager
    script_manager = ScriptManager(max_simul_runs)
    
    # create events
    for _, name, _ in pkgutil.iter_modules(module.__path__):
        
        # import the module
        mod = f"{module_name}.{name}"
        mod = importlib.import_module(mod)
        
        if (mod.ID in script_manager.scripts.keys()):
            raise ScriptIDAlreadyExists(mod.ID)
        
        # each module needs to have NAME, DESCRIPTION and execute function
        # create event
        new_script = Script(
            script_id=mod.ID,
            name=mod.NAME,
            description=mod.DESCRIPTION,
            execute_fn=mod.execute,
        )
        script_manager.add_script(new_script)
        
    return script_manager

# if (__name__ == "__main__"):
#     scripts_init()