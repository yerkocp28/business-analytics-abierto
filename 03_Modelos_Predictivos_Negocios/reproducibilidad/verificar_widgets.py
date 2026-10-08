"""Prueba cambios reales de valores y respuestas de widgets de la edición MPN en kernels nuevos."""
from pathlib import Path
import json
import os

import nbformat
from nbclient import NotebookClient

CURSO = Path(__file__).resolve().parents[1]
CACHE = CURSO.parent / ".cache-fba"
for var, nombre in [("IPYTHONDIR", "ipython"), ("MPLCONFIGDIR", "matplotlib"), ("JUPYTER_RUNTIME_DIR", "jupyter-runtime")]:
    p = CACHE / nombre
    p.mkdir(parents=True, exist_ok=True)
    os.environ[var] = str(p)

PRUEBA = r'''
import json
from IPython.utils import io as _io
_cambios = 0
for _nombre in __FUNCIONES__:
    _funcion = globals()[_nombre]
    _interfaz = _funcion.widget
    _salida = _interfaz.children[-1]
    for _control in _interfaz.children:
        if isinstance(_control, (widgets.IntSlider, widgets.FloatSlider)):
            _valores = [_control.min, _control.max]
        elif isinstance(_control, (widgets.Dropdown, widgets.SelectionSlider)):
            _opciones = list(_control.options)
            _valores = [_opciones[0], _opciones[-1]]
        else:
            continue
        _original = _control.value
        for _valor in _valores:
            _control.value = _valor
            with _io.capture_output():
                _funcion(**_interfaz.kwargs)      # fuera de Output: una excepción no queda oculta
            assert not [o for o in _salida.outputs if o.get("output_type") == "error"], _nombre
            _cambios += 1
        _control.value = _original
_quiz = globals()[__QUIZ__]
_radio, _boton, _out = _quiz.children[1], _quiz.children[2], _quiz.children[3]
_radio.value = None; _boton.click()
assert "Selecciona una respuesta" in _out.value
_radio.value = _radio.options[1]; _boton.click()
assert "Correcto." in _out.value
_radio.value = _radio.options[0]; _boton.click()
assert "Revisa tu respuesta" in _out.value
print("MPN_QA=" + json.dumps({"cambios_de_control": _cambios, "autoevaluacion": "OK"}))
'''
FUNCIONES = {
    "01": ["explorar_ruido", "explorar_red"],
    "02": ["explorar_imputacion"],
    "03": ["explorar_regularizacion", "explorar_escenario"],
    "04": ["explorar_sigmoide", "explorar_campania"],
    "05": ["explorar_complejidad", "explorar_umbral"],
    "06": ["explorar_deriva", "explorar_mensaje"],
    "07": ["explorar_pronostico"],
}


def main():
    resultados = []
    for archivo in sorted((CURSO / "notebooks").glob("*.ipynb")):
        numero = archivo.name.split("_")[1]
        print("Probando controles: " + archivo.name, flush=True)
        nb = nbformat.read(archivo, as_version=4)
        nb.cells.append(nbformat.v4.new_code_cell(PRUEBA.replace("__FUNCIONES__", repr(FUNCIONES[numero]))
                                                  .replace("__QUIZ__", repr("auto_" + numero))))
        NotebookClient(nb, timeout=900, allow_errors=False, kernel_name="python3",
                       resources={"metadata": {"path": str(CURSO / "notebooks")}}).execute()
        texto = "".join(o.get("text", "") for o in nb.cells[-1].outputs)
        resultado = json.loads(texto.split("MPN_QA=")[-1].strip())
        resultado["notebook"] = archivo.name
        resultado["funciones"] = FUNCIONES[numero]
        resultados.append(resultado)
        print(json.dumps(resultado, ensure_ascii=False), flush=True)
    (CURSO / "reproducibilidad" / "verificacion_widgets.json").write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
