from flask import Flask, Response, render_template, jsonify, request
from . import db, config, load_scripts

def create_app() -> Flask:
    # load config
    config.load_config()

    # load scripts
    script_manager = load_scripts.scripts_init()
    
    # create the app object
    app = Flask(__name__)
    
    # register database
    db.init_app(app=app)
    
    # main page
    @app.route("/")
    def index() -> str:
        # get all scripts
        scripts = [
            {
                "name": script.name,
                "description": script.description,
            } for script in script_manager.scripts
        ]
        return render_template("home.html", scripts=scripts)
    
    # start worker: create a new process to start a worker
    @app.route("/start-worker", methods=["POST"])
    def start_worker() -> Response:
        if (request.method == "POST"):
            
            # create a process
            print("Starting a worker")
            script_manager.start_script(0)
            
            # return a None response
            return Response(None)
    
    # end worker: stop a process to end the script
    @app.route("/stop-worker", methods=["POST"])
    def stop_worker() -> Response:
        if (request.method == "POST"):
            
            # ending a process
            print("Ending a worker")
            script_manager.end_script(0)
            
            # return a None response
            return Response(None)
    
    @app.route("/poll/<int:script_id>", methods=["GET"])
    def poll(script_id: int):
        
        start = 0
        if (request.args.get("start") is not None):
            start = int(request.args.get("start"))
        
        conn = db.get_db()
        items = conn.lrange("script:"+str(script_id), start=start, end=-1)
        
        return jsonify({
            "events": [item for item in items],
            "end": start+len(items),
        })
    
    @app.route("/scripts/<int:script_id>", methods=["GET"])
    def script_log(script_id: int):
        conn = db.get_db()
        # items = 
        return render_template("script_log.html")
    
    return app