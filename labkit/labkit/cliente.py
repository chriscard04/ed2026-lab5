"""Cliente del laboratorio: inicia sesión, lee tus datos por la API REST y envía respuestas."""

from __future__ import annotations

import atexit
import json
import os
import sys
import time

import requests

from . import formatos, visual
from .config import SUPABASE_KEY, SUPABASE_URL

ORDEN_POR_TABLA = {"grid_nodes": "id", "stations": "code", "segments": "id", "assignments": "key", "questions": "position"}
LIMITE_POR_PETICION = 1000


class ErrorLab(Exception):
    pass


def _leer_secreto(nombre):
    """Lee un secreto de Colab (ícono de la llave) o, si no estás en Colab, una variable de entorno."""
    try:
        from google.colab import userdata  # type: ignore

        return userdata.get(nombre)
    except ImportError:
        return os.environ.get(nombre)
    except Exception as e:  # secreto inexistente o sin permiso
        raise ErrorLab(
            f"No pude leer el secreto {nombre} de Colab ({type(e).__name__}).\n"
            "Abre el ícono de la llave (Secrets) a la izquierda, crea LAB_EMAIL y LAB_PASSWORD\n"
            "con tus credenciales y activa el interruptor 'Acceso del notebook'."
        ) from None


class Lab:
    """Tu conexión al laboratorio. Créala con: lab = Lab.login()"""

    def __init__(self, url, clave, sesion, email):
        self.url = url.rstrip("/")
        self.clave = clave
        self.email = email
        self._sesion = sesion
        self._http = requests.Session()
        self._eventos = []
        self._retos = {}
        self._asignacion = None
        self.nodos_conocidos = set()
        self.estaciones_conocidas = set()
        self.preguntas = {p["id"]: p for p in self.descargar("questions", silencioso=True)}
        atexit.register(self._enviar_eventos)

    # ── Sesión ──────────────────────────────────────────────────────────
    @classmethod
    def login(cls, email=None, password=None):
        url = os.environ.get("LAB_SUPABASE_URL", SUPABASE_URL)
        clave = os.environ.get("LAB_SUPABASE_KEY", SUPABASE_KEY)
        email = (email or _leer_secreto("LAB_EMAIL") or "").strip().lower()
        password = password or _leer_secreto("LAB_PASSWORD") or ""
        if not email or not password:
            raise ErrorLab("Faltan tus credenciales: crea los secretos LAB_EMAIL y LAB_PASSWORD en Colab.")
        r = requests.post(f"{url}/auth/v1/token?grant_type=password",
                          headers={"apikey": clave}, json={"email": email, "password": password}, timeout=30)
        if r.status_code != 200:
            raise ErrorLab(f"No se pudo iniciar sesión ({r.status_code}). Revisa tu correo y tu clave temporal.")
        lab = cls(url, clave, r.json(), email)
        lab._evento("login", {"python": sys.version.split()[0]})
        print(f"Sesión iniciada: {email}")
        try:
            a = lab.asignacion()
            print(f"Tu sector: {a['sector']['nombre']} · Tu estación cerrada: {a['estacion_cerrada']}")
        except Exception:
            pass
        return lab

    def _token(self):
        if time.time() > self._sesion.get("expires_at", 0) - 120:
            r = requests.post(f"{self.url}/auth/v1/token?grant_type=refresh_token",
                              headers={"apikey": self.clave},
                              json={"refresh_token": self._sesion["refresh_token"]}, timeout=30)
            if r.status_code == 200:
                self._sesion = r.json()
        return self._sesion["access_token"]

    def _headers(self):
        return {"apikey": self.clave, "Authorization": f"Bearer {self._token()}"}

    # ── Lectura de datos (REST) ─────────────────────────────────────────
    def get(self, tabla, params=None):
        """GET /rest/v1/<tabla> con tus credenciales. Devuelve la respuesta HTTP tal cual."""
        r = self._http.get(f"{self.url}/rest/v1/{tabla}", headers=self._headers(), params=params or {}, timeout=60)
        filas = None
        try:
            datos = r.json()
            filas = len(datos) if isinstance(datos, list) else None
        except ValueError:
            pass
        self._evento("get", {"tabla": tabla, "params": params or {}, "status": r.status_code, "filas": filas})
        return r

    def descargar(self, tabla, select="*", silencioso=False):
        """Descarga TODAS las filas de una tabla, pidiéndolas de 1000 en 1000."""
        filas, offset = [], 0
        while True:
            r = self.get(tabla, {"select": select, "order": ORDEN_POR_TABLA.get(tabla, "id"),
                                 "limit": LIMITE_POR_PETICION, "offset": offset})
            if r.status_code != 200:
                raise ErrorLab(f"Error {r.status_code} al leer {tabla}: {r.text[:200]}")
            lote = r.json()
            filas.extend(lote)
            if len(lote) < LIMITE_POR_PETICION:
                break
            offset += LIMITE_POR_PETICION
        if tabla == "grid_nodes":
            self.nodos_conocidos = {f["id"] for f in filas if "id" in f}
        if tabla == "stations":
            self.estaciones_conocidas = {f["code"] for f in filas if "code" in f}
        if not silencioso:
            print(f"{tabla}: {len(filas)} filas")
        return filas

    def asignacion(self):
        """Tu asignación personal (falla, pares origen-destino, estación cerrada...) como diccionario."""
        if self._asignacion is None:
            self._asignacion = {f["key"]: f["value"] for f in self.descargar("assignments", silencioso=True)}
        return self._asignacion

    # ── Respuestas ──────────────────────────────────────────────────────
    def _rpc(self, nombre, **params):
        self._enviar_eventos()
        r = self._http.post(f"{self.url}/rest/v1/rpc/{nombre}", headers=self._headers(), json=params, timeout=60)
        if r.status_code != 200:
            raise ErrorLab(f"Error {r.status_code} en {nombre}: {r.text[:300]}")
        return r.json()

    def pregunta(self, pid):
        """Muestra el enunciado, el formato y un ejemplo de envío de una pregunta."""
        q = self._q(pid)
        print(f"{q['id']} · {q['title']}\n{q['prompt']}\n\nFormato: {q['format']}\n"
              f"Ejemplo de envío: lab.responder(\"{q['id']}\", {json.dumps(q['example'], ensure_ascii=False)})")

    def _q(self, pid):
        if pid not in self.preguntas:
            raise ErrorLab(f'No existe la pregunta "{pid}". Ejemplos de ids: M0.1, M1.P1, M2.3, INF.E1.')
        return self.preguntas[pid]

    def reto(self, pid):
        """Pide un reto sorpresa al servidor y devuelve su parámetro."""
        self._q(pid)
        r = self._rpc("pedir_reto", p_pregunta=pid)
        if r.get("estado") != "ok":
            print("NO SE PUDO ·", r.get("mensaje"))
            return None
        self._retos[pid] = r["reto_id"]
        print(f"Tu reto para {pid}: {r['parametro']}")
        return r["parametro"]

    def responder(self, pid, valor):
        """Envía tu respuesta. Antes revisa el formato aquí mismo (si está mal, no gasta intento)."""
        q = self._q(pid)
        valor = formatos.normalizar(valor)
        error = formatos.validar(q["type"], valor, self.nodos_conocidos, self.estaciones_conocidas)
        if error:
            self._evento("formato_local", {"pregunta": pid, "error": error})
            print(f"FORMATO · {pid} · No se envió (no gastaste intento).\n  {error}\n"
                  f"  Formato: {q['format']}\n"
                  f"  Ejemplo: lab.responder(\"{pid}\", {json.dumps(q['example'], ensure_ascii=False)})")
            return
        params = {"p_pregunta": pid, "p_valor": valor}
        if q["is_challenge"]:
            if pid not in self._retos:
                print(f'FALTA EL RETO · Primero ejecuta: lab.reto("{pid}")')
                return
            params["p_reto"] = self._retos.pop(pid)
        r = self._rpc("responder", **params)
        self._mostrar(pid, r)
        if r.get("estado") == "recibido":
            self.revisar(pid)

    def _mostrar(self, pid, r):
        estado = r.get("estado")
        titulo = {"correcto": "CORRECTO", "incorrecto": "INCORRECTO", "agotado": "SIN INTENTOS",
                  "formato": "FORMATO", "ya_respondida": "YA RESPONDIDA", "recibido": "RECIBIDO",
                  "cerrado": "CERRADO"}.get(estado, estado.upper() if estado else "ERROR")
        print(f"{titulo} · {pid} · {r.get('mensaje', '')}")
        if r.get("pista"):
            print(f"  Pista: {r['pista']}")
        if r.get("intentos_restantes") is not None:
            print(f"  Intentos restantes: {r['intentos_restantes']}")
        if estado == "correcto" and r.get("explicacion"):
            print(f"  Por qué: {r['explicacion']}")
        if estado == "agotado":
            if r.get("explicacion"):
                print(f"  Explicación: {r['explicacion']}")
            if r.get("esperado") is not None:
                print(f"  Respuesta esperada: {json.dumps(r['esperado'], ensure_ascii=False)}")
        if estado == "formato" and r.get("ejemplo") is not None:
            print(f"  Ejemplo: lab.responder(\"{pid}\", {json.dumps(r['ejemplo'], ensure_ascii=False)})")

    def revisar(self, pid):
        """Pide la retroalimentación de Claude para tu último análisis de esa pregunta."""
        print("  Claude está revisando tu análisis (unos segundos)...")
        try:
            r = self._http.post(f"{self.url}/functions/v1/revisar", headers=self._headers(),
                                json={"pregunta": pid}, timeout=90)
            datos = r.json()
        except Exception as e:
            print(f"  No se pudo obtener la revisión ahora ({type(e).__name__}). Tu respuesta SÍ quedó guardada.\n"
                  f'  Intenta de nuevo con lab.revisar("{pid}").')
            return
        if r.status_code != 200 or datos.get("estado") != "ok":
            print(f"  {datos.get('mensaje', 'No se pudo revisar ahora.')} Tu respuesta quedó guardada.")
            return
        s = datos["revision"]
        marca = {"si": "cumple", "parcial": "en parte", "no": "falta"}
        print(f"\nREVISIÓN · {pid} · nivel sugerido {s['nivel_sugerido']}/3 (el docente confirma la nota)")
        for c in s.get("criterios", []):
            print(f"  - {c['descripcion']}: {marca.get(c['cumple'], c['cumple'])}")
        print(f"\n  {s['retroalimentacion']}")
        if s.get("pregunta_para_pensar"):
            print(f"  Para pensar: {s['pregunta_para_pensar']}")
        quedan = datos.get("revisiones_restantes", 0)
        if quedan > 0:
            print(f"\n  Puedes mejorar tu texto y enviarlo otra vez ({quedan} revisión restante).")

    def estado(self):
        """Tabla con todas las preguntas: qué respondiste, qué falta y cuántos intentos te quedan."""
        filas = self._rpc("estado")
        actual = None
        for f in filas:
            if f["mision"] != actual:
                actual = f["mision"]
                print(f"\n{actual}")
            extra = " (opcional)" if f["opcional"] else ""
            nivel = f" · nivel sugerido {f['nivel_sugerido']}/3" if f.get("nivel_sugerido") is not None else ""
            print(f"  {f['id']:<7} {f['estado']:<11} {f['intentos']}/{f['max_intentos']}  {f['titulo']}{extra}{nivel}")

    def entregar(self):
        """Marca tu entrega y muestra el resumen."""
        r = self._rpc("entregar")
        s = r["resumen"]
        print(f"Entrega registrada a las {r['hora']}.\n"
              f"  Respuestas automáticas correctas: {s['correctas']}/{s['automaticas']}\n"
              f"  Predicciones al primer intento: {s['predicciones_primer_intento']}/{s['predicciones']}\n"
              f"  Análisis enviados: {s['analisis_enviados']}/{s['analisis']}\n"
              f"  Obligatorias pendientes: {s['obligatorias_pendientes']}")

    # ── Registro de actividad ───────────────────────────────────────────
    def anotar(self, bloque, **datos):
        """Deja constancia de un ajuste que hiciste (por ejemplo, qué frontera elegiste)."""
        self._evento("ajuste", {"bloque": bloque, **{k: str(v) for k, v in datos.items()}})

    def _evento(self, evento, datos):
        self._eventos.append({"evento": evento, "datos": datos})
        if len(self._eventos) >= 20:
            self._enviar_eventos()

    def _enviar_eventos(self):
        if not self._eventos:
            return
        lote, self._eventos = self._eventos[:200], self._eventos[200:]
        try:
            self._http.post(f"{self.url}/rest/v1/rpc/registrar_lote", headers=self._headers(),
                            json={"p_eventos": lote}, timeout=30)
        except Exception:
            pass

    # ── Atajos de dibujo ────────────────────────────────────────────────
    ver_subarbol = staticmethod(visual.ver_subarbol)
    ver_frontera = staticmethod(visual.ver_frontera)
    ver_heap = staticmethod(visual.ver_heap)
    ver_mapa = staticmethod(visual.ver_mapa)
    ver_cargas = staticmethod(visual.ver_cargas)
