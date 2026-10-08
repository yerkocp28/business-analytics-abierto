"""Calcula los datos que la guía maestra MPN incrusta para funcionar sin conexión.

Usa las mismas especificaciones que los notebooks (03, 04, 05 y 07). Reemplaza solo el bloque
<script id="mpn-datos" type="application/json"> … </script> de guia_maestra_mpn.html.
Ejecutar desde cualquier carpeta del repositorio con el entorno de la edición.
"""
from pathlib import Path
import json
import re
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.model_selection import StratifiedKFold, cross_val_predict, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import average_precision_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mpn_recursos as mr  # noqa: E402

GUIA = mr.CURSO / "guia_maestra_mpn.html"
SEMILLA = mr.SEMILLA


def r(v, d=4):
    return float(round(float(v), d))


# ---------------------------------------------------------------- QuillayMarket (notebook 03)
def indicadores(marco, mes_categorico, quitar_referencia):
    d = pd.get_dummies(marco, columns=["categoria_producto"] + (["mes"] if mes_categorico else []),
                       drop_first=quitar_referencia, dtype=float)
    d["precio_miles"] = d.pop("precio_promedio_clp") / 1000
    d["marketing_100mil"] = d.pop("inversion_marketing_clp") / 1e5
    return d


def matriz_diseno(marco, mes_categorico=False, columnas=None):
    """Al ajustar elimina la referencia; al predecir crea todas las categorías y alinea columnas."""
    if columnas is None:
        return indicadores(marco, mes_categorico, True)
    return indicadores(marco, mes_categorico, False).reindex(columns=columnas, fill_value=0.0)


def ampliar(marco, columnas=None):
    d = indicadores(marco, True, columnas is None)
    for c in [col for col in d.columns if col.startswith("categoria_producto_")]:
        d[c + "×promoción"] = d[c] * d["promocion_activa"]
        d[c + "×precio"] = d[c] * d["precio_miles"]
        d[c + "×marketing"] = d[c] * d["marketing_100mil"]
    return d if columnas is None else d.reindex(columns=columnas, fill_value=0.0)


def datos_quillaymarket():
    demanda = mr.quillaymarket_demanda()
    X = demanda.drop(columns=["registro_id", "ventas_unidades"]); y = demanda["ventas_unidades"]
    Xe, Xv, Xt, ye, yv, yt = mr.particion_tres(X, y, estratificar=False)
    De = matriz_diseno(Xe, True)
    estacional = LinearRegression().fit(De, ye)
    pred_est = estacional.predict(matriz_diseno(Xv, True, De.columns))
    De_l = matriz_diseno(Xe, False)
    pred_lin = LinearRegression().fit(De_l, ye).predict(matriz_diseno(Xv, False, De_l.columns))
    abs_res = np.abs(yv.values - pred_est)
    q80 = float(np.quantile(abs_res, min(1, np.ceil((len(abs_res) + 1) * .8) / len(abs_res))))
    residuos = pd.DataFrame({"mes": Xv["mes"].values, "numero": yv.values - pred_lin,
                             "categoria": yv.values - pred_est}).groupby("mes").mean()
    rangos = demanda.groupby("categoria_producto")["precio_promedio_clp"].agg(["min", "max"]) / 1000
    escenario = {"intercepto": r(estacional.intercept_, 6),
                 "coef": {c: r(b, 6) for c, b in zip(De.columns, estacional.coef_)},
                 "q80": r(q80, 4), "categorias": sorted(demanda["categoria_producto"].unique()),
                 "referencia": "Alimentos",
                 "rango_precio_miles": {k: [r(v["min"], 2), r(v["max"], 2)] for k, v in rangos.iterrows()}}
    meses = {"mes": [int(m) for m in residuos.index], "numero": [r(v, 2) for v in residuos["numero"]],
             "categoria": [r(v, 2) for v in residuos["categoria"]],
             "rmse_numero": r(mr.metricas_regresion(yv, pred_lin)["RMSE"], 2),
             "rmse_categoria": r(mr.metricas_regresion(yv, pred_est)["RMSE"], 2)}
    Ae = ampliar(Xe); Av = ampliar(Xv, Ae.columns)
    grilla = [r(v, 2) for v in np.arange(-3, 2.51, .25)]
    camino = {"nombres": list(Ae.columns), "log10_alpha": grilla, "Ridge": [], "Lasso": []}
    for tipo in ["Ridge", "Lasso"]:
        for la in grilla:
            est = Ridge(alpha=10 ** la) if tipo == "Ridge" else Lasso(alpha=10 ** la, max_iter=100_000)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", ConvergenceWarning)
                m = Pipeline([("escalar", StandardScaler()), ("modelo", est)]).fit(Ae, ye)
            coef = m.named_steps["modelo"].coef_
            camino[tipo].append({"coef": [r(c, 4) for c in coef],
                                 "rmse": r(mr.metricas_regresion(yv, m.predict(Av))["RMSE"], 3),
                                 "no_nulos": int((np.abs(coef) > 1e-8).sum())})
    return escenario, meses, camino


