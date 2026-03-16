# ─────────────────────────────────────────────
# B+ TREE (orden t = 4, máx 3 claves/nodo) (Codificado con ayuda de Claude Sonnet y GitHub Copilot)
# ─────────────────────────────────────────────

class NodoBP:
    """Nodo del B+ tree."""
    def __init__(self, es_hoja: bool):
        self.es_hoja   = es_hoja
        self.claves    = []          # lista de claves (ids)
        self.hijos     = []          # punteros a hijos (solo nodos internos)
        self.datos     = []          # datos reales (solo hojas)
        self.siguiente = None        # enlace al próximo nodo hoja


class BPlusTree:
    """
    B+ Tree de orden t = 4.
    Cada nodo interno: entre t//2 y t-1 claves → entre 2 y 3 claves -> 50% a 100% lleno
    Cada hoja:         entre t//2 y t-1 datos  → entre 2 y 3 entradas -> 50% a 100% lleno
    
    Ventajas sobre ABB:
    - Siempre balanceado (altura garantizada).
    - Hojas enlazadas → consultas de rango y orden lineal eficientes.
    - En producción, t ≈ 100-500 (un nodo = un bloque de disco).
    """

    ORDEN = 4   # máximo de claves por nodo = ORDEN - 1

    def __init__(self):
        self.raiz = NodoBP(es_hoja=True)

    # ── Búsqueda ────────────────────────────────
    def buscar(self, id_buscado):
        """Desciende hasta la hoja correcta → O(log n)."""
        hoja = self._encontrar_hoja(self.raiz, id_buscado)
        for i, k in enumerate(hoja.claves):
            if k == id_buscado:
                return hoja.datos[i]
        return None

    def _encontrar_hoja(self, nodo, clave):
        """Navega el árbol desde la raíz hasta la hoja que contendría 'clave'."""
        if nodo.es_hoja:
            return nodo
        # Encontrar el hijo correcto
        i = 0
        while i < len(nodo.claves) and clave >= nodo.claves[i]:
            i += 1
        return self._encontrar_hoja(nodo.hijos[i], clave)

    # ── Inserción ──────────────────────────────
    def insertar(self, estudiante):
        clave = estudiante["id"]
        raiz  = self.raiz

        # Si la raíz está llena, hay que dividirla
        if len(raiz.claves) == self.ORDEN - 1:
            nueva_raiz        = NodoBP(es_hoja=False)
            nueva_raiz.hijos  = [raiz]
            self._dividir_hijo(nueva_raiz, 0)
            self.raiz         = nueva_raiz

        self._insertar_no_lleno(self.raiz, clave, estudiante)

    def _insertar_no_lleno(self, nodo, clave, dato):
        """Inserta en un nodo que NO está lleno."""
        if nodo.es_hoja:
            # Encontrar la posición correcta para mantener orden
            posicion = 0
            for i in range(len(nodo.claves)):
                if clave >= nodo.claves[i]:
                    posicion = i + 1
            
            # Insertar en la posición correcta
            nodo.claves.insert(posicion, clave)
            nodo.datos.insert(posicion, dato)
        else:
            # Encontrar el hijo destino
            idx_hijo = 0
            for i in range(len(nodo.claves)):
                if clave < nodo.claves[i]:
                    idx_hijo = i
                    break
                else:
                    idx_hijo = i + 1
            
            # Si el hijo está lleno, dividirlo primero
            if len(nodo.hijos[idx_hijo].claves) == self.ORDEN - 1:
                self._dividir_hijo(nodo, idx_hijo)
                # Si la clave es mayor que la nueva clave del padre, ir al hijo derecho
                if clave > nodo.claves[idx_hijo]:
                    idx_hijo = idx_hijo + 1
            
            self._insertar_no_lleno(nodo.hijos[idx_hijo], clave, dato)

    def _dividir_hijo(self, padre, idx_hijo):
        """
        Divide el hijo lleno en dos y sube la clave media al padre.
        En B+ tree: la clave mediana SE COPIA al padre (no se mueve),
        y permanece en la hoja derecha para mantener todos los datos en hojas.
        """
        t     = self.ORDEN // 2          # punto de división
        hijo  = padre.hijos[idx_hijo]
        nuevo = NodoBP(es_hoja=hijo.es_hoja)

        if hijo.es_hoja:
            # La clave mediana sube al padre pero queda también en la hoja derecha
            nuevo.claves = hijo.claves[t:]
            nuevo.datos  = hijo.datos[t:]
            hijo.claves  = hijo.claves[:t]
            hijo.datos   = hijo.datos[:t]
            clave_subida = nuevo.claves[0]
            # Mantener enlace entre hojas
            nuevo.siguiente = hijo.siguiente
            hijo.siguiente  = nuevo
        else:
            # Nodo interno: la clave mediana sube y se elimina del hijo
            nuevo.claves    = hijo.claves[t + 1:]
            nuevo.hijos     = hijo.hijos[t + 1:]
            clave_subida    = hijo.claves[t]
            hijo.claves     = hijo.claves[:t]
            hijo.hijos      = hijo.hijos[:t + 1]

        # Insertar en el padre
        padre.claves.insert(idx_hijo, clave_subida)
        padre.hijos.insert(idx_hijo + 1, nuevo)

    # ── Listar ordenado (usa la lista enlazada de hojas) ──
    def listar_ordenado(self):
        """
        Recorre la lista enlazada de hojas de izquierda a derecha.
        Esto es O(n) y completamente secuencial → muy eficiente en disco.
        """
        resultado = []
        
        # Bajar hasta la hoja más a la izquierda
        nodo = self.raiz
        while not nodo.es_hoja:
            nodo = nodo.hijos[0]
        
        # Caminar por los enlaces de hojas
        while nodo is not None:
            for dato in nodo.datos:
                resultado.append(dato)
            nodo = nodo.siguiente
        
        return resultado

    # ── Altura ───────────────────────────────────
    def altura(self):
        h, nodo = 0, self.raiz
        while not nodo.es_hoja:
            h += 1
            nodo = nodo.hijos[0]
        return h + 1