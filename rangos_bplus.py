# ─────────────────────────────────────────────
# DEMO: BÚSQUEDA POR RANGO (Codificado con ayuda de Claude Sonnet y GitHub Copilot)
# ─────────────────────────────────────────────

from bplus import *
from main import generar_estudiantes

def demo_rango(bpt: BPlusTree, id_min: int, id_max: int):
    """
    Simula: SELECT * FROM estudiantes WHERE id BETWEEN id_min AND id_max
    Usando la lista enlazada de hojas del B+ tree.
    """
    print(f"\n{'DEMO RANGO':─<35}")
    print(f"  Consulta: id BETWEEN {id_min} AND {id_max}")

    # Encontrar la hoja de inicio
    nodo = bpt.raiz
    while not nodo.es_hoja:
        i = 0
        while i < len(nodo.claves) and id_min >= nodo.claves[i]:
            i += 1
        nodo = nodo.hijos[i]

    # Caminar hacia la derecha por la lista enlazada
    resultados = []
    while nodo is not None:
        for i, k in enumerate(nodo.claves):
            if id_min <= k <= id_max:
                resultados.append(nodo.datos[i])
            elif k > id_max:
                break
        if nodo.claves and nodo.claves[-1] > id_max:
            break
        nodo = nodo.siguiente

    print(f"  Encontrados: {len(resultados)} estudiantes")
    for e in resultados[:5]:
        print(f"    ID {e['id']} | {e['nombre']} | promedio {e['promedio']}")
    if len(resultados) > 5:
        print(f"    ... y {len(resultados)-5} más")
        
        
if __name__ == "__main__":
        # Demo rango con B+
    print("=" * 60)
    print("  DEMO: B+ Tree con rango de búsqueda")
    print("=" * 60)
    bpt2 = BPlusTree()
    for e in generar_estudiantes(200, ordenados=False):
        bpt2.insertar(e)
    demo_rango(bpt2, id_min=1050, id_max=1080)

    print("\n" + "=" * 60)
    print("  Fin del benchmark. ¡El B+ gana en rangos!")
    print("=" * 60)
    