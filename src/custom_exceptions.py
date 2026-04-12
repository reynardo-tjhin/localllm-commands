class ScriptIDAlreadyExists(Exception):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' already exists.")


class ScriptIDError(Exception):
    pass
        
        
class BadScriptIDLength(ScriptIDError):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' is not exactly 32 characters.")


class BadScriptIDFormat(ScriptIDError):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' contains characters that are not 0-9 or a-f.")
        
        
class ScriptNotFoundError(Exception):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' not found.")


class DuplicateScriptError(Exception):
    def __init__(self):
        super().__init__("Cannot have duplicate scripts")


class ScriptAlreadyRan(Exception):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' is currently running. Refresh the events if you are confident it has finished running.")


class ScriptManagerLimitExceededError(Exception):
    def __init__(self, max_simul_no: int):
        self.max_simul_no = max_simul_no
        super().__init__(f"Number of script running has reached the maximum, i.e. {max_simul_no}.")
        

class ScriptNotRunningError(Exception):
    pass


class ScriptNotInRunningProcessesError(ScriptNotRunningError):
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' is not in running processes")
        
        
class ScriptProcessNotAliveError(ScriptNotRunningError):
    """The difference between this error and 'ScriptNotRunningError' is that this error
    is raised due to the process object is not alive. While the other error is raised due to
    the process is still in the running_processes list.
    """
    def __init__(self, script_id: str):
        self.script_id = script_id
        super().__init__(f"Script '{script_id}' process is not alive")
        

class RedisConnectionError(Exception):
    def __init__(self):
        super().__init__("No connection to the Redis server.")