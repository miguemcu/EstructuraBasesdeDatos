import statistics
from geopy.distance import geodesic

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
        
        # Los puntos que caen exactamente en la mediana se quedan en este nodo
        datos_nodo = [punto for punto in puntos if punto[eje] == mediana]
        puntos_restantes = [punto for punto in puntos if punto[eje] != mediana]
        
        # El resto se separa según quede a la izquierda o a la derecha del corte
        puntos_izq = [punto for punto in puntos_restantes if punto[eje] < mediana]
        puntos_der = [punto for punto in puntos_restantes if punto[eje] > mediana]
        
        izquierda = self.construir_arbol(puntos_izq, nivel+1)
        derecha = self.construir_arbol(puntos_der, nivel+1)
        
        return Nodo(datos_nodo, izquierda, derecha)
    
    def buscar_mas_cercano(self, punto, nodo=None, nivel=0, mejor_punto=None, mejor_distancia=float('inf')):
        if nodo is None:
            nodo = self.raiz # Si no me pasan nodo, empiezo por la raiz
        
        if nodo is None:
            return None, float('inf')
        
        # Primero reviso los puntos guardados en el nodo actual
        for dato in nodo.datos:
            distancia = geodesic(punto, dato).m
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_punto = dato
        
        eje = nivel % len(punto)
        coordenada_corte = nodo.datos[0][eje]
        
        # Elijo primero la rama que tiene probablemente esté más cerca
        if punto[eje] < coordenada_corte:
            rama_cercana = nodo.izquierda # Si estoy a la izquierda del corte, busco primero rama izquierda
            rama_lejana = nodo.derecha # La otra queda por si depronto
        else:
            rama_cercana = nodo.derecha # Si estoy a la derecha del corte, entro primero por derecha
            rama_lejana = nodo.izquierda # La contraria se evalua solo si vale la pena
        
        if rama_cercana is not None:
            mejor_punto, mejor_distancia = self.buscar_mas_cercano(punto, rama_cercana, nivel+1, mejor_punto, mejor_distancia)
        
        # Lo que vendría siendo la poda
        if eje == 0:
            punto_corte = (coordenada_corte, punto[1]) # Mismo y, solo muevo x hasta la linea de corte
        else:
            punto_corte = (punto[0], coordenada_corte) # Mismo x, solo muevo y hasta la linea de corte
        distancia_al_corte = geodesic(punto, punto_corte).m
        if rama_lejana is not None and distancia_al_corte <= mejor_distancia:
            mejor_punto, mejor_distancia = self.buscar_mas_cercano(punto, rama_lejana, nivel+1, mejor_punto, mejor_distancia)
        
        return mejor_punto, mejor_distancia

    def buscar_en_rango(self, punto, rango, nodo=None, nivel=0, resultados=None):
        if nodo is None:
            nodo = self.raiz # Si no me pasan nodo, inicio desde la raiz

        if resultados is None:
            resultados = []

        if nodo is None:
            return resultados

        # Reviso los puntos del nodo actual y me quedo solo con los que entran en el rango
        for dato in nodo.datos:
            distancia = geodesic(punto, dato).m
            if distancia <= rango:
                resultados.append((dato, distancia))

        eje = nivel % len(punto)
        coordenada_corte = nodo.datos[0][eje]

        # Igual que en nearest, primero bajo por la rama que parece más prometedora
        if punto[eje] < coordenada_corte:
            rama_cercana = nodo.izquierda
            rama_lejana = nodo.derecha
        else:
            rama_cercana = nodo.derecha
            rama_lejana = nodo.izquierda

        if rama_cercana is not None:
            self.buscar_en_rango(punto, rango, rama_cercana, nivel+1, resultados)

        # Si la distancia al corte es menor o igual al rango, todavía podría haber puntos válidos en la otra rama
        if eje == 0:
            punto_corte = (coordenada_corte, punto[1])
        else:
            punto_corte = (punto[0], coordenada_corte)
        distancia_al_corte = geodesic(punto, punto_corte).m
        if rama_lejana is not None and distancia_al_corte <= rango:
            self.buscar_en_rango(punto, rango, rama_lejana, nivel+1, resultados)

        return resultados