# ---------------------------------------------------------------- FinCordillera (notebook 04)
def datos_fincordillera():
    banco = mr.fincordillera_clientes()
    X = banco.drop(columns=["cliente_id", "churn"]); y = banco["churn"]
    num = X.select_dtypes("number").columns.tolist()
    Xe, Xv, Xt, ye, yv, yt = mr.particion_tres(X, y)
    m = Pipeline([("preparar", mr.preprocesador(num, ["region"])),
                  ("modelo", LogisticRegression(max_iter=2000))]).fit(Xe, ye)
    nombres = [n.split("__")[-1] for n in m.named_steps["preparar"].get_feature_names_out()]
    coef = m.named_steps["modelo"].coef_[0]
    p_val = m.predict_proba(Xv)[:, 1]
    lift = mr.lift_deciles(yv, p_val)
    return {"variables": nombres, "coef": [r(c) for c in coef], "odds_ratio": [r(np.exp(c)) for c in coef],
            "metricas_validacion": {k: r(v) for k, v in mr.ks_gini(yv, p_val).items()} | {
                "AP": r(average_precision_score(yv, p_val))},
            "captura_acumulada": [r(v) for v in lift["captura_acumulada"]],
            "tasa_por_decil": [r(v) for v in lift["tasa"]], "tasa_base": r(yv.mean())}


# ---------------------------------------------------------------- PulpaLenga (notebook 05)
def datos_celulosa():
    calidad = mr.celulosa_calidad()
    X = mr.desvios_pulpa(calidad); y = calidad["defecto"]
    desvios = [c for c in X.columns if c.startswith("desv_")] + ["humedad_madera_pct", "velocidad_linea_m_min"]
    Xe, Xv, Xt, ye, yv, yt = mr.particion_tres(X, y)
    cv = StratifiedKFold(5, shuffle=True, random_state=SEMILLA)
    modelo = Pipeline([("escalar", StandardScaler()), ("modelo", LogisticRegression(max_iter=2000, C=10))])
    Xd, yd = pd.concat([Xe, Xv]), pd.concat([ye, yv])
    p_oof = cross_val_predict(modelo, Xd[desvios], yd, cv=cv, method="predict_proba")[:, 1]
    umbral = {"y": [int(v) for v in yd], "p": [r(v, 4) for v in p_oof], "c_fn": 800, "c_fp": 90,
              "fuente": "Predicciones fuera de pliegue (5 pliegues) en entrenamiento + validación"}
    profundidades = list(range(1, 16))
    ent, val = [], []
    for k in profundidades:
        res = cross_validate(DecisionTreeClassifier(max_depth=k, random_state=SEMILLA), Xe[desvios], ye, cv=cv,
                             scoring="average_precision", return_train_score=True)
        ent.append(r(res["train_score"].mean())); val.append(r(res["test_score"].mean()))
    return umbral, {"profundidad": profundidades, "entrenamiento": ent, "validacion_cruzada": val}


