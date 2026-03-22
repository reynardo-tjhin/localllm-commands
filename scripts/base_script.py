from multiprocessing import Queue
# from src.models import EventQueue

def execute(output_queue: Queue):

    output_queue.put("")
    
    # first task: count the sum of 1 to 10000000
    first_task = "Running the first task: counting the sum of 1 to 10000000"
    # yield "data: {}\n\n".format(first_task)
    output_queue.put(first_task)
    
    total = sum([i for i in range(1, 10000001)])
    log = "The total is " + str(total)
    # yield "data: {}\n\n".format(log)
    output_queue.put(log)
    
    # second task: count the sum of 5 to 50000000
    second_task = "Running the second task: counting the sum of 5 to 50000000"
    # yield "data: {}\n\n".format(second_task)
    output_queue.put(second_task)
    
    total = sum([i for i in range(5, 50000001)])
    log = "The total is " + str(total)
    # yield "data: {}\n\n".format(log)
    output_queue.put(log)
    
    # third task: count the sum of 10 to 1000000
    third_task = "Running the third task: counting the sum of 10 to 10000000"
    # yield "data: {}\n\n".format(third_task)
    output_queue.put(third_task)
    
    total = sum([i for i in range(10, 10000001)])
    log = "The total is " + str(total)
    # yield "data: {}\n\n".format(log)
    output_queue.put(log)
    
    # close the event source / stream response
    # yield "data: done\n\n"
    output_queue.put(None)
    
    return

# create new event
# new_event = Event(
#     name="Basic Event",
#     description="For initial testing",
#     task_count=3,
#     execute_fn=execute,
# )