"""El esqueleto único del laboratorio: frontera + visitados.

Es la misma función que aparece en el notebook (bloque 1.1). Se incluye aquí para
que el generador de datos del docente calcule las respuestas con EXACTAMENTE el
mismo código que ejecutan los estudiantes.
"""

from __future__ import annotations


def recorrer(vecinos, inicio, frontera, minutos=None, destino=None):
    """Recorre un árbol o un grafo desde `inicio`.

    vecinos  : diccionario {nodo: [vecinos en orden alfabético]}
    frontera : CustomPila() -> DFS · CustomCola() -> BFS · FronteraHeap() -> Dijkstra
    minutos  : diccionario {(u, v): minutos} (solo para grafos con peso)
    destino  : si se indica, el recorrido se detiene al sacarlo de la frontera

    Devuelve tres cosas:
      orden  : nodos en el orden en que se visitaron
      padre  : {nodo: desde qué nodo se llegó}  (sirve para reconstruir caminos)
      costo  : {nodo: costo acumulado al visitarlo}
    """
    padre, costo, orden = {}, {}, []
    frontera.agregar(inicio, padre=None, costo=0)
    while not frontera.esta_vacia():
        nodo, de_donde, acumulado = frontera.sacar()
        if nodo in padre:  # ya visitado: se descarta
            continue
        padre[nodo] = de_donde
        costo[nodo] = acumulado
        orden.append(nodo)
        if nodo == destino:
            break
        for vecino in vecinos.get(nodo, []):
            if vecino not in padre:
                paso = minutos[(nodo, vecino)] if minutos else 1
                frontera.agregar(vecino, padre=nodo, costo=acumulado + paso)
    return orden, padre, costo


def camino(padre, destino):
    """Reconstruye el camino inicio -> destino siguiendo los padres hacia atrás."""
    if destino not in padre:
        return []
    ruta = []
    nodo = destino
    while nodo is not None:
        ruta.append(nodo)
        nodo = padre[nodo]
    return list(reversed(ruta))
