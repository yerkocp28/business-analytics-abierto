"""Utilidades de la edición MPN. Los modelos y su interpretación se desarrollan en los notebooks.

El módulo concentra rutas, contratos de datos, particiones, preprocesamiento y métricas
reutilizables. No modifica los CSV originales.
"""
from pathlib import Path
import hashlib
import html

import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, mean_absolute_error,
                             precision_score, r2_score, recall_score, roc_auc_score,
                             root_mean_squared_error)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CURSO = Path(__file__).resolve().parents[1]
RAIZ = CURSO.parent
DATOS = RAIZ / "_transversal" / "datos"
SEMILLA = 2026

# Puntos óptimos de operación del caso ficticio PulpaLenga (ver _transversal/datos/generar_datos.py).
OPTIMOS_PULPA = {"temperatura_coccion_c": 168.0, "presion_digestor_bar": 7.2,
                 "tiempo_coccion_min": 115.0, "concentracion_alcali_pct": 17.5}


# ---------------------------------------------------------------- datos y contratos
def _leer(caso, archivo):
    return pd.read_csv(DATOS / caso / "originales" / archivo)


def fincordillera_clientes():
    """950 clientes simulados; churn binario. Contrato mínimo antes de modelar."""
    df = _leer("fincordillera", "fincordillera_clientes.csv")
    assert df["cliente_id"].is_unique, "cliente_id dejó de ser único"
    assert df.notna().all().all(), "Aparecieron vacíos no documentados"
    assert set(df["churn"].unique()) <= {0, 1}
    assert (df["edad"].between(18, 100)).all() and (df["ingreso_mensual_clp"] > 0).all()
    return df


def fincordillera_transacciones():
    """1.200 transacciones simuladas; fraude es un evento raro (2,5%)."""
    df = _leer("fincordillera", "fincordillera_transacciones.csv")
    assert df["transaccion_id"].is_unique
    assert set(df["fraude"].unique()) <= {0, 1}
    assert df["hora_transaccion"].between(0, 23).all() and (df["monto_clp"] > 0).all()
    return df


def quillaymarket_demanda():
    """480 réplicas transversales: diez por categoría/mes, sin tienda ni año.

    No constituyen un panel ni una serie longitudinal; la partición aleatoria evalúa
    réplicas intercambiables del simulador, no meses futuros de tiendas reales."""
    df = _leer("quillaymarket", "quillaymarket_demanda_mensual.csv")
    assert df["registro_id"].is_unique
    assert df["mes"].between(1, 12).all()
    assert set(df["promocion_activa"].unique()) <= {0, 1}
    assert (df["ventas_unidades"] >= 0).all() and (df["precio_promedio_clp"] > 0).all()
    return df


def celulosa_calidad():
    """950 lotes simulados del digestor; defecto binario."""
    df = _leer("pulpa_lenga", "pulpalenga_calidad_pulpa.csv")
    assert df["lote_id"].is_unique
    assert set(df["defecto"].unique()) <= {0, 1}
    assert df.notna().all().all()
    return df


def celulosa_energia():
    """480 lotes simulados; consumo energético en MWh."""
    df = _leer("pulpa_lenga", "pulpalenga_consumo_energetico.csv")
    assert df["lote_id"].is_unique
    assert set(df["tipo_proceso"].unique()) <= {"Kraft", "Mecanico"}
    assert (df["consumo_energetico_mwh"] > 0).all()
    return df


def desvios_pulpa(df):
    """Ingeniería de variables con conocimiento del proceso: distancia absoluta al óptimo."""
    salida = df.drop(columns=[c for c in ["lote_id", "defecto"] if c in df]).copy()
    for variable, optimo in OPTIMOS_PULPA.items():
        salida["desv_" + variable] = (salida[variable] - optimo).abs()
    return salida


def huella(archivo):
    return hashlib.sha256(Path(archivo).read_bytes()).hexdigest()


# ---------------------------------------------------------------- particiones y preparación
def particion_tres(X, y, estratificar=True, semilla=SEMILLA, prueba=.20, validacion=.25):
    """Entrenamiento/validación/prueba 60/20/20 por defecto, sin filas compartidas."""
    estrato = y if estratificar else None
    Xd, Xt, yd, yt = train_test_split(X, y, test_size=prueba, stratify=estrato, random_state=semilla)
    estrato = yd if estratificar else None
    Xe, Xv, ye, yv = train_test_split(Xd, yd, test_size=validacion, stratify=estrato, random_state=semilla)
    assert set(Xe.index).isdisjoint(Xv.index) and set(Xd.index).isdisjoint(Xt.index)
    return Xe, Xv, Xt, ye, yv, yt


def preprocesador(numericas, categoricas=(), escalar=True):
    """Transformaciones aprendidas solo con los datos que recibe .fit (dentro de un Pipeline)."""
    pasos_num = [("imputar", SimpleImputer(strategy="median"))]
    if escalar:
        pasos_num.append(("escalar", StandardScaler()))
    bloques = [("num", Pipeline(pasos_num), list(numericas))]
    if categoricas:
        bloques.append(("cat", Pipeline([("imputar", SimpleImputer(strategy="most_frequent")),
                                         ("codificar", OneHotEncoder(handle_unknown="ignore", drop="first",
                                                                     sparse_output=False))]),
                        list(categoricas)))
    return ColumnTransformer(bloques)


# ---------------------------------------------------------------- métricas
def metricas_regresion(y_real, y_pred):
    y_real, y_pred = np.asarray(y_real, float), np.asarray(y_pred, float)
    salida = {"MAE": mean_absolute_error(y_real, y_pred), "RMSE": root_mean_squared_error(y_real, y_pred),
              "R2": r2_score(y_real, y_pred) if np.ptp(y_real) > 0 else np.nan,
              "sesgo_medio": float(np.mean(y_pred - y_real))}
    salida["MAPE_%"] = float(np.mean(np.abs((y_real - y_pred) / y_real)) * 100) if (y_real != 0).all() else np.nan
    return salida


def metricas_umbral(y_real, prob, umbral, c_fn=5.0, c_fp=1.0):
    """Matriz de confusión, métricas y costo medio para una regla prob >= umbral."""
    decision = np.asarray(prob) >= umbral
    tn, fp, fn, tp = confusion_matrix(y_real, decision, labels=[0, 1]).ravel()
    return {"umbral": float(umbral), "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
            "accuracy": accuracy_score(y_real, decision),
            "precision": precision_score(y_real, decision, zero_division=0),
            "recall": recall_score(y_real, decision, zero_division=0),
            "F1": f1_score(y_real, decision, zero_division=0),
            "costo_medio": (c_fn * fn + c_fp * fp) / len(decision)}


def tabla_umbrales(y_real, prob, c_fn=5.0, c_fp=1.0, grilla=None):
    """Recorre umbrales; incluye <0 y >1 para las reglas «todos positivos» y «ninguno positivo»."""
    if grilla is None:
        grilla = np.r_[-0.001, np.linspace(0, 1, 101), 1.001]
    return pd.DataFrame([metricas_umbral(y_real, prob, t, c_fn, c_fp) for t in grilla])


def umbral_bayes(c_fn, c_fp):
    """Umbral óptimo si las probabilidades están calibradas: c_FP / (c_FP + c_FN)."""
    return c_fp / (c_fp + c_fn)


def ks_gini(y_real, prob):
    """KS: máxima distancia entre distribuciones acumuladas de puntaje; Gini = 2·AUC − 1."""
    y_real, prob = np.asarray(y_real), np.asarray(prob)
    puntos = np.unique(prob)
    pos, neg = prob[y_real == 1], prob[y_real == 0]
    fpos = np.searchsorted(np.sort(pos), puntos, side="right") / len(pos)
    fneg = np.searchsorted(np.sort(neg), puntos, side="right") / len(neg)
    auc = roc_auc_score(y_real, prob)
    return {"KS": float(np.max(np.abs(fneg - fpos))), "AUC": float(auc), "Gini": float(2 * auc - 1)}


def lift_deciles(y_real, prob, grupos=10):
    """Tasa del evento y lift por grupo de puntaje (1 = mayor riesgo)."""
    tabla = pd.DataFrame({"y": np.asarray(y_real), "p": np.asarray(prob)}).sort_values("p", ascending=False)
    tabla["grupo"] = np.arange(len(tabla)) * grupos // len(tabla) + 1
    base = tabla["y"].mean()
    resumen = tabla.groupby("grupo").agg(casos=("y", "size"), eventos=("y", "sum"), tasa=("y", "mean"))
    resumen["lift"] = resumen["tasa"] / base
    resumen["captura_acumulada"] = resumen["eventos"].cumsum() / tabla["y"].sum()
    return resumen


