from dataclasses import dataclass
from multiprocessing import Process, Queue
from typing import List, Callable

# @dataclass
# class Event:
#     """Class for an event with tasks"""
#     name: str
#     description: str
#     task_count: int
#     execute_fn: Callable[[Queue], None] # function that takes in zero arguments and return None
#     output_queue: Queue
    
#     def __init__(self, name: str, description: str, task_count: int, execute_fn: Callable[[Queue], None], output_queue: Queue):
#         self.name = name
#         self.description = description
#         self.task_count = task_count
#         self.execute_fn = execute_fn
#         self.output_queue = output_queue

@dataclass
class Event:
    """Class for an event with tasks"""
    execute_fn: Callable[[Queue], None]
    
    def __init__(self, execute_fn: Callable[[Queue], None]):
        self.execute_fn = execute_fn
        
@dataclass
class EventManager:
    """Class to handle events"""
    output_queue: Queue
    events: List[Event]
    
    def __init__(self, output_queue: Queue):
        self.events = []
        self.output_queue = output_queue
    
    def add_event(self, event: Event) -> None:
        if event is not None:
            self.events.append(event)
            
    def start_event(self, index: int) -> None:
        if (index is None):
            raise TypeError("index cannot be None")
    
        if (index < 0):
            raise ValueError("index cannot be less than 0")
    
        if (index > len(self.events) - 1):
            raise ValueError("index cannot be greater than the total number of events")
        
        new_process = Process(target=self.events[index].execute_fn, args=(self.output_queue,))
        new_process.daemon = False
        new_process.start()
        
    def event_status(self, index: int) -> str:
        pass
