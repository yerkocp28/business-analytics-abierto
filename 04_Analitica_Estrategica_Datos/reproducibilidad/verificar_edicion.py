import os
"""Comprueba integridad, cobertura, cálculos, interacción sin red y presentación AED."""
from pathlib import Path
import csv
import hashlib
import json
import re
from urllib.parse import unquote,urlparse
import nbformat
import numpy as np
import pymupdf as fitz
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from aed_recursos import CURSO, RAIZ, casapeumo, indicadores, plan_produccion, decision

SALIDA=CURSO/'reproducibilidad'


def main():
    resultado={'edicion':'2026-10-08','notebooks':[],'html':{},'pdf':{}}
    capturas=SALIDA/'capturas';capturas.mkdir(exist_ok=True)
    for archivo in sorted((CURSO/'notebooks').glob('*.ipynb')):
        nb=nbformat.read(archivo,as_version=4);nbformat.validate(nb)
        cells=[c for c in nb.cells if c.cell_type=='code']
        assert cells and all(c.execution_count is not None for c in cells),archivo.name
        assert not [o for c in cells for o in c.outputs if o.output_type=='error'],archivo.name
        states=nb.metadata.get('widgets',{}).get('application/vnd.jupyter.widget-state+json',{}).get('state',{})
        assert states,archivo.name
        for state in states.values():
            assert not [o for o in state.get('state',{}).get('outputs',[]) if o.get('output_type')=='error']
        assert not any(re.search('[\x00-\x08\x0b\x0c\x0e-\x1f]',c.source) for c in nb.cells)
        resultado['notebooks'].append({'nombre':archivo.name,'celdas_codigo':len(cells),'widgets':len(states),'resultado':'OK'})
    assert len(resultado['notebooks'])==8

    guia=CURSO/'guia_maestra_aed.html';manual=CURSO/'material_propio/AED_manual_cientifico.html'
    soups={p:BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser') for p in [guia,manual]}
    links=0
    for path,soup in soups.items():
        ids=[tag['id'] for tag in soup.find_all(id=True)]
        assert len(ids)==len(set(ids)),path.name
        for tag in soup.select('a[href]'):
            ref=tag['href'];parts=urlparse(ref)
            if parts.scheme or ref.startswith('//') or not ref:continue
            target=(path.parent/unquote(parts.path)).resolve() if parts.path else path
            assert target.exists(),f'{path.name}: {ref}'
            if parts.fragment and target.suffix=='.html':
                dest=soups.get(target) or BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
                assert dest.find(id=unquote(parts.fragment)),ref
            links+=1
    with (CURSO/'matriz_cobertura.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    esperados={f'1.{i}' for i in range(1,5)}|{f'2.{i}' for i in range(1,6)}|{f'3.{i}' for i in range(1,5)}
    assert {r['criterio_o_tema'] for r in rows if r['nivel']=='nucleo'}==esperados
    for row in rows:
        assert soups[guia].find(id=row['html_ancla']),row
        assert soups[manual].find(id=row['qmd_ancla']),row
        nb=nbformat.read(CURSO/row['notebook'],as_version=4)
        assert any(f'id="{row["notebook_ancla"]}"' in c.source for c in nb.cells),row
    resultado['cobertura']={'criterios_oficiales':13,'filas':len(rows),'anclas_y_rutas':'OK'}

    df,_,_=casapeumo();filters=0;changes=0
    with sync_playwright() as p:
        browser=p.chromium.launch(channel=os.environ.get('BA_BROWSER_CHANNEL','chrome'),headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];network=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        def route(r):
            if r.request.url.startswith(('http:','https:')):network.append(r.request.url);r.abort()
            else:r.continue_()
        page.route('**/*',route)
        page.goto(guia.as_uri(),wait_until='load')
        assert not errors,errors
        assert page.evaluate('typeof window.AED')=='object'
        page.screenshot(path=str(capturas/'guia_inicio.png'))
        for canal in ['Todos',*sorted(df.Canal.unique())]:
            for region in ['Todas',*sorted(df['Región'].unique())]:
                page.select_option('#canal',canal);page.select_option('#region',region)
                actual=page.evaluate('([c,r])=>AED.getKPIs(c,r)',[canal,region])
                f=df
                if canal!='Todos':f=f.loc[f.Canal.eq(canal)]
                if region!='Todas':f=f.loc[f['Región'].eq(region)]
                expected=indicadores(f)
                assert actual['n']==expected['ventas']
                for key in ['ingreso','margen','margen_pct','ticket']:assert np.isclose(actual[key],expected[key]),(canal,region,key)
                assert np.isclose(actual['reclamos'],expected['reclamos_por_1000'])
                filters+=1
        page.select_option('#canal','Todos');page.select_option('#region','Todas')
        page.locator('#visualizacion').scroll_into_view_if_needed();page.screenshot(path=str(capturas/'guia_tablero.png'))
        for H,M in [(100,90),(0,0),(0,90),(180,10),(10,180),(180,180),(70,80)]:
            js=page.evaluate('([h,m])=>AED.solveLP(h,m)',[H,M]);py=plan_produccion(H,M)
            assert py.success and np.isclose(js['valor'],-py.fun)
            assert np.allclose([js['a'],js['b']],py.x)
        for prob in [0,.4,.5,1]:
            js=page.evaluate('(p)=>AED.getDecision(p)',prob);ev,evpi=decision(prob)
            assert np.allclose(js['ev'],ev) and np.isclose(js['evpi'],evpi)
        assert page.evaluate('AED.getDecision(.5).indices.length')==2
        embedded=json.loads(soups[guia].find(id='datos-aed').string)
        z=np.asarray(embedded['normales'])
        for tasa,escala,rho in [(.1,1,-.25),(0,.7,-.8),(.25,1.3,.8)]:
            js=page.evaluate('([r,p,c])=>AED.simulate(r,p,c)',[tasa,escala,rho])
            q=1000*np.exp(.12*z[:,0]-.12**2/2)
            price=100*escala*np.exp(.2*(rho*z[:,0]+np.sqrt(1-rho*rho)*z[:,1])-.2**2/2)
            van=-250+(q*price/1000-30)*sum((1+tasa)**(-t) for t in range(1,6))
            assert np.allclose(js['values'],van,atol=1e-10)
            assert np.isclose(js['mean'],van.mean()) and np.isclose(js['se'],van.std(ddof=1)/np.sqrt(len(van)))
            assert np.isclose(js['prob'],np.mean(van<0)) and np.isclose(js['p05'],np.quantile(van,.05))
        for control in page.locator('input[type=range]').all():
            original=control.input_value()
            for attr in ['min','max']:
                value=control.get_attribute(attr)
                control.evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}));}',value)
                assert not errors,errors;changes+=1
            control.evaluate('(e,v)=>{e.value=v;e.dispatchEvent(new Event("input",{bubbles:true}));}',original)
        for selector in ['#pregunta-tecnica','#audiencia']:
            options=page.locator(selector+' option').evaluate_all('(xs)=>xs.map(x=>x.value)')
            for option in options:page.select_option(selector,option);changes+=1
        for i in range(8):
            page.locator(f'button[data-quiz="{i}"][data-option="0"]').click()
            assert 'Revisa' in page.locator(f'#feedback-{i}').inner_text()
            page.locator(f'button[data-quiz="{i}"][data-option="1"]').click()
            assert 'Correcto.' in page.locator(f'#feedback-{i}').inner_text()
        page.locator('#simulacion').scroll_into_view_if_needed();page.screenshot(path=str(capturas/'guia_simulacion.png'))
        page.set_viewport_size({'width':390,'height':844});page.goto(guia.as_uri(),wait_until='load')
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+2'),'Desbordamiento móvil'
        page.locator('#ba-menu').click();assert page.locator('#ba-menu').get_attribute('aria-expanded')=='true'
        page.locator('#ba-menu').click();page.screenshot(path=str(capturas/'guia_movil.png'))
        page.set_viewport_size({'width':1440,'height':1000});page.goto(manual.as_uri(),wait_until='load')
        assert page.locator('math').count()>=10
        page.screenshot(path=str(capturas/'manual_html.png'))
        assert not errors,errors
        assert not network,network
        browser.close()
    resultado['html']={'javascript':'OK','sin_red':'OK','enlaces_locales':links,
      'filtros_contrastados_python':filters,'cambios_controles':changes,'quizzes':8,
      'LP_EVPI_MonteCarlo_contrastados':'OK','movil_390x844':'OK'}
    pdf=fitz.open(CURSO/'material_propio/AED_manual_cientifico.pdf')
    text='\n'.join(page.get_text() for page in pdf)
    assert len(pdf)>=12 and len(text)>35000
    for term in ['SolarSur','BoldoNet','CasaPeumo','Bellman','Referencias','Glosario','Monte Carlo']:
        assert term.casefold() in text.casefold(),term
    assert not re.search(r'\[@[a-z_]+\]',text),'Citas sin resolver'
    paginas_muestra = [0,len(pdf)//2,len(pdf)-1]
    nombres_muestra = {f'manual_pagina_{i+1:02}.png' for i in paginas_muestra}
    for anterior in capturas.glob('manual_pagina_*.png'):
        if anterior.name not in nombres_muestra:
            assert anterior.resolve().is_relative_to(capturas.resolve())
            anterior.unlink()
    for i in paginas_muestra:pdf[i].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(capturas/f'manual_pagina_{i+1:02}.png')
    resultado['pdf']={'paginas':len(pdf),'caracteres_extraidos':len(text),'resultado':'OK'}
    pdf.close()
    (SALIDA/'verificacion_edicion.json').write_text(json.dumps(resultado,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(resultado,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
