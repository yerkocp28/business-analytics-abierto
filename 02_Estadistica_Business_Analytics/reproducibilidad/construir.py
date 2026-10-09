"""Ejecuta, renderiza manual, deriva guía y verifica toda la edición."""
from pathlib import Path
import argparse, os, shutil, subprocess, sys
C=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser();p.add_argument('--solo-render',action='store_true');args=p.parse_args()
    quarto=shutil.which('quarto')
    if not quarto:raise SystemExit('Instale Quarto CLI y agréguelo al PATH.')
    env=os.environ.copy();env['QUARTO_PYTHON']=sys.executable;env['PYTHONUTF8']='1'
    for variable,subdir in [('IPYTHONDIR','ipython'),('MPLCONFIGDIR','matplotlib'),('JUPYTER_RUNTIME_DIR','runtime'),('JUPYTER_CONFIG_DIR','jupyter')]:
        d=C.parent/'.cache-fba/eba'/subdir;d.mkdir(parents=True,exist_ok=True);env[variable]=str(d)
    def run(cmd):subprocess.run(cmd,cwd=C.parent,env=env,check=True)
    def script(name):run([sys.executable,str(C/'reproducibilidad'/name)])
    if not args.solo_render:
        script('ejecutar_notebooks.py')
        # El notebook 07 escribe su libro en salidas/ (excluida de Git); la edición publica esa versión.
        shutil.copy2(C.parent/'salidas'/'EBA_tablero_excel.xlsx',C/'material_propio'/'EBA_tablero_excel.xlsx')
    run([quarto,'render',str(C/'material_propio/EBA_manual_cientifico.qmd'),'--to','all'])
    script('construir_guia.py')
    run([sys.executable,str(C.parent/'_transversal/construir_interfaz.py'),'--curso','EBA'])
    script('verificar_edicion.py')
    print('Edición construida y verificada. Revise los cambios y la evidencia antes de publicar.')
if __name__=='__main__':main()
