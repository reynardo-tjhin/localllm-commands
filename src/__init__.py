from flask import Flask, Response, render_template, jsonify, request
from . import db, config, load_scripts

def create_app() -> Flask:
    # load config
    config.load_config()

    # load events
    evt_manager = load_scripts.scripts_init()
    
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
    
    # start worker: create a new process to start a worker
    @app.route("/start-worker", methods=["POST"])
    def start_worker() -> Response:
        if (request.method == "POST"):
            
            # create a process
            print("Starting a worker")
            evt_manager.start_event(0)
            
            # return a None response
            return Response(None)
    
    # end worker: stop a process to end the script
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