# ─────────────────────────────────────────────
# LISTA (Codificado con ayuda de Claude Sonnet y GitHub Copilot)
# ─────────────────────────────────────────────

class Lista:
    """
    La forma más simple: guardamos todo en una lista Python.
    Buscar = recorrer uno por uno → O(n).
    Insertar = append → O(1).
    """

    def __init__(self):
        self.datos = []

    def insertar(self, estudiante):
        self.datos.append(estudiante)

    def buscar(self, id_buscado):
        for e in self.datos:
            if e["id"] == id_buscado:
                return e
        return None

    def listar_ordenado(self):
        return sorted(self.datos, key=lambda e: e["id"])
