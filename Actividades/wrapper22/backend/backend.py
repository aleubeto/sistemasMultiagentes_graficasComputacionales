import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from pacman import Maze

games = {}

app = flask.Flask(__name__)
CORS(app)

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
    ghost = model.schedule.agents[0]
    return jsonify({"x": ghost.pos[0], "y": ghost.pos[1]})

app.run()