from flask import Flask, render_template, Response, stream_with_context, request
from multiprocessing import Queue
from .models import EventManager, Event

from scripts.base_script import execute

# shared queue that outlives any single request
output_queue = Queue()

# create new event
new_evt = Event(execute_fn=execute)

# create event manager
evt_manager = EventManager(output_queue)
evt_manager.add_event(new_evt)

def create_app():
    # create the app object
    app = Flask(__name__)
    
    # main page
    @app.route("/")
    def index():
        
        # register all Events
        # - event object
        
        return render_template("home.html")
    
    # start worker
    @app.route("/start-worker", methods=["POST"])
    def start_worker() -> Response:
        if (request.method == "POST"):
            
            # create a process
            print("Starting a worker")
            # new_process = Process(target=execute, args=(output_queue,))
            # new_process.daemon = False
            # new_process.start()
            
            evt_manager.start_event(0)
            
            # return a None response
            return Response(None)
    
    # stream some stuff
    @app.route("/stream")
    def stream():
        def generate():
            while True:
                item = output_queue.get() # blocks until data is available
                if item is None:
                    yield f"data: done\n\n"
                    break
                elif item != "":
                    yield f"data: {item}\n\n"
        
        return Response(stream_with_context(generate()), mimetype="text/event-stream")
    
    return app