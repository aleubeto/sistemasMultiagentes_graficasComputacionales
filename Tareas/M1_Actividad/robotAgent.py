from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as pathGrid
from pathfinding.finder.a_star import AStarFinder
from mesa.visualization.UserParam import UserSettableParameter
from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule

class Robot(Agent):

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        for element in self.model.grid.iter_cell_list_contents(self.pos):
            if type(element) == WallBlock:
                self.model.grid.remove_agent(element)
                return

        next_moves = self.model.grid.get_neighborhood(self.pos, moore=True)
        next_move = self.random.choice(next_moves)

        step = True
        for element in self.model.grid.iter_cell_list_contents(next_move):
            if type(element) == Robot:
                step = False

        if step:
            self.model.grid.move_agent(self, next_move)

class WallBlock(Agent):

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

    def step(self):
        pass

class Maze(Model):

    def __init__(self, height=50, width=50, agents=10, dirtiness=0.50, step_counter=1, time_limit=10):

        super().__init__()

        self.schedule = RandomActivation(self)

        self.step_counter = step_counter
        self.time_limit = time_limit

        self.grid = MultiGrid(height, width, torus=False)

        for i in range(agents):
            robot = Robot(self, (1, 1))
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)

        for _,x,y in self.grid.coord_iter():

            if self.random.random() < dirtiness:

                wall = WallBlock(self, (x, y))
                self.grid.place_agent(wall, wall.pos)
                self.schedule.add(wall)

    def step(self):
        self.step_counter += 1
        self.schedule.step()
        if self.step_counter >= self.time_limit:
            self.running = False

def agent_portrayal(agent):
    if type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}

    elif type(agent) == Robot:
        return {"Shape": "Imagenes/robot-vacuum-cleaner.png", "Layer": 0}

grid = CanvasGrid(agent_portrayal, 50, 50, 450, 450)

server = ModularServer(Maze, [grid], "Equipo 10 - M1. Actividad",
                        {"dirtiness": UserSettableParameter(
                            "slider", "Suciedad", 0.50, 0.01, 1.0, 0.01),
                        "agents": UserSettableParameter(
                            "number", "Número de agentes", 10),
                        "height": UserSettableParameter(
                            "number", "Altura", 50),
                        "width": UserSettableParameter(
                            "number", "Anchura", 50),
                        "time_limit": UserSettableParameter(
                            "number", "Tiempo máximo de ejecución", 10)})
server.port = 8522
server.launch()
