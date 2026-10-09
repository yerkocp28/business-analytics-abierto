import os
"""Comprobaciones de publicación local: notebooks, datos, HTML interactivo y PDF."""
from pathlib import Path
import csv
import json
import math
import re
import sys
from urllib.parse import unquote, urlparse
import nbformat
import pandas as pd
import numpy as np
import pymupdf as fitz
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

CURSO=Path(__file__).resolve().parents[1]
RAIZ=CURSO.parent
SALIDA=CURSO/'reproducibilidad'
CAPTURAS=SALIDA/'capturas'
CAPTURAS.mkdir(exist_ok=True)
sys.path.insert(0,str(SALIDA))
from fba_recursos import ventas, resumen_ventas


def main():
    resultado={'edicion':'2026-10-08','notebooks':[], 'html':{},'pdf':{}}
    for file in sorted((CURSO/'notebooks').glob('*.ipynb')) + sorted(CURSO.glob('U*/**/*.ipynb')):
        nb=nbformat.read(file,as_version=4)
        nbformat.validate(nb)
        code=[c for c in nb.cells if c.cell_type=='code']
        assert all(c.execution_count is not None for c in code),file.name
        assert not [o for c in code for o in c.outputs if o.output_type=='error'],file.name
        # Las excepciones capturadas por widgets también deben detectarse.
        states=nb.metadata.get('widgets',{}).get('application/vnd.jupyter.widget-state+json',{}).get('state',{})
        for state in states.values():
            assert not [o for o in state.get('state',{}).get('outputs',[]) if o.get('output_type')=='error'],file.name
        assert not any(re.search('[\x00-\x08\x0b\x0c\x0e-\x1f]',c.source) for c in nb.cells),file.name
        resultado['notebooks'].append({'nombre':file.name,'celdas_codigo':len(code),'widgets':len(states),'resultado':'OK'})

    links=0
    for file in [CURSO/'guia_maestra_ba.html',CURSO/'material_propio/FBA_manual_cientifico.html']:
        soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
        ids=[tag['id'] for tag in soup.find_all(id=True)]
        assert len(ids)==len(set(ids)),f'ID HTML repetido: {file.name}'
        for tag in soup.select('a[href]'):
            ref=tag['href'];parts=urlparse(ref)
            if parts.scheme or ref.startswith('//') or not ref:continue
            if parts.path:
                target=(file.parent/unquote(parts.path)).resolve()
                assert target.exists(),f'Enlace ausente {file.name}: {ref}'
            elif parts.fragment:
                assert unquote(parts.fragment) in ids,f'Ancla ausente {file.name}: {ref}'
            links+=1
    resultado['html']['enlaces_locales_verificados']=links
    with (CURSO/'matriz_cobertura.csv').open(encoding='utf-8-sig',newline='') as f:
        cobertura=list(csv.DictReader(f))
    esperados={f'1.{i}' for i in range(1,5)}|{f'2.{i}' for i in range(1,6)}|{f'3.{i}' for i in range(1,7)}
    assert {r['criterio_o_tema'] for r in cobertura if r['nivel']=='nucleo'}==esperados
    guia=BeautifulSoup((CURSO/'guia_maestra_ba.html').read_text(encoding='utf-8'),'html.parser')
    manual=BeautifulSoup((CURSO/'material_propio/FBA_manual_cientifico.html').read_text(encoding='utf-8'),'html.parser')
    for fila in cobertura:
        assert guia.find(id=fila['html_ancla']),fila
        assert manual.find(id=fila['qmd_ancla']),fila
        n=nbformat.read(CURSO/fila['notebook'],as_version=4)
        assert any(f'id="{fila["notebook_ancla"]}"' in c.source for c in n.cells),fila
    resultado['cobertura']={'criterios_oficiales':len(esperados),'filas_temas':len(cobertura),'anclas_y_rutas':'OK'}
    df=ventas()
    q2=df[df.Fecha.dt.quarter.eq(2)]
    with sync_playwright() as p:
        browser=p.chromium.launch(channel=os.environ.get('BA_BROWSER_CHANNEL','chrome'),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000},device_scale_factor=1)
        errores=[];network=[]
        page.on('pageerror',lambda error:errores.append(str(error)))
        def ruta(route):
            if route.request.url.startswith(('http:','https:')):
                network.append(route.request.url);route.abort()
            else:route.continue_()
        page.route('**/*',ruta)
        page.goto((CURSO/'guia_maestra_ba.html').as_uri(),wait_until='load')
        page.screenshot(path=str(CAPTURAS/'guia_inicio.png'))
        assert not errores,errores
        assert not network,network
        resumen=page.evaluate('window.FBA_ULTIMO_RESUMEN')
        assert resumen['n']==len(q2)
        assert np.isclose(resumen['ingreso'],q2.Monto.sum())
        page.select_option('#fba-trimestre','0')
        assert page.evaluate('window.FBA_ULTIMO_RESUMEN.n')==180
        for region in sorted(df.Region.unique()):
            page.select_option('#fba-region',region)
            for product in sorted(df.Producto.unique()):
                page.select_option('#fba-producto',product)
                r=page.evaluate('window.FBA_ULTIMO_RESUMEN')
                exp=df[df.Region.eq(region)&df.Producto.eq(product)]
                assert r['n']==len(exp)
                assert np.isclose(r['ingreso'],exp.Monto.sum())
        page.select_option('#fba-region','Todas');page.select_option('#fba-producto','Todos')
        page.select_option('#fba-trimestre','2')
        assert abs(page.evaluate('fbaDelta(100,.2,.05,.3)'))<1e-10
        assert np.isclose(page.evaluate('fbaDelta(100,.1,.05,.3)'),-2.5)
        page.locator('#c14').scroll_into_view_if_needed()
        page.screenshot(path=str(CAPTURAS/'guia_herramientas.png'))
        desc=page.evaluate('describe([1,2,3,4])')
        assert np.isclose(desc['mean'],2.5) and np.isclose(desc['varr'],5/3)
        assert desc['q1']==1.75 and desc['q3']==3.25
        assert np.isclose(page.evaluate('normCdf(1)'),.841344746,atol=2e-7)
        page.fill('#ds-input','5 5 5 5');page.evaluate('calcDesc()')
        assert 'dispersión cero' in page.locator('#ds-interp').inner_text()
        page.fill('#ds-input','texto');page.evaluate('calcDesc()')
        assert 'al menos dos' in page.locator('#ds-stats').inner_text()
        page.evaluate("loadEjemplo('bimodal')")
        for val in ['-100','0','100']:
            page.eval_on_selector('#corr-slider',f"e=>{{e.value='{val}';e.dispatchEvent(new Event('input'));}}")
        page.evaluate('crispGo(5)');page.evaluate('crispStep(1)')
        page.evaluate('regDemo();toggleResid();kmReset();kmStep();drawCM()')
        page.evaluate('regPts=[[10,20],[10,30]];drawReg()')
        assert 'no tiene variabilidad' in page.locator('#reg-stats').inner_text()
        page.evaluate('regPts=[[10,20],[30,20]];drawReg()')
        page.evaluate('regDemo()')
        page.eval_on_selector('#sd-slider',"e=>{e.value='40';e.dispatchEvent(new Event('input'));}")
        page.eval_on_selector('#th-slider',"e=>{e.value='95';e.dispatchEvent(new Event('input'));}")
        page.check('#clase-toggle');page.wait_for_timeout(100);page.uncheck('#clase-toggle')
        page.fill('#glos-search','correlación')
        assert page.locator('#glos-list').count() or page.locator('text=Correlación de Pearson').count()
        # Probar una pregunta real y comprobar retroalimentación.
        quiz_key=page.evaluate('Object.keys(BANK)[0]')
        page.evaluate('(key)=>startQuiz(key)',quiz_key)
        page.evaluate('pick(0)')
        page.evaluate("startQuiz('c14');pick(1)")
        assert 'Correct' in page.locator('#feedback').inner_text()
        assert not errores,errores
        page.set_viewport_size({'width':390,'height':844})
        page.goto((CURSO/'guia_maestra_ba.html').as_uri(),wait_until='load')
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth+2'), 'Desbordamiento móvil'
        page.screenshot(path=str(CAPTURAS/'guia_movil.png'))
        page.set_viewport_size({'width':1440,'height':1000})
        page.goto((CURSO/'material_propio/FBA_manual_cientifico.html').as_uri(),wait_until='load')
        assert page.locator('math').count()>10,'Fórmulas MathML ausentes'
        assert not network,network
        assert not errores,errores
        page.screenshot(path=str(CAPTURAS/'manual_html.png'))
        browser.close()
    resultado['html'].update({'javascript':'OK','uso_sin_red':'OK','filtros_contrastados_python':'OK',
                               'simuladores_y_quiz':'OK','movil_sin_desbordamiento':'OK'})
    pdf=fitz.open(CURSO/'material_propio/FBA_manual_cientifico.pdf')
    assert len(pdf)>=15,'PDF incompleto'
    texto='\n'.join(page.get_text() for page in pdf)
    for term in ['CRISP','Glosario','Referencias','QuillayMarket','regresión','Monte Carlo']:
        assert term.casefold() in texto.casefold(),term
    assert 'undefined' not in texto.lower()
    for index in [0, min(8,len(pdf)-1),len(pdf)-1]:
        pdf[index].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(CAPTURAS/f'manual_pagina_{index+1:02}.png')
    resultado['pdf']={'paginas':len(pdf),'caracteres_extraidos':len(texto),'resultado':'OK'}
    pdf.close()
    (SALIDA/'verificacion_edicion.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(resultado,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
