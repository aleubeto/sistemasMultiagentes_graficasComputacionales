# Advertencia: ejecutar archivo dentro de la carpeta traffic-simple

import numpy as np
import random

from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer

from SimpleContinuousModule import SimpleCanvas

class Car(Agent):
    def __init__(self, model: Model, pos, speed):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.speed = speed
        self.accelerating = True

    def step(self):

        # Imprimir coordenadas de auto azul
        '''if (self.unique_id == 1):
            neigbors = []
            for i in self.model.space.get_neighbors(self.pos,1):
                neigbors.append(i.unique_id)
            #print(f'{self.unique_id}: {self.pos}, {self.speed[0]}, {neigbors}')
            print(f'{self.unique_id}: {neigbors}')'''

        neigbors = []
        for i in self.model.space.get_neighbors(self.pos,2):
            neigbors.append(i.unique_id)
        #print(f'{self.unique_id}: {self.pos}, {self.speed[0]}, {neigbors}')
        print(f'{self.unique_id}: {neigbors}')

        # Detección de autos en frente
        #car_ahead = self.car_ahead()

        # Aceleración y desaceleración
        #new_speed = self.accelerate() if car_ahead == None else self.decelerate(car_ahead)
        new_speed = self.accelerate()
        if new_speed >= 1.0:
            new_speed = 1.0
            self.accelerating = False
        elif new_speed <= 0.0:
            new_speed = 0.0
            self.accelerating = True

        # Movimiento de vehículos
        self.speed = np.array([new_speed, 0.0])
        new_pos = self.pos + np.array([0.5,0]) * self.speed
        self.model.space.move_agent(self, new_pos)

    def car_ahead(self):
        for neighbor in self.model.space.get_neighbors(self.pos,1):
            if neighbor.pos[0] > self.pos[0]:
                return neighbor
            return None

    # Método de aceleración
    def accelerate(self):
        return self.speed[0] + 0.05

    # Método de desaceleración
    def decelerate(self):
        return self.speed[0] - 0.1

class Street(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(25, 25, True)
        self.schedule = RandomActivation(self)

        # Creación de carro inicial de color azul
        first = True
        px = 12
        py = 12

        car = Car(self, np.array([px,py]), np.array([1.0,0.0]))
        self.space.place_agent(car, car.pos)
        self.schedule.add(car)
        car2 = Car(self, np.array([px,py-2]), np.array([1.0,0.0]))
        self.space.place_agent(car2, car2.pos)
        self.schedule.add(car2)
        car3 = Car(self, np.array([px+2,py]), np.array([1.0,0.0]))
        self.space.place_agent(car3, car3.pos)
        self.schedule.add(car3)
        car4 = Car(self, np.array([px,py+2]), np.array([1.0,0.0]))
        self.space.place_agent(car4, car4.pos)
        self.schedule.add(car4)
        car5 = Car(self, np.array([px-2,py]), np.array([1.0,0.0]))
        self.space.place_agent(car5, car5.pos)
        self.schedule.add(car5)

        '''for px in np.random.choice(25 + 1, 5, replace=False):
            if first:
                car = Car(self, np.array([px,py]), np.array([1.0,0.0]))
                first = False
            else:
                car = Car(self, np.array([px,py]), np.array([random.randrange(2,7,2)/10,0.0]))
            # self.random.random() para velocidades aleatorias
            py+=2
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)'''

    def step(self):
        self.schedule.step()

def car_draw(agent):
    color = "Blue" if agent.unique_id == 1 else "Brown"
    return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}

canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
