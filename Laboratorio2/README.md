# KD-Tree vs Fuerza Bruta (Laboratorio 2)

## Explicacion y uso
En este laboratorio hice un KD-Tree para comparar contra busqueda lineal (fuerza bruta), usando distancias geodesicas en metros.

La construccion del arbol la intente dejar pensada para K dimensiones (por eso el eje va rotando con el nivel), pero las busquedas y la parte visual por ahora las deje en 2D (latitud y longitud), que era lo que necesitaba para el contexto de ciudad.

Para usar todo el flujo completo no hace falta correr varios archivos: ejecuta `analisis.py`.

Ese archivo hace todo en una sola corrida:
- Te pide cantidad de puntos, punto consulta y radio.
- Valida KD vs fuerza bruta.
- Muestra las graficas de mas cercano y radio.
- Luego corre el analisis de tiempos por diferentes sizes.

Ejemplo de salida en terminal:

```text
Cantidad de puntos [10000]: 
Ingresa el punto consulta (Enter para usar el valor por defecto):
Latitud [6.251]: 
Longitud [-75.57]: 
Radio en metros [500]: 
Validacion nearest: OK (KD-Tree coincide con fuerza bruta)
Validacion rango: OK (KD-Tree coincide con fuerza bruta)

Resumen:
Cantidad de puntos: 10000
Punto consulta: (6.251, -75.57)
Mas cercano (KD-Tree): (6.25097153475943, -75.56977698511702)
Distancia mas cercana (m): 24.88
Cantidad en radio: 43
Mas cercano coincide con fuerza bruta: True
Radio coincide con fuerza bruta: True

Analisis de tiempos:
size=    10 | mas cercano KD=0.0885s vs bruta=0.1222s | radio KD=0.0840s vs bruta=0.0835s
size=    25 | mas cercano KD=0.1196s vs bruta=0.2046s | radio KD=0.0512s vs bruta=0.1396s
size=    50 | mas cercano KD=0.1040s vs bruta=0.2538s | radio KD=0.0633s vs bruta=0.2540s
size=   100 | mas cercano KD=0.0975s vs bruta=0.5301s | radio KD=0.0700s vs bruta=0.6838s
size=   500 | mas cercano KD=0.1681s vs bruta=3.7733s | radio KD=0.1597s vs bruta=2.7645s
size=  1000 | mas cercano KD=0.1569s vs bruta=6.4722s | radio KD=0.1970s vs bruta=5.6871s

Resumen estricto:
- Mas cercano (solo busqueda): KD ya es mejor desde size=10
- Radio (solo busqueda): KD ya es mejor desde size=25
```

## Conclusiones
- En sizes pequeños, los tiempos pueden salir bastante parecidos, y aunque el resumen estricto marque un size donde KD ya pasa a ser mejor, ese punto exacto puede variar entre corridas por pequenas variaciones de ejecucion (centesimas o milisegundos). A partir de 10-50 los tiempos el KD son mejores, y a partir de 500-1000 ya se vuelve demasiado evidente. Para los 10000 cada búsqueda lineal toma casi 30s.
- En busqueda de mas cercano, la diferencia se nota antes. La poda del nearest ayuda mucho porque una consulta individual descarta ramas rapido y eso le da ventaja al KD-Tree desde sizes bajos.
- En busqueda por radio tambien hay mejora, pero la diferencia suele tardar un poco mas en verse porque se devuelven varios puntos y, dependiendo del radio, se exploran mas nodos.
- A medida que sube el size, la diferencia entre KD y fuerza bruta se hace cada vez mas clara. En fuerza bruta el costo crece lineal por consulta y termina pegando duro cuando ya hay muchos puntos.
- Si el radio crece, el KD-Tree tiene que abrir mas ramas y se le reduce un poco la ventaja, pero aun asi sigue siendo mucho mas eficiente que revisar todos los puntos uno por uno.