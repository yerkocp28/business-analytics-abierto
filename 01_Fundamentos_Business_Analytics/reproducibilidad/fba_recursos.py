"""Utilidades pequeñas de la edición FBA. Los cálculos se explican en los notebooks."""
from pathlib import Path
import hashlib
import html
import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, Markdown

CURSO = Path(__file__).resolve().parents[1]
RAIZ = CURSO.parent
DATOS = RAIZ / "_transversal" / "datos"
SEMILLA = 2026


def ventas():
    """180 transacciones del caso docente existente; no modifica el CSV."""
    archivo = DATOS / "quillaymarket" / "originales" / "quillaymarket_ventas_detalle.csv"
    frame = pd.read_csv(archivo, parse_dates=["Fecha"])
    assert frame["ID_Venta"].is_unique, "La clave de transacción dejó de ser única"
    assert frame[["Unidades", "Precio_Unitario", "Monto"]].notna().all().all()
    assert np.allclose(frame["Monto"], frame["Unidades"] * frame["Precio_Unitario"])
    return frame


def huella(archivo):
    return hashlib.sha256(Path(archivo).read_bytes()).hexdigest()


def resumen_ventas(frame):
    """Distingue ingresos, transacciones, unidades y precio ponderado."""
    n, unidades, ingreso = len(frame), frame["Unidades"].sum(), frame["Monto"].sum()
    return {"transacciones": n, "unidades": int(unidades), "ingreso": float(ingreso),
            "ticket_medio": float(ingreso / n) if n else np.nan,
            "precio_por_unidad": float(ingreso / unidades) if unidades else np.nan}


def pregunta(enunciado, opciones, correcta, explicacion):
    """Autoevaluación local; no recopila respuestas ni envía información."""
    elegir = widgets.RadioButtons(options=opciones, value=None, layout={"width": "95%"})
    boton = widgets.Button(description="Comprobar", button_style="info")
    salida = widgets.HTML(value='<p role="status">Selecciona una respuesta y pulsa Comprobar.</p>')

    def revisar(_):
        if elegir.value is None:
            mensaje = "Selecciona una respuesta para recibir retroalimentación."
        else:
            acierto = elegir.value == opciones[correcta]
            mensaje = ("Correcto. " if acierto else "Revisa tu respuesta. ") + explicacion
        salida.value = '<p role="status" aria-live="polite">' + html.escape(mensaje) + '</p>'

    boton.on_click(revisar)
    caja = widgets.VBox([widgets.HTML("<b>" + html.escape(enunciado) + "</b>"), elegir, boton, salida])
    display(caja)
    return caja
