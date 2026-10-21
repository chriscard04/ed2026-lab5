# 4. Consultas REST (recetas para copiar y pegar)

La API sigue la sintaxis de PostgREST. Con `labkit` escribes los parámetros como diccionario:

```python
respuesta = lab.get("tabla", {"parametro": "valor", ...})
filas = respuesta.json()
```

## Elegir columnas: `select`

```python
lab.get("grid_nodes", {"select": "id,kind,demand_kw"})
```

## Filtrar

| Quiero | Parámetro | Ejemplo |
|---|---|---|
| igual a | `columna=eq.valor` | `{"kind": "eq.transformador"}` |
| distinto de | `neq` | `{"status": "neq.cerrada"}` |
| mayor / menor | `gt`, `gte`, `lt`, `lte` | `{"demand_kw": "gte.100"}` |
| es nulo / no es nulo | `is.null`, `not.is.null` | `{"critical": "not.is.null"}` |
| está en una lista | `in.(a,b)` | `{"mode": "in.(metro,bus)"}` |
| empieza con | `like` | `{"id": "like.T1-*"}` |

```python
# Todos los clientes críticos de tu red
lab.get("grid_nodes", {"select": "id,name,critical", "critical": "not.is.null"}).json()

# Los hijos de un nodo
lab.get("grid_nodes", {"select": "id,kind", "parent_id": "eq.R1-1", "order": "id"}).json()

# Tramos de bus que tardan 8 minutos o más
lab.get("segments", {"mode": "eq.bus", "minutes": "gte.8"}).json()
```

## Ordenar y limitar

```python
lab.get("grid_nodes", {"order": "demand_kw.desc.nullslast", "limit": 5})   # 5 clientes con más demanda
```

## Paginar

```python
filas, offset = [], 0
while True:
    lote = lab.get("grid_nodes", {"order": "id", "limit": 1000, "offset": offset}).json()
    filas.extend(lote)
    if len(lote) < 1000:
        break
    offset += 1000
```

`lab.descargar("grid_nodes")` hace exactamente esto.

## Sin labkit: `requests` puro

Esto es lo que `labkit` hace por dentro (no lo necesitas en clase):

```python
import requests

URL = "https://<proyecto>.supabase.co"
CLAVE_PUBLICA = "sb_publishable_..."

# 1. Iniciar sesión → token
r = requests.post(f"{URL}/auth/v1/token?grant_type=password",
                  headers={"apikey": CLAVE_PUBLICA},
                  json={"email": "tu.correo@utp.ac.pa", "password": "tu clave"})
token = r.json()["access_token"]

# 2. Leer una tabla con el token
cabeceras = {"apikey": CLAVE_PUBLICA, "Authorization": f"Bearer {token}"}
r = requests.get(f"{URL}/rest/v1/stations", headers=cabeceras, params={"status": "eq.cerrada"})
print(r.status_code, r.json())

# 3. Enviar una respuesta (función del servidor)
r = requests.post(f"{URL}/rest/v1/rpc/responder", headers=cabeceras,
                  json={"p_pregunta": "M0.2", "p_valor": 1693})
print(r.json())
```

## Funciones del servidor (RPC)

| Endpoint | Cuerpo | Devuelve |
|---|---|---|
| `POST /rest/v1/rpc/responder` | `{"p_pregunta": "M1.3", "p_valor": 2453, "p_reto": null}` | `{"estado": "correcto", ...}` |
| `POST /rest/v1/rpc/pedir_reto` | `{"p_pregunta": "M1.2"}` | `{"reto_id": "...", "parametro": "T3-04"}` |
| `POST /rest/v1/rpc/estado` | `{}` | lista con el estado de cada pregunta |
| `POST /rest/v1/rpc/entregar` | `{}` | resumen de tu entrega |
| `POST /functions/v1/revisar` | `{"pregunta": "M1.A1"}` | retroalimentación de Claude sobre tu análisis |
