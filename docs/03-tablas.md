# 3. Tablas

Todas se leen con `GET /rest/v1/<tabla>`. Solo ves **tus** filas.

## `grid_nodes` · tu red eléctrica (árbol)

| Columna | Tipo | Descripción |
|---|---|---|
| `student_id` | uuid | tu id (siempre el mismo) |
| `id` | texto | id del nodo (ver formatos abajo) |
| `parent_id` | texto o `null` | id del padre; `null` solo en la subestación |
| `kind` | texto | `subestacion`, `circuito`, `ramal`, `transformador`, `poste` o `cliente` |
| `name` | texto | nombre legible |
| `demand_kw` | entero o `null` | demanda en kW (solo clientes) |
| `capacity_kw` | entero o `null` | capacidad en kW (solo transformadores) |
| `critical` | texto o `null` | `hospital`, `escuela`, `bombeo`, `centro_salud` o `null` |

Formatos de `id`:

| Tipo | Formato | Ejemplo |
|---|---|---|
| subestación | `SE` | `SE` |
| circuito | `C#` | `C3` |
| ramal | `R#-#` | `R1-1` |
| transformador | `T#-##` | `T4-07` |
| poste | `P#-####` | `P6-0412` |
| cliente | `K-####` | `K-0031` |

Ejemplo de fila:

```json
{"student_id": "4b1c…", "id": "T1-01", "parent_id": "R1-1", "kind": "transformador",
 "name": "Transformador 1-01", "demand_kw": null, "capacity_kw": 18, "critical": null}
```

## `stations` · estaciones y paradas (vértices del grafo)

| Columna | Tipo | Descripción |
|---|---|---|
| `code` | texto | 3 letras para el Metro (`ALB`) o `B#-##` para paradas de bus (`B3-01`) |
| `name` | texto | nombre de la estación |
| `line` | texto | `L1`, `L2`, `L1/L2` o la ruta de bus (`B3`) |
| `status` | texto | `operativa` o `cerrada` |
| `x`, `y` | número | posición para dibujar el mapa |

## `segments` · tramos (aristas del grafo, sin dirección)

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | entero | id del tramo |
| `from_code`, `to_code` | texto | estaciones que une (se viaja en los dos sentidos) |
| `minutes` | entero | minutos que tarda el tramo (el peso) |
| `mode` | texto | `metro` o `bus` |
| `line` | texto | línea o ruta |

## `assignments` · tu asignación personal

Pares `key` → `value` (JSON). Usa `lab.asignacion()` para tenerlos como diccionario.

| key | Ejemplo de value | Qué es |
|---|---|---|
| `sector` | `{"nombre": "Betania", "subestacion": "SE"}` | tu sector |
| `ramal_practica` | `"R1-1"` | ramal para las predicciones |
| `prediccion_bfs_k` | `5` | el k de M1.P1 |
| `falla` | `{"nodo": "R3-2", "descripcion": "..."}` | la falla de tu red |
| `heap_valores` | `[71, 140, 111, 126, 81]` | valores del bloque del heap |
| `top_k` | `5` | cuántos transformadores van en el top |
| `estacion_cerrada` | `"SMG"` | estación en mantenimiento |
| `par1`, `par2` | `{"origen": "ALB", "destino": "PED"}` | pares origen → destino |
| `prediccion_bfs_k_m2` | `4` | el k de M2.P1 |
| `origen_radio`, `radio_paradas` | `"DOC"`, `3` | para M2.8 |

## `questions` · catálogo de preguntas

Igual para todos. Columnas útiles: `id`, `title`, `type`, `prompt`, `format`, `example`,
`max_attempts`, `optional`, `is_challenge`. Ver [6. Formatos de respuesta](06-formatos-de-respuesta.md).
