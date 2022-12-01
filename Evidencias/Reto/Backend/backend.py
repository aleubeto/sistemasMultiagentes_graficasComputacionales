import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from traffic import Street, Car, Nodo

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
    games[id] = Street()

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
    result = [] #Array of arrays with dictionaries with agent info
    cars = [] #Array of car info
    nodes = [] #Array of nodes info
    model_array = []
    g = dict()
    g["run"] = model.running
    model_array.append(g)
    for agent in model.schedule.agents:
        g = dict() #Dictionary with agent info
        g["id"] = agent.unique_id
        g["x"] = agent.pos[0]
        g["y"] = agent.pos[1]
        
        if type(agent) == Car:    #Add to car array
            cars.append(g)
        elif type(agent) == Nodo: #Add to node array
            nodes.append(g)
            
    result.append(cars)
    result.append(nodes)
    result.append(model_array)
    return jsonify(result)

app.run()
