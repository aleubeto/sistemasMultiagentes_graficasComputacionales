import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from robotAgent import Room, Robot

games = {}

app = flask.Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def sayhello():
    return jsonify("hello")

@app.route("/games", methods=["POST"])
def create():
    global games
    id = str(uuid.uuid4())
    games[id] = Room()

    response = jsonify("ok")
    response.status_code = 201
    response.headers['Location'] = f"/games/{id}"
    response.headers['Access-Control-Expose-Headers'] = '*'
    response.autocorrect_location_header = False
    return response

@app.route("/games/<id>", methods=["GET"])
def queryState(id):
    global model
    model = games[id]
    model.step()
    result = [] #Array of dictionaries with robot info
    for agent in model.schedule.agents:
        if type(agent) == Robot:
            g = dict() #Dictionary with robot info
            g["id"] = agent.unique_id
            g["x"] = agent.pos[0]
            g["y"] = agent.pos[1]
            result.append(g)
    return jsonify(result)

app.run()
