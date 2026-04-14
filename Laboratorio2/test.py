import random

import matplotlib.pyplot as plt
from geopy.distance import geodesic

from KDTree import KD_Tree


def generar_puntos(n, centro, tol_latt=0.06, tol_long=0.06):
	puntos_generados = []
	for _ in range(n):
		latitud = centro[0] + random.uniform(-tol_latt, tol_latt) # Los genera alrededor del centro con una tolerancia
		longitud = centro[1] + random.uniform(-tol_long, tol_long)
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
	# Como la grafica usa coordenadas geograficas, el radio no puede quedarse en metros
	# Aprox: 1 grado de latitud son ~111139 m
	return metros / 111139


def validar_resultados(puntos, punto_consulta, rango_metros, arbol):
	cercano_kd, distancia_kd = arbol.buscar_mas_cercano(punto_consulta)
	cercano_bruta, distancia_bruta = nearest_fuerza_bruta(puntos, punto_consulta)

	resultados_kd = arbol.buscar_en_rango(punto_consulta, rango_metros)
	resultados_bruta = rango_fuerza_bruta(puntos, punto_consulta, rango_metros)

	# Una tolerancia minima para comparar distancias por decimales
	nearest_coincide = abs(distancia_kd - distancia_bruta) <= 1e-6

	conjunto_kd = {punto for punto, distancia in resultados_kd}
	conjunto_bruta = {punto for punto, distancia in resultados_bruta}

	# Comparar rango por conjunto de puntos para revisar que sean los mismos
	rango_coincide = conjunto_kd == conjunto_bruta

	if nearest_coincide:
		print('Validacion nearest: OK (KD-Tree coincide con fuerza bruta)')
	else:
		print('Validacion nearest: NO coincide con fuerza bruta')

	if rango_coincide:
		print('Validacion rango: OK (KD-Tree coincide con fuerza bruta)')
	else:
		print('Validacion rango: NO coincide con fuerza bruta')

	return (cercano_kd, distancia_kd), resultados_kd, nearest_coincide, rango_coincide


def graficar_resultados(puntos, punto_consulta, resultado_nearest, resultados_rango, rango_metros):
	fig, axes = plt.subplots(1, 2, figsize=(14, 6))

	latitudes = [punto[0] for punto in puntos]
	longitudes = [punto[1] for punto in puntos]

	# Grafica 1: nearest neighbor
	ax1 = axes[0]
	ax1.scatter(longitudes, latitudes, s=20, c='#355070', alpha=0.75, label='Puntos')
	ax1.scatter(punto_consulta[1], punto_consulta[0], s=90, c='#e76f51', marker='x', label='Consulta')
	ax1.scatter(resultado_nearest[0][1], resultado_nearest[0][0], s=100, c='#2a9d8f', marker='*', label='Mas cercano')
	ax1.plot([punto_consulta[1], resultado_nearest[0][1]], [punto_consulta[0], resultado_nearest[0][0]], c='#2a9d8f', lw=1.5)
	ax1.set_title('Nearest Neighbor (KD-Tree)')
	ax1.set_xlabel('Longitud')
	ax1.set_ylabel('Latitud')
	ax1.legend(loc='best')
	ax1.grid(alpha=0.2)

	# Grafica 2: busqueda por rango
	ax2 = axes[1]
	ax2.scatter(longitudes, latitudes, s=20, c='#355070', alpha=0.5, label='Puntos')
	ax2.scatter(punto_consulta[1], punto_consulta[0], s=90, c='#e76f51', marker='x', label='Consulta')

	if resultados_rango:
		latitudes_rango = [punto[0] for punto, distancia in resultados_rango]
		longitudes_rango = [punto[1] for punto, distancia in resultados_rango]
		ax2.scatter(longitudes_rango, latitudes_rango, s=40, c='#f4a261', label='Dentro del rango')

	# El círculo se hace aprox usando conversion de metros a grados en latitud
	radio_en_grados = metros_a_grados_lat(rango_metros)
	circulo = plt.Circle((punto_consulta[1], punto_consulta[0]), radio_en_grados, color='#e76f51', fill=False, lw=2, alpha=0.8)
	ax2.add_patch(circulo)

	ax2.set_title('Busqueda Por Rango (KD-Tree)')
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
	arbol = KD_Tree(puntos)

	resultado_nearest, resultados_rango, nearest_coincide, rango_coincide = validar_resultados(puntos, punto_consulta, rango_metros, arbol)

	print('Cantidad de puntos:', n)
	print('Punto consulta:', punto_consulta)
	print('Mas cercano (KD-Tree):', resultado_nearest[0])
	print('Distancia mas cercana (m):', round(resultado_nearest[1], 2))
	print('Cantidad en rango:', len(resultados_rango))
	print('Nearest coincide con fuerza bruta:', nearest_coincide)
	print('Rango coincide con fuerza bruta:', rango_coincide)

	graficar_resultados(puntos, punto_consulta, resultado_nearest, resultados_rango, rango_metros)


if __name__ == '__main__':
	main()