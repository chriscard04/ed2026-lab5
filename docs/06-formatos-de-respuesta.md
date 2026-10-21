# 6. Formatos de respuesta

El servidor valida cada respuesta con reglas **estrictas**. Antes de enviar, `labkit` revisa el
formato en tu computadora: si algo está mal, te dice qué corregir y **no gastas intento**.

Todas las respuestas se envían igual:

```python
lab.responder("<ID de la pregunta>", <tu valor>)
```

## Tipos de respuesta

### `entero` · Número entero

Número entero, sin comillas, sin puntos ni comas de miles, sin decimales y sin unidades.

| Válido ✅ | No válido ❌ |
|---|---|
| `1482` | `"1482"` |
| `0` | `1,482` |
|  | `1482.0` |
|  | `"1482 kW"` |

### `nodo` · Id de nodo

Texto entre comillas con el id EXACTO del nodo, como aparece en tus datos (mayúsculas, guion y ceros).

| Válido ✅ | No válido ❌ |
|---|---|
| `"K-0002"` | `"k-0002"` |
| `"T1-01"` | `"K-2"` |
| `"R1-1"` | `"Cliente 0002"` |
|  | `K-0002 (sin comillas)` |

### `lista_nodos` · Lista de ids de nodo

Lista entre corchetes [ ] con ids de nodo entre comillas, separados por comas, en el orden que pide la pregunta.

| Válido ✅ | No válido ❌ |
|---|---|
| `["T1-01", "K-0004"]` | `"T1-01, K-0004"` |
| `[]` | `("T1-01", "K-0004")` |
|  | `["t1-01"]` |

### `lista_enteros` · Lista de enteros

Lista entre corchetes [ ] con números enteros separados por comas, en el orden del arreglo.

| Válido ✅ | No válido ❌ |
|---|---|
| `[81, 126, 111, 140]` | `"81, 126"` |
|  | `["81", "126"]` |
|  | `(81, 126)` |

### `estacion` · Código de estación

Texto entre comillas con el código de la estación: 3 letras MAYÚSCULAS (Metro) o B#-## (parada de bus).

| Válido ✅ | No válido ❌ |
|---|---|
| `"ALB"` | `"alb"` |
| `"B3-01"` | `"Albrook"` |
|  | `" ALB"` |
|  | `"B3-1"` |

### `lista_estaciones` · Lista de estaciones

Lista entre corchetes [ ] con códigos de estación entre comillas, desde el origen hasta el destino.

| Válido ✅ | No válido ❌ |
|---|---|
| `["ALB", "CUR", "CMY"]` | `"ALB, CUR"` |
|  | `["Albrook", "Curundú"]` |
|  | `("ALB", "CUR")` |

### `frontera` · Frontera

Una de estas tres palabras, en minúscula y entre comillas: "pila", "cola" o "heap".

| Válido ✅ | No válido ❌ |
|---|---|
| `"heap"` | `"Pila"` |
| `"cola"` | `"CustomPila"` |
|  | `"dijkstra"` |
|  | `"BFS"` |

### `tramo` · Tramo

Diccionario con tres claves: "desde" y "hasta" (códigos de estación) y "minutos" (entero de 1 a 30).

| Válido ✅ | No válido ❌ |
|---|---|
| `{"desde": "PNU", "hasta": "PDA", "minutos": 6}` | `["PNU", "PDA", 6]` |
|  | `{"desde": "PNU", "hasta": "PDA", "minutos": "6"}` |
|  | `{"de": "PNU", "a": "PDA"}` |

### `analisis` · Texto de análisis

Texto entre comillas de 40 a 600 caracteres, en oraciones completas. Usa los datos de TU caso.

| Válido ✅ | No válido ❌ |
|---|---|
| `"BFS cuenta paradas y no minutos; por eso en mi par ALB → PED..."` | `""` |
|  | `"porque sí"` |
|  | `un texto de más de 600 caracteres` |

## Todas las preguntas

Los ejemplos muestran la **forma** de la respuesta, no el valor correcto: tus datos son distintos.

### Misión 0 · Conéctate a tus datos

| ID | Pregunta | Tipo | Ejemplo de envío | Intentos |
|---|---|---|---|---|
| `M0.1` | Filas sin paginar | `entero` | `lab.responder("M0.1", 250)` | 3 |
| `M0.2` | Total de nodos de tu red | `entero` | `lab.responder("M0.2", 1693)` | 3 |
| `M0.3` | Peticiones de la paginación | `entero` | `lab.responder("M0.3", 7)` | 3 |

### Misión 1 · Se fue la luz

