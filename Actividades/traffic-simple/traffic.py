# Advertencia: ejecutar archivo dentro de la carpeta traffic-simple

import numpy as np

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

    def step(self):

        # Imprimir coordenadas de auto azul
        if (self.unique_id == 1):
            print(self.pos)

        # Movimiento de vehículos
        new_pos = self.pos + np.array([0.5,0]) * self.speed
        self.model.space.move_agent(self, new_pos)

class Street(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(25, 10, True)
        self.schedule = RandomActivation(self)

        for px in np.random.choice(25 + 1, 5, replace=False):
            # self.random.random() para velocidades aleatorias
            car = Car(self, np.array([px, 5]), np.array([self.random.random(), 0.0]))
            self.space.place_agent(car, car.pos)
            self.schedule.add(car)

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
