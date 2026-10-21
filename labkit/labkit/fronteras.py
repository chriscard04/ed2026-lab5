"""Fronteras del laboratorio: pila, cola y heap con la misma interfaz.

Las tres guardan elementos (nodo, padre, costo) y tienen los mismos métodos:
    agregar(nodo, padre=None, costo=0)
    sacar()        -> (nodo, padre, costo)
    esta_vacia()   -> bool

Lo único que cambia es QUÉ elemento sale primero:
    CustomPila    sale el último que entró       -> DFS
    CustomCola    sale el primero que entró      -> BFS
    FronteraHeap  sale el de menor costo         -> Dijkstra
                  (si empatan en costo, sale el código alfabéticamente menor)

Además, cada frontera "graba" lo que pasa (traza) para que puedas verlo con
lab.ver_frontera(frontera).
"""

from __future__ import annotations

import heapq
from collections import Counter, deque

# Para no llenar la memoria en recorridos grandes, solo se graban los primeros pasos.
MAX_PASOS_GRABADOS = 400


class _Frontera:
    nombre = "frontera"
    descripcion = ""

    def __init__(self):
        self.pasos = [{"sale": None, "agrega": [], "frontera": []}]
        self.veces_agregado = Counter()
        self.total_sacados = 0

    # --- interfaz común -------------------------------------------------
    def agregar(self, nodo, padre=None, costo=0):
        self._poner(nodo, padre, costo)
        self.veces_agregado[nodo] += 1
        if len(self.pasos) <= MAX_PASOS_GRABADOS:
            self.pasos[-1]["agrega"].append(nodo)
            self.pasos[-1]["frontera"] = self.contenido()

    def sacar(self):
        if self.esta_vacia():
            raise IndexError(f"La {self.nombre} está vacía: no hay nada que sacar.")
        elemento = self._quitar()
        self.total_sacados += 1
        if len(self.pasos) <= MAX_PASOS_GRABADOS:
            self.pasos.append({"sale": elemento[0], "agrega": [], "frontera": self.contenido()})
        return elemento

    def esta_vacia(self):
        return len(self) == 0

    # --- para mostrar ---------------------------------------------------
    def contenido(self):
        """Nodos que esperan en la frontera, en el orden en que se dibujan."""
        raise NotImplementedError

    def orden_de_salida(self):
        """Nodos que salieron, en orden (incluye los repetidos que se descartaron)."""
        return [p["sale"] for p in self.pasos[1:]]

    def __repr__(self):
        return f"{type(self).__name__}({self.contenido()})"


class CustomPila(_Frontera):
    """Pila (LIFO): sale el ÚLTIMO que entró. Con ella, el recorrido es DFS."""

    nombre = "pila"
    descripcion = "fondo → tope"

    def __init__(self):
        super().__init__()
        self._datos = []

    def _poner(self, nodo, padre, costo):
        self._datos.append((nodo, padre, costo))

    def _quitar(self):
        return self._datos.pop()

    def contenido(self):
        return [n for n, _, _ in self._datos]

    def __len__(self):
        return len(self._datos)


class CustomCola(_Frontera):
    """Cola (FIFO): sale el PRIMERO que entró. Con ella, el recorrido es BFS."""

    nombre = "cola"
    descripcion = "frente → final"

    def __init__(self):
        super().__init__()
        self._datos = deque()

    def _poner(self, nodo, padre, costo):
        self._datos.append((nodo, padre, costo))

    def _quitar(self):
        return self._datos.popleft()

    def contenido(self):
        return [n for n, _, _ in self._datos]

    def __len__(self):
        return len(self._datos)


class FronteraHeap(_Frontera):
    """Heap de mínimos: sale el de MENOR costo acumulado. Con ella, el recorrido es Dijkstra.

    Internamente guarda tuplas (costo, nodo, padre) en un heapq de Python. Si dos
    elementos empatan en costo, sale el de código alfabéticamente menor.
    """

    nombre = "heap"
    descripcion = "en orden de salida (menor costo primero)"

    def __init__(self):
        super().__init__()
        self._datos = []

    def _poner(self, nodo, padre, costo):
        heapq.heappush(self._datos, (costo, nodo, "" if padre is None else padre))

    def _quitar(self):
        costo, nodo, padre = heapq.heappop(self._datos)
        return nodo, (None if padre == "" else padre), costo

    def contenido(self):
        return [f"{n}({c})" for c, n, _ in sorted(self._datos)]

    def arreglo(self):
        """El arreglo interno del heap, tal como lo guarda heapq."""
        return [(c, n) for c, n, _ in self._datos]

    def __len__(self):
        return len(self._datos)


def nombre_frontera(frontera) -> str:
    """'pila', 'cola' o 'heap' según el tipo de frontera."""
    return getattr(frontera, "nombre", type(frontera).__name__)
