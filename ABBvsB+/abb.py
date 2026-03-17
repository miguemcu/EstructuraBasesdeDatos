# ─────────────────────────────────────────────
# ARBOL ABB (Codificado con ayuda de Claude Sonnet y GitHub Copilot)
# ─────────────────────────────────────────────

class NodoABB:
    """Nodo de un ABB. Guarda la clave (id) y el dato completo."""
    def __init__(self, estudiante):
        self.clave  = estudiante["id"]
        self.dato   = estudiante
        self.izq    = None
        self.der    = None


class ABB:
    """
    Árbol Binario de Búsqueda clásico.
    - Buscar:  O(log n) promedio, O(n) peor caso (datos ordenados).
    - Insertar: O(log n) promedio.
    - Recorrido in-order devuelve datos ordenados.
    """

    def __init__(self):
        self.raiz = None

    # ── Inserción (iterativa para evitar RecursionError en peor caso) ─
    def insertar(self, estudiante):
        nuevo = NodoABB(estudiante)
        if self.raiz is None:
            self.raiz = nuevo
            return
        actual = self.raiz
        while True:
            if estudiante["id"] < actual.clave:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                actual = actual.izq
            elif estudiante["id"] > actual.clave:
                if actual.der is None:
                    actual.der = nuevo
                    break
                actual = actual.der
            else:
                break  # id duplicado, ignorar

    # ── Búsqueda (iterativa) ─────────────────────
    def buscar(self, id_buscado):
        actual = self.raiz
        while actual is not None:
            if id_buscado == actual.clave:
                return actual.dato
            actual = actual.izq if id_buscado < actual.clave else actual.der
        return None

    # ── Listar en orden (iterativo con pila) ──────
    def listar_ordenado(self):
        resultado = []
        pila = []
        actual = self.raiz
        
        while actual is not None or len(pila) > 0:
            # Bajar hasta el nodo más a la izquierda
            while actual is not None:
                pila.append(actual)
                actual = actual.izq
            
            # El nodo más a la izquierda está en la cima de la pila
            actual = pila.pop()
            resultado.append(actual.dato)
            
            # Visitar el subárbol derecho
            actual = actual.der
        
        return resultado

    # ── Altura (iterativa con BFS) ─────────────────
    def altura(self):
        if self.raiz is None:
            return 0
        
        from collections import deque
        cola = deque()
        cola.append((self.raiz, 1))
        max_altura = 0
        
        while len(cola) > 0:
            nodo, altura_actual = cola.popleft()
            max_altura = max(max_altura, altura_actual)
            
            if nodo.izq is not None:
                cola.append((nodo.izq, altura_actual + 1))
            if nodo.der is not None:
                cola.append((nodo.der, altura_actual + 1))
        
        return max_altura