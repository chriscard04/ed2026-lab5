# 7. Errores y qué hacer

## Mensajes de `lab.responder`

| Mensaje | Qué significa | Qué hacer |
|---|---|---|
| `FORMATO · ... No se envió` | `labkit` detectó un formato inválido en tu computadora | Corrige según el formato y el ejemplo que muestra. **No gastaste intento.** |
| `FORMATO · ...` (del servidor) | El servidor rechazó el formato | Igual que arriba. No gasta intento. |
| `INCORRECTO · ... Pista: ...` | Formato correcto, respuesta incorrecta | Lee la pista, revisa tu código y vuelve a enviar. |
| `SIN INTENTOS` | Se acabaron los intentos | Lee la explicación y la respuesta esperada; sigue con el lab. |
| `FALTA EL RETO` | Es una pregunta con reto | Ejecuta `lab.reto("ID")` antes de responder. |
| `Ese reto ya se usó` | Cada reto sirve para un envío | Pide otro con `lab.reto("ID")` y recalcula. |
| `YA RESPONDIDA` | Ya la tienes correcta | Nada: sigue adelante. |
| `CERRADO` | El laboratorio terminó | Ya no se reciben respuestas. |

## Errores de Python frecuentes

| Error | Causa probable | Solución |
|---|---|---|
| `SyntaxError` en una línea con `???` | No cambiaste el ajuste `✏️` | Reemplaza `???` por lo que pide el comentario |
| `NameError: name 'hijos' is not defined` | Colab se reinició o te saltaste una celda | *Entorno de ejecución → Ejecutar anteriores* |
| `KeyError: 'XYZ'` | Un id o código que no existe en tus datos | Revisa mayúsculas y guiones; usa los de tus tablas |
| `RecursionError` | Recursión demasiado profunda | Es parte del bloque 1.4: se resuelve con la pila |
| `ErrorLab: No pude leer el secreto` | Faltan los secretos o su permiso | Llave 🔑 → crea `LAB_EMAIL`/`LAB_PASSWORD` y activa *Acceso del notebook* |
| `ErrorLab: No se pudo iniciar sesión (400)` | Correo o clave incorrectos | Copia la clave temporal sin espacios |

## Códigos HTTP

| Código | Significado |
|---|---|
| `200` | Todo bien |
| `400` | La petición está mal formada (parámetro inválido) |
| `401` | No autenticado: token ausente o vencido (ejecuta `Lab.login()` otra vez) |
| `403` | Autenticado, pero sin permiso para eso |
| `404` | La tabla o función no existe (o no es pública) |
| `409` | Conflicto: por ejemplo, el análisis ya fue revisado |
| `429` | Demasiadas peticiones o revisiones agotadas |
| `5xx` | Falla del servidor: espera unos segundos y reintenta |
