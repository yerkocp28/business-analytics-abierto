"""Comprobaciones de la edición MPN: notebooks, cobertura, guía interactiva contra Python y PDF."""
from pathlib import Path
import csv
import json
import re
import sys
from urllib.parse import unquote, urlparse

import nbformat
import numpy as np
import pymupdf as fitz
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from sklearn.linear_model import LinearRegression
from sklearn.metrics import roc_auc_score

CURSO = Path(__file__).resolve().parents[1]
SALIDA = CURSO / "reproducibilidad"
CAPTURAS = SALIDA / "capturas"
CAPTURAS.mkdir(exist_ok=True)
sys.path.insert(0, str(SALIDA))
import mpn_recursos as mr  # noqa: E402
import datos_guia as dg  # noqa: E402

GUIA = CURSO / "guia_maestra_mpn.html"
MANUAL_HTML = CURSO / "material_propio" / "MPN_manual_cientifico.html"
MANUAL_PDF = CURSO / "material_propio" / "MPN_manual_cientifico.pdf"


def verificar_notebooks():
    salida = []
    for archivo in sorted((CURSO / "notebooks").glob("*.ipynb")):
        nb = nbformat.read(archivo, as_version=4)
        nbformat.validate(nb)
        codigo = [c for c in nb.cells if c.cell_type == "code"]
        assert all(c.execution_count is not None for c in codigo), archivo.name
        assert not [o for c in codigo for o in c.outputs if o.output_type == "error"], archivo.name
        assert not [o for c in codigo for o in c.outputs if o.output_type == "stream" and o.name == "stderr"], archivo.name
        estados = nb.metadata.get("widgets", {}).get("application/vnd.jupyter.widget-state+json", {}).get("state", {})
        for estado in estados.values():
            assert not [o for o in estado.get("state", {}).get("outputs", []) if o.get("output_type") == "error"], archivo.name
        assert not any(re.search("[\x00-\x08\x0b\x0c\x0e-\x1f]", c.source) for c in nb.cells), archivo.name
        texto = json.dumps(nb.dict())
        assert ":\\\\Users\\\\" not in texto and "ipykernel_" not in texto, f"Ruta local en {archivo.name}"
        salida.append({"nombre": archivo.name, "celdas_codigo": len(codigo), "widgets": len(estados), "resultado": "OK"})
    return salida


def verificar_enlaces():
    total = 0
    for archivo in [GUIA, MANUAL_HTML]:
        soup = BeautifulSoup(archivo.read_text(encoding="utf-8"), "html.parser")
        ids = [t["id"] for t in soup.find_all(id=True)]
        assert len(ids) == len(set(ids)), f"ID repetido en {archivo.name}"
        for tag in soup.select("a[href]"):
            ref = tag["href"]; partes = urlparse(ref)
            if partes.scheme or ref.startswith("//") or not ref:
                continue
            if partes.path:
                destino = (archivo.parent / unquote(partes.path)).resolve()
                assert destino.exists(), f"Enlace ausente {archivo.name}: {ref}"
            elif partes.fragment:
                assert unquote(partes.fragment) in ids, f"Ancla ausente {archivo.name}: {ref}"
            total += 1
    return total


def verificar_cobertura():
    with (CURSO / "matriz_cobertura.csv").open(encoding="utf-8-sig", newline="") as f:
        filas = list(csv.DictReader(f))
    esperados = {f"1.{i}" for i in range(1, 5)} | {f"2.{i}" for i in range(1, 7)} | {f"3.{i}" for i in range(1, 6)}
    assert {r["criterio_o_tema"] for r in filas if r["nivel"] == "nucleo"} == esperados
    guia = BeautifulSoup(GUIA.read_text(encoding="utf-8"), "html.parser")
    manual = BeautifulSoup(MANUAL_HTML.read_text(encoding="utf-8"), "html.parser")
    for fila in filas:
        assert guia.find(id=fila["html_ancla"]), fila
        assert manual.find(id=fila["qmd_ancla"]), fila
        nb = nbformat.read(CURSO / fila["notebook"], as_version=4)
        assert any(f'id="{fila["notebook_ancla"]}"' in c.source for c in nb.cells), fila
    return {"criterios_oficiales": len(esperados), "filas_temas": len(filas), "anclas_y_rutas": "OK"}


