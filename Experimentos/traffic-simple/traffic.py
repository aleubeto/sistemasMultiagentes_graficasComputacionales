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
        #Crea una variable donde va a guardar al auto que tenga en frente este auto, si
        #es que hay uno o None si no no hay.
        car_ahead = self.car_ahead()
        
        #Crea una nueva velocidad para el auto. Para eso usa dos funciones, accelerate y
        #decelerate. Si accelerating es verdadero, acelera. En caso contrario desacelera.
        new_speed = self.accelerate() if car_ahead == None else self.decelerate(car_ahead)
        #Las siguientes dos condiciones lo que hacen es mantener la velocidad del auto
        #siempre entre 0 y 1.
        #Si la nueva velocidad es igual o mayor a uno, la fija en uno.
        if new_speed >= 1.0:
            new_speed = 1.0
        #Si la nueva velocidad es igual o menor a cero, la fija en cero y comienza a acelerar.
        elif new_speed <= 0.0:
            new_speed = 0.0
            
        #La velocidad actual ahora es igual a esa nueva velocidad.
        self.speed = np.array([new_speed, 0.0])
        
        #Crea una nueva posicion del auto.
        #Para eso, lo que hace es que  a la posicion actual le suma la multiplicacion de
        #vectores de la velocidad por un factor de escala. Ojo, en x es 0.3 y 0 en y porque
        #solo se mueve en un eje.
        new_pos = self.pos + np.array([0.3, 0.0]) * self.speed
        #Coloca el agente en esa nueva posicion
        self.model.space.move_agent(self, new_pos)
        
    #funcion para detectar si hay un auto al frente.
    def car_ahead(self):
        #escanea todos los vecinos de este auto en un radio de 1 unidad.
        for neighbor in self.model.space.get_neighbors(self.pos, 1):
            #si la posicion en x del vecino es mayor que la posicion en x del auto,
            #significa que esta en frente del mismo.
            if neighbor.pos[0] > self.pos[0]:
                #regresa al vecino
                return neighbor
        #en caso contrario, regresa None
        return None
    
    #funcion de acelerar. Regresa la velocidad de x incrementada en 0.05.
    def accelerate(self):
        return self.speed[0] + 0.05
    
    #funcion de acelerar. Regresa la velocidad de x disminuida en 0.1.
    def decelerate(self, car_ahead):
        return car_ahead.speed[0] - 0.1

#Modelo de la calle
class Street(Model):
    #Constructor de la calle.
    def __init__(self):
        super().__init__()
        
        #Va a crear un continuous space de 25 x 10 con toroide verdadero
        self.space = ContinuousSpace(25, 10, True)
        #El schedule va a tener el modo de RandomActivation
        self.schedule = RandomActivation(self)
        
        #crea un booleano y lo declara como verdadero. Este booleano
        #se va a usar para detectar al primer auto.
        first = True
        #posicion en y guardada como variable. Ahora empieza en 1 y va a incrementar.
        py = 1
        
        #por cada posicion en x generada aleatoriamente:
        #px - posicion en x generada aleatoriamente. Elegida de entre 5 numeros del 0 al 25 sin repetir.
        for px in np.random.choice(25 + 1, 5, replace=False):
            #si la variable true es verdadera:
            if first:
                #crea un auto con una posicion de (px, py). Es decir, este auto va a estar sobre el 1 en el
                #eje y. Va a tener una velocidad de 1 en el eje x y 0 en el y.
                car = Car(self, np.array([px, py]), np.array([1.0, 0.0]))
                #cambia a falso first porque ya se creo el primer auto
                first = False
            else:
                #Crea un auto con una posicion de (px, py). Es decir, este auto va a estar sobre el py en el
                # eje y. Como velocidad, le asigna un numero aleatorio del 2 al 7 con pasos de 2 y dividido
                #entre 10. Es decir, las velocidades posibles van a ser 0.2, 0.4 y 0.6
                car = Car(self, np.array([px, py]), np.array([self.random.randrange(2, 7, 2)/10, 0.0]))
            #Incrementa py en 2. Esto es para ir construyendo los autos cada vez mas abajo
            #py += 2
            
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
canvas = SimpleCanvas(car_draw, 500, 500)

model_params = {}

server = ModularServer(Street, [canvas], "Traffic", model_params)
server.port = 8522
server.launch()
