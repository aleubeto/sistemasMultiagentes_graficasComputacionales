# %%
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np
from mesa import Agent, Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

# %%
class Boid(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = pos
        self.model = model
        self.heading = np.random.uniform(-1, 1, 2)

    def coherence(self, neighbors):
        if len(neighbors) == 0:
            return self.heading

        overall_distance = np.zeros(2)
        for neighbor in neighbors:
            overall_distance += neighbor.pos - self.pos

        return overall_distance / len(neighbors)

    def alignment(self, neighbors):
        if len(neighbors) == 0:
            return self.heading

        overall_heading = np.zeros(2)
        for neighbor in neighbors:
            overall_heading += neighbor.heading

        return overall_heading / len(neighbors)

    def separation(self, neighbors):
        if len(neighbors) == 0:
            return self.heading
        separation_vector = np.zeros(2)
        for neighbor in neighbors:
            if self.model.space.get_distance(self.pos, neighbor.pos) < 8:
                separation_vector += neighbor.pos - self.pos
        return separation_vector / len(neighbors)

    def step(self):
        neighbors = self.model.space.get_neighbors(self.pos, 10, False)
        self.heading = (
            self.heading 
            + self.coherence(neighbors) * 0.25
            + self.alignment(neighbors) * 0.05 
            - self.separation(neighbors) * 0.25
            ) / 3
        self.heading = self.heading / np.linalg.norm(self.heading)
        new_pos = self.pos + self.heading * 1 # 1 is the speed
        self.model.space.move_agent(self, new_pos) 
        

# %%
class Sky(Model):
    def __init__(self):
        super().__init__()
        self.space = ContinuousSpace(50, 50, True)
        self.schedule = RandomActivation(self)

        for id in range(1, 101):
            pos = np.random.randint(0, 50, 2)
            boid = Boid(id, self, pos)
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()

# %%
from SimpleContinuousModule import SimpleCanvas

def boid_draw(agent):
    return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Brown"}

canvas = SimpleCanvas(boid_draw, 600, 600)

model_params = {}

server = ModularServer(Sky, [canvas], "Boids", model_params)
server.port = 8522
server.launch()