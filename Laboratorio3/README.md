# Quadtree vs Fuerza Bruta (Laboratorio 3)
## Explicación y uso
Este laboratorio implementa un Quadtree para realizar búsquedas espaciales eficientes y lo compara contra una búsqueda lineal (fuerza bruta). Para el cálculo de cercanía, se utilizan distancias geodésicas (metros) aplicadas a un contexto de ciudad.

A diferencia del laboratorio anterior, aquí la estructura se divide en cuatro cuadrantes para optimizar las consultas en 2D (latitud y longitud). El sistema permite realizar dos tipos de operaciones principales:

Nearest Neighbor (Vecino más cercano): Encuentra el punto más próximo a una coordenada consulta.

Búsqueda por Rango: Encuentra todos los puntos dentro de un radio circular (en metros).

## Requisitos
Es necesario tener instaladas las siguientes librerías:

pip install matplotlib geopy

## Ejecución
Para ejecutar el flujo completo (validación, gráficas y análisis de tiempos), usa:

python analisis.py
El script solicitará la configuración inicial, validará que ambos métodos retornen los mismos resultados y generará las comparativas de rendimiento.

## Ejemplo de salida en terminal
Plaintext
Analisis de tiempos:

Analisis nearest neighbor (tiempo promedio de 20 corridas vs size):
size=    25 | QT prom=0.0368s vs bruta prom=0.0631s)
size=    50 | QT prom=0.0376s vs bruta prom=0.1185s)
size=   100 | QT prom=0.0514s vs bruta prom=0.2555s)
size=   250 | QT prom=0.0545s vs bruta prom=0.5851s)
size=   500 | QT prom=0.0597s vs bruta prom=1.1467s)
size=  1000 | QT prom=0.0634s vs bruta prom=2.2527s)

Analisis rango (tiempo promedio de 20 corridas vs radio, 1000 puntos fijos):
radio=   100m | QT prom=0.0508s vs bruta prom=2.3140s)
radio=   500m | QT prom=0.0989s vs bruta prom=2.3679s)
radio=  1000m | QT prom=0.2046s vs bruta prom=2.6344s)
radio=  2000m | QT prom=0.5195s vs bruta prom=2.6247s)
radio=  3000m | QT prom=0.9118s vs bruta prom=2.6012s)

## Análisis Visual
El laboratorio genera gráficas que muestran el comportamiento de ambos algoritmos:

- Se observa cómo la fuerza bruta crece de forma lineal, mientras que el Quadtree mantiene un tiempo casi constante (logarítmico), alejándose drásticamente a partir de los 200 puntos.

- Con una cantidad de puntos fija, se analiza cómo afecta el tamaño del área de búsqueda.

## Conclusiones
- En la búsqueda por rangos, el Quadtree es exageradamente superior a la fuerza bruta. Mientras que la fuerza bruta se mantiene constante (en un tiempo alto) porque siempre debe recorrer la lista completa independientemente del radio, el Quadtree es mucho más veloz al descartar regiones enteras del espacio.

- Se observa que a medida que el radio de búsqueda aumenta, el tiempo del Quadtree crece gradualmente. Esto ocurre porque el algoritmo debe descender hacia más ramas y procesar más nodos conforme el área de consulta abarca más cuadrantes.

- Aunque estrictamente el Quadtree empieza a ser mejor en el Nearest Neighbor desde n=25, la diferencia real se vuelve crítica a partir de los 200 puntos, donde la fuerza bruta ya alcanza casi el medio segundo frente a los tiempos casi imperceptibles del árbol.

- Las gráficas confirman la teoría: la búsqueda con Quadtree sigue una recta con una pendiente mucho menor, casi plana, mientras que la fuerza bruta muestra un crecimiento lineal (O(n)) por cada consulta, lo que la hace inviable para aplicaciones de geolocalización a gran escala.