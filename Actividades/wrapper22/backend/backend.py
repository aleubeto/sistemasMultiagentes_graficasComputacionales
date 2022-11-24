import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from pacman import Maze

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
    games[id] = Maze()

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
    result = []
    for ghost in model.schedule.agents:
        g = dict()
        g["id"] = ghost.unique_id
        g["x"] = ghost.pos[0]
        g["y"] = ghost.pos[1]
        result.append(g)
    return jsonify(result)

app.run()
