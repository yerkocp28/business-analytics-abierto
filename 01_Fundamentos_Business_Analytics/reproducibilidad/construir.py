"""Reconstrucción de la edición FBA. Requiere el entorno, Quarto y Chrome."""
from pathlib import Path
import argparse
import os
import shutil
import subprocess
import sys

CURSO=Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--solo-render',action='store_true',help='Regenerar únicamente los formatos del QMD')
    args=parser.parse_args()
    quarto=shutil.which('quarto')
    if not quarto:
        raise SystemExit('Instale Quarto CLI y asegure que quarto está en PATH.')
    env=os.environ.copy()
    env['QUARTO_PYTHON']=sys.executable
    env['PYTHONUTF8']='1'
    def run(command):
        subprocess.run([str(v) for v in command],cwd=CURSO.parent,env=env,check=True)
    if not args.solo_render:
        run([sys.executable,CURSO/'reproducibilidad/ejecutar_notebooks.py','--originales'])
        run([sys.executable,CURSO/'reproducibilidad/verificar_widgets.py'])
        run([sys.executable,CURSO/'reproducibilidad/datos_guia.py'])
    run([quarto,'render',CURSO/'material_propio/FBA_manual_cientifico.qmd','--to','all'])
    run([sys.executable, CURSO.parent / '_transversal/construir_interfaz.py', '--curso', 'FBA'])
    run([sys.executable, CURSO / 'reproducibilidad/verificar_edicion.py'])
    print('Construcción terminada. Revise las salidas y la evidencia de ejecución antes de publicar.')


if __name__=='__main__':
    main()
