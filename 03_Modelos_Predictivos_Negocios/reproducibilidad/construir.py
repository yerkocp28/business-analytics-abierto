"""Reconstrucción de la edición MPN. Requiere el entorno de la colección, Quarto y Chrome."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys

CURSO = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--solo-render", action="store_true", help="Regenerar únicamente PDF y HTML del manual")
    args = parser.parse_args()
    quarto = shutil.which("quarto")
    if not quarto:
        raise SystemExit("Instale Quarto CLI y asegure que quarto está en PATH.")
    env = os.environ.copy()
    env["QUARTO_PYTHON"] = sys.executable
    env["PYTHONUTF8"] = "1"
    repro = CURSO / "reproducibilidad"

    def run(comando):
        subprocess.run([str(v) for v in comando], cwd=CURSO.parent, env=env, check=True)

    if not args.solo_render:
        run([sys.executable, repro / "ejecutar_notebooks.py"])
        run([sys.executable, repro / "verificar_widgets.py"])
        run([sys.executable, repro / "datos_guia.py"])
    run([quarto, "render", CURSO / "material_propio" / "MPN_manual_cientifico.qmd", "--to", "all"])
    run([sys.executable, CURSO.parent / '_transversal/construir_interfaz.py', '--curso', 'MPN'])
    run([sys.executable, CURSO / 'reproducibilidad/verificar_edicion.py'])
    print("Construcción terminada. Revise la evidencia de ejecución antes de publicar.")


if __name__ == "__main__":
    main()
