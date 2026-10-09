"""Construye y comprueba la colección abierta con un único entorno Python."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from rutas import CURSOS

RAIZ=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--solo-render',action='store_true');p.add_argument('--solo-verificar',action='store_true');args=p.parse_args()
    if args.solo_render and args.solo_verificar:p.error('Elija solo una modalidad.')
    env=os.environ.copy();env['PYTHONUTF8']='1';env['PYTHONIOENCODING']='utf-8';env['QUARTO_PYTHON']=sys.executable
    env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env.get('PATH','')
    for variable,folder in [('IPYTHONDIR','ipython'),('MPLCONFIGDIR','matplotlib'),('JUPYTER_RUNTIME_DIR','runtime'),('JUPYTER_CONFIG_DIR','jupyter')]:
        path=RAIZ/'.cache-fba'/folder;path.mkdir(parents=True,exist_ok=True);env[variable]=str(path)
    logs=RAIZ/'.cache-fba/verificacion';logs.mkdir(parents=True,exist_ok=True)
    results=[]
    evidence=RAIZ/'verificacion';evidence.mkdir(exist_ok=True)
    packages={name:importlib.metadata.version(name) for name in ['numpy','pandas','scipy','scikit-learn','statsmodels','nbclient','ipywidgets','playwright','pymupdf']}
    summary={'fecha_utc':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'plataforma':platform.system(),
             'modo':'solo_verificar' if args.solo_verificar else 'solo_render' if args.solo_render else 'completo',
             'dependencias':packages,'quarto':subprocess.check_output([shutil.which('quarto'),'--version'],text=True).strip(),
             'pruebas':results,'resultado':'EN_CURSO'}
    def registrar(estado):
        summary['resultado']=estado
        (evidence/'ultima_ejecucion.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    registrar('EN_CURSO')
    def run(name,command):
        start=time.monotonic();print(f'{name}: en curso',flush=True)
        with (logs/(name+'.log')).open('w',encoding='utf-8') as log:
            result=subprocess.run(command,cwd=RAIZ,env=env,stdout=log,stderr=subprocess.STDOUT)
        item={'prueba':name,'codigo':result.returncode,'segundos':round(time.monotonic()-start,2)};results.append(item)
        print(json.dumps(item),flush=True)
        registrar('ERROR' if result.returncode else 'EN_CURSO')
        if result.returncode:
            print((logs/(name+'.log')).read_text(encoding='utf-8')[-8000:]);raise SystemExit(result.returncode)
    if not args.solo_verificar:
        run('recursos_herramientas',[sys.executable,str(RAIZ/'_transversal/herramientas.py')])
        run('perfil_datos',[sys.executable,str(RAIZ/'_transversal/datos/perfilar.py')])
        run('rutas_fuentes',[sys.executable,str(RAIZ/'_transversal/construir_interfaz.py'),'--fuentes'])
    for code,course in CURSOS.items():
        script='verificar_edicion.py' if args.solo_verificar else 'construir.py'
        command=[sys.executable,str(RAIZ/course['carpeta']/'reproducibilidad'/script)]
        if args.solo_render:command.append('--solo-render')
        run(code,command)
    run('metodologia',[sys.executable,str(RAIZ/'_transversal/verificar_metodologia.py')])
    run('interfaz',[sys.executable,str(RAIZ/'_transversal/verificar_interfaz.py')])
    run('publico',[sys.executable,str(RAIZ/'_transversal/verificar_publico.py')])
    registrar('OK')
    print('Colección construida y comprobada; evidencia en verificacion/.',flush=True)

if __name__=='__main__':main()
