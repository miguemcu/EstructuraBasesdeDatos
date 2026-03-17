## Codificado con ayuda de Claude Sonnet y GitHub Copilot

"""
Sistema de Búsqueda de Estudiantes

Implementa y compara tres estructuras de datos:
  1. Lista (búsqueda lineal)
  2. ABB (Árbol Binario de Búsqueda)
  3. B+ Tree (orden 4)
"""
from lista import Lista
from abb import *
from bplus import *
import random
import time


# ─────────────────────────────────────────────
# GENERACIÓN DE DATOS
# ─────────────────────────────────────────────

def generar_estudiantes(n=10_000, ordenados=False):
    """Genera n estudiantes con id, nombre y promedio."""
    nombres = ["Miguel", "Neira", "Ana", "Carlos", "María", "Pedro", 
               "Laura", "Juan", "Sofía", "Andrés", "Valentina", "Diego",
               "Camila", "Santiago", "Isabella", "Sebastián", "Luisa"]
    ids = list(range(1000, 1000 + n))
    if not ordenados:
        random.shuffle(ids)

    estudiantes = []
    for i in range(n):
        estudiante = {
            "id": ids[i],
            "nombre": random.choice(nombres),
            "promedio": round(random.uniform(3, 5.0), 2)
        }
        estudiantes.append(estudiante)

    return estudiantes

# ─────────────────────────────────────────────
# PRUEBAS
# ─────────────────────────────────────────────

def medir_tiempo(f):
    """Ejecuta f() y devuelve (resultado, tiempo_en_segundos)."""
    t0 = time.perf_counter()
    res = f()
    return res, time.perf_counter() - t0


def benchmark(n=10_000, n_busquedas=100, ordenados=False):
    print("=" * 60)
    modo = "ORDENADOS (peor caso ABB)" if ordenados else "ALEATORIOS"
    print(f"  IDs {modo} | {n:,} estudiantes | {n_busquedas} búsquedas")
    print("=" * 60)

    estudiantes = generar_estudiantes(n, ordenados=ordenados)
    ids_todos   = [e["id"] for e in estudiantes]

    # ── Construcción ──────────────────────────────
    lista = Lista()
    abb   = ABB()
    bpt   = BPlusTree()

    # Vamos midiendo el tiempo de unas funciones que insertan en un for por compresión
    _, t_lista = medir_tiempo(lambda: [lista.insertar(e) for e in estudiantes])
    _, t_abb   = medir_tiempo(lambda: [abb.insertar(e)   for e in estudiantes])
    _, t_bpt   = medir_tiempo(lambda: [bpt.insertar(e)   for e in estudiantes])

    # print(f"\n{'INSERCIÓN':─<35}")
    # print(f"  Lista  : {t_lista*1000:.1f} ms")
    # print(f"  ABB    : {t_abb*1000:.1f} ms")
    # print(f"  B+     : {t_bpt*1000:.1f} ms")

    # ── Búsqueda ──────────────────────────────────
    ids_buscar = random.choices(ids_todos, k=n_busquedas)

    def busquedas_lista():
        resultados = []
        for id_buscado in ids_buscar:
            resultados.append(lista.buscar(id_buscado))
        return resultados

    def busquedas_abb():
        resultados = []
        for id_buscado in ids_buscar:
            resultados.append(abb.buscar(id_buscado))
        return resultados

    def busquedas_bpt():
        resultados = []
        for id_buscado in ids_buscar:
            resultados.append(bpt.buscar(id_buscado))
        return resultados

    _, t_bl = medir_tiempo(busquedas_lista)
    _, t_ba = medir_tiempo(busquedas_abb)
    _, t_bb = medir_tiempo(busquedas_bpt)

    print(f"\n{'BÚSQUEDA ('+str(n_busquedas)+' aleatorias)':─<35}")
    print(f"  Lista  : {t_bl:.4f} s")
    print(f"  ABB    : {t_ba:.4f} s  ({t_bl/t_ba:.0f}x más rápido que lista)")
    print(f"  B+     : {t_bb:.4f} s  ({t_bl/t_bb:.0f}x más rápido que lista)")

    # # ── Diagnóstico del árbol ──────────────────────
    # print(f"\n{'ESTADÍSTICAS DEL ÁRBOL':─<35}")
    # print(f"  ABB altura : {abb.altura()} niveles")
    # print(f"  B+  altura : {bpt.altura()} niveles")

    # # ── Listado ordenado ──────────────────────────
    # _, t_lo_lista = medir_tiempo(lista.listar_ordenado)
    # _, t_lo_abb   = medir_tiempo(abb.listar_ordenado)
    # _, t_lo_bpt   = medir_tiempo(bpt.listar_ordenado)

    # print(f"\n{'LISTAR ORDENADO':─<35}")
    # print(f"  Lista  : {t_lo_lista*1000:.1f} ms  (Python sort)")
    # print(f"  ABB    : {t_lo_abb*1000:.1f} ms  (in-order traversal)")
    # print(f"  B+     : {t_lo_bpt*1000:.1f} ms  (recorrido de hojas enlazadas)")

    # print()

# ─────────────────────────────────────────────
# AHORA SI, LO QUE FUE FUE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    random.seed(1000000)   # Asegurar una "bd" fija entre pruebas

    # Escenario 1: IDs aleatorios (caso normal)
    benchmark(n=10_000, n_busquedas=4000, ordenados=False)

    # Escenario 2: IDs ordenados (peor caso para el ABB)
    benchmark(n=10_000, n_busquedas=4000, ordenados=True)
    
    # # Crear datos y estructuras
    # estudiantes = generar_estudiantes(10_000, ordenados=False)

    # lista = Lista()
    # abb = ABB()
    # bpt = BPlusTree()

    # for e in estudiantes:
    #     lista.insertar(e)
    #     abb.insertar(e)
    #     bpt.insertar(e)

    # # Mostrar resultado de una búsqueda puntual
    # id_prueba = 10999
    # print(f"\nBuscando ID {id_prueba}...")
    # print("Lista:", lista.buscar(id_prueba))
    # print("ABB  :", abb.buscar(id_prueba))
    # print("B+   :", bpt.buscar(id_prueba))

    # # Mostrar lista ordenada (solo primeros 10)
    # orden_bpt = bpt.listar_ordenado()

    # print("\nPrimeros/Últimos 10 ordenados por ID:")
        
    # i = 0
    # for e in orden_bpt[-10:]:
    #     i += 1
    #     print(f"{i}. {e["id"]} {e["nombre"]}: {e["promedio"]}")