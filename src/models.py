import os

from dataclasses import dataclass
from multiprocessing import Process, Queue
from typing import List, Callable, Dict

@dataclass
class Script:
    """Class to store details of Script with tasks"""
    name: str
    description: str
    execute_fn: Callable[[Queue], None]
    
    def __init__(self, name: str, description: str, execute_fn: Callable[[Queue], None]):
        self.name = name
        self.description = description
        self.execute_fn = execute_fn
        
@dataclass
class ScriptManager:
    """Class to handle events"""
    scripts: List[Script]
    running_processes: Dict[int, Process]
    
    def __init__(self):
        self.scripts = []
        self.running_processes = {}
    
    def add_script(self, script: Script) -> None:
        if script is not None:
            self.scripts.append(script)
            
    def start_script(self, index: int) -> None:
        if (index is None):
            raise TypeError("index cannot be None")
    
        if (index < 0):
            raise ValueError("index cannot be less than 0")
    
        if (index > len(self.scripts) - 1):
            raise ValueError("index cannot be greater than the total number of scripts")
        
        new_process = Process(target=self.scripts[index].execute_fn, args=(index,))
        new_process.daemon = False
        try:
            new_process.start()
            self.running_processes[index] = new_process
            
            print("new process added to running processes")
        except Exception:
            raise Exception("Issue with starting a process")
                
    def end_script(self, index: int) -> bool:
        if (index is None):
            raise TypeError("index cannot be None")
    
        if (index < 0):
            raise ValueError("index cannot be less than 0")
    
        if (index > len(self.events) - 1):
            raise ValueError("index cannot be greater than the total number of scripts")
        
        if (self.running_processes.get(index) is None):
            raise KeyError(f"Script with index {index} is not running")
    
        running_process = self.running_processes.get(index)
        running_process.terminate() # graceful shutdown process
        del self.running_processes[index]
        return True
        
    def script_status(self, index: int) -> int:
        """
        
        """
        {
            -1: "process is not alive but still lives in the running_processes dictionary",
            0: "process is alive and also in the running_processes dictionary",
            1: "process is not in the running_processes dictionary",
        }
        
        running_process = self.running_processes.get(index)
        if (running_process is not None):
            is_alive = running_process.is_alive()
            if (is_alive):
                return 0 # process returns alive and is also in the dictionary
            return -1 # process is not alive but still lives in the dictionary
        return 1 # process is not alive
        
        
        
        
        
