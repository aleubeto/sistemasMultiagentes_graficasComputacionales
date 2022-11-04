from mesa import Agent, Model
from mesa.space import Grid
from mesa.time import RandomActivation
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid as pathGrid
from pathfinding.finder.a_star import AStarFinder

#Mesa se compone de dos elementos principales: un Modelo y un Agente. Un Modelo es una corrida de una simulación, 
#es el master, el global, el entorno, donde actúan los agentes. Un Agente es un elemento atómico en una simulación.
#Un Modelo tiene un grid, que vendría a representar un tablero donde se mueven los agentes y un scheduler, que rige
#los eventos que transcurren en la simulación y su orden.
#Un agente tiene atributos y realiza una acción en un step, que vendria a ser un tick que cada que ocurre puede pasar
#algo en la simulacion.

#------------------------ INICIA LA PARTE "DURA", AQUÍ SE DEFINE LA LÓGICA DE LA SIMULACIÓN ---------------------

#Un Agente llamado Ghost. Es una instancia (subclase?) de la clase de mesa Agent.
class Ghost(Agent):
    
    #Constructor de un Agente Ghost. Recibe self, el modelo en el que va a actuar y una posición.
    def __init__(self, model, pos): 
        
        #crea  el Agente. Le asigna la siguiente id que tenga disponible el modelo y lo asigna al modelo que se
        #pase como parametro.
        super().__init__(model.next_id(), model)
        
        #Asigna la posición del agente como la posición que se pase como parametro.
        self.pos = pos
        
        #Creo un contador iniciado en 0 (esto lo usaré después para el recorrido de pathfinding).
        self.sig = 0
        
        #Se copia la misma matriz que tiene el Modelo de Maze para que el Agente Ghost pueda conocer el entorno
        #en que se mueve.
        self.matrix = [
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
        
        
        #--------------------- INICIA PATHFINDING ---------------------
        
        #Se crea una grid (OJO: no es la misma que tiene el Modelo Maze de Mesa, sino que esta es de la libreria
        #de pathfinding), pero con las mismas dimensiones de altura y ancho que la grid del Modelo. Después se
        #toma la matriz de arriba para determinar el escenario del pathfinding. Sigue las mismas reglas: 1 significa
        #que puede moverse, 0 que no.
        self.grid = pathGrid(width=14, height=17, matrix=self.matrix)
        
        #se define un nodo de inicio dentro de la grid de Pathfinding, el cual tiene como coordenadas las coordenadas
        #de la posicion del Agente Ghost.
        self.start = self.grid.node(self.pos[0], self.pos[1])
        
        #Se define un nodo de fin dentro de la grid de Pathfinding, el cual tiene como coordenadas 1,1 (seleccionadas
        # arbitrariamente).
        self.end = self.grid.node(1, 1)
        
        #Aquí se indica el algoritmo de búsqueda de caminos que se va a implementar. En este caso implementa A*.
        #DiagonalMovement.always significa que se puede mover en 8 direcciones en todo momento. 'never' lo contrario.
        self.finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        
        #Guarda el camino resultante de implementar el algoritmo A* en dos variables:
        #- path es utilizado para guardar el camino óptimo a seguir en un arreglo de coordenadas.
        #- runs guarda 'metadatos' del algoritmo, como la cantidad de corridas necesarias o el tamaño del path.
        self.path, self.runs = self.finder.find_path(self.start, self.end, self.grid)
        
        #Se imprime el camino resultante de forma visual.
        print(self.grid.grid_str(path=self.path, start=self.start, end=self.end))
        
        #Se imprimen los 'metadatos' del algoritmo.
        print('operations:', self.runs, 'path length:', len(self.path))
        
        #--------------------- TERMINA PATHFINDING ---------------------
        
    #Definición de lo que hace en cada step. Recibe self
    def step(self):
        
        #Escanea cuáles son las casillas vecinas a las que podría moverse y las guarda en next_moves. Me parece
        #que lo guarda en un arreglo
        #Self.pos indica que realiza el escaneo a partir de la casilla en que se encuentra actualmente
        #moore me parece que indica movimiento en las 8 direcciones (arriba, abajo, izq, der y 4 esquinas).
        next_moves = self.model.grid.get_neighborhood(self.pos, moore=False)
        
        #Elige una casilla a la cual moverse al azar de entre las casillas que escaneó y guardó en next_move.
        next_move = self.random.choice(next_moves)
        
        #El agente se mueve siguiendo el camino encontrado con pathfinding. En cada step, se mueve hacia las 
        #coordenadas del elemento actual de path, de acuerdo con el contador sig que incrementa en cada step mientras
        #sea menor a la longitud de path.
        if self.sig < len(self.path):
            self.model.grid.move_agent(self, self.path[self.sig])
            self.sig = self.sig + 1
            
        #El agente se mueve dentro de la grid del Modelo hacia la casilla que seleccionó en next_move.
        #Restricción: solo se mueve a esa posición seleccionada si su posición equivalente en la matriz matrix 
        #tiene un '1'.
        #if (self.matrix[next_move[1]][next_move[0]] == 1):
        #    self.model.grid.move_agent(self, next_move)

#Un Agente llamado WallBlock. Es una instancia (subclase?) de la clase de mesa Agent
class WallBlock(Agent):
    
    #Constructor de un Agente WallBlock. Recibe self, el modelo en el que va a actuar y una posición
    def __init__(self, model, pos): 
        
        #Crea  el Agente. Le asigna la siguiente id que tenga disponible el modelo y lo asigna al modelo que se
        #pase como parametro.
        super().__init__(model.next_id(), model)
        
        #Asigna la posición del agente como la posición que se pase como parametro.
        self.pos = pos
    
    #Definición de lo que hace en cada step. Recibe self.
    def step(self):
        
        #Este agente actua como una parte inerte del escenario, así que su única acción es pass.
        pass

#Un Agente llamado Maze. Es una instancia de la clase de mesa Model
class Maze(Model):
    
    #Constructor de un Modelo Maze. Recibe self.
    def __init__(self):
        
        #Crea  el Modelo.
        super().__init__()
        
        #Crea su schedule y lo asigna a que sean activaciones aleatorias. Me imagino que puede tener otro criterio
        #para realizar las activaciones (el profe mencionó round robin).
        self.schedule = RandomActivation(self)
        
        #Crea la grid del Modelo. En el atributo grid del modelo instancía un objeto de tipo Grid con dimensiones de 
        #17 x 14. Torus indica movimiento "circular" (cuando atraviesa un borde del mapa, se teletransporta del lado opuesto).
        self.grid = Grid(17, 14, torus=False)

        #Crea una instancia de un Agente Ghost. Lo asigna a sí mismo (por eso el parametro es self) y le asigna la posición (8, 6).
        ghost = Ghost(self, (8, 6))
        
        #Inserta el Agente recién creado en la grid del Modelo, en la posición que ahora tiene el Agente como atributo.
        self.grid.place_agent(ghost, ghost.pos)
        
        #Añade al Agente dentro de la schedule, por lo que ahora puede realizar acciones en step dentro del modelo.
        self.schedule.add(ghost)
        
        #Se guarda la disposición de muros y caminos libres en una matriz. 0 representa la presencia de un muro, 1 es un camino libre.
        #Es para que el Modelo sepa dónde colocar los muros a continuación.
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
        
        #itera por cada casilla dentro de la matriz
        for _,x,y in self.grid.coord_iter():
            
            #si la el elemento es igual a 0:
            if matrix[y][x] == 0:
                
                #Crea una instancia de un Agente WallBlock. Lo asigna a sí mismo (por eso el parametro es self) y le asigna la posición de la casilla actual.
                wall = WallBlock(self, (x, y))
                
                #Inserta el Agente recién creado en la grid del Modelo, en la posición que ahora tiene el Agente como atributo.
                self.grid.place_agent(wall, wall.pos)
                
                #Añade al Agente dentro de la schedule, por lo que ahora puede realizar acciones en step dentro del modelo.
                self.schedule.add(wall)
    
    #Definición de lo que hace en cada step. Recibe self.
    def step(self):
        
        #Parece un poco redundante, pero aqui es cuando hace el step. Por decir, entiendo que el step pasa de manera
        #global y tanto el Modelo como los Agentes pueden realizar diferentes cosas en un step. Lo que hace aquí es que
        #por cada step, lo propaga hacia lo que esté en el scheduler para que también eso realice su acción de step cuando
        #sea su turno.
        self.schedule.step()

#------------------------ TERMINA LA PARTE "DURA", AQUÍ SE DEFINE LA LÓGICA DE LA SIMULACIÓN ---------------------


#------------------------ INICIA LA PARTE "DE ESTILO", AQUÍ SE DEFINE LA APARIENCIA DE LA SIMULACIÓN ---------------------

#Aquí se define la apariencia que tendrá cada agente.
def agent_portrayal(agent):
    
    #Caso en que se trata de un Agente WallBlock.
    if type(agent) == WallBlock:
        
        #Se le otorga una figura, que es un rectangulo de 1x1, lleno y de color gris, y la capa en la que se encuentra, para manejar su visibilidad (tal vez colisiones también?)
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    
    #Caso en que se trata de un Agente Ghost.
    elif type(agent) == Ghost:
        
        #Se le otorga una figura, que es un png, y la capa en la que se encuentra, para manejar su visibilidad (tal vez colisiones también?)
        return {"Shape": "ghost.png", "Layer": 0}

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