################# AGREGAR LO DE INSTALAR MATPLOTLIB Y GEOPY EN EL README ####################

import random
import time
import matplotlib.pyplot as plt

from QuadTree import Quad_Tree
from test import (
	generar_puntos,
	nearest_fuerza_bruta,
	rango_fuerza_bruta,
	validar_resultados,
	graficar_resultados,
)

def primer_size_qt_mejor(resultados, campo_qt, campo_bruta, clave='size'):
    for fila in resultados:
        if fila[campo_qt] < fila[campo_bruta]:
            return fila[clave]
    return None


def analizar_nearest(sizes, consultas_por_size, centro, corridas_por_size=1):
	resumen = []
	for size in sizes:
		tiempos_qt = []
		tiempos_bruta = []

		for i in range(corridas_por_size):
			puntos = generar_puntos(size, centro)
			consultas = generar_puntos(consultas_por_size, centro)
			arbol = Quad_Tree(puntos)

			inicio = time.perf_counter()
			for p in consultas:
				arbol.buscar_mas_cercano(p)
			tiempos_qt.append(time.perf_counter() - inicio)

			inicio = time.perf_counter()
			for p in consultas:
				nearest_fuerza_bruta(puntos, p)
			tiempos_bruta.append(time.perf_counter() - inicio)

		tiempo_qt_promedio = sum(tiempos_qt) / corridas_por_size
		tiempo_bruta_promedio = sum(tiempos_bruta) / corridas_por_size

		resumen.append({'size': size, 'tiempo_qt': tiempo_qt_promedio, 'tiempo_bruta': tiempo_bruta_promedio})
		print(
			f"size={size:6d} | QT prom={tiempo_qt_promedio:.4f}s vs "
			f"bruta prom={tiempo_bruta_promedio:.4f}s)"
		)

	return resumen


def analizar_rango(radios, consultas_por_radio, centro, size_fijo, corridas_por_radio=1):
	resumen = []

	for radio in radios:
		tiempos_qt = []
		tiempos_bruta = []

		for i in range(corridas_por_radio):
			puntos = generar_puntos(size_fijo, centro)
			consultas = generar_puntos(consultas_por_radio, centro)
			arbol = Quad_Tree(puntos)

			inicio = time.perf_counter()
			for p in consultas:
				arbol.buscar_en_rango(p, radio)
			tiempos_qt.append(time.perf_counter() - inicio)

			inicio = time.perf_counter()
			for p in consultas:
				rango_fuerza_bruta(puntos, p, radio)
			tiempos_bruta.append(time.perf_counter() - inicio)

		tiempo_qt_promedio = sum(tiempos_qt) / corridas_por_radio
		tiempo_bruta_promedio = sum(tiempos_bruta) / corridas_por_radio

		resumen.append({'radio': radio, 'tiempo_qt': tiempo_qt_promedio, 'tiempo_bruta': tiempo_bruta_promedio})
		print(
			f"radio={radio:6d}m | QT prom={tiempo_qt_promedio:.4f}s vs "
			f"bruta prom={tiempo_bruta_promedio:.4f}s)"
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

def graficar_nearest(resumen):
    sizes = [f['size'] for f in resumen]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(sizes, [f['tiempo_qt']    for f in resumen], marker='o', label='Quad-Tree',    c='#2a9d8f')
    ax.plot(sizes, [f['tiempo_bruta'] for f in resumen], marker='o', label='Fuerza bruta', c='#e76f51')
    ax.set_title('Nearest Neighbor: tiempo vs cantidad de puntos')
    ax.set_xlabel('Cantidad de puntos')
    ax.set_ylabel('Tiempo (s)')
    ax.legend()
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()


def graficar_rango(resumen):
    radios = [f['radio'] for f in resumen]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(radios, [f['tiempo_qt']    for f in resumen], marker='o', label='Quad-Tree',    c='#2a9d8f')
    ax.plot(radios, [f['tiempo_bruta'] for f in resumen], marker='o', label='Fuerza bruta', c='#e76f51')
    ax.set_title('Busqueda por Rango: tiempo vs radio')
    ax.set_xlabel('Radio (m)')
    ax.set_ylabel('Tiempo (s)')
    ax.legend()
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.show()

def main():
	random.seed(90)

	centro_medellin = (6.245, -75.57151)
	consultas_por_size = 25
	corridas_por_size = 20
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
# tiempo promedio de {corridas_por_size} vs size:
	print('\nAnalisis de tiempos:')
	sizes = [25, 50, 100, 250, 500, 1000]
	radios = [100, 500, 1000, 2000, 3000]
	size_fijo_rango = 1000

	print(f'\nAnalisis nearest neighbor (tiempo promedio de {corridas_por_size} corridas vs size):')
	resumen_nearest = analizar_nearest(sizes, consultas_por_size, centro_medellin, corridas_por_size)

	print(f'\nAnalisis rango (tiempo promedio de {corridas_por_size} corridas vs radio, {size_fijo_rango} puntos fijos):')
	resumen_rango = analizar_rango(radios, consultas_por_size, centro_medellin, size_fijo_rango, corridas_por_size)

	primer_size = primer_size_qt_mejor(resumen_nearest, 'tiempo_qt', 'tiempo_bruta')
	primer_radio = primer_size_qt_mejor(resumen_rango, 'tiempo_qt', 'tiempo_bruta', clave='radio')

	print('\nResumen estricto:')
	if primer_size:
		print(f'- Nearest: QT ya es mejor desde size={primer_size}')
	else:
		print('- Nearest: en estos sizes aun no es claramente mejor')

	graficar_nearest(resumen_nearest)
	graficar_rango(resumen_rango)
	


if __name__ == '__main__':
	main()