def psi(esperado, actual, cortes=10, tipo="auto", epsilon=1e-6):
    """PSI con categorías explícitas o tramos aprendidos solo en referencia.

    Auto trata como categóricas las variables no numéricas o con <= cortes valores
    de referencia. Conserva categorías nuevas y faltantes en celdas propias.
    epsilon regulariza celdas vacías; el resultado depende de este convenio.
    """
    e, a = pd.Series(esperado), pd.Series(actual)
    if e.empty or a.empty or int(cortes) != cortes or cortes < 2:
        raise ValueError("Muestras no vacías y al menos dos cortes enteros.")
    if tipo not in {"auto", "categorico", "continuo"} or not 0 < epsilon < 1:
        raise ValueError("Tipo o regularización fuera del dominio.")
    numericas = pd.api.types.is_numeric_dtype(e) and pd.api.types.is_numeric_dtype(a)
    categorico = tipo == "categorico" or (tipo == "auto" and
                   (not numericas or e.nunique(dropna=True) <= cortes))
    if categorico:
        # Tuplas separan de forma inequívoca el faltante de una categoría literal.
        def contar(x):
            return x.map(lambda v: ("faltante",) if pd.isna(v) else ("valor", v)).value_counts()
        ec, ac = contar(e), contar(a)
        claves = ec.index.union(ac.index, sort=False)
        ep = ec.reindex(claves, fill_value=0).to_numpy(float) / len(e)
        ap = ac.reindex(claves, fill_value=0).to_numpy(float) / len(a)
    else:
        if not numericas or np.isinf(e.dropna()).any() or np.isinf(a.dropna()).any():
            raise ValueError("El PSI continuo requiere números finitos o faltantes.")
        referencia = e.dropna().to_numpy(float)
        if len(np.unique(referencia)) < 2:
            raise ValueError("Referencia constante o vacía: use tipo='categorico'.")
        interiores = np.unique(np.quantile(referencia, np.linspace(0, 1, cortes + 1)[1:-1]))
        limites = np.r_[-np.inf, interiores, np.inf]
        ep = np.r_[np.histogram(referencia, limites)[0], e.isna().sum()] / len(e)
        ap = np.r_[np.histogram(a.dropna().to_numpy(float), limites)[0], a.isna().sum()] / len(a)
    ep, ap = np.maximum(ep, epsilon), np.maximum(ap, epsilon)
    ep, ap = ep / ep.sum(), ap / ap.sum()
    return float(np.sum((ap - ep) * np.log(ap / ep)))


def particion_con_calibracion(X, y):
    """60% ajuste, 10% selección, 10% calibración y 20% prueba, sin solapamiento."""
    Xe, Xv, Xt, ye, yv, yt = particion_tres(X, y, estratificar=False)
    Xv, Xcal, yv, ycal = train_test_split(Xv, yv, test_size=.5, random_state=SEMILLA + 1)
    grupos = [set(d.index) for d in [Xe, Xv, Xcal, Xt]]
    assert all(grupos[i].isdisjoint(grupos[j]) for i in range(4) for j in range(i))
    return Xe, Xv, Xcal, Xt, ye, yv, ycal, yt


def cuantil_conformal(residuos_absolutos, nivel=.8):
    """Estadístico de orden ceil((n+1)*nivel); infinito si n no permite ese nivel."""
    r = np.asarray(residuos_absolutos, float)
    if r.ndim != 1 or len(r) == 0 or not np.isfinite(r).all() or (r < 0).any() or not 0 < nivel < 1:
        raise ValueError("Residuos finitos no negativos y nivel entre cero y uno.")
    k = int(np.ceil((len(r) + 1) * nivel))
    return float(np.sort(r)[k - 1]) if k <= len(r) else np.inf


def brier(y_real, prob):
    return float(np.mean((np.asarray(prob, float) - np.asarray(y_real, float)) ** 2))


# ---------------------------------------------------------------- autoevaluación
import sys
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from _transversal.evaluacion import pregunta as _pregunta

def pregunta(enunciado, opciones, correcta, explicacion):
    return _pregunta(enunciado, opciones, correcta, explicacion)