# ---------------------------------------------------------------- Pronóstico (notebook 07)
def pronosticar(historia, horizonte, metodo):
    pasos = np.arange(1, horizonte + 1)
    if metodo == "Ingenuo":
        return np.repeat(historia.iloc[-1], horizonte)
    if metodo == "Ingenuo estacional":
        return np.array([historia.iloc[-12 + (h - 1) % 12] for h in pasos])
    if metodo == "Media":
        return np.repeat(historia.mean(), horizonte)
    X_h = pd.get_dummies(pd.Categorical(historia.index.month, categories=range(1, 13)), prefix="mes",
                         drop_first=True, dtype=float)
    X_h.insert(0, "t", np.arange(len(historia)))
    modelo = LinearRegression().fit(X_h, historia.to_numpy())
    futuro = pd.period_range(historia.index[-1] + 1, periods=horizonte, freq="M")
    X_f = pd.get_dummies(pd.Categorical(futuro.month, categories=range(1, 13)), prefix="mes",
                         drop_first=True, dtype=float)
    X_f.insert(0, "t", np.arange(len(historia), len(historia) + horizonte))
    return modelo.predict(X_f)


def datos_pronostico():
    demanda = mr.quillaymarket_demanda()
    perfil = demanda.groupby("mes")["ventas_unidades"].mean()
    indice = (perfil / perfil.mean()).to_numpy()
    g = np.random.default_rng(SEMILLA)
    fechas = pd.period_range("2020-01", "2025-12", freq="M")
    t = np.arange(len(fechas))
    serie = pd.Series((1200 + 6 * t) * indice[fechas.month - 1] + g.normal(0, 45, len(t)), index=fechas)
    metodos = ["Ingenuo", "Ingenuo estacional", "Media", "Tendencia + estacionalidad"]
    metricas, ultimo = {}, {}
    for h in range(1, 13):
        filas = []
        for origen in range(36, len(serie) - h + 1):
            historia, real = serie.iloc[:origen], serie.iloc[origen:origen + h].to_numpy()
            escala = np.mean(np.abs(historia.iloc[12:].to_numpy() - historia.iloc[:-12].to_numpy()))
            for metodo in metodos:
                e = real - pronosticar(historia, h, metodo)
                filas.append({"metodo": metodo, "MAE": np.mean(np.abs(e)), "MAPE": np.mean(np.abs(e / real)) * 100,
                              "MASE": np.mean(np.abs(e)) / escala})
        tabla = pd.DataFrame(filas).groupby("metodo").mean()
        metricas[str(h)] = {m: {k: r(tabla.loc[m, k], 3) for k in ["MAE", "MAPE", "MASE"]} for m in metodos}
        ultimo[str(h)] = {m: [r(v, 2) for v in pronosticar(serie.iloc[:-h], h, m)] for m in metodos}
    return {"fechas": [str(p) for p in fechas], "valores": [r(v, 2) for v in serie], "metodos": metodos,
            "metricas": metricas, "ultimo_origen": ultimo, "indice_estacional": [r(v) for v in indice]}


def calcular():
    escenario, meses, camino = datos_quillaymarket()
    umbral, complejidad = datos_celulosa()
    return {"edicion": "2026-10-08", "semilla": SEMILLA, "escenario": escenario, "residuos_mes": meses,
            "regularizacion": camino, "fincordillera": datos_fincordillera(), "umbral": umbral,
            "complejidad": complejidad, "pronostico": datos_pronostico()}


def main():
    datos = calcular()
    texto = GUIA.read_text(encoding="utf-8")
    bloque = json.dumps(datos, ensure_ascii=False, separators=(",", ":"))
    patron = re.compile(r'(<script id="mpn-datos" type="application/json">)(.*?)(</script>)', re.S)
    assert patron.search(texto), "No se encontró el bloque de datos en la guía"
    texto = patron.sub(lambda m: m.group(1) + bloque + m.group(3), texto, count=1)
    GUIA.write_text(texto, encoding="utf-8")
    print(f"Datos actualizados en {GUIA.name}: {len(bloque) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
