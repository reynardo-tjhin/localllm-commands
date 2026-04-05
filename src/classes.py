import os
import re

from dataclasses import dataclass
from multiprocessing import Process
from typing import Callable, Dict
from redis import Redis
from datetime import datetime
from .custom_exceptions import *

@dataclass
class Script:
    """The Script object contains the basic descriptions like name and
    description. It has an attribute that points to the address of the
    execute function in the .py script.
    
    The function :func:`scripts_init` will look at all the .py files in
    the `script` folder and initialise each of the .py file as a Script
    object. Usually, initialising Script object is not needed, but can be
    initialised this way::
    
        new_script = Script(
            "d38134b0435f4d2392c953f6160e9e64",
            "Keep Alive Script", 
            "Sending Keep Alive",
            execute
        )
    
    :param script_id: The ID that represents this script.
    :param name: The name of the script. It will also be shown in the web
        interface to differentiate from the other scripts.
    :param description: The additional details of the script.
    :param execute_fn: The function that executes the script. The function
        takes in an integer argument. The script will be identified based on
        this integer.
    """
    # the ID of the script
    # generated from :func:`uuid4` of the :class:`uuid`.
    # instead of storing as a UUID object, it is stored as a hex string instead.
    # this will also be used as the key in the redis database.
    # the ID of the script cannot be changed once it is saved to Redis database.
    # changing it will save it to a new key of the redis database.
    # the past logs may not be shown once the ID of the script is changed.
    script_id: str
    
    # the name of the script
    # this name can also be different from the python filename.
    # it must be initialised as a constant at the start of the file.
    name: str
    
    # the description of the script
    # same as the name, it must be initialised as a constant at the
    # start of the file.
    description: str
    
    # the function that runs the script
    # it takes in a string argument which is the script ID.
    execute_fn: Callable[[str], None]
    
    def __init__(self, script_id: str, name: str, description: str, execute_fn: Callable[[str], None]):
        self.script_id = script_id
        self.name = name
        self.description = description
        self.execute_fn = execute_fn
        
