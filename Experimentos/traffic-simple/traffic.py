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
        
        """
        self.aStar(inicial, final)
        for nodo in self.closedList:
            print(nodo.unique_id)
        """
        
    def step(self):
        """
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
        """

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
        self.width = 1800
        self.height = 1200
        self.space = ContinuousSpace(self.width, self.height, False)
        self.schedule = RandomActivation(self)
        self.nodos = []
        """
        self.matrix = [
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 1, 0]
        ]
        """
        
        self.matrix = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        
        """
        for i in range(len(self.matrix)):
            nodo = Nodo(self, np.array([12.5, 2]))
            self.space.place_agent(nodo, nodo.pos)
            self.schedule.add(nodo)
            self.nodos.append(nodo)
        
        
        for i in range(len(self.matrix)):
            print("----------------------------")
            print(i + 1)
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == 1:
                    print(j + 1)
            print("----------------------------")
        """
        
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
        #nodo 1
        nodo = Nodo(self, np.array([906.22 , 15.85 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 2
        nodo = Nodo(self, np.array([943.29, 17.21 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 3
        nodo = Nodo(self, np.array([1283.53 , 14.65 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 4
        nodo = Nodo(self, np.array([1311.69  , 41.11 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 5
        nodo = Nodo(self, np.array([1761.60  , 204.91 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 6
        nodo = Nodo(self, np.array([1779.89 , 238.23  ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 7
        nodo = Nodo(self, np.array([1780.44 , 582.76 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 8
        nodo = Nodo(self, np.array([1778.62 , 621.12 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 9
        nodo = Nodo(self, np.array([1736.14 , 1154.79 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 10
        nodo = Nodo(self, np.array([1707.37 , 1180.24 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 11
        nodo = Nodo(self, np.array([1099.87 , 1170.77 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 12
        nodo = Nodo(self, np.array([1060.94 , 1177.68 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 13
        nodo = Nodo(self, np.array([822.37 , 1175.17 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 14
        nodo = Nodo(self, np.array([784.07 , 1171.40 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 15
        nodo = Nodo(self, np.array([386.15 , 1185.39 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 16
        nodo = Nodo(self, np.array([352.48 , 1170.86 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 17
        nodo = Nodo(self, np.array([25.40 , 882.06 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 18
        nodo = Nodo(self, np.array([16.11 , 848.49 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 19
        nodo = Nodo(self, np.array([20.40 , 521.63 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 20
        nodo = Nodo(self, np.array([21.25 , 485.63 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 21
        nodo = Nodo(self, np.array([170.33 , 40.06 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 22
        nodo = Nodo(self, np.array([198.62 , 15.21 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 23
        nodo = Nodo(self, np.array([675.42 , 21.78 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 24
        nodo = Nodo(self, np.array([712.58 , 9.78 ]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 25
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 26
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 27
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 28
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 29
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 30
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 31
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 32
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 33
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 34
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 35
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 36
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 37
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 38
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 39
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 40
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 41
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 42
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 43
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 44
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 45
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 46
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 47
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 48
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 49
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 50
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 51
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 52
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 53
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 54
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 55
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 56
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 57
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 58
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 59
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 60
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 61
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 62
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 63
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 64
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 65
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 66
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 67
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 68
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 69
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 70
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 71
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        #nodo 72
        nodo = Nodo(self, np.array([12.5, 2]))
        self.space.place_agent(nodo, nodo.pos)
        self.schedule.add(nodo)
        self.nodos.append(nodo)
        
        
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
        """
        
        car = Car(self, np.array([12.5, 1]), np.array([0.1, 0.1]), self.nodos[0], self.nodos[12])
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
