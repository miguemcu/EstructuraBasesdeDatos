import random
import time

from KDTree import KD_Tree
from test import (
	generar_puntos,
	nearest_fuerza_bruta,
	rango_fuerza_bruta,
	validar_resultados,
	graficar_resultados,
)


def primer_size_kd_mejor(resultados, campo_kd, campo_bruta):
	for fila in resultados:
		tiempo_kd = fila[campo_kd]
		tiempo_bruta = fila[campo_bruta]
		if tiempo_kd < tiempo_bruta:
			return fila['size']
	return None


def analizar_sizes(sizes, consultas_por_size, centro, radio):
	resumen = []

	for size in sizes:
		puntos = generar_puntos(size, centro)
		consultas = generar_puntos(consultas_por_size, centro)

		arbol = KD_Tree(puntos)

		# Tiempo del más cercano con KD
		inicio_nearest_kd = time.perf_counter()
		for punto_consulta in consultas:
			arbol.buscar_mas_cercano(punto_consulta)
		tiempo_nearest_kd = time.perf_counter() - inicio_nearest_kd

		# Tiempo del más cercano con Fza Bruta
		inicio_nearest_bruta = time.perf_counter()
		for punto_consulta in consultas:
			nearest_fuerza_bruta(puntos, punto_consulta)
		tiempo_nearest_bruta = time.perf_counter() - inicio_nearest_bruta

		# Búsqueda del rango con Fza KD
		inicio_rango_kd = time.perf_counter()
		for punto_consulta in consultas:
			arbol.buscar_en_rango(punto_consulta, radio)
		tiempo_rango_kd = time.perf_counter() - inicio_rango_kd

		# Búsqueda del rango con Fza Bruta
		inicio_rango_bruta = time.perf_counter()
		for punto_consulta in consultas:
			rango_fuerza_bruta(puntos, punto_consulta, radio)
		tiempo_rango_bruta = time.perf_counter() - inicio_rango_bruta

		fila = {
			'size': size,
			'tiempo_nearest_kd': tiempo_nearest_kd,
			'tiempo_nearest_bruta': tiempo_nearest_bruta,
			'tiempo_rango_kd': tiempo_rango_kd,
			'tiempo_rango_bruta': tiempo_rango_bruta,
		}
		resumen.append(fila)

		print(
			f"size={size:6d} | "
			f"mas cercano KD={tiempo_nearest_kd:.4f}s vs bruta={tiempo_nearest_bruta:.4f}s | "
			f"radio KD={tiempo_rango_kd:.4f}s vs bruta={tiempo_rango_bruta:.4f}s"
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
	print('\nIngresa el punto consulta (Enter para usar el valor por defecto):')
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

	# Primero hago la misma parte visual/interactiva para no ejecutar test.py por separado
	cantidad_puntos_visual = leer_int(f'Cantidad de puntos [{cantidad_puntos_visual}]: ', cantidad_puntos_visual)
	punto_consulta = leer_punto_consulta(punto_consulta_default[0], punto_consulta_default[1])
	radio = leer_float(f'Radio en metros [{radio_default}]: ', radio_default)

	puntos_visual = generar_puntos(cantidad_puntos_visual, centro_medellin)
	arbol_visual = KD_Tree(puntos_visual)

	resultado_nearest, resultados_radio, nearest_coincide, radio_coincide = validar_resultados(
		puntos_visual,
		punto_consulta,
		radio,
		arbol_visual,
	)

	print('\nResumen:')
	print('Cantidad de puntos:', cantidad_puntos_visual)
	print('Punto consulta:', punto_consulta)
	print('Mas cercano (KD-Tree):', resultado_nearest[0])
	print('Distancia mas cercana (m):', round(resultado_nearest[1], 2))
	print('Cantidad en radio:', len(resultados_radio))
	print('Mas cercano coincide con fuerza bruta:', nearest_coincide)
	print('Radio coincide con fuerza bruta:', radio_coincide)

	graficar_resultados(puntos_visual, punto_consulta, resultado_nearest, resultados_radio, radio)

	# Una vez mostrado lo visual, hago el analisis de tiempos
	print('\nAnalisis de tiempos:')

	# Puedes ampliar esta lista si quieres un analisis mas fino
	sizes = [10, 25, 50, 100, 500, 1000]

	resultados = analizar_sizes(sizes, consultas_por_size, centro_medellin, radio)

	primer_size_nearest_mejor = primer_size_kd_mejor(resultados, 'tiempo_nearest_kd', 'tiempo_nearest_bruta')
	primer_size_radio_mejor = primer_size_kd_mejor(resultados, 'tiempo_rango_kd', 'tiempo_rango_bruta')

	print('\nResumen estricto:')
	if primer_size_nearest_mejor is not None:
		print(f'- Mas cercano (solo busqueda): KD ya es mejor desde size={primer_size_nearest_mejor}')
	else:
		print('- Mas cercano (solo busqueda): en estos sizes aun no es claramente mejor')

	if primer_size_radio_mejor is not None:
		print(f'- Radio (solo busqueda): KD ya es mejor desde size={primer_size_radio_mejor}')
	else:
		print('- Radio (solo busqueda): en estos sizes aun no es claramente mejor')

if __name__ == '__main__':
	main()
