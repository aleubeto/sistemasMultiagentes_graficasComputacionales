from mesa import Agent, Model
from mesa.space import Grid
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as pathGrid
from pathfinding.finder.a_star import AStarFinder

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
        
        paso = True
        
        for element in self.model.grid.iter_cell_list_contents(next_move):
            if type(element) == Robot:
                paso = False
                
        if paso:
            self.model.grid.move_agent(self, next_move)

class WallBlock(Agent):
    
    def __init__(self, model, pos): 
        super().__init__(model.next_id(), model)
        self.pos = pos
    
    def step(self):
        pass

class Maze(Model):
    
    def __init__(self):
        
        super().__init__()
        
        self.schedule = RandomActivation(self)
        
        self.grid = MultiGrid(17, 14, torus=False)

        robot = Robot(self, (1, 1))
        robot2 = Robot(self, (1, 1))
        
        self.grid.place_agent(robot, robot.pos)
        self.grid.place_agent(robot2, robot2.pos)
        self.schedule.add(robot)
        self.schedule.add(robot2)
        
        matrix = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
            [0,1,0,1,0,0,0,1,1,1,0,1,0,1,0,1,0],
            [0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0],
            [0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0],
            [0,1,0,1,0,1,0,0,0,0,0,1,1,1,0,1,0],
            [0,1,1,1,0,1,0,1,1,1,0,1,0,1,0,1,0],
            [0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0],
            [0,1,0,1,1,1,0,0,1,0,0,1,0,1,1,1,0],
            [0,1,0,0,0,1,1,1,1,1,1,1,0,0,0,1,0],
            [0,1,1,1,0,1,0,0,0,0,0,1,0,1,1,1,0],
            [0,1,0,1,0,1,0,1,1,1,0,0,0,1,0,1,0],
            [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        
        for _,x,y in self.grid.coord_iter():
            
            if matrix[y][x] == 0:
                
                wall = WallBlock(self, (x, y))
                
                self.grid.place_agent(wall, wall.pos)
                
                self.schedule.add(wall)
    
    def step(self):
        
        self.schedule.step()

#Aquí se define la apariencia que tendrá cada agente.
def agent_portrayal(agent):
    
    #Caso en que se trata de un Agente WallBlock.
    if type(agent) == WallBlock:
        
        #Se le otorga una figura, que es un rectangulo de 1x1, lleno y de color gris, y la capa en la que se encuentra, para manejar su visibilidad (tal vez colisiones también?)
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    
    #Caso en que se trata de un Agente Ghost.
    elif type(agent) == Robot:
        
        #Se le otorga una figura, que es un png, y la capa en la que se encuentra, para manejar su visibilidad (tal vez colisiones también?)
        return {"Shape": "Imagenes/ghost.png", "Layer": 0}

#Aquí se define cómo se mostrara la grid de la simulación. Primero va la apariencia de los agentes, después el tamaño
#de la grid en x y y. Después va el tamaño del recuadro que se mostrará en la representación web.
grid = CanvasGrid(agent_portrayal, 17, 14, 450, 450)

#------------------------ TERMINA LA PARTE "DE ESTILO", AQUÍ SE DEFINE LA APARIENCIA DE LA SIMULACIÓN ---------------------


#------------------------ INICIA LA PARTE "DEL SERVIDOR", AQUÍ SE DEFINE EN QUÉ MEDIO SE DESPLIEGA LA SIMULACIÓN ---------------------

#Crea un servidor modular utilizando como modelo Maze (el cual también incluye sus Agentes), la grid que se va a emplear, el nombre
#del sitio que se va a generar y no sé que haga '{}'.
server = ModularServer(Maze, [grid], "PacMan", {})

#Se asigna un puerto en el que se va a mostrar la simulación.
server.port = 8522

#Finalmente se lanza la simulación.
server.launch()
#------------------------ TERMINA LA PARTE "DEL SERVIDOR", AQUÍ SE DEFINE EN QUÉ MEDIO SE DESPLIEGA LA SIMULACIÓN ---------------------