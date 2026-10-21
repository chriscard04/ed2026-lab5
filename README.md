# Lab 5 · Árboles y grafos con datos reales

**Estructura de Datos · Universidad Tecnológica de Panamá · ED2026**

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/chriscard04/ed2026-lab5/blob/estable/notebooks/Lab5_Arboles_Grafos.ipynb)

En este laboratorio usas árboles y grafos con **tus propios datos**, que descargas de una API:

- **Misión 1 · Se fue la luz:** la red eléctrica de tu sector es un árbol. Calculas cargas, encuentras
  quién se quedó sin luz y priorizas reparaciones con DFS, BFS y un heap.
- **Misión 2 · Moverse por tu ciudad:** el Metro y los buses forman un grafo con pesos. Comparas BFS,
  DFS y Dijkstra, y reconectas la ciudad cuando cierran una estación.

## Empieza en 5 pasos

1. Pulsa **Abrir en Colab** (arriba).
2. En Colab: *Archivo → Guardar una copia en Drive*. Trabaja siempre en **tu copia**.
3. Abre el ícono de la **llave** (Secrets) y crea `LAB_EMAIL` y `LAB_PASSWORD` con tus credenciales.
   Activa *Acceso del notebook* en ambos.
4. Ejecuta la **Celda 0**. Debe decir `Sesión iniciada: tu.correo@utp.ac.pa`.
5. Sigue el notebook bloque por bloque.

## Documentación

| | |
|---|---|
| [1. Primeros pasos](docs/01-primeros-pasos.md) | Colab, secretos, sesión y `lab.estado()` |
| [2. Conceptos](docs/02-conceptos.md) | REST, JSON → diccionario, token, RLS, paginación |
| [3. Tablas](docs/03-tablas.md) | Columnas y ejemplos de `grid_nodes`, `stations`, `segments`, `assignments`, `questions` |
| [4. Consultas REST](docs/04-consultas-rest.md) | Recetas para copiar y pegar: filtros, orden, paginación |
| [5. Referencia de labkit](docs/05-labkit.md) | Todas las funciones de `labkit` |
| [6. Formatos de respuesta](docs/06-formatos-de-respuesta.md) | **Formato exacto de cada respuesta**, con ejemplos válidos e inválidos |
| [7. Errores](docs/07-errores.md) | Qué significa cada error y qué hacer |
| [8. Preguntas frecuentes](docs/08-preguntas-frecuentes.md) | |

## Contenido del repositorio

```
labkit/       paquete de Python que usa el notebook (se instala solo en la Celda 0)
notebooks/    el notebook del laboratorio
docs/         esta documentación
```

`labkit` es código abierto: puedes leerlo para entender qué hace. No contiene respuestas: cada
respuesta se valida en el servidor con tus datos.
