from flask import Flask, render_template, Response, stream_with_context, request
from queue import Empty
from . import db, config
from .models import EventManager, Event

from scripts.keep_alive_script import execute

# create new events
new_evt = Event("Keep Alive Event", "Sending Keep Alive", execute_fn=execute)

# create event manager
evt_manager = EventManager()
evt_manager.add_event(new_evt)

def create_app():
    # create the app object
    app = Flask(__name__)
    
    # register database
    db.init_app(app=app)
    
    # main page
    @app.route("/")
    def index() -> str:
        events = [
            {
                "name": event.name,
                "description": event.description,
            } for event in evt_manager.events
        ]
        return render_template("home.html", events=events)
    
    # start worker
    @app.route("/start-worker", methods=["POST"])
    def start_worker() -> Response:
        if (request.method == "POST"):
            
            # create a process
            print("Starting a worker")
            evt_manager.start_event(0)
            
            # return a None response
            return Response(None)
        
    @app.route("/stop-worker", methods=["POST"])
    def stop_worker() -> Response:
        if (request.method == "POST"):
            
            # ending a process
            print("Ending a worker")
            evt_manager.stop_event(0)
            
            # retur a None response
            return Response(None)
    
    # stream some stuff
    @app.route("/stream")
    def stream() -> Response:
        def generate():

            yield f"data: ready\n\n"
            
            # stream
            while True:
                try:
                    item = evt_manager.output_queue.get(timeout=0.5) # blocks until data is available
                    if item is None:
                        yield f"data: done\n\n"
                        break
                    elif item != "":
                        print(item)
                        yield f"data: {item}\n\n"
                except Empty:
                    continue
        
        response = Response(stream_with_context(generate()), mimetype="text/event-stream")

        # Set the Content-Type header to 'text/event-stream' to indicate that 
        # the response will be an SSE stream
        response.headers["Content-Type"] = "text/event-stream"

        # Prevent caching of the stream (important to ensure real-time updates)
        response.headers["Cache-Control"] = "no-cache"

        # disables Nginx buffering if behind a proxy
        response.headers["X-Accel-Buffering"] = "no" 

        # Keep the connection alive to continuously send events
        response.headers["Connection"] = "keep-alive"
        return response
    
    return app