from mesa import Agent, Model
from mesa.space import ContinuousSpace

openList = []
closedList = []

def encontrar_adyacentes(actual, openList, closedList, matrizAdy, n, modelo):
    for i in range(len(matrizAdy[actual.unique_id])):
        if matrizAdy[actual.unique_id][i] == 1 and modelo.nodos[i] in openList == False and modelo.nodos[i] in closedList == False:
            openList.append(modelo.nodos[i])
            

def encontrar_menor(openList, final):
    menor = 25
    for nodo in openList:
        comparar = nodo.model.space.get_distance(nodo, final) 
        if comparar < menor:
            nodoMenor = nodo
            menor = comparar
    return nodoMenor
    
        

def aStar(matrizAdy, inicial, final, modelo):
    openList.append(inicial)
    while (len(openList) > 0 and actual != final):
        actual = encontrar_menor(openList, final)
        openList.clear()
        encontrar_adyacentes(actual, openList, closedList, matrizAdy, len(matrizAdy), modelo)
        openList.remove(actual)
        closedList.append(actual)
    
    return closedList