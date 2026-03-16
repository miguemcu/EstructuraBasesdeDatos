Este "proyecto" compara tres estructuras de datos para almacenar y consultar estudiantes por ID:

- lista.py: lista de Python con búsqueda lineal.
- abb.py: árbol binario de búsqueda (ABB).
- bplus.py: B+ Tree de orden 4.
- main.py: benchmark principal.
- rangos_bplus.py: demo de búsqueda por rango con B+ Tree.

### Cómo ejecutar

1. Ubícate en la carpeta del proyecto.
2. Tras asegurarse de haber guardado y ejecutado los archivos abb.py, bplus.py y lista.py. Ejecuta el benchmark principal:

    python main.py

(OPCIONAL) 3. Ejecuta la demo de rangos del B+ Tree:

    python rangos_bplus.py

### Qué se mide de forma fija en el benchmark

En el estado actual de main.py, el benchmark muestra siempre los tiempos de búsqueda para las tres estructuras:

- Lista
- ABB
- B+

Se ejecutan dos escenarios:

- IDs aleatorios (caso normal).
- IDs ordenados (peor caso para ABB).

Esto permite ver claramente cómo cambia el rendimiento de búsqueda según la distribución de inserción.

### Pruebas adicionales (actualmente ocultas/comentadas)

En main.py ya están implementadas, pero comentadas, estas mediciones extra:

- Tiempo de inserción por estructura.
- Altura de los árboles (ABB y B+).
- Tiempo para listar ordenado.

Si quieres activarlas, solo descomenta los bloques correspondientes dentro de la función benchmark en main.py.

### Prueba de rangos para B+ Tree

La búsqueda por rango está en rangos_bplus.py.  
Esta prueba simula una consulta tipo:

- ID entre mínimo y máximo

y aprovecha los nodos hoja enlazados del B+ Tree para recorrer secuencialmente los resultados del rango de forma eficiente.

### Parámetros que puedes ajustar

En main.py puedes modificar fácilmente:

- Cantidad de estudiantes (n).
- Número de búsquedas aleatorias (n_busquedas).
- Escenario con IDs ordenados o aleatorios.

En rangos_bplus.py puedes cambiar:

- id_min
- id_max
- cantidad de estudiantes de la demo

### Interpretación rápida esperada

- Lista: simple, pero lenta en búsqueda grande.
- ABB: rápido en promedio, pero puede degradarse con inserciones ordenadas.
- B+ Tree: mantiene buena búsqueda y destaca en consultas por rango.