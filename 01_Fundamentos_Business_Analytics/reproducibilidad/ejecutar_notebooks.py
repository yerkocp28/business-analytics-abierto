"""Ejecuta notebooks desde kernels nuevos y escribe resultados solo si finalizan."""
from pathlib import Path
import argparse
import json
import os
import sys
import time
import nbformat
from nbclient import NotebookClient

CURSO = Path(__file__).resolve().parents[1]
RAIZ = CURSO.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--originales", action="store_true", help="Incluir también los dos notebooks heredados de FBA")
    parser.add_argument("--solo", help="Fragmento de nombre para repetir una verificación concreta")
    args = parser.parse_args()
    cache = RAIZ / ".cache-fba"
    for variable, subdir in [("IPYTHONDIR", "ipython"), ("MPLCONFIGDIR", "matplotlib"),
                            ("JUPYTER_RUNTIME_DIR", "jupyter-runtime"), ("JUPYTER_CONFIG_DIR", "jupyter-config")]:
        directory = cache / subdir
        directory.mkdir(parents=True, exist_ok=True)
        os.environ[variable] = str(directory)
    os.environ["PYTHONUTF8"] = "1"
    archivos = sorted((CURSO / "notebooks").glob("*.ipynb"))
    if args.originales:
        archivos += sorted(CURSO.glob("U*/**/*.ipynb"))
    if args.solo:
        archivos = [p for p in archivos if args.solo in p.name]
    if not archivos:
        raise SystemExit("No se encontraron notebooks para ejecutar")
    resultados = []
    for archivo in archivos:
        inicio = time.monotonic()
        print("Ejecutando " + archivo.name, flush=True)
        nb = nbformat.read(archivo, as_version=4)
        nbformat.validate(nb)
        cliente = NotebookClient(nb, timeout=240, kernel_name="python3", allow_errors=False,
                                 resources={"metadata": {"path": str(CURSO)}}, store_widget_state=True)
        cliente.execute()
        errores = [o for c in nb.cells if c.cell_type == "code" for o in c.outputs if o.output_type == "error"]
        assert not errores, archivo.name
        nbformat.write(nb, archivo)
        registro = {"archivo": str(archivo.relative_to(RAIZ)).replace("\\", "/"),
                    "resultado": "OK", "celdas_codigo": sum(c.cell_type == "code" for c in nb.cells),
                    "segundos": round(time.monotonic()-inicio, 2),
                    "widgets_guardados": bool(nb.metadata.get("widgets"))}
        resultados.append(registro)
        print(json.dumps(registro, ensure_ascii=False), flush=True)
    output = CURSO / "reproducibilidad" / ("ejecucion_parcial.json" if args.solo else "ejecucion_notebooks.json")
    output.write_text(json.dumps({"python": sys.version.split()[0], "fecha_edicion": "2026-10-08",
                                  "notebooks": resultados}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
