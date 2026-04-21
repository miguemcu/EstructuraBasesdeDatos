from geopy.distance import geodesic


class Nodo:
	def __init__(self, dato, centro, radio):
		self.dato = dato           # Un único punto (lat, lon)
		self.centro = centro       # (lat, lon) del centro de esta región
		self.radio = radio   # Mitad del lado del cuadrado que representa esta región
		self.hijos = [None, None, None, None] # Hijos en el orden: NO, NE, SE, SO


class Quad_Tree:
	def __init__(self, puntos):
		if not puntos:
			self.raiz = None
			return

		# Calculo la región original (raíz) a partir del conjunto de puntos inicial
		lat_min = min(p[0] for p in puntos)
		lat_max = max(p[0] for p in puntos)
		lon_min = min(p[1] for p in puntos)
		lon_max = max(p[1] for p in puntos)

		centro_lat = (lat_min + lat_max) / 2
		centro_lon = (lon_min + lon_max) / 2
		# El *1.01 es para que los puntos justo en el borde queden dentro y no en el límite exacto
		radio = max(lat_max - lat_min, lon_max - lon_min) / 2 * 1.01 # La distancia del centro hacia el borde del cuadrado

		self.raiz = None
		for punto in puntos:
			self.raiz = self.insertar(self.raiz, punto, (centro_lat, centro_lon), radio)

	def cuadrante(self, punto, centro): # Para ubicar el idx_cuadrante (en la lista) respecto al centro
		# 0=NO, 1=NE, 2=SE, 3=SO  (Puntos cardinales clásicos)
		if punto[0] >= centro[0] and punto[1] < centro[1]:
			return 0  # NO: lat >= centro_lat, lon < centro_lon
		elif punto[0] >= centro[0] and punto[1] >= centro[1]:
			return 1  # NE: lat >= centro_lat, lon >= centro_lon
		elif punto[0] < centro[0] and punto[1] >= centro[1]:
			return 2  # SE: lat < centro_lat, lon >= centro_lon
		else:
			return 3  # SO: lat < centro_lat, lon < centro_lon

	def centro_hijo(self, centro, radio, cuadrante):
		# Calcula el centro del cuadrante hijo dado el centro del padre y el "radio" (la mitad del lado)
		# El "radio" del hijo es la mitad del del padre
		nuevo_radio = radio / 2
		if cuadrante == 0:   # NO
			return (centro[0] + nuevo_radio, centro[1] - nuevo_radio)
		elif cuadrante == 1: # NE
			return (centro[0] + nuevo_radio, centro[1] + nuevo_radio)
		elif cuadrante == 2: # SE
			return (centro[0] - nuevo_radio, centro[1] + nuevo_radio)
		else:                # SO
			return (centro[0] - nuevo_radio, centro[1] - nuevo_radio)

	def insertar(self, nodo, punto, centro, radio):
		if nodo is None: # Si no hay nada, será hoja con ese punto
			return Nodo(punto, centro, radio)

		if nodo.dato == punto: # Si el punto ya está, no es necesario insertarlo
			return nodo

		# El nodo ya tiene un dato, así que determino en qué cuadrante cae el nuevo punto
		cuadrante = self.cuadrante(punto, nodo.centro)
		centro_hijo = self.centro_hijo(nodo.centro, nodo.radio, cuadrante)
		radio_hijo = nodo.radio / 2

		nodo.hijos[cuadrante] = self.insertar(
			nodo.hijos[cuadrante], punto, centro_hijo, radio_hijo)
		return nodo

	def buscar_mas_cercano(self, punto, nodo=None, mejor_punto=None, mejor_distancia=float('inf')):
		if nodo is None:
			nodo = self.raiz
 
		if nodo is None:
			return None, float('inf') # Literalmente cualquier número va a ser mejor que infinito
		
		# Reviso primero el punto del nodo raiz
		distancia = geodesic(punto, nodo.dato).m
		if distancia < mejor_distancia:
			mejor_distancia = distancia
			mejor_punto = nodo.dato

		# La rama más prometedora es la del cuadrante donde está el punto a buscar
		cuadrante_directo = self.cuadrante(punto, nodo.centro)
		orden = [cuadrante_directo] + [i for i in range(4) if i != cuadrante_directo] # Vamos a ir revisando cuadrante por cuadrante

		for cuadrante in orden:
			hijo = nodo.hijos[cuadrante]
			if hijo is None:
				continue

			# Poda: calculo la distancia mínima posible al cuadrado del hijo
			# y si esa distancia ya es mayor que la mejor que tengo, no tiene sentido entrar
			dist_a_cuad = self.distancia_a_cuadrado(punto, hijo.centro, hijo.radio)
			if dist_a_cuad >= mejor_distancia:
				continue

			mejor_punto, mejor_distancia = self.buscar_mas_cercano(
				punto, hijo, mejor_punto, mejor_distancia)

		return mejor_punto, mejor_distancia

	def buscar_en_rango(self, punto, rango, nodo=None, resultados=None):
		if nodo is None:
			nodo = self.raiz

		if resultados is None:
			resultados = []

		if nodo is None:
			return resultados

		# Reviso si el punto de este nodo cae dentro del rango
		distancia = geodesic(punto, nodo.dato).m
		if distancia <= rango:
			resultados.append((nodo.dato, distancia))

		# Solo entro a un hijo si su rectángulo podría contener puntos dentro del rango
		# Si la distancia mínima al rectángulo del hijo ya supera el rango, lo descarto completo
		for hijo in nodo.hijos:
			if hijo is None:
				continue
			dist_min_rect = self.distancia_a_cuadrado(punto, hijo.centro, hijo.radio)
			if dist_min_rect <= rango:
				self.buscar_en_rango(punto, rango, hijo, resultados)

		return resultados

	def distancia_a_cuadrado(self, punto, centro, radio):
		# Para calcular la distancia mínima entre el punto consulta y el rectángulo del nodo
		# El punto más cercano del rectángulo es la esquina o el borde más próximo
		lat_min = centro[0] - radio
		lat_max = centro[0] + radio
		lon_min = centro[1] - radio
		lon_max = centro[1] + radio

		# Busco el borde del cuadrado
		# (usando min y max porque desconozco si el punto está "antes" o "despues") del cuadrado
		lat_cercana = max(lat_min, min(punto[0], lat_max)) 
		lon_cercana = max(lon_min, min(punto[1], lon_max))

		return geodesic(punto, (lat_cercana, lon_cercana)).m