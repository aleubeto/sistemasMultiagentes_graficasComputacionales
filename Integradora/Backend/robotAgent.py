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
    def __init__(self, model, pos, width, height, intelligence):
        super().__init__(model.next_id(), model)
        self.condition = self.DEAMBULANDO
        self.color = "Blue"
        self.pos = pos
        self.move_counter = 0
        self.w = width
        self.h = height
        self.intelligence = intelligence
        self.sig = 1
        self.c_dir = 0
        self.path = []
        self.activo = True
        self.carga = None
        self.direccion = (0, 0)
        self.hallazgo = None
        self.objetivo = None

    def step(self):
        ##print("soy el robot", self.unique_id, "en la", self.pos, "estoy", self.condition)
        if self.activo == False:
            self.color = "Gray"
            #print("estoy muerto")
            self.revivir()
            return
            
        if self.condition == self.DEAMBULANDO:
            if self.intelligence:
                self.objetivo = self.encontrar_caja()
                self.sig = 1
                if self.objetivo == None:
                    #print("no encontre caja, me mato")
                    self.activo = False
                    self.color = "Gray"
                else:
                    #print("voy hacia", self.objetivo.pos)
                    self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 1
                    self.path = self.pathfinding(self.objetivo.pos)
                    if self.path != []:
                        self.objetivo.condition = self.objetivo.OCUPADA
                        self.objetivo.color = "Green"
                        #print(self.path)
                        self.condition = self.ENCAMINO
                    else:
                        self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 0
            else:
                if self.hallazgo != None:
                    self.path = self.pathfinding(self.hallazgo)
                    self.sig = 1
                    self.condition = self.ENCAMINO

                else:
                    self.detectar_caja()

                    if self.carga == None:
                        siguiente = (self.pos[0] + self.direccion[0], self.pos[1] + self.direccion[1])
                        paso = True
                        if self.model.grid.is_cell_empty(siguiente):
                            self.model.grid.move_agent(self, siguiente)
                            self.model.move_counter += 1
                        #for element in self.model.grid.get_cell_list_contents(siguiente):
                        #    if type(element) == Robot:
                        #        element.cambiar_direccion()
                        #        paso = False
                        #    elif type(element) == WallBlock:
                        #        paso = False
                        else:
                            self.cambiar_direccion()
                            
        elif self.condition == self.ENCAMINO:
            if self.sig < len(self.path) - 1:
                paso = True
                for element in self.model.grid.get_cell_list_contents(self.path[self.sig]):
                    if type(element) == Robot:
                        #print("hice un cambio de caja con ", element.unique_id)
                        self.cambiar(element)                        
                        return
                        
                if paso:
                    self.model.grid.move_agent(self, self.path[self.sig])
                    self.model.move_counter += 1
                    if self.carga != None:
                        self.model.grid.move_agent(self.carga, self.pos)
                    elif self.intelligence == False:
                        self.detectar_caja()
                    self.sig = self.sig + 1
            else:
                if self.carga != None and len(self.path) > 0:
                    #self.model.grid.move_agent(self, self.path[self.path])
                    self.model.grid.move_agent(self.carga, self.path[len(self.path) - 1])
                    self.condition = self.DEAMBULANDO
                    self.model.boxstack_counter += 1
                    self.objetivo.cuenta_stack += 1
                    self.carga.numero = self.objetivo.cuenta_stack
                    self.hallazgo = None
                    self.carga = None
                    #print("guarde una caja")
                else:
                    self.condition = self.DEAMBULANDO
                    self.hallazgo = None
                    if self.intelligence:
                        self.carga = self.objetivo
                        self.model.grid.move_agent(self.carga, self.pos)
                        self.objetivo.cargada = True
                        self.condition = self.REGRESARESTANTE

        elif self.condition == self.REGRESARESTANTE:
            self.objetivo = self.encontrar_estante()
            self.sig = 1
            if self.objetivo == None:
                #print("no encontre estante, me mato")
                self.activo = False
                self.color = "Gray"
            else:
                self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 1
                self.path = self.pathfinding(self.objetivo.pos)
                self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 0
                if self.path == []:
                    self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 0
                    self.objetivo = self.encontrar_estante_emergencia()
                    if (self.objetivo == None):
                        self.activo = False
                        self.color = "Gray"
                    else:
                        self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 1
                        self.path = self.pathfinding(self.objetivo.pos)
                        self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 0
                if self.path != []:
                    self.objetivo.cuenta_cajas += 1
                    #print(self.path)
                    self.condition = self.ENCAMINO
                else:
                    self.model.matrix[self.objetivo.pos[1]][self.objetivo.pos[0]] = 0
                
        #print("soy el robot", self.unique_id, "en la", self.pos, "estoy", self.condition, "fuera")
        
    def cambiar_direccion(self):        
        if self.c_dir == 0:
            self.direccion = (1, 0)
        elif self.c_dir == 1:
            self.direccion = (0, 1)
        elif self.c_dir == 2:
            self.direccion = (-1, 0)
        elif self.c_dir == 3:
            self.direccion = (0, -1)
            
        self.c_dir += 1
        
        if self.c_dir == 4:
            self.c_dir = 0
    
    def detectar_caja(self):
        buscando = True
        for element in self.model.grid.neighbor_iter(self.pos, False):
            if type(element) == Caja and buscando:
                if element.condition == element.DISPONIBLE:
                    buscando = False
                    self.model.grid.move_agent(self, element.pos)
                    self.model.move_counter += 1
                    element.condition = element.OCUPADA
                    element.color = "Green"
                    self.carga = element
                    self.model.matrix[self.carga.pos[1]][self.carga.pos[0]] = 1
                    element.cargada = True
                    for robot in self.model.robot_list:
                        if robot.condition == robot.DEAMBULANDO:
                            robot.hallazgo = element.pos
                    if self.condition == self.ENCAMINO:
                        self.sig = len(self.path)
                    self.condition = self.REGRESARESTANTE
    
    def encontrar_caja(self):
        menor = self.w * self.h
        caja_menor = None
        for caja in self.model.box_list:
            distancia = ((caja.pos[0] - self.pos[0]) * (caja.pos[0] - self.pos[0])) + ((caja.pos[1] - self.pos[1]) * (caja.pos[1] - self.pos[1])) 
            if distancia < menor and caja.condition == caja.DISPONIBLE:
                menor = distancia
                caja_menor = caja

        return caja_menor
    
    def encontrar_estante(self):
        mejor = 0
        estante_mejor = None
        for estante in self.model.shelf_list:
            cantidad = estante.cuenta_cajas  
            if cantidad >= mejor and cantidad < 5:
                mejor = cantidad
                estante_mejor = estante
            
        return estante_mejor
    
    def encontrar_estante_emergencia(self):
        menor = self.w * self.h
        estante_menor = None
        for estante in self.model.shelf_list:
            distancia = ((estante.pos[0] - self.pos[0]) * (estante.pos[0] - self.pos[0])) + ((estante.pos[1] - estante.pos[1]) * (estante.pos[1] - self.pos[1])) 
            if distancia < menor and estante.cuenta_cajas < 5:
                menor = distancia
                estante_menor = estante

        return estante_menor
    
    def cambiar(self, robot):
        if self == robot:
            return
        
        robot.activo = True
        
        temporal = self.carga
        self.carga = robot.carga
        robot.carga = temporal
        
        temporal = self.sig
        self.sig = robot.sig + 1
        robot.sig = temporal + 1
        
        temporal = self.path
        self.path = robot.path
        robot.path = temporal
        
        temporal = self.condition
        self.condition = robot.condition
        robot.condition = temporal
        
        self.hallazgo = None
        robot.hallazgo = None
        
        temporal = self.objetivo
        self.objetivo = robot.objetivo
        robot.objetivo = temporal
        
        if (self.carga != None):
            self.model.grid.move_agent(self.carga, self.pos)
        if (robot.carga != None):
            robot.model.grid.move_agent(robot.carga, robot.pos)
    
    def revivir(self):
        check = False
        for caja in self.model.box_list:
            if caja.condition == caja.DISPONIBLE:
                check = True
        if check:
            for robot in self.model.robot_list:
                robot.activo = True
    
    def pathfinding(self, destino):
        grid = pathGrid(width=self.w, height=self.h, matrix=self.model.matrix)
        start = grid.node(self.pos[0], self.pos[1])
        end = grid.node(destino[0], destino[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        #print(grid.grid_str(path=self.path, start=start, end=end))
        return path

class Caja(Agent):
    OCUPADA = 0
    DISPONIBLE = 1
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.condition = self.DISPONIBLE
        self.pos = pos
        self.cargada = False
        self.numero = 0
        self.color = "Brown"

    def step(self):
        pass
    
class Estante(Agent):

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.cuenta_cajas = 0
        self.cuenta_stack = 0

    def step(self):
        pass
    
class WallBlock(Agent):
    
    def __init__(self, model, pos): 
        super().__init__(model.next_id(), model)
        
        self.pos = pos
    
    def step(self):
        pass

class Room(Model):

    def __init__(self, height=30, width=30, space_rows=3, space_cols=2, length_wall=6, robots=10, boxes=25, shelves=5, step_counter=1, move_counter=0, boxstack_counter=0, time_limit=50, intelligence=False):
        
        super().__init__()
        
        self.schedule = RandomActivation(self)
        
        self.h = height
        self.w = width
        self.space_rows = space_rows
        self.space_cols = space_cols
        self.length_wall = length_wall
        
        self.step_counter = step_counter
        self.move_counter = move_counter
        self.boxstack_counter = boxstack_counter
        self.time_limit = time_limit
        
        self.intelligence = intelligence
        
        self.box_list = []
        self.shelf_list = []
        self.robot_list = []
        
        self.grid = MultiGrid(self.w, self.h, torus=False)
        
        self.matrix = []
        
        for i in range(self.h):
            self.matrix.append([])
            continuar = False
            for j in range(self.w):
                if (i == 0 or j == 0 or i == self.h - 1 or j == self.w - 1):
                    self.matrix[i].append(0)
                    wall = WallBlock(self, (j, i))
                    self.grid.place_agent(wall, wall.pos)
                    self.schedule.add(wall)
                elif (i % (self.space_rows + 1) == 0 and j % (self.space_cols + self.length_wall) == 0 and continuar == False):
                    continuar = True
                    contador_continuar = 0
                    self.matrix[i].append(0)
                    wall = WallBlock(self, (j, i))
                    self.grid.place_agent(wall, wall.pos)
                    self.schedule.add(wall)
                elif continuar and contador_continuar < self.length_wall - 1:
                    self.matrix[i].append(0)
                    wall = WallBlock(self, (j, i))
                    self.grid.place_agent(wall, wall.pos)
                    self.schedule.add(wall)
                    contador_continuar += 1
                    if contador_continuar >= self.length_wall - 1:
                        continuar = False
                    
                else:
                    self.matrix[i].append(1)
                    
        for i in range(robots):
            x = self.random.randrange(0, self.w)
            y = self.random.randrange(0, self.h)
            if self.grid.is_cell_empty((x, y)):
                robot = Robot(self, (x, y), self.w, self.h, self.intelligence)
            else:
                robot = Robot(self, self.grid.find_empty(), self.w, self.h, self.intelligence)
            
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)
            self.robot_list.append(robot)
        
        for i in range(boxes):
            x = self.random.randrange(0, self.w)
            y = self.random.randrange(0, self.h)
            if self.grid.is_cell_empty((x, y)):
                caja = Caja(self, (x, y))                
            else:
                caja = Caja(self, self.grid.find_empty())
            self.matrix[caja.pos[1]][caja.pos[0]] = 0

            self.grid.place_agent(caja, caja.pos)
            self.schedule.add(caja)
            self.box_list.append(caja)
                
        for i in range(shelves):
            x = self.random.randrange(0, self.w)
            y = self.random.randrange(0, self.h)
            if self.grid.is_cell_empty((x, y)):
                estante = Estante(self, (x, y))
            else:
                estante = Estante(self, self.grid.find_empty())
            self.matrix[estante.pos[1]][estante.pos[0]] = 0
            
            self.grid.place_agent(estante, estante.pos)
            self.schedule.add(estante)
            self.shelf_list.append(estante)
            
        #print(self.matrix)
         # Recolector de información: procentaje de celdas limpiadas
        #self.boxesleft = self.count_type(self)
        self.time_datacollector = DataCollector({"Tiempo transcurrido": lambda m: self.step_counter})
        #self.datacollector = DataCollector({"Porcentaje de celdas limpias": lambda m: ((width*height)-self.count_type(m)) * 100 / (width*height)})
       #self.boxes_datacollector = DataCollector({"Cantidad de cajas recogidas": lambda m: (self.boxesleft-self.count_type(m))})
        self.move_datacollector = DataCollector({"Movimientos realizados": lambda m: self.move_counter})
    # Método para contar cantidad de celdas en cierto estado
    
    @staticmethod
    def count_type(model):
        count = 0
        for box in model.schedule.agents:
            if type(box) == Caja:
                count += 1
        return count
    
    def step(self):
        self.step_counter += 1
        self.schedule.step()
        self.time_datacollector.collect(self)
        #self.boxes_datacollector.collect(self)
        self.move_datacollector.collect(self)
        #print("cuenta cajas", self.count_type(self))
        #print("cuenta apiladas", self.boxstack_counter)
        if self.step_counter >= self.time_limit or self.count_type(self)==self.boxstack_counter:
            self.running = False
            
def agent_portrayal(agent):
    if type(agent) == Caja:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": agent.color, "Layer": 0}
    
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
        return {"Shape": "circle", "r": 1, "Filled": "true", "Color": agent.color, "Layer": 3}

"""
grid = CanvasGrid(agent_portrayal, 30, 30, 450, 450)

# Creación de tabla que grafica datacollector
#
#chart_cajas = ChartModule([{"Label": "Cantidad de cajas restante", "Color": "Black"}], data_collector_name='boxes_datacollector')
#
chart_tiempo = ChartModule([{"Label": "Tiempo transcurrido", "Color": "Black"}], data_collector_name='time_datacollector')
chart_movimientos = ChartModule([{"Label": "Movimientos realizados", "Color": "Black"}], data_collector_name='move_datacollector')

server = ModularServer(Room, [grid, chart_tiempo, chart_movimientos], "Equipo 10 - Evidencia 1. Actividad Integradora",
                        {"width": UserSettableParameter(
                            "slider", "Anchura", 30, 1, 30, 1),
                        "height": UserSettableParameter(
                            "slider", "Altura", 30, 1, 30, 1),
                        "space_rows": UserSettableParameter(
                            "number", "Espacio entre filas", 3),
                        "space_cols": UserSettableParameter(
                            "number", "Espacio entre columnas", 3),
                        "length_wall": UserSettableParameter(
                            "number", "Largo de muros", 3),
                        "robots": UserSettableParameter(
                            "number", "Número de agentes", 10),
                        "boxes": UserSettableParameter(
                            "number", "Número de cajas", 5),
                        "shelves": UserSettableParameter(
                            "number", "Número de estantes", 1),
                        "time_limit": UserSettableParameter(
                            "number", "Tiempo máximo de ejecución", 50),
                        "intelligence": UserSettableParameter(
                            "checkbox", "Omnisciencia de robots", False)})
server.port = 8522
server.launch()
"""