import numpy as np

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer


from SimpleContinuousModule import SimpleCanvas

class Car(Agent):
    def __init__(self, model: Model, pos, speed, inicial, final):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.speed = speed
        #self.objetivos = objetivos
        self.contador = 0;
        self.contadorNodos = 0;
        self.openList = []
        self.closedList = []
        self.aStar(inicial, final)
        
    def step(self):
        car_ahead = self.car_ahead()
        
        new_speed = self.accelerate() if car_ahead == None else self.decelerate(car_ahead)
        if new_speed >= 1.0:
            new_speed = 1.0
        elif new_speed <= 0.0:
            new_speed = 0.0
         
        self.speed = np.array([new_speed, new_speed])
        
        if self.contadorNodos >= len(self.closedList):
            return
        
        if self.model.space.get_distance(self.pos, self.closedList[self.contadorNodos].pos) > 0.1:
            if self.pos[0] >= 0 and self.pos[0] < self.model.width and self.pos[1] >= 0 and self.pos[1] < self.model.height:
                self.pos += (self.closedList[self.contadorNodos].pos - self.pos) * self.speed * self.contador
                self.model.space.move_agent(self, self.pos)
                self.contador += 0.1
        else:
            self.contadorNodos += 1
            self.contador = 0

    def encontrar_adyacentes(self, actual):
        indice_actual = actual.unique_id - 1
        for i in range(len(self.model.matrix[indice_actual])):
            if self.model.matrix[indice_actual][i] == 1:
                if self.model.nodos[i] in self.closedList:
                    continue
                    
                self.openList.append(self.model.nodos[i])


    def encontrar_menor(self, final):
        menor = 25
        for nodo in self.openList:
            comparar = nodo.model.space.get_distance(nodo.pos, final.pos) 
            if comparar < menor:
                nodoMenor = nodo
                menor = comparar
        return nodoMenor

    def aStar(self, inicial, final):
        actual = inicial
        self.openList.append(inicial)
        while (len(self.openList) > 0 and actual != final):
            actual = self.encontrar_menor(final)
            self.openList.clear()
            self.encontrar_adyacentes(actual)
            self.closedList.append(actual)
                
    def car_ahead(self):
        for neighbor in self.model.space.get_neighbors(self.pos, 1):
            if type(neighbor) == Car:
                if neighbor.pos[0] > self.pos[0] or neighbor.pos[1] > self.pos[1]:
                    return neighbor
        return None
    
    def accelerate(self):
        return self.speed[0] + 0.05
    
    def decelerate(self, car_ahead):
        return car_ahead.speed[0] - 0.1
    
class Nodo(Agent):
    def __init__(self, model: Model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        
    def step(self):
        pass
        
class Street(Model):
    def __init__(self):
        super().__init__()
        self.width = 25
        self.height = 10
        self.space = ContinuousSpace(self.width, self.height, False)
        self.schedule = RandomActivation(self)
        self.matrix = [
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0]
        ]
        self.nodos = []
        
        """
        first = True
        py = 1
        
        for px in np.random.choice(25 + 1, 5, replace=False):
            if first:
                car = Car(self, np.array([px, py]), np.array([1.0, 0.0]))
                first = False
            else:
                car = Car(self, np.array([px, py]), np.array([self.random.randrange(2, 7, 2)/10, 0.0]))
            py += 2
            
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)
        """
        
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        nodo1 = Nodo(self, np.array([12.5, 6]))
        self.space.place_agent(nodo1, nodo1.pos)
        self.schedule.add(nodo1)
        nodo2 = Nodo(self, np.array([6, 4]))
        self.space.place_agent(nodo2, nodo2.pos)
        self.schedule.add(nodo2)
        nodo3 = Nodo(self, np.array([4, 8]))
        self.space.place_agent(nodo3, nodo3.pos)
        self.schedule.add(nodo3)
        nodo4 = Nodo(self, np.array([10, 9]))
        self.space.place_agent(nodo4, nodo4.pos)
        self.schedule.add(nodo4)
        nodo5 = Nodo(self, np.array([16, 5]))
        self.space.place_agent(nodo5, nodo5.pos)
        self.schedule.add(nodo5)
        nodo6 = Nodo(self, np.array([21, 4]))
        self.space.place_agent(nodo6, nodo6.pos)
        self.schedule.add(nodo6)
        
        self.nodos = [nodo, nodo1, nodo2, nodo3, nodo4, nodo5, nodo6]
        
        car = Car(self, np.array([12.5, 1]), np.array([0.1, 0.1]), nodo4, nodo6)
        self.space.place_agent(car, car.pos)
        self.schedule.add(car)
        
        """
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    self.matrix[i][j] = self.space.get_distance(self.nodos[i].pos, self.nodos[j].pos)
                    
        print(self.matrix)
        """
        
    def step(self):
        self.schedule.step()

def car_draw(agent):
    if type(agent) == Car:
        color = "Blue" if agent.unique_id == 1 else "Brown"
        return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}
    elif type(agent) == Nodo:
        return {"Shape": "rect", "w": 0.02, "h": 0.02, "Filled": "true", "Color": "Red"}

canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
