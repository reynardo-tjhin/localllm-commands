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
                "id": script_id,
                "name": script_manager.scripts.get(script_id).name,
                "description": script_manager.scripts.get(script_id).description,
            } for script_id in script_manager.scripts.keys()
        ]
        return render_template("home.html", scripts=scripts)
    
    # start worker: create a new process to start a worker
    @app.route("/start-worker/<string:script_id>", methods=["POST"])
    def start_worker(script_id: str) -> Response:
        if (request.method == "POST"):
            
            # create a process
            print("Starting a worker")
            script_manager.start_script(script_id)
            
            return jsonify({
                "status": "ok",
                "message": "script started",
            }), 200
    
    # end worker: stop a process to end the script
    @app.route("/stop-worker/<string:script_id>", methods=["POST"])
    def stop_worker(script_id: str) -> Response:
        if (request.method == "POST"):
            
            # ending a process
            print("Ending a worker")
            script_manager.end_script(script_id)
            
            # return a None response
            return Response(None)
        
    # check if worker is running
    @app.route("/worker-status/<string:script_id>", methods=["GET"])
    def worker_status(script_id: str) -> Response:
        status = script_manager.script_status(script_id)
        return jsonify({
            "script_id": script_id,
            "status": status,
        })
    
    @app.route("/poll/<string:script_id>", methods=["GET"])
    def poll(script_id: str) -> Response:
        
        start = 0
        if (request.args.get("start") is not None):
            start = int(request.args.get("start"))
        
        conn = db.get_db()
        items = conn.lrange("script:"+script_id, start=start, end=-1)
        
        return jsonify({
            "events": [item for item in items],
            "end": start+len(items),
        })
    
    return app