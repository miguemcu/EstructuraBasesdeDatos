import statistics

class Nodo:
    def __init__(self, datos, izquierda, derecha):
        self.datos = datos # Un array que puede guardar uno o más puntos
        self.izquierda = izquierda
        self.derecha = derecha
        
class KD_Tree:
    def __init__(self, puntos):
        self.raiz = self.construir_arbol(puntos, 0)
    
    def construir_arbol(self, puntos, nivel):
        if not puntos:
            return None
        
        # Alternar entre 0,1,2... para el eje x,y,z...
        eje = nivel % len(puntos[0])
        
        
        # Una vez elegido el eje (x, y, z...), construyo un array solo con los datos de ese eje para sacar la mediana
        coordenadas_eje = [punto[eje] for punto in puntos]
        mediana = statistics.median_high(coordenadas_eje)
        
        datos_nodo = []
        for punto in puntos:
            if punto[eje] == mediana:
                datos_nodo.append(punto)
                puntos.remove(punto)
        
        puntos_izq = [punto for punto in puntos if punto[eje] < mediana]
        puntos_der = [punto for punto in puntos if punto[eje] > mediana]
        
        izquierda = self.construir_arbol(puntos_izq, nivel+1)
        derecha = self.construir_arbol(puntos_der, nivel+1)
        
        return Nodo(datos_nodo, izquierda, derecha)
      
puntos = [(3,4), (2,3), (5,7), (8,1)]
arbol = KD_Tree(puntos)
print(arbol.raiz.izquierda.izquierda.datos)
    