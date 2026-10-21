"""Dibujos del laboratorio: árboles en texto, la frontera paso a paso, el heap y el mapa."""

from __future__ import annotations


def ver_subarbol(hijos, info, raiz, max_nodos=40):
    """Dibuja en texto el subárbol que cuelga de `raiz`."""
    lineas = []

    def etiqueta(u):
        n = info[u]
        extra = ""
        if n.get("demand_kw"):
            extra = f" · {n['demand_kw']} kW"
        if n.get("critical"):
            extra += f" · CRÍTICO ({n['critical']})"
        return f"{u}  [{n['kind']}] {n['name']}{extra}"

    def dibujar(u, prefijo, ultimo, es_raiz):
        if len(lineas) >= max_nodos:
            return
        if es_raiz:
            lineas.append(etiqueta(u))
            nuevo = ""
        else:
            lineas.append(prefijo + ("└── " if ultimo else "├── ") + etiqueta(u))
            nuevo = prefijo + ("    " if ultimo else "│   ")
        hs = hijos.get(u, [])
        for i, h in enumerate(hs):
            dibujar(h, nuevo, i == len(hs) - 1, False)

    dibujar(raiz, "", True, True)
    print("\n".join(lineas))
    if len(lineas) >= max_nodos:
        print(f"... (se muestran solo {max_nodos} nodos)")


def ver_frontera(frontera, max_pasos=20):
    """Muestra paso a paso qué salió, qué se agregó y cómo quedó la frontera."""
    pasos = frontera.pasos
    vistos = set()
    ancho = 12
    print(f"Frontera: {type(frontera).__name__}  ·  se dibuja {frontera.descripcion}\n")
    print(f"{'Paso':>4} | {'Sale':<{ancho}} | {'¿Nuevo?':<8} | {'Agrega':<28} | Frontera")
    print("-" * 95)
    for i, p in enumerate(pasos[: max_pasos + 1]):
        sale = p["sale"] or "—"
        if p["sale"] is None:
            nuevo = "—"
        elif p["sale"] in vistos:
            nuevo = "no"
        else:
            nuevo = "sí"
            vistos.add(p["sale"])
        agrega = ", ".join(p["agrega"]) or "—"
        if len(agrega) > 28:
            agrega = agrega[:25] + "..."
        cont = " ".join(p["frontera"]) or "(vacía)"
        if len(cont) > 60:
            cont = cont[:57] + "..."
        print(f"{i:>4} | {sale:<{ancho}} | {nuevo:<8} | {agrega:<28} | {cont}")
    if len(pasos) > max_pasos + 1:
        print(f"... ({len(pasos) - 1} pasos en total; se muestran {max_pasos})")


def ver_heap(arreglo):
    """Dibuja un heap (lista de Python) como árbol, con el índice de cada posición."""
    if not arreglo:
        print("(heap vacío)")
        return
    print("Arreglo:", list(arreglo))
    print("Índices:", list(range(len(arreglo))))
    print()

    def dibujar(i, prefijo, ultimo, es_raiz):
        if i >= len(arreglo):
            return
        if es_raiz:
            print(f"[{i}] {arreglo[i]}")
            nuevo = ""
        else:
            print(prefijo + ("└── " if ultimo else "├── ") + f"[{i}] {arreglo[i]}")
            nuevo = prefijo + ("    " if ultimo else "│   ")
        hijos = [h for h in (2 * i + 1, 2 * i + 2) if h < len(arreglo)]
        for k, h in enumerate(hijos):
            dibujar(h, nuevo, k == len(hijos) - 1, False)

    dibujar(0, "", True, True)
    print("\nRegla: hijos del índice i → 2i+1 y 2i+2 · padre del índice i → (i-1)//2")


COLORES = {"L1": "#1f6feb", "L2": "#d29922", "L1/L2": "#8250df"}


def ver_mapa(estaciones, tramos, rutas=None, titulo="Tu ciudad"):
    """Dibuja la red: Metro en color, buses punteados, estación cerrada en gris y rutas encima."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("No se encontró matplotlib (en Colab ya viene instalado).")
        return
    pos = {e["code"]: (e["x"], e["y"]) for e in estaciones}
    estado = {e["code"]: e["status"] for e in estaciones}
    fig, ax = plt.subplots(figsize=(13, 6))
    for t in tramos:
        a, b = t["from_code"], t["to_code"]
        (x1, y1), (x2, y2) = pos[a], pos[b]
        cerrado = estado[a] == "cerrada" or estado[b] == "cerrada"
        if t["mode"] == "metro":
            ax.plot([x1, x2], [y1, y2], color="#bbbbbb" if cerrado else COLORES.get(t["line"], "#555"), lw=3, zorder=1)
        else:
            ax.plot([x1, x2], [y1, y2], color="#bbbbbb" if cerrado else "#2da44e", lw=1.5, ls="--", zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(t["minutes"]), fontsize=7, color="#666", zorder=4)
    estilos_ruta = [("#cf222e", 7), ("#0969da", 5), ("#8250df", 3)]
    for k, (nombre, ruta) in enumerate((rutas or {}).items()):
        color, ancho = estilos_ruta[k % 3]
        xs = [pos[c][0] for c in ruta]
        ys = [pos[c][1] for c in ruta]
        ax.plot(xs, ys, color=color, lw=ancho, alpha=0.45, zorder=2, label=nombre)
    for e in estaciones:
        x, y = pos[e["code"]]
        if e["status"] == "cerrada":
            ax.scatter([x], [y], marker="X", s=160, color="#6e7781", zorder=5)
        else:
            ax.scatter([x], [y], s=40 if "-" in e["code"] else 70, color="white",
                       edgecolor="#333", zorder=5)
        ax.text(x, y + 0.25, e["code"], fontsize=8, ha="center", zorder=6)
    ax.set_title(titulo + "  ·  números = minutos por tramo · X = estación cerrada · punteado = bus")
    ax.axis("off")
    if rutas:
        ax.legend(loc="lower left")
    plt.tight_layout()
    plt.show()


def ver_cargas(carga, info, tipo="circuito", top=None, porcentaje=None):
    """Gráfico de barras con la carga (kW) de los nodos de un tipo."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("No se encontró matplotlib.")
        return
    ids = [u for u in carga if info[u]["kind"] == tipo]
    ids.sort(key=lambda u: -carga[u])
    if top:
        ids = ids[:top]
    valores = [porcentaje[u] if porcentaje else carga[u] for u in ids]
    fig, ax = plt.subplots(figsize=(10, max(2.5, 0.35 * len(ids))))
    ax.barh([f"{u} · {info[u]['name']}"[:45] for u in ids][::-1], valores[::-1], color="#1f6feb")
    ax.set_xlabel("% de su capacidad" if porcentaje else "kW")
    if porcentaje:
        ax.axvline(100, color="#cf222e", ls="--")
    plt.tight_layout()
    plt.show()
