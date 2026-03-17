# Matriz 100000x100000

Intento de generar una matriz de $100{,}000 \times 100{,}000$ con 0s y 1s sin explotar la RAM.

- `matriz_str.py`: escribe en texto plano (`matriz_escrita.txt`). Crea una fila de puros 0s y otra de puros 1s, y las alterna hasta completar 100,000 filas.
- `matriz_bin.py`: escribe en binario (`matriz.bin`). Genera una fila `0101...` en bytes y la repite 100,000 veces con `itertools.repeat`.

La idea en ambos casos es no construir toda la matriz en memoria, sino escribir por filas directamente en disco.