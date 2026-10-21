"""Prevalidación local de respuestas (las mismas reglas que aplica el servidor).

Si el formato está mal, labkit NO envía nada y no gastas intento.
"""

from __future__ import annotations

import difflib
import re

PATRON_NODO = re.compile(r"^(SE|C[0-9]|R[0-9]-[0-9]|T[0-9]-[0-9]{2}|P[0-9]-[0-9]{4}|K-[0-9]{4})$")
PATRON_ESTACION = re.compile(r"^([A-Z]{3}|B[0-9]-[0-9]{2})$")
FRONTERAS = ("pila", "cola", "heap")


def normalizar(valor):
    """Convierte tipos de numpy/pandas a tipos de Python (sin cambiar el formato)."""
    tipo = type(valor).__module__
    if tipo.startswith("numpy"):
        try:
            return valor.item()
        except AttributeError:
            return valor.tolist()
    if isinstance(valor, list):
        return [normalizar(v) for v in valor]
    if isinstance(valor, dict):
        return {k: normalizar(v) for k, v in valor.items()}
    return valor


def _es_entero(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _sugerencia(valor, conocidos):
    if not conocidos or not isinstance(valor, str):
        return ""
    candidatos = difflib.get_close_matches(valor.strip().upper(), conocidos, n=1, cutoff=0.6)
    return f' ¿Quisiste decir "{candidatos[0]}"?' if candidatos else ""


def validar(tipo, v, nodos_conocidos=None, estaciones_conocidas=None):
    """Devuelve None si el formato es correcto; si no, un mensaje que explica qué corregir."""
    if v is None:
        return "Llegó None: todavía no pusiste tu respuesta (cambia el valor de ejemplo)."
    if v is ...:
        return "Llegó ... (puntos suspensivos): todavía no pusiste tu respuesta."

    if tipo == "entero":
        if isinstance(v, float) and v.is_integer():
            return f"Llegó {v} (con decimales). Envía un entero: int({v}) → {int(v)}."
        if isinstance(v, str):
            return f'Llegó el texto "{v}". Envía el número sin comillas, por ejemplo 1482.'
        if not _es_entero(v):
            return f"Se esperaba un número entero; llegó {v!r} ({type(v).__name__})."
        return None

    if tipo in ("nodo", "estacion"):
        patron = PATRON_NODO if tipo == "nodo" else PATRON_ESTACION
        conocidos = nodos_conocidos if tipo == "nodo" else estaciones_conocidas
        ejemplo = '"K-0002" o "T1-01"' if tipo == "nodo" else '"ALB" o "B3-01"'
        if not isinstance(v, str):
            return f"Se esperaba un texto entre comillas, por ejemplo {ejemplo}; llegó {v!r}."
        if not patron.match(v):
            return f'"{v}" no tiene el formato de un {"id de nodo" if tipo == "nodo" else "código de estación"} ({ejemplo}).' + _sugerencia(v, conocidos)
        if conocidos and v not in conocidos:
            return f'"{v}" no existe en tus datos.' + _sugerencia(v, conocidos)
        return None

    if tipo == "frontera":
        if not isinstance(v, str) or v not in FRONTERAS:
            pista = ""
            if isinstance(v, str) and v.strip().lower() in FRONTERAS:
                pista = f' Escríbelo en minúscula y sin espacios: "{v.strip().lower()}".'
            elif isinstance(v, str) and "pila" in v.lower():
                pista = ' Escribe solo "pila".'
            return f'Se esperaba "pila", "cola" o "heap"; llegó {v!r}.' + pista
        return None

    if tipo in ("lista_nodos", "lista_estaciones", "lista_enteros"):
        if isinstance(v, tuple):
            return "Llegó una tupla ( ). Usa corchetes [ ] para la lista: list(tu_tupla)."
        if isinstance(v, str):
            return "Llegó un texto. La respuesta es una LISTA entre corchetes, por ejemplo [\"A\", \"B\"]."
        if not isinstance(v, list):
            return f"Se esperaba una lista entre corchetes [ ]; llegó {type(v).__name__}."
        if tipo == "lista_estaciones" and not v:
            return "La lista está vacía. Una ruta tiene al menos el origen y el destino."
        interno = {"lista_nodos": "nodo", "lista_estaciones": "estacion", "lista_enteros": "entero"}[tipo]
        for i, e in enumerate(v, start=1):
            error = validar(interno, e, nodos_conocidos, estaciones_conocidas)
            if error:
                return f"Elemento {i} de la lista: {error}"
        return None

    if tipo == "tramo":
        if not isinstance(v, dict):
            return 'Se esperaba un diccionario {"desde": "...", "hasta": "...", "minutos": 6}.'
        if sorted(v) != ["desde", "hasta", "minutos"]:
            return f'El diccionario debe tener exactamente las claves "desde", "hasta" y "minutos"; tiene {sorted(v)}.'
        for clave in ("desde", "hasta"):
            error = validar("estacion", v[clave], None, estaciones_conocidas)
            if error:
                return f'En "{clave}": {error}'
        if not _es_entero(v["minutos"]) or not 1 <= v["minutos"] <= 30:
            return '"minutos" debe ser un número entero entre 1 y 30, sin comillas.'
        return None

    if tipo == "analisis":
        if not isinstance(v, str):
            return "Se esperaba un texto entre comillas."
        n = len(v.strip())
        if n < 40:
            return f"Tu texto tiene {n} caracteres; escribe al menos 40, en oraciones completas."
        if n > 600:
            return f"Tu texto tiene {n} caracteres; el máximo es 600. Resume."
        return None

    return f"Tipo de pregunta desconocido: {tipo}"
