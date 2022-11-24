from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as pathGrid
from pathfinding.finder.a_star import AStarFinder

class Robot(Agent):
    DEAMBULANDO = 0
    ENCAMINO = 1
    REGRESARESTANTE = 2
    def __init__(self, model, pos, width, height):
        super().__init__(model.next_id(), model)
        self.condition = self.DEAMBULANDO
        self.pos = pos
        self.move_counter = 0
        self.w = width
        self.h = height
        self.sig = 1
        self.path = []
        self.activo = True
        self.carga = None
        self.direccion = (0, 0)
        self.hallazgo = None

    def step(self):
        if self.activo == False:
            return
        
        if self.condition == self.DEAMBULANDO:
            if self.hallazgo != None:
                self.path = self.pathfinding(self.hallazgo)
                self.sig = 1
                self.condition = self.ENCAMINO
                
            else:
                self.encontrar_caja()

                if self.carga == None:
                    siguiente = (self.pos[0] + self.direccion[0], self.pos[1] + self.direccion[1])
                    if self.model.grid.is_cell_empty(siguiente):
                        self.model.grid.move_agent(self, siguiente)
                    else:
                        self.cambiar_direccion()
                        for element in self.model.grid.get_cell_list_contents(siguiente):
                            if type(element) == Robot:
                                element.cambiar_direccion()

        elif self.condition == self.ENCAMINO:
            if self.sig < len(self.path):
                paso = True
                for element in self.model.grid.get_cell_list_contents(self.path[self.sig]):
                    if type(element) == Robot:
                        element.model.grid.move_agent(element, self.path[self.sig - 1])
                        paso = False
                        
                if paso:
                    self.model.grid.move_agent(self, self.path[self.sig])
                    if self.carga != None:
                        self.carga.model.grid.move_agent(self.carga, self.path[self.sig])
                    else:
                        self.encontrar_caja()
                    self.sig = self.sig + 1
            else:
                if self.carga != None:
                    self.condition = self.DEAMBULANDO
                    self.model.grid.remove_agent(self.carga)
                    self.model.schedule.remove(self.carga)
                    self.model.box_list.remove(self.carga)
                    self.hallazgo = None
                    self.carga = None
                    print("elimine una caja")
                else:
                    self.condition = self.DEAMBULANDO
                    self.hallazgo = None
            
        elif self.condition == self.REGRESARESTANTE:
            self.objetivo = self.encontrar_estante()
            self.sig = 1
            if self.objetivo == None:
                self.activo = False
            else:
                self.path = self.pathfinding(self.objetivo.pos)
                self.condition = self.ENCAMINO
    
    def cambiar_direccion(self):
        random = self.random.randrange(0, 3, 1)
        if random == 0:
            self.direccion = (1, 0)
        elif random == 1:
            self.direccion = (0, 1)
        elif random == 2:
            self.direccion = (-1, 0)
        elif random == 3:
            self.direccion = (0, -1)
    
    def encontrar_caja(self):
        buscando = True
        for element in self.model.grid.neighbor_iter(self.pos, False):
            if type(element) == Caja and buscando:
                if element.condition == element.DISPONIBLE:
                    buscando = False
                    self.model.grid.move_agent(self, element.pos)
                    element.condition = element.OCUPADA
                    self.carga = element
                    for robot in self.model.robot_list:
                        if robot.condition == robot.DEAMBULANDO:
                            robot.hallazgo = element.pos
                    if self.condition == self.ENCAMINO:
                        self.sig = len(self.path)
                    self.condition = self.REGRESARESTANTE
    
    def encontrar_estante(self):
        mejor = 0
        estante_mejor = None
        for estante in self.model.shelf_list:
            cantidad = estante.cuenta_cajas  
            if cantidad >= mejor and cantidad < 5:
                mejor = cantidad
                estante_mejor = estante
        if estante_mejor != None:
            estante_mejor.cuenta_cajas += 1
            
        return estante_mejor
                
    def pathfinding(self, destino):
        grid = pathGrid(width=self.w, height=self.h, matrix=self.model.matrix)
        start = grid.node(self.pos[0], self.pos[1])
        end = grid.node(destino[0], destino[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        
        return path

class Caja(Agent):
    OCUPADA = 0
    DISPONIBLE = 1
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.condition = self.DISPONIBLE
        self.pos = pos

    def step(self):
        pass
    
class Estante(Agent):

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.cuenta_cajas = 0

    def step(self):
        pass
    
class WallBlock(Agent):
    
    def __init__(self, model, pos): 
        super().__init__(model.next_id(), model)
        
        self.pos = pos
    
    def step(self):
        pass

class Room(Model):

    def __init__(self, height=30, width=30, agents=10, boxes=5, shelves=1, step_counter=1, time_limit=50):
        
        super().__init__()
        
        self.schedule = RandomActivation(self)
        
        self.h = height
        self.w = width
        
        self.step_counter = step_counter
        self.time_limit = time_limit
        
        self.box_list = []
        self.shelf_list = []
        self.robot_list = []
        
        self.grid = MultiGrid(self.w, self.h, torus=False)
        
        self.matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        for _,x,y in self.grid.coord_iter():
            if self.matrix[y][x] == 0:
                wall = WallBlock(self, (x, y))
                self.grid.place_agent(wall, wall.pos)
                self.schedule.add(wall)
        
        """
        for i in range(self.w):
            self.box_matrix.append([])
            self.shelf_matrix.append([])
            for j in range(self.h):
                self.box_matrix[i].append(0)
                self.shelf_matrix[i].append(0)
        """
        
        for i in range(agents):
            x = self.random.randrange(0, self.w)
            y = self.random.randrange(0, self.h)
            if self.grid.is_cell_empty((x, y)):
                robot = Robot(self, (x, y), self.w, self.h)
                self.grid.place_agent(robot, robot.pos)
                self.schedule.add(robot)
                self.robot_list.append(robot)
        
        for i in range(boxes):
            x = self.random.randrange(0, self.w)
            y = self.random.randrange(0, self.h)
            if self.grid.is_cell_empty((x, y)):
                caja = Caja(self, (x, y))
                self.grid.place_agent(caja, caja.pos)
                self.schedule.add(caja)
                self.box_list.append(caja)
                
        for i in range(shelves):
            x = self.random.randrange(0, self.w)
            y = self.random.randrange(0, self.h)
            if self.grid.is_cell_empty((x, y)):
                estante = Estante(self, (x, y))
                self.grid.place_agent(estante, estante.pos)
                self.schedule.add(estante)
                self.shelf_list.append(estante)
            
         # Recolector de información: procentaje de celdas limpiadas
        self.boxesleft = self.count_type(self)
        self.time_datacollector = DataCollector({"Tiempo transcurrido": lambda m: self.step_counter})
        #self.datacollector = DataCollector({"Porcentaje de celdas limpias": lambda m: ((width*height)-self.count_type(m)) * 100 / (width*height)})
        self.boxes_datacollector = DataCollector({"Cantidad de cajas recogidas": lambda m: (self.boxesleft-self.count_type(m))})
        self.move_datacollector = DataCollector({"Movimientos realizados": lambda m: self.count_moves(m)})
    # Método para contar cantidad de celdas en cierto estado
    
    @staticmethod
    def count_type(model):
        count = 0
        for box in model.schedule.agents:
            if type(box) == Caja:
                count += 1
        return count
    
    @staticmethod
    def count_moves(model):
        count = 0
        for robot in model.schedule.agents:
            if type(robot) == Robot:
                count += robot.move_counter
        return count
    
    def step(self):
        self.step_counter += 1
        self.schedule.step()
        self.time_datacollector.collect(self)
        self.boxes_datacollector.collect(self)
        self.move_datacollector.collect(self)
        if self.step_counter >= self.time_limit or self.count_type(self)==0:
            self.running = False
            
def agent_portrayal(agent):
    if type(agent) == Caja:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Brown", "Layer": 0}
    
    elif type(agent) == Estante:
        if agent.cuenta_cajas >= 0 and agent.cuenta_cajas < 2:
            return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Black", "Layer": 1}
        elif agent.cuenta_cajas >= 2 and agent.cuenta_cajas <= 4:
            return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Orange", "Layer": 1}
        if agent.cuenta_cajas == 5:
            return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Red", "Layer": 1}
    
    elif type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 2}
    
    elif type(agent) == Robot:
        return {"Shape": "circle", "r": 1, "Filled": "true", "Color": "Blue", "Layer": 3}
    
grid = CanvasGrid(agent_portrayal, 30, 30, 450, 450)

# Creación de tabla que grafica datacollector
#chart_tiempo = ChartModule([{"Label": "Tiempo transcurrido", "Color": "Black"}], data_collector_name='time_datacollector')
#
#chart_cajas = ChartModule([{"Label": "Cantidad de cajas restante", "Color": "Black"}], data_collector_name='boxes_datacollector')
#
#chart_movimientos = ChartModule([{"Label": "Movimientos realizados", "Color": "Black"}], data_collector_name='move_datacollector')

server = ModularServer(Room, [grid], "Equipo 10 - M1. Actividad",
                        {"width": UserSettableParameter(
                            "number", "Anchura", 30),
                        "height": UserSettableParameter(
                            "number", "Altura", 30),
                        "agents": UserSettableParameter(
                            "number", "Número de agentes", 10),
                        "boxes": UserSettableParameter(
                            "number", "Número de cajas", 5, 1, 10, 1),
                        "shelves": UserSettableParameter(
                            "number", "Número de estantes", 1, 1, 10, 1),
                        "time_limit": UserSettableParameter(
                            "number", "Tiempo máximo de ejecución", 50)})
server.port = 8522
server.launch()