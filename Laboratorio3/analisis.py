################# AGREGAR LO DE INSTALAR MATPLOTLIB Y GEOPY EN EL README ####################

import random
import time

from QuadTree import Quad_Tree
from test import (
	generar_puntos,
	nearest_fuerza_bruta,
	rango_fuerza_bruta,
	validar_resultados,
	graficar_resultados,
)


def primer_size_qt_mejor(resultados, campo_qt, campo_bruta):
	for fila in resultados:
		if fila[campo_qt] < fila[campo_bruta]:
			return fila['size']
	return None


def analizar_sizes(sizes, consultas_por_size, centro, radio):
	resumen = []

	for size in sizes:
		puntos = generar_puntos(size, centro)
		consultas = generar_puntos(consultas_por_size, centro)

		arbol = Quad_Tree(puntos)

		# Tiempo del más cercano con Quad-Tree
		inicio_nearest_qt = time.perf_counter()
		for punto_consulta in consultas:
			arbol.buscar_mas_cercano(punto_consulta)
		tiempo_nearest_qt = time.perf_counter() - inicio_nearest_qt

		# Tiempo del más cercano con fuerza bruta
		inicio_nearest_bruta = time.perf_counter()
		for punto_consulta in consultas:
			nearest_fuerza_bruta(puntos, punto_consulta)
		tiempo_nearest_bruta = time.perf_counter() - inicio_nearest_bruta

		# Búsqueda por rango con Quad-Tree
		inicio_rango_qt = time.perf_counter()
		for punto_consulta in consultas:
			arbol.buscar_en_rango(punto_consulta, radio)
		tiempo_rango_qt = time.perf_counter() - inicio_rango_qt

		# Búsqueda por rango con fuerza bruta
		inicio_rango_bruta = time.perf_counter()
		for punto_consulta in consultas:
			rango_fuerza_bruta(puntos, punto_consulta, radio)
		tiempo_rango_bruta = time.perf_counter() - inicio_rango_bruta

		fila = {
			'size': size,
			'tiempo_nearest_qt': tiempo_nearest_qt,
			'tiempo_nearest_bruta': tiempo_nearest_bruta,
			'tiempo_rango_qt': tiempo_rango_qt,
			'tiempo_rango_bruta': tiempo_rango_bruta,
		}
		resumen.append(fila)

		print(
			f"size={size:6d} | "
			f"mas cercano QT={tiempo_nearest_qt:.4f}s vs bruta={tiempo_nearest_bruta:.4f}s | "
			f"radio QT={tiempo_rango_qt:.4f}s vs bruta={tiempo_rango_bruta:.4f}s"
		)

	return resumen


def leer_float(mensaje, valor_por_defecto):
	texto = input(mensaje).strip()
	if texto == '':
		return valor_por_defecto
	return float(texto)


def leer_int(mensaje, valor_por_defecto):
	texto = input(mensaje).strip()
	if texto == '':
		return valor_por_defecto
	return int(texto)


def leer_punto_consulta(valor_lat_por_defecto, valor_lon_por_defecto):
	print("\nPunto de consulta:")
	latitud = leer_float(f'Latitud [{valor_lat_por_defecto}]: ', valor_lat_por_defecto)
	longitud = leer_float(f'Longitud [{valor_lon_por_defecto}]: ', valor_lon_por_defecto)
	return (latitud, longitud)


def main():
	random.seed(90)

	centro_medellin = (6.245, -75.57151)
	consultas_por_size = 25
	cantidad_puntos_visual = 10000
	punto_consulta_default = (6.2510, -75.5700)
	radio_default = 500

	print('\nIngresa los datos para la consulta (Enter para usar el valor por defecto):')
	cantidad_puntos_visual = leer_int(f'Cantidad de puntos de la ciudad [{cantidad_puntos_visual}]: ', cantidad_puntos_visual)
	punto_consulta = leer_punto_consulta(punto_consulta_default[0], punto_consulta_default[1])
	radio = leer_float(f'Radio en metros [{radio_default}]: ', radio_default)

	puntos_visual = generar_puntos(cantidad_puntos_visual, centro_medellin)
	arbol_visual = Quad_Tree(puntos_visual)

	resultado_nearest, resultados_radio, nearest_coincide, radio_coincide = validar_resultados(
		puntos_visual,
		punto_consulta,
		radio,
		arbol_visual,
	)

	print('\nResumen:')
	print('Cantidad de puntos:', cantidad_puntos_visual)
	print('Punto consulta:', punto_consulta)
	print('Mas cercano (Quad-Tree):', resultado_nearest[0])
	print('Distancia mas cercana (m):', round(resultado_nearest[1], 2))
	print('Cantidad en radio:', len(resultados_radio))
	print('Mas cercano coincide con fuerza bruta:', nearest_coincide)
	print('Radio coincide con fuerza bruta:', radio_coincide)

	graficar_resultados(puntos_visual, punto_consulta, resultado_nearest, resultados_radio, radio, arbol_visual)

	print('\nAnalisis de tiempos:')
	sizes = [10, 25, 50, 100, 500, 1000]

	resultados = analizar_sizes(sizes, consultas_por_size, centro_medellin, radio)

	primer_size_nearest_mejor = primer_size_qt_mejor(resultados, 'tiempo_nearest_qt', 'tiempo_nearest_bruta')
	primer_size_radio_mejor = primer_size_qt_mejor(resultados, 'tiempo_rango_qt', 'tiempo_rango_bruta')

	print('\nResumen estricto:')
	if primer_size_nearest_mejor is not None:
		print(f'- Mas cercano (solo busqueda): QT ya es mejor desde size={primer_size_nearest_mejor}')
	else:
		print('- Mas cercano (solo busqueda): en estos sizes aun no es claramente mejor')

	if primer_size_radio_mejor is not None:
		print(f'- Radio (solo busqueda): QT ya es mejor desde size={primer_size_radio_mejor}')
	else:
		print('- Radio (solo busqueda): en estos sizes aun no es claramente mejor')


if __name__ == '__main__':
	main()