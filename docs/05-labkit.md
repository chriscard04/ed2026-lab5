# 5. Referencia de labkit

```python
from labkit import Lab, CustomPila, CustomCola, FronteraHeap, nombre_frontera, camino
lab = Lab.login()
```

## Sesión y datos

| Función | Qué hace |
|---|---|
| `Lab.login()` | Inicia sesión con los secretos `LAB_EMAIL` y `LAB_PASSWORD` de Colab |
| `lab.get(tabla, params)` | `GET /rest/v1/<tabla>`; devuelve la respuesta HTTP (`.status_code`, `.json()`) |
| `lab.descargar(tabla)` | Descarga todas las filas paginando de 1000 en 1000; devuelve una lista de diccionarios |
| `lab.asignacion()` | Tu asignación personal como diccionario |

## Respuestas

| Función | Qué hace |
|---|---|
| `lab.pregunta(id)` | Muestra el enunciado, el formato y un ejemplo |
| `lab.responder(id, valor)` | Revisa el formato en tu computadora y, si está bien, envía la respuesta |
| `lab.reto(id)` | Pide un reto sorpresa (`M1.2`, `M2.5`) y devuelve su parámetro |
| `lab.revisar(id)` | Pide de nuevo la retroalimentación de Claude sobre tu último análisis |
| `lab.estado()` | Tabla con el estado de todas tus preguntas |
| `lab.entregar()` | Registra tu entrega y muestra un resumen |

## Fronteras

Las tres tienen la misma interfaz:

```python
f.agregar(nodo, padre=None, costo=0)
nodo, padre, costo = f.sacar()
f.esta_vacia()
```

| Clase | Sale primero | Extra |
|---|---|---|
| `CustomPila()` | el último que entró | `f.pasos`: la traza grabada |
| `CustomCola()` | el primero que entró | `f.pasos` |
| `FronteraHeap()` | el de menor costo (empate: código menor) | `f.veces_agregado[nodo]`: cuántas veces entró cada nodo |

`nombre_frontera(f)` devuelve `"pila"`, `"cola"` o `"heap"`.

## Recorrido

```python
orden, padre, costo = recorrer(vecinos, inicio, frontera, minutos=None, destino=None)
ruta = camino(padre, destino)
```

- `orden`: nodos en el orden en que se visitaron.
- `padre`: de dónde se llegó a cada nodo (sirve para reconstruir rutas con `camino`).
- `costo`: niveles (sin `minutos`) o minutos acumulados (con `minutos`).

## Dibujos

| Función | Qué dibuja |
|---|---|
| `lab.ver_subarbol(hijos, info, raiz)` | un subárbol en texto |
| `lab.ver_frontera(frontera)` | la frontera paso a paso: qué salió, qué entró, cómo quedó |
| `lab.ver_heap(lista)` | un heap como árbol, con índices |
| `lab.ver_mapa(estaciones, tramos, rutas={...})` | el mapa de tu ciudad, con rutas superpuestas |
| `lab.ver_cargas(carga, info, tipo=...)` | barras de carga por circuito o transformador |

## Registro

`labkit` registra tu actividad en el servidor (peticiones, ajustes `✏️` y respuestas) para que el
docente pueda acompañar tu proceso. `lab.anotar(bloque, ...)` deja constancia de un ajuste.