@dataclass
class ScriptManager:
    """The Script Manager object manages the scripts. It performs tasks like
    starting the script and ending the script. Each script's ID is generated using 
    uuid's uuid4 function and is stored as a hex string.
    
    The function :func:`scripts_init` initialises the script manager and then
    adds the script objects. After the script manager is initialised, it will
    create an empty list of script objects and an empty dictionary that takes in
    integer (which represents the id of the script) as the key and its corresponding
    process as the value.
    
    :param max_simul_runs: maximum number of scripts running at the same time
        defaults to 4.
    :param scripts: a dictionary of Script ID as the key and the Script object as the
        value.
    :param running_processes: a dictionary. The key is the id of the Script
        and the value represents the Process object corresponding to the ID of the
        script.
    """
    # maximum number of scripts running at the same time
    max_simul_runs: int
    
    # a dictionary of Script ID as the key and the Script object as the value.
    scripts: Dict[str, Script]
    
    # a dictionary of ID of the script as the key and Process object
    # as the value.
    running_processes: Dict[str, Process]
    
    def __init__(self, max_simul_runs: int = 4):
        self.max_simul_runs = max_simul_runs
        self.scripts = {}
        self.running_processes = {}
    
    def add_script(self, script: Script) -> None:
        """Add a script object to the :attr:`scripts`. 
        The same Script object cannot be added again. This method does not
        accept a None script object.
        
        :param script: the Script object to be added
        """
        if script is None:
            raise TypeError("Script cannot be None")
    
        if script.script_id in self.scripts.keys():
            raise DuplicateScriptError()
        
        self.scripts[script.script_id] = script
            
    def start_script(self, script_id: str) -> bool:
        """Start the script based on the ID of the script given as an argument.
        Create a new process object :class:`Process` from the :module:`multiprocessing`.
        Script ID cannot be None, must adhere the hex format and only 32 characters are allowed.
        
        :param script_id: the ID of the Script. It is the hex string of a UUID4 object.
        """
        if (script_id is None):
            raise TypeError("script_id cannot be None")
    
        if (len(script_id) != 32):
            raise BadScriptIDLength(script_id)
    
        if (not bool(re.match("^[0-9a-f]+$", script_id))):
            raise BadScriptIDFormat(script_id)
        
        if (self.scripts.get(script_id) is None):
            raise ScriptNotFoundError(script_id)
        
        if (self.running_processes.get(script_id) is not None):
            raise ScriptAlreadyRan(script_id)
        
        if (len(self.running_processes) >= self.max_simul_runs):
            raise ScriptManagerLimitExceededError(self.max_simul_runs)
        
        # refresh the internals
        self.__refresh()
        
        # get the script object
        script = self.scripts.get(script_id)
        script_fn = script.execute_fn
        
        # create a new process
        # pass the index as an argument to the execute function of the Script object
        # the index is for logging purposes as the key for the Redis database
        new_process = Process(target=script_fn, args=())
        
        # if the parent process ends (the one that calls this process)
        # then the subprocess (which is the one created here) will continue
        # it might be an orphan process if not handled properly
        new_process.daemon = False

        # start the process
        new_process.start()
        self.running_processes[script_id] = new_process
        print(f"[INFO] Script ID '{script_id}' has started")
    
        return True
                
    def end_script(self, script_id: str) -> bool:
        """End the script based on the ID of the script given as an argument.
        End the process by calling :func:`terminate` from the :class:`multiprocessing` class.
        Script ID cannot be None, must adhere the hex format and only 32 characters are allowed.
        
        :param script_id: the ID of the Script. It is the hex string of a UUID4 object.
        """
        if (script_id is None):
            raise TypeError("script_id cannot be None")
    
        if (len(script_id) != 32):
            raise BadScriptIDLength(script_id)
    
        if (not bool(re.match("^[0-9a-f]+$", script_id))):
            raise BadScriptIDFormat(script_id)
        
        if (self.scripts.get(script_id) is None):
            raise ScriptNotFoundError(script_id)
        
        if (self.running_processes.get(script_id) is None):
            raise ScriptNotInRunningProcessesError(script_id)
        
        if (self.running_processes.get(script_id).is_alive() is False):
            raise ScriptProcessNotAliveError(script_id)

        # refresh the internals
        self.__refresh()
    
        running_process = self.running_processes.get(script_id)
        running_process.terminate() # graceful shutdown process
        del self.running_processes[script_id]
        print(f"[INFO] Script ID '{script_id}' has been terminated successfully")
        
        return True
        
    def script_status(self, script_id: str) -> int:
        """Gets the script status. It will return one of the three integer values below:
        - -1: process is not alive according to :func:`process.is_alive` function
        - 0: process is still running
        - 1: process is not running
        
        Instead of implementing a process/function that keeps track of each of the scripts,
        it is easier to just check from the process' :func:`is_alive` function and deletes the script
        from :attr:`running_processes` when :func:`is_alive` function returns False.
        
        :param script_id: the ID of the Script. It is the hex string of a UUID4 object.
        """
        if (script_id is None):
            raise TypeError("script_id cannot be None")
    
        if (len(script_id) != 32):
            raise BadScriptIDLength(script_id)
    
        if (not bool(re.match("^[0-9a-f]+$", script_id))):
            raise BadScriptIDFormat(script_id)
        
        if (self.scripts.get(script_id) is None):
            raise ScriptNotFoundError(script_id)
        
        self.__refresh()
        
        # get the running process
        running_process = self.running_processes.get(script_id)
        if (running_process is not None):

            is_alive = running_process.is_alive()
            
            # process returns alive and is also in the dictionary
            if (is_alive):
                return 0
            
            # process is not alive but still lives in the dictionary
            # delete the script from the running_processes
            del self.running_processes[script_id]
            return -1

        # process is not alive
        return 1
    
    def __refresh(self) -> None:
        """Refreshes the internals of the Script Manager object.
        Removes any processes that are not running from the :attr:`running_processes`.
        """
        for key in list(self.running_processes.keys()):
            running_process = self.running_processes.get(key)
            if running_process is not None:
                if not running_process.is_alive():
                    del self.running_processes[key]
            
        return None

@dataclass
class Logger:
    """Class to handle logging to redis database. Currently, only redis is supported.
    The reason why Server-Sent Events (SSE) are not used is because the events
    were lost while implementing streaming of the messages.
    """
    # the connection to redis database
    conn: Redis
    
    # each script will have its own Logger object.
    # then the script will log its messages to the keys stored in redis
    # database.
    key: str
    
    def __init__(self, key: str):
        
        # create a redis instance
        self.conn = Redis(
            host=os.getenv('REDIS_HOST'),
            port=os.getenv('REDIS_PORT'),
            decode_responses=True,
            password=os.getenv('REDIS_PASSWORD'),
        )
        
        # check if the redis server is up and running
        if (self.conn.info() is None):
            raise RedisConnectionError()
        
        # the logger's key
        self.key = "script:" + key
        
    def log(self, message: str) -> None:
        """
        Log the message to redis database
        
        :param message: the message that is send to the user
        """
        message = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "|" + message
        self.conn.rpush(self.key, message)
        
        return None