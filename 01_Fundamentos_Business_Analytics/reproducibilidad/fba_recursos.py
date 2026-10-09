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


import sys
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from _transversal.evaluacion import pregunta as _pregunta

def pregunta(enunciado, opciones, correcta, explicacion):
    return _pregunta(enunciado, opciones, correcta, explicacion)