| ID | Pregunta | Tipo | Ejemplo de envío | Intentos |
|---|---|---|---|---|
| `M1.P1` | Predicción BFS en el ramal | `nodo` | `lab.responder("M1.P1", "K-0002")` | 3 |
| `M1.P2` | Predicción de la pila | `lista_nodos` | `lab.responder("M1.P2", ["T1-01", "K-0004", "K-0005"])` | 3 |
| `M1.T1` | Traza DFS del ramal | `lista_nodos` | `lab.responder("M1.T1", ["R1-1", "T1-02", "K-0006", "K-0005", "K-0004", "T1-01", "K-0003", "K-0002"])` | 3 |
| `M1.2` | Reto sorpresa: carga de un nodo (con reto) | `entero` | `lab.responder("M1.2", 2453)` | 3 |
| `M1.3` | Carga total del sector | `entero` | `lab.responder("M1.3", 2453)` | 3 |
| `M1.4` | Clientes sin luz | `entero` | `lab.responder("M1.4", 18)` | 3 |
| `M1.5` | Clientes críticos afectados (el orden no importa) | `lista_nodos` | `lab.responder("M1.5", ["K-0379"])` | 3 |
| `M1.6` | Primer cliente crítico que encuentra BFS | `nodo` | `lab.responder("M1.6", "K-0001")` | 3 |
| `M1.7` | Altura de la red (opcional) | `entero` | `lab.responder("M1.7", 1257)` | 3 |
| `M1.P3` | Heap: nueva raíz | `entero` | `lab.responder("M1.P3", 81)` | 3 |
| `M1.P4` | Heap: arreglo después de sacar | `lista_enteros` | `lab.responder("M1.P4", [81, 126, 111, 140])` | 3 |
| `M1.8` | Top de transformadores sobrecargados | `lista_nodos` | `lab.responder("M1.8", ["T4-04", "T4-01", "T3-05", "T1-02", "T4-06"])` | 3 |
| `M1.A1` | ¿Por qué funciona el orden al revés? | `analisis` | `lab.responder("M1.A1", "En mi red, ...")` | 2 revisiones |
| `M1.A2` | BFS frente a DFS para encontrar lo urgente | `analisis` | `lab.responder("M1.A2", "En mi red, ...")` | 2 revisiones |
| `M1.A3` | Heap de mínimos para buscar los mayores | `analisis` | `lab.responder("M1.A3", "En mi red, ...")` | 2 revisiones |
| `M1.A4` | ¿A dónde mandas la primera cuadrilla? | `analisis` | `lab.responder("M1.A4", "En mi red, ...")` | 2 revisiones |

### Misión 2 · Moverse por tu ciudad

| ID | Pregunta | Tipo | Ejemplo de envío | Intentos |
|---|---|---|---|---|
| `M2.P1` | Predicción BFS en tu ciudad | `estacion` | `lab.responder("M2.P1", "FDC")` | 3 |
| `M2.1` | Ruta con menos paradas | `lista_estaciones` | `lab.responder("M2.1", ["IGC", "STO", "LOT", "B4-01", "B4-02", "PDA", "LAN"])` | 3 |
| `M2.2` | Ruta más rápida | `lista_estaciones` | `lab.responder("M2.2", ["IGC", "VAR", "FDC", "ING", "DOC", "PNU", "SMG", "PDA", "LAN"])` | 3 |
| `M2.3` | Minutos de la ruta más rápida | `entero` | `lab.responder("M2.3", 25)` | 3 |
| `M2.4` | Reingresos al heap | `entero` | `lab.responder("M2.4", 5)` | 3 |
| `M2.5` | Reto sorpresa: ruta más rápida (con reto) | `lista_estaciones` | `lab.responder("M2.5", ["ALB", "CUR", "CMY"])` | 3 |
| `M2.6` | Componentes con la estación cerrada | `entero` | `lab.responder("M2.6", 4)` | 3 |
| `M2.7` | Tramo que reconecta la ciudad | `tramo` | `lab.responder("M2.7", {"desde": "PNU", "hasta": "PDA", "minutos": 6})` | 3 |
| `M2.8` | Radio de 3 paradas (opcional) | `entero` | `lab.responder("M2.8", 11)` | 3 |
| `M2.A1` | ¿Qué ruta recomiendas? | `analisis` | `lab.responder("M2.A1", "En mi red, ...")` | 2 revisiones |
| `M2.A2` | Reingresos y visitados | `analisis` | `lab.responder("M2.A2", "En mi red, ...")` | 2 revisiones |
| `M2.A3` | Tu tramo propuesto | `analisis` | `lab.responder("M2.A3", "En mi red, ...")` | 2 revisiones |

### Informe final

| ID | Pregunta | Tipo | Ejemplo de envío | Intentos |
|---|---|---|---|---|
| `INF.E1` | Escenario: ambulancia | `frontera` | `lab.responder("INF.E1", "cola")` | 3 |
| `INF.E2` | Escenario: ¿sigue conectada? | `frontera` | `lab.responder("INF.E2", "heap")` | 3 |
| `INF.E3` | Escenario: turista | `frontera` | `lab.responder("INF.E3", "pila")` | 3 |
| `INF.A1` | Tu hallazgo principal | `analisis` | `lab.responder("INF.A1", "En mi red, ...")` | 2 revisiones |

## Preguntas con reto sorpresa

En `M1.2` y `M2.5` primero pides un reto. El servidor te da un parámetro distinto cada vez:

```python
nodo = lab.reto("M1.2")          # por ejemplo "T3-04"
lab.responder("M1.2", carga[nodo])
```

Cada reto sirve para **un** envío. Si fallas, pide otro reto y vuelve a calcular.

## Lo que pasa después de enviar

| Estado | Significado | ¿Gasta intento? |
|---|---|---|
| `correcto` | Respuesta correcta | Sí |
| `incorrecto` | No es correcta; recibes una pista | Sí |
| `agotado` | Se acabaron los intentos; ves la explicación y la respuesta esperada | — |
| `formato` | El valor no tiene el formato pedido | **No** |
| `recibido` | Tu análisis se guardó y pasa a revisión | Usa 1 de 2 revisiones |
