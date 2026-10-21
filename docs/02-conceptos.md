# 2. Conceptos

## API REST

Una **API** es una puerta para que un programa pida datos a otro. En una API **REST**, cada recurso
tiene una URL y se usan los métodos de HTTP:

| Método | Para qué | En este lab |
|---|---|---|
| `GET` | leer | leer tus tablas: `GET /rest/v1/grid_nodes` |
| `POST` | enviar o ejecutar | enviar respuestas: `POST /rest/v1/rpc/responder` |

Cada respuesta trae un **código de estado**: `200` = bien, `401` = no autenticado, `404` = no existe,
`400`/`422` = la petición está mal formada. Lista completa en [7. Errores](07-errores.md).

## JSON → diccionario

La API responde en **JSON**. En Python, `respuesta.json()` lo convierte en listas y diccionarios:

```json
[{"id": "K-0002", "parent_id": "T1-01", "kind": "cliente", "demand_kw": 4}]
```

```python
filas = respuesta.json()
filas[0]["demand_kw"]   # 4
```

Cada fila de una tabla es un **registro**: un diccionario con los nombres de las columnas como claves.

## Token y sesión

Al ejecutar `Lab.login()`, el servidor verifica tu correo y tu clave y te entrega un **token**
(un JWT). `labkit` lo envía en cada petición, en la cabecera:

```
Authorization: Bearer eyJhbGciOi...
```

El token vence en una hora; `labkit` lo renueva solo.

## RLS: cada quien ve sus filas

Todas las personas leen las **mismas tablas**, pero PostgreSQL aplica una regla de seguridad por fila
(*Row Level Security*):

```sql
create policy "solo mis filas" on grid_nodes
  for select using (student_id = auth.uid());
```

`auth.uid()` sale de tu token. Aunque pidas las filas de otra persona, la base de datos no te las da.

## Paginación

El servidor devuelve **como máximo 1000 filas por petición**. Para traer más se pide por páginas:

| Petición | `limit` | `offset` | Filas |
|---|---|---|---|
| 1 | 1000 | 0 | 0 a 999 |
| 2 | 1000 | 1000 | 1000 a 1999 |
| 3 | 1000 | 2000 | las que queden (menos de 1000 → era la última) |

Siempre pagina con un `order` fijo (por ejemplo `order=id`). Sin orden, dos páginas podrían repetir
o saltarse filas.

## De tablas a estructuras

| Tabla | Estructura | Cómo se arma |
|---|---|---|
| `grid_nodes` | **árbol** | `hijos[parent_id].append(id)` |
| `stations` + `segments` | **grafo con pesos** | `vecinos[a].append(b)`, `vecinos[b].append(a)` y `minutos[(a, b)]` |

## Un esqueleto, tres recorridos

```python
orden, padre, costo = recorrer(vecinos, inicio, frontera, minutos=None, destino=None)
```

| Frontera | Sale primero | Recorrido | Sirve para |
|---|---|---|---|
| `CustomPila()` | el último que entró | **DFS** | componentes, recorrer sin recursión, postorden |
| `CustomCola()` | el primero que entró | **BFS** | menos paradas o niveles, lo más cercano |
| `FronteraHeap()` | el de menor costo | **Dijkstra** | menos minutos (pesos ≥ 0) |
