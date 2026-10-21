# 1. Primeros pasos

## Antes de la clase (10 minutos)

1. Abre el notebook con el botón **Abrir en Colab** del [README](../README.md).
2. *Archivo → Guardar una copia en Drive*. Desde ahora trabaja en esa copia.
3. Crea tus **secretos** en Colab:
   - Barra izquierda → ícono de la **llave** 🔑 → *Agregar nuevo secreto*.
   - Nombre `LAB_EMAIL`, valor: tu correo institucional (por ejemplo `nombre.apellido@utp.ac.pa`).
   - Nombre `LAB_PASSWORD`, valor: la clave temporal que te entregó el docente.
   - Activa el interruptor **Acceso del notebook** en los dos.
4. Ejecuta la **Celda 0**. Si todo está bien verás:

   ```
   Sesión iniciada: nombre.apellido@utp.ac.pa
   Tu sector: ... · Tu estación cerrada: ...
   ```

> **¿Por qué secretos?** Una clave escrita en el código termina compartida por accidente (capturas,
> copias del notebook, GitHub). Los secretos de Colab quedan fuera del código.

## Durante la clase

| Quiero... | Uso |
|---|---|
| ver mi asignación personal | `lab.asignacion()` |
| ver qué me falta | `lab.estado()` |
| ver el enunciado y el formato de una pregunta | `lab.pregunta("M1.3")` |
| enviar una respuesta | `lab.responder("M1.3", valor)` |
| pedir un reto sorpresa | `lab.reto("M1.2")` |
| pedir otra vez la revisión de un análisis | `lab.revisar("M1.A1")` |
| entregar | `lab.entregar()` |

## Si se reinicia Colab

Colab borra la memoria si se desconecta. Vuelve a ejecutar las celdas desde el principio
(*Entorno de ejecución → Ejecutar anteriores*). **Tus respuestas no se pierden:** están en el servidor.
