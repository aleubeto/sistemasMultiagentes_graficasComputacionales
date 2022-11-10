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
        
        for i in range(10):
            robot = Robot(self, (1, 1))
            self.grid.place_agent(robot, robot.pos)
            self.schedule.add(robot)
        
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
        if self.schedule.time == 25:
            self.running = False
        self.schedule.step()

def agent_portrayal(agent):
    if type(agent) == WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    
    elif type(agent) == Robot:
        return {"Shape": "Imagenes/ghost.png", "Layer": 0}

grid = CanvasGrid(agent_portrayal, 17, 14, 450, 450)

server = ModularServer(Maze, [grid], "PacMan", {})
server.port = 8522
server.launch()
