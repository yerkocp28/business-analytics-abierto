"""Ejecuta cada laboratorio en un kernel nuevo y prueba controles y autoevaluaciones."""
from pathlib import Path
import argparse
import json
import os
import sys
import time
import nbformat
from nbclient import NotebookClient

CURSO=Path(__file__).resolve().parents[1]
RAIZ=CURSO.parent

PRUEBA=r'''
import json
_cambios=0
_funciones=[f for nombre,f in list(globals().items()) if callable(f) and hasattr(f,'widget')]
for _f in _funciones:
    _interfaz=_f.widget
    for _control in _interfaz.children:
        if isinstance(_control,(widgets.IntSlider,widgets.FloatSlider)):
            _valores=[_control.min,_control.max]
        elif isinstance(_control,widgets.Checkbox): _valores=[False,True]
        elif isinstance(_control,widgets.Dropdown):
            _opciones=list(_control.options);_valores=[_opciones[0],_opciones[-1]]
        else: continue
        _original=_control.value
        for _valor in _valores:
            _control.value=_valor
            _f(**_interfaz.kwargs)  # Fuera de Output: las excepciones detienen la prueba.
            assert not [o for o in _interfaz.children[-1].outputs if o.get('output_type')=='error']
            _cambios+=1
        _control.value=_original
_quiz=globals()['auto___NUM__'];_radio=_quiz.children[1];_boton=_quiz.children[2];_out=_quiz.children[3]
_radio.value=None;_boton.click();assert 'Selecciona' in _out.value
_radio.value=next(v for _, v in _radio.options if v != _quiz._ba_clave);_boton.click();assert 'Revisa' in _out.value
_radio.value=_quiz._ba_clave;_boton.click();assert 'Correcto.' in _out.value
_radio.value=None;_boton.click()
print('EBA_QA='+json.dumps({'cambios_controles':_cambios,'autoevaluacion':'OK'}))
'''


def configurar():
    for var,name in [('IPYTHONDIR','ipython'),('MPLCONFIGDIR','matplotlib'),
                     ('JUPYTER_RUNTIME_DIR','runtime'),('JUPYTER_CONFIG_DIR','jupyter')]:
        p=RAIZ/'.cache-fba/eba'/name;p.mkdir(parents=True,exist_ok=True);os.environ[var]=str(p)
    os.environ['PYTHONUTF8']='1'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--solo');args=parser.parse_args()
    configurar();resultados=[]
    archivos=sorted((CURSO/'notebooks').glob('*.ipynb'))
    if args.solo:archivos=[p for p in archivos if args.solo in p.name]
    if not archivos:raise SystemExit('No se encontraron notebooks')
    for archivo in archivos:
        inicio=time.monotonic();print('Ejecutando y probando '+archivo.name,flush=True)
        nb=nbformat.read(archivo,as_version=4);nbformat.validate(nb)
        num=archivo.name.split('_')[1]
        nb.cells.append(nbformat.v4.new_code_cell(PRUEBA.replace('__NUM__',num)))
        NotebookClient(nb,timeout=240,kernel_name='python3',allow_errors=False,
                       resources={'metadata':{'path':str(CURSO)}},store_widget_state=True).execute()
        texto=''.join(o.get('text','') for o in nb.cells[-1].outputs)
        qa=json.loads(texto.split('EBA_QA=')[-1].strip());nb.cells.pop()
        assert not [o for c in nb.cells if c.cell_type=='code' for o in c.outputs if o.output_type=='error']
        nbformat.write(nb,archivo)
        registro={'archivo':archivo.relative_to(RAIZ).as_posix(),'resultado':'OK',
                  'celdas_codigo':sum(c.cell_type=='code' for c in nb.cells),
                  'segundos':round(time.monotonic()-inicio,2),**qa}
        resultados.append(registro);print(json.dumps(registro,ensure_ascii=False),flush=True)
    destino=CURSO/'reproducibilidad/ejecucion_notebooks.json'
    if args.solo and destino.exists():
        prev=json.loads(destino.read_text(encoding='utf-8'))['notebooks']
        nuevos={r['archivo'] for r in resultados};resultados=[r for r in prev if r['archivo'] not in nuevos]+resultados
    destino.write_text(json.dumps({'python':sys.version.split()[0],'edicion':'2026-10-08',
        'notebooks':sorted(resultados,key=lambda r:r['archivo'])},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
