"""Prueba cambios reales de valores y respuestas de widgets en kernels nuevos."""
from pathlib import Path
import json
import os
import nbformat
from nbclient import NotebookClient

CURSO=Path(__file__).resolve().parents[1]
CACHE=CURSO.parent/'.cache-fba'
for var,name in [('IPYTHONDIR','ipython'),('MPLCONFIGDIR','matplotlib'),('JUPYTER_RUNTIME_DIR','jupyter-runtime')]:
    p=CACHE/name;p.mkdir(parents=True,exist_ok=True);os.environ[var]=str(p)

PRUEBA=r'''
import json
_cambios=0
for _nombre in __FUNCIONES__:
    _funcion=globals()[_nombre]
    _interfaz=_funcion.widget
    _salida=_interfaz.children[-1]
    for _control in _interfaz.children:
        if isinstance(_control,(widgets.IntSlider,widgets.FloatSlider)):
            _valores=[_control.min,_control.max]
        elif isinstance(_control,(widgets.Dropdown,widgets.SelectionSlider)):
            _opciones=list(_control.options)
            _valores=[_opciones[0],_opciones[-1]]
        else: continue
        _original=_control.value
        for _valor in _valores:
            _control.value=_valor
            # Ejecutar también la función fuera de Output para que una excepción
            # no quede oculta por el manejador de errores del widget.
            _funcion(**_interfaz.kwargs)
            assert not [o for o in _salida.outputs if o.get('output_type')=='error'],_nombre
            _cambios+=1
        _control.value=_original
_quiz=globals()[__QUIZ__]
_radio=_quiz.children[1];_boton=_quiz.children[2];_out=_quiz.children[3]
_radio.value=None;_boton.click()
assert 'Selecciona una respuesta' in _out.value
_radio.value=_radio.options[1];_boton.click()
assert 'Correcto.' in _out.value
print('FBA_QA='+json.dumps({'cambios_de_control':_cambios,'autoevaluacion':'OK'}))
'''
FUNCIONES={
 '01':['explorar_decision'],
 '02':['efecto_extremo','tablero_visual'],
 '03':['explorar_filtros','explorar_margen'],
 '04':['explorar_bayes','distribucion','area_normal','simular_medias'],
 '05':['explorar_umbral','explorar_profundidad','explorar_clusters']
}
resultados=[]
for archivo in sorted((CURSO/'notebooks').glob('*.ipynb')):
    numero=archivo.name.split('_')[1]
    print('Probando controles: '+archivo.name,flush=True)
    nb=nbformat.read(archivo,as_version=4)
    nb.cells.append(nbformat.v4.new_code_cell(PRUEBA.replace('__FUNCIONES__',repr(FUNCIONES[numero])).replace('__QUIZ__',repr('auto_'+numero))))
    NotebookClient(nb,timeout=240,allow_errors=False,kernel_name='python3',resources={'metadata':{'path':str(CURSO)}}).execute()
    texto=''.join(o.get('text','') for o in nb.cells[-1].outputs)
    result=json.loads(texto.split('FBA_QA=')[-1].strip())
    result['notebook']=archivo.name
    resultados.append(result)
    print(json.dumps(result),flush=True)
(CURSO/'reproducibilidad/verificacion_widgets.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
