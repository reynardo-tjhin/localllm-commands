from flask import Flask, render_template, Response, stream_with_context, request, jsonify
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
        # get all events
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
            
            # return a None response
            return Response(None)
    
    @app.route("/poll", methods=["GET"])
    def poll():
        
        start = 0
        if (request.args.get("start") is not None):
            start = int(request.args.get("start"))
        
        conn = db.get_db()
        items = conn.lrange(0, start=start, end=-1)
        
        return jsonify({
            "events": [item for item in items],
            "end": start+len(items),
        })
    
    return app