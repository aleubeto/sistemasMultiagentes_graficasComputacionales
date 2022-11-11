from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
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
                self.model.schedule.remove(element)
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

        self.grid = MultiGrid(width, height, torus=False)

        for i in range(agents):
            robot = Robot(self, (1, 1))
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)

        for _,x,y in self.grid.coord_iter():

            if self.random.random() < dirtiness:

                wall = WallBlock(self, (x, y))
                self.grid.place_agent(wall, wall.pos)
                self.schedule.add(wall)

         # Recolector de información: procentaje de celdas limpiadas
        self.dirtycells = self.count_type(self)
        #self.datacollector = DataCollector({"Porcentaje de celdas limpias": lambda m: ((width*height)-self.count_type(m)) * 100 / (width*height)})
        self.datacollector = DataCollector({"Porcentaje de celdas limpiadas": lambda m: (self.dirtycells-self.count_type(m)) * 100 / self.dirtycells})

    # Método para contar cantidad de celdas en cierto estado
    @staticmethod
    def count_type(model):
        count = 0
        for dirty in model.schedule.agents:
            if type(dirty) == WallBlock:
                count += 1
        return count

    def step(self):
        self.step_counter += 1
        self.schedule.step()
        self.datacollector.collect(self)
        if self.step_counter >= self.time_limit or self.count_type(self)==0:
            self.running = False

def agent_portrayal(agent):
    if type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}

    elif type(agent) == Robot:
        return {"Shape": "Imagenes/robot-vacuum-cleaner.png", "Layer": 0}

grid = CanvasGrid(agent_portrayal, 50, 50)

# Creación de tabla que grafica datacollector
chart = ChartModule([{"Label": "Porcentaje de celdas limpiadas", "Color": "Black"}], data_collector_name='datacollector')

server = ModularServer(Maze, [grid,chart], "Equipo 10 - M1. Actividad",
                        {"width": UserSettableParameter(
                            "number", "Anchura", 50),
                        "height": UserSettableParameter(
                            "number", "Altura", 50),
                        "agents": UserSettableParameter(
                            "number", "Número de agentes", 10),
                        "dirtiness": UserSettableParameter(
                            "slider", "Suciedad", 0.50, 0.01, 1.0, 0.01),
                        "time_limit": UserSettableParameter(
                            "number", "Tiempo máximo de ejecución", 30)})
server.port = 8522
server.launch()