def verificar_guia():
    datos_html = json.loads(re.search(r'<script id="mpn-datos" type="application/json">(.*?)</script>',
                                      GUIA.read_text(encoding="utf-8"), re.S).group(1))
    assert datos_html == json.loads(json.dumps(dg.calcular())), "Los datos incrustados no coinciden con datos_guia.py"
    y = np.array(datos_html["umbral"]["y"]); p = np.array(datos_html["umbral"]["p"])
    # Modelo de escenarios reconstruido con scikit-learn, igual que en el notebook 03
    demanda = mr.quillaymarket_demanda()
    X = demanda.drop(columns=["registro_id", "ventas_unidades"]); yd = demanda["ventas_unidades"]
    Xe, *_ , ye, _, _ = mr.particion_tres(X, yd, estratificar=False)
    De = dg.matriz_diseno(Xe, True)
    estacional = LinearRegression().fit(De, ye)
    resultado = {}
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(channel="chrome", headless=True)
        pagina = navegador.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
        errores, red = [], []
        pagina.on("pageerror", lambda e: errores.append(str(e)))
        pagina.on("console", lambda m: errores.append(m.text) if m.type == "error" else None)
        def ruta(route):
            if route.request.url.startswith(("http:", "https:")):
                red.append(route.request.url); route.abort()
            else:
                route.continue_()
        pagina.route("**/*", ruta)
        pagina.goto(GUIA.as_uri(), wait_until="load")
        pagina.screenshot(path=str(CAPTURAS / "guia_inicio.png"))
        assert pagina.evaluate("window.MPN_LISTA") is True
        # Umbral: conteos y costos idénticos a Python sobre los mismos datos
        for t in [0.0, .05, .1, 90 / 890, .25, .5, .9, 1.0]:
            js = pagina.evaluate(f"MPN.evaluarUmbral({t}, 800, 90)")
            py = mr.metricas_umbral(y, p, t, 800, 90)
            assert all(js[k] == py[k] for k in ["TP", "FP", "FN", "TN"]), (t, js, py)
            assert np.isclose(js["costo_medio"], py["costo_medio"]) and np.isclose(js["recall"], py["recall"])
        assert np.isclose(pagina.evaluate("MPN.aucUmbral()"), roc_auc_score(y, p), atol=1e-12)
        # Escenarios: predicción idéntica al modelo de scikit-learn
        for cat, mes, promo, precio, mkt in [("Vestuario", 11, 1, 20, 5), ("Alimentos", 1, 0, 12, 3),
                                             ("Tecnologia", 7, 1, 28, 8), ("Electrohogar", 12, 0, 18.5, 1)]:
            fila = dg.matriz_diseno(__import__("pandas").DataFrame([{"mes": mes, "categoria_producto": cat,
                       "precio_promedio_clp": precio * 1000, "promocion_activa": promo,
                       "inversion_marketing_clp": mkt * 1e5}]), True, De.columns)
            esperado = float(estacional.predict(fila)[0])
            obtenido = pagina.evaluate(f"MPN.predecir('{cat}', {mes}, {promo}, {precio}, {mkt})")
            assert abs(esperado - obtenido) < 1e-3, (cat, esperado, obtenido)
        # Calculadoras
        cm = pagina.evaluate("MPN.metricasConfusion(30, 10, 20, 140, 5, 1)")
        assert np.isclose(cm["accuracy"], .85) and np.isclose(cm["precision"], .6) and np.isclose(cm["recall"], .75)
        assert np.isclose(cm["F1"], 2 * .6 * .75 / 1.35) and np.isclose(cm["costo_medio"], .35)
        s8r = [95, 140, 185, 230, 260, 175, 210, 255, 300, 340, 380, 410, 445, 470, 520]
        s8p = [88, 121, 168, 199, 236, 160, 184, 226, 271, 301, 345, 368, 402, 431, 468]
        js_r = pagina.evaluate(f"MPN.metricasRegresion({s8r}, {s8p})"); py_r = mr.metricas_regresion(s8r, s8p)
        for a, b in [("MAE", "MAE"), ("RMSE", "RMSE"), ("R2", "R2"), ("sesgo", "sesgo_medio"), ("MAPE", "MAPE_%")]:
            assert np.isclose(js_r[a], py_r[b]), (a, js_r[a], py_r[b])
        e, a = np.array([20] * 5) / 100, np.array([12, 16, 20, 24, 28]) / 100
        assert np.isclose(pagina.evaluate("MPN.psi([20,20,20,20,20],[12,16,20,24,28])"), np.sum((a - e) * np.log(a / e)))
        # Sesgo–varianza: el error de entrenamiento no sube con la complejidad
        entr = [pagina.evaluate(f"MPN.sesgoVarianza({k}, 12).train") for k in range(1, 11)]
        assert all(entr[i + 1] <= entr[i] + 1e-6 for i in range(9)), entr
        assert .8 * 144 <= pagina.evaluate("MPN.sesgoVarianza(2, 12).nuevo") <= 1.5 * 144
        # Regularización, pronóstico, recorridos y textos
        assert pagina.evaluate("MPN.regularizacion('Lasso', 0).no_nulos") >= pagina.evaluate("MPN.regularizacion('Lasso', 22).no_nulos")
        assert np.isclose(pagina.evaluate("MPN.pronostico(3, 'Tendencia + estacionalidad').metricas.MASE"),
                          datos_html["pronostico"]["metricas"]["3"]["Tendencia + estacionalidad"]["MASE"])
        assert pagina.evaluate("MPN.crisp(5)") == "Despliegue"
        assert pagina.evaluate("MPN.responderTipo(0, 'Clasificación')") is True
        assert pagina.evaluate("MPN.auditarFuga([true,true,false,true,false,false,true]).correctas") == 7
        assert "Situación" in pagina.evaluate("MPN.mensaje('Directorio')")
        assert pagina.evaluate("MPN.semanas") == 12 and pagina.evaluate("MPN.totalPreguntas") >= 36
        # Interacción real con controles
        for selector, valor in [("#um-t", "10"), ("#sv-grado", "9"), ("#reg-alpha", "20"), ("#cx-prof", "12"), ("#pr-h", "12")]:
            pagina.eval_on_selector(selector, f"e=>{{e.value='{valor}';e.dispatchEvent(new Event('input'));}}")
        pagina.select_option("#reg-tipo", "Ridge"); pagina.select_option("#res-modo", "categoria")
        pagina.select_option("#esc-cat", "Tecnologia"); pagina.select_option("#scr-aud", "Comité de riesgo de modelos")
        pagina.fill("#psi-new", "texto"); pagina.click("#psi-calc")
        assert "Ingresa" in pagina.locator("#psi-hint").inner_text()
        pagina.fill("#mr-pred", "1 2"); pagina.click("#mr-calc")
        assert "Ingresa" in pagina.locator("#mr-hint").inner_text()
        pagina.evaluate("startQuiz('c9'); pick(1)")
        assert "Correcto" in pagina.locator("#feedback").inner_text()
        pagina.evaluate("startQuiz('c1'); pick(0)")
        assert "Revisa" in pagina.locator("#feedback").inner_text()
        pagina.fill("#glos-search", "calibración")
        assert pagina.locator("#glos-list dt").count() >= 1
        pagina.check("#clase-toggle"); pagina.wait_for_timeout(120); pagina.uncheck("#clase-toggle")
        for cid in ["c1", "c4", "c6", "c9", "c12", "c16"]:
            pagina.locator("#" + cid).scroll_into_view_if_needed(); pagina.wait_for_timeout(80)
            pagina.screenshot(path=str(CAPTURAS / f"guia_{cid}.png"))
        assert not errores, errores
        assert not red, red
        pagina.set_viewport_size({"width": 390, "height": 844})
        pagina.goto(GUIA.as_uri(), wait_until="load")
        assert pagina.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), "Desbordamiento móvil"
        pagina.screenshot(path=str(CAPTURAS / "guia_movil.png"))
        pagina.set_viewport_size({"width": 1440, "height": 1000})
        pagina.goto(MANUAL_HTML.as_uri(), wait_until="load")
        assert pagina.locator("math").count() > 10, "Fórmulas MathML ausentes"
        pagina.screenshot(path=str(CAPTURAS / "manual_html.png"))
        assert not errores and not red, (errores, red)
        navegador.close()
    resultado.update({"javascript": "OK", "uso_sin_red": "OK", "umbral_contrastado_python": "OK",
                      "auc_contrastado_sklearn": "OK", "escenarios_contrastados_sklearn": "OK",
                      "calculadoras": "OK", "datos_incrustados_actualizados": "OK",
                      "simuladores_y_quiz": "OK", "movil_sin_desbordamiento": "OK"})
    return resultado


