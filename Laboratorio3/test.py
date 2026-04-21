import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from geopy.distance import geodesic

from QuadTree import Quad_Tree


def generar_puntos(n, centro, tol_lat=0.06, tol_lon=0.06):
	puntos_generados = []
	for _ in range(n):
		latitud = centro[0] + random.uniform(-tol_lat, tol_lat)
		longitud = centro[1] + random.uniform(-tol_lon, tol_lon)
		puntos_generados.append((latitud, longitud))
	return puntos_generados


def nearest_fuerza_bruta(puntos, punto_consulta):
	mejor_punto = None
	mejor_distancia = float('inf')
	for punto in puntos:
		distancia = geodesic(punto_consulta, punto).m
		if distancia < mejor_distancia:
			mejor_distancia = distancia
			mejor_punto = punto
	return mejor_punto, mejor_distancia


def rango_fuerza_bruta(puntos, punto_consulta, rango_metros):
	resultados = []
	for punto in puntos:
		distancia = geodesic(punto_consulta, punto).m
		if distancia <= rango_metros:
			resultados.append((punto, distancia))
	return resultados


def metros_a_grados_lat(metros):
	# Aprox: 1 grado de latitud son ~111139 m
	return metros / 111139


def validar_resultados(puntos, punto_consulta, rango_metros, arbol):
	cercano_qt, distancia_qt = arbol.buscar_mas_cercano(punto_consulta)
	cercano_bruta, distancia_bruta = nearest_fuerza_bruta(puntos, punto_consulta)

	resultados_qt = arbol.buscar_en_rango(punto_consulta, rango_metros)
	resultados_bruta = rango_fuerza_bruta(puntos, punto_consulta, rango_metros)

	nearest_coincide = abs(distancia_qt - distancia_bruta) <= 1e-6

	conjunto_qt = {punto for punto, distancia in resultados_qt}
	conjunto_bruta = {punto for punto, distancia in resultados_bruta}
	rango_coincide = conjunto_qt == conjunto_bruta

	if nearest_coincide:
		print('Validacion nearest: OK (Quad-Tree coincide con fuerza bruta)')
	else:
		print('Validacion nearest: NO coincide con fuerza bruta')

	if rango_coincide:
		print('Validacion rango: OK (Quad-Tree coincide con fuerza bruta)')
	else:
		print('Validacion rango: NO coincide con fuerza bruta')

	return (cercano_qt, distancia_qt), resultados_qt, nearest_coincide, rango_coincide


def _dibujar_nodo(ax, nodo):
	# Dibuja recursivamente los rectángulos de cada nodo del árbol
	if nodo is None:
		return
	x = nodo.centro[1] - nodo.radio
	y = nodo.centro[0] - nodo.radio
	lado = nodo.radio * 2
	rect = patches.Rectangle(
		(x, y), lado, lado,
		linewidth=0.4, edgecolor='#888888', facecolor='none', alpha=0.5
	)
	ax.add_patch(rect)
	for hijo in nodo.hijos:
		_dibujar_nodo(ax, hijo)


def graficar_resultados(puntos, punto_consulta, resultado_nearest, resultados_rango, rango_metros, arbol):
	fig, axes = plt.subplots(1, 2, figsize=(16, 7))

	latitudes = [p[0] for p in puntos]
	longitudes = [p[1] for p in puntos]

	# Grafica 1: nearest neighbor con particiones del árbol superpuestas
	ax1 = axes[0]
	_dibujar_nodo(ax1, arbol.raiz)
	ax1.scatter(longitudes, latitudes, s=10, c='#355070', alpha=0.6, label='Puntos')
	ax1.scatter(punto_consulta[1], punto_consulta[0], s=90, c='#e76f51', marker='x', label='Consulta')
	ax1.scatter(resultado_nearest[0][1], resultado_nearest[0][0], s=100, c='#2a9d8f', marker='*', label='Mas cercano')
	ax1.plot(
		[punto_consulta[1], resultado_nearest[0][1]],
		[punto_consulta[0], resultado_nearest[0][0]],
		c='#2a9d8f', lw=1.5
	)
	ax1.set_title('Nearest Neighbor (Quad-Tree)')
	ax1.set_xlabel('Longitud')
	ax1.set_ylabel('Latitud')
	ax1.legend(loc='best')
	ax1.grid(alpha=0.2)

	# Grafica 2: búsqueda por rango
	ax2 = axes[1]
	ax2.scatter(longitudes, latitudes, s=10, c='#355070', alpha=0.5, label='Puntos')
	ax2.scatter(punto_consulta[1], punto_consulta[0], s=90, c='#e76f51', marker='x', label='Consulta')

	if resultados_rango:
		lats_rango = [p[0] for p, _ in resultados_rango]
		lons_rango = [p[1] for p, _ in resultados_rango]
		ax2.scatter(lons_rango, lats_rango, s=40, c='#f4a261', label='Dentro del rango')

	radio_grados = metros_a_grados_lat(rango_metros)
	circulo = plt.Circle(
		(punto_consulta[1], punto_consulta[0]), radio_grados,
		color='#e76f51', fill=False, lw=2, alpha=0.8
	)
	ax2.add_patch(circulo)

	ax2.set_title('Busqueda Por Rango (Quad-Tree)')
	ax2.set_xlabel('Longitud')
	ax2.set_ylabel('Latitud')
	ax2.legend(loc='best')
	ax2.grid(alpha=0.2)

	plt.tight_layout()
	plt.show()


def main():
	random.seed(10)

	n = 10000
	centro_medellin = (6.2442, -75.5812)
	punto_consulta = (6.2510, -75.5700)
	rango_metros = 1200

	puntos = generar_puntos(n, centro_medellin)
	arbol = Quad_Tree(puntos)

	resultado_nearest, resultados_rango, nearest_coincide, rango_coincide = validar_resultados(
		puntos, punto_consulta, rango_metros, arbol
	)

	print('Cantidad de puntos:', n)
	print('Punto consulta:', punto_consulta)
	print('Mas cercano (Quad-Tree):', resultado_nearest[0])
	print('Distancia mas cercana (m):', round(resultado_nearest[1], 2))
	print('Cantidad en rango:', len(resultados_rango))

	graficar_resultados(puntos, punto_consulta, resultado_nearest, resultados_rango, rango_metros, arbol)


if __name__ == '__main__':
	main()