"""Reconstruye y verifica la edición AED sin modificar datos originales ni el catálogo."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys

CURSO=Path(__file__).resolve().parents[1]
RAIZ=CURSO.parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--solo-render',action='store_true');args=p.parse_args()
    quarto=shutil.which('quarto')
    if not quarto:raise SystemExit('Instale Quarto y agréguelo al PATH para generar PDF/HTML.')
    env=os.environ.copy();env['QUARTO_PYTHON']=sys.executable;env['PYTHONUTF8']='1'
    def script(nombre):subprocess.run([sys.executable,str(CURSO/'reproducibilidad'/nombre)],cwd=RAIZ,env=env,check=True)
    if not args.solo_render:script('ejecutar_notebooks.py')
    script('construir_guia.py')
    subprocess.run([quarto,'render',str(CURSO/'material_propio/AED_manual_cientifico.qmd'),'--to','all'],cwd=RAIZ,env=env,check=True)
    script('verificar_edicion.py')
    print('Edición verificada. Revise resultados y actualice el catálogo conservando hashes originales.')


if __name__=='__main__':main()