def verificar_pdf():
    pdf = fitz.open(MANUAL_PDF)
    assert len(pdf) >= 12, "PDF incompleto"
    texto = "\n".join(pagina.get_text() for pagina in pdf)
    for termino in ["CRISP-DM", "Glosario", "Referencias", "PulpaLenga", "umbral", "calibr", "PSI", "QuillayMarket"]:
        assert termino.casefold() in texto.casefold(), termino
    assert "undefined" not in texto.lower() and "?@" not in texto
    for indice in [0, min(6, len(pdf) - 1), len(pdf) - 1]:
        pdf[indice].get_pixmap(matrix=fitz.Matrix(1.2, 1.2)).save(CAPTURAS / f"manual_pagina_{indice + 1:02}.png")
    resultado = {"paginas": len(pdf), "caracteres_extraidos": len(texto), "resultado": "OK"}
    pdf.close()
    return resultado


def main():
    resultado = {"edicion": "2026-10-08", "notebooks": verificar_notebooks(),
                 "html": {"enlaces_locales_verificados": verificar_enlaces()},
                 "cobertura": verificar_cobertura()}
    resultado["html"].update(verificar_guia())
    resultado["pdf"] = verificar_pdf()
    (SALIDA / "verificacion_edicion.json").write_text(json.dumps(resultado, ensure_ascii=False, indent=2) + "\n",
                                                      encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
