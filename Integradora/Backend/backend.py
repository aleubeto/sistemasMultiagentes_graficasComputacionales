import flask
from flask_cors import CORS
from flask.json import jsonify
import uuid
from robotAgent import Room, Robot, WallBlock, Caja, Estante

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
    result = [] #Array of arrays with dictionaries with agent info
    robots = [] #Array of robot info
    walls = [] #Array of wall info
    boxes = [] #Array of box info
    shelves = [] #Array of shelf info
    for agent in model.schedule.agents:
        g = dict() #Dictionary with agent info
        g["id"] = agent.unique_id
        g["x"] = agent.pos[0]
        g["y"] = agent.pos[1]
        
        if type(agent) == Robot:    #Add to robot array
            robots.append(g)
        elif type(agent) == WallBlock: #Add to wall array
            walls.append(g)
        elif type(agent) == Caja: #Add to box array
            g["status"] = agent.cargada
            g["stack"] = agent.numero
            boxes.append(g)
        else:
            g["count"] = agent.cuenta_cajas
            shelves.append(g)
            
    result.append(robots)
    result.append(walls)
    result.append(boxes)
    result.append(shelves)
    return jsonify(result)

app.run()
