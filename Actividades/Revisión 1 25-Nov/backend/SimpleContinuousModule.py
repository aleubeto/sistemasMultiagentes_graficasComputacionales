#importa lo necesario para visualizar la simulacion
from mesa.visualization.ModularVisualization import VisualizationElement

#definicion de la clase simpleCanvas. Hereda de visualizationElement asi como
#auto hereda de agente y calle de modelo. Esta es la que se utiliza en traffic.py
class SimpleCanvas(VisualizationElement):
    #incluye el archivo js que viene tambien en la carpeta
    local_includes = ["simple_continuous_canvas.js"]
    #No asume ningun metodo de representacion predeterminado
    portrayal_method = None
    #asigna las dimensiones del canvas
    canvas_height = 1200
    canvas_width = 1800
    
    #constructor del canvas. Recibe self, un metodo de representacion y las dimensiones.
    def __init__(self, portrayal_method, canvas_height=1200, canvas_width=1800):
        """
        Instantiate a new SimpleCanvas
        """
        #asigna como atributos propios los que acaba de agarrar
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        
        #Lo siguiente es para conectarse con el archivo js. Lo que pasa aqui
        #es que new_element esta guardando una instruccion que va a entender el js.
        #Es basicamente un nuevo objeto (new) de tipo Simple_Continuous_Module que va a
        #tener dos parametros, los cuales se pasan con format: ancho y alto. 
        #en donde va cada '{}' corresponde un atributo de format.
        new_element = "new Simple_Continuous_Module({}, {})".format(
            self.canvas_width, self.canvas_height
        )
        #hace la llamada al codigo de java, lo "pushea" a elements que esta en el archivo .js
        self.js_code = "elements.push(" + new_element + ");"
        
    #funcion para renderizar el canvas. Recibe el modelo
    def render(self, model):
        #empieza con un arreglo vacio de space state
        space_state = []
        #por cada agente del modelo
        for obj in model.schedule.agents:
            #Representa al agente de acuerdo con el metodo de representacion que esta en el modelo,
            #el cual a su vez utiliza draw rectangle del archiv js.
            portrayal = self.portrayal_method(obj)
            #guarda en x y en y la posicion del agente que esta iterando
            x, y = obj.pos
            #convierte la posicion de la simulacion en una posicion dentro del canvas
            x = (x - model.space.x_min) / (model.space.x_max - model.space.x_min)
            y = (y - model.space.y_min) / (model.space.y_max - model.space.y_min)
            #pasa esas posiciones del canvas al metodo de representacion
            portrayal["x"] = x
            portrayal["y"] = y
            #añade esta representacion al arreglo space_state, el cual contiene la representacion
            #grafica de tods los agentes de la simulacion
            space_state.append(portrayal)
            
        #regresa este arreglo
        return space_state
