"""
Search for script modules
"""
import importlib
import pathlib
import sys
import pkgutil

from .models import Event, EventManager

def scripts_init() -> EventManager:
    
    # get the path of the repository
    path = pathlib.Path(__file__).parent.parent
    
    # add the path to sys.path
    sys.path.append(str(path))
    
    # import the module by name
    module = importlib.import_module("scripts")
    
    # pop off the path
    sys.path.pop()
    
    # create new event manager
    evt_manager = EventManager()
    
    # create events
    for _, name, _ in pkgutil.iter_modules(module.__path__):
        
        # import the module
        mod = f"scripts.{name}"
        mod = importlib.import_module(mod)
        
        # each module needs to have NAME, DESCRIPTION and execute function
        # create event
        new_event = Event(
            name=mod.NAME,
            description=mod.DESCRIPTION,
            execute_fn=mod.execute,
        )
        evt_manager.add_event(new_event)
        
    return evt_manager

# if (__name__ == "__main__"):
#     scripts_init()