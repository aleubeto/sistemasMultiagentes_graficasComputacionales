#importa numpy como np
import numpy as np

#Todas las librerias que usamos de mesa
from mesa import Agent, Model
#Esta es nueva y sustituye a grid
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.visualization.ModularVisualization import ModularServer

#Del archivo de python homonimo
from SimpleContinuousModule import SimpleCanvas

#Clase de auto
class Car(Agent):
    #Su constructor. Recibe el modelo, la posicion y la velocidad.
    def __init__(self, model: Model, pos, speed):
        #Cuando se llama al constructor, crea un auto con la siguiente ID que tenga
        #disponible el modelo y lo asigna a ese mismo modelo.
        super().__init__(model.next_id(), model)
        #Asigna los valores de posicion y velocidad
        self.pos = pos
        self.speed = speed
        
    #Step del auto
    def step(self):
        #Crea una nueva posicion del auto.
        #Para eso, lo que hace es que  a la posicion actual le suma la multiplicacion de
        #vectores de la velocidad por un factor de escala. Ojo, en x es 0.5 y 0 en y porque
        #solo se mueve en un eje.
        new_pos = self.pos + np.array([1,0]) * self.speed
        #Coloca el agente en esa nueva posicion
        self.model.space.move_agent(self, new_pos)

#Modelo de la calle
class Street(Model):
    #Constructor de la calle.
    def __init__(self):
        super().__init__()
        #Va a crear un continuous space de 25 x 10 con toroide verdadero
        self.space = ContinuousSpace(1000, 1000, True)
        #El schedule va a tener el modo de RandomActivation
        self.schedule = RandomActivation(self)
        
        #por cada posicion en x generada aleatoriamente:
        #px - posicion en x generada aleatoriamente. Elegida de entre 5 numeros del 0 al 25 sin repetir.
        for px in np.random.choice(1000 + 1, 5, replace=False):
            #Crea un auto con una posicion de (px, 5). Es decir, todos van a estar fijos en el eje y.
            #Como velocidad, le asigna 1 en el eje x y 0 en el y.
            car = Car(self, np.array([px, 5]), np.array([1.0, 0.0]))
            #Coloca al agente en el espacio en la posicion asignada.
            self.space.place_agent(car, car.pos)
            #Agrega el auto al schedule
            self.schedule.add(car)

    #Step del modelo
    def step(self):
        #Simplemente lo propaga
        self.schedule.step()

#Forma en que el modelo representa a los agentes
def car_draw(agent):
    #Basicamente, al auto con la ID de 1 le asigna el color azul. Los demas son cafes
    color = "Blue" if agent.unique_id == 1 else "Brown"
    #Los crea como rectangulos de 0.034 * 0.02
    return {"Shape": "rect", "w": 0.034, "h": 0.02, "Filled": "true", "Color": color}

#Lo de siempre todo de aqui para abajo
canvas = SimpleCanvas(car_draw, 1000, 1000)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
