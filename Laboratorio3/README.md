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
Cantidad de puntos [1000]: 
Ingresa el punto consulta:
Latitud [6.251]: 
Longitud [-75.57]: 
Radio en metros [500]: 

Validacion nearest: OK (Quadtree coincide con bruta)
Validacion rango: OK (Quadtree coincide con bruta)

Analisis nearest neighbor (tiempo vs size):
size=    10 | QT=0.0249s vs bruta=0.0219s
size=    25 | QT=0.0261s vs bruta=0.0550s
size=    50 | QT=0.0370s vs bruta=0.1073s
...
size=   500 | QT=0.0510s vs bruta=1.0544s
size=  1000 | QT=0.0648s vs bruta=2.1004s

Analisis rango (tiempo vs radio, 1000 puntos fijos):
radio=   100m | QT=0.0518s vs bruta=2.1072s
radio=   500m | QT=0.0956s vs bruta=2.1022s
radio=  1500m | QT=0.2782s vs bruta=2.1005s
radio=  3000m | QT=0.7532s vs bruta=2.1217s 

## Análisis Visual
El laboratorio genera gráficas que muestran el comportamiento de ambos algoritmos:

- Se observa cómo la fuerza bruta crece de forma lineal, mientras que el Quadtree mantiene un tiempo casi constante (logarítmico), alejándose drásticamente a partir de los 200 puntos.

- Con una cantidad de puntos fija, se analiza cómo afecta el tamaño del área de búsqueda.

## Conclusiones
Superioridad del Quadtree: En la búsqueda por rangos, el Quadtree es exageradamente superior a la fuerza bruta. Mientras que la fuerza bruta se mantiene constante (en un tiempo alto) porque siempre debe recorrer la lista completa independientemente del radio, el Quadtree es mucho más veloz al descartar regiones enteras del espacio.

- Se observa que a medida que el radio de búsqueda aumenta, el tiempo del Quadtree crece gradualmente. Esto ocurre porque el algoritmo debe descender hacia más ramas y procesar más nodos conforme el área de consulta abarca más cuadrantes.

- Aunque estrictamente el Quadtree empieza a ser mejor en el Nearest Neighbor desde n=25, la diferencia real se vuelve crítica a partir de los 200 puntos, donde la fuerza bruta ya alcanza casi el medio segundo frente a los tiempos casi imperceptibles del árbol.

- Las gráficas confirman la teoría: la búsqueda con Quadtree sigue una tendencia logarítmica, mientras que la fuerza bruta muestra un crecimiento lineal (O(n)) por cada consulta, lo que la hace inviable para aplicaciones de geolocalización a gran escala.