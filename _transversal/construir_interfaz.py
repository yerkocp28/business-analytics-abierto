"""Construye recursos de aprendizaje y navegación sin servicios externos."""
from pathlib import Path
import argparse
import hashlib
import html
import re
import nbformat
from bs4 import BeautifulSoup
from rutas import CURSOS, modulos
from practicas import PRACTICAS

RAIZ = Path(__file__).resolve().parents[1]
E = html.escape

def recursos(codigo):
    curso = CURSOS[codigo]
    carpeta = RAIZ / curso['carpeta']
    rows = []
    for m in modulos(codigo):
        m['notebook'] = next((carpeta/'notebooks').glob(f'{codigo}_{m["numero"]:02}_*.ipynb')).name
        rows.append(m)
    return carpeta, rows

def preparar_fuentes(codigo):
    curso = CURSOS[codigo]; carpeta, rows = recursos(codigo)
    intro = (f'**Preparación de entrada:** {curso["prerrequisito"]}\n\n'
             'Los tiempos orientan una práctica guiada y deben ajustarse al diagnóstico del grupo. '
             'Cada módulo sigue la secuencia: anticipar → ejecutar → modificar → explicar. '
             'La profundización se consulta después del núcleo.\n\n')
    md = f'# Ruta de aprendizaje · {curso["nombre"]}\n\n[Curso](README.md) · [Guía]({curso["guia"]}#ruta-aprendizaje)\n\n' + intro
    pauta = '# Pauta docente · ' + curso['nombre'] + '\n\n[Guía](../' + curso['guia'] + ') · [Ruta](../RUTA_APRENDIZAJE.md)\n\nResolver primero las prácticas de los notebooks. Esta pauta formativa separa respuestas y errores frecuentes; no es una evaluación institucional.\n\n'
    manual = '## Objetivos y evidencias por módulo {#sec-aprendizaje}\n\n' + intro
    for m in rows:
        n=m['numero']; title=f'{n:02} · {m["titulo"]}'
        block=(f'**Objetivo:** {m["objetivo"]}\n\n**Preparación:** {m["preparacion"]}\n\n'
               f'**Ejemplo de referencia:** {m["ejemplo"]}\n\n**Práctica:** {m["actividad"]}\n\n'
               f'**Criterio de logro:** {m["logro"]}\n\n'
               f'**Distribución orientativa:** explicación {m["explicacion_min"]} min; práctica guiada {m["practica_min"]} min; trabajo autónomo {m["autonomo_min"]} min. Ajustar tras una clase piloto.\n\n' )
        md += f'## {title}\n\n{m["nivel"]} · {m["duracion"]} orientativos.\n\n' + block
        md += f'[Capítulo]({curso["guia"]}#{m["ancla"]}) · [Manual](material_propio/{codigo}_manual_cientifico.html#{m["manual"]}) · [Notebook](notebooks/{m["notebook"]})\n\n'
        manual += f'**NB{n:02} · {m["titulo"]} ({m["nivel"]}).** {m["objetivo"]} **Evidencia:** {m["logro"]}\n\n'
        path=carpeta/'notebooks'/m['notebook']; nb=nbformat.read(path,as_version=4)
        nb.cells=[c for c in nb.cells if 'ruta-aprendizaje' not in c.metadata.get('tags',[])]
        cell=nbformat.v4.new_markdown_cell(f'### Antes de ejecutar\n\n{m["nivel"]} · {m["duracion"]} orientativos.\n\n'+block+
            f'[Guía y secuencia](../{curso["guia"]}#ruta-aprendizaje) · [Fundamento del manual](../material_propio/{codigo}_manual_cientifico.html#{m["manual"]})')
        cell.metadata['tags']=['ruta-aprendizaje'];cell.id=hashlib.sha256(f'{codigo}-{n}-ruta'.encode()).hexdigest()[:12]
        nb.cells.insert(1,cell)
        nb.cells=[c for c in nb.cells if not set(c.metadata.get('tags',[])) & {'practica-transferencia','respuesta-estudiante'}]
        consigna,solucion,error,discusion=PRACTICAS[codigo][n-1]
        practica=nbformat.v4.new_markdown_cell(f'## Práctica de transferencia {n:02}\n\n{consigna}\n\n**Entrega:** hipótesis previa, cálculo con unidades, interpretación y límite. Completa tu respuesta antes de consultar la [pauta docente](../material_propio/PAUTA_DOCENTE.md#nb{n:02}).\n\n**Discusión:** {discusion}')
        practica.metadata['tags']=['practica-transferencia'];practica.id=hashlib.sha256(f'{codigo}-{n}-practica'.encode()).hexdigest()[:12]
        respuesta=nbformat.v4.new_markdown_cell('### Tu resolución\n\nEdita esta celda: escribe tu hipótesis, procedimiento, resultado, interpretación y una comprobación. Adjunta tu código o gráfico si la actividad lo requiere.\n\n**Auto-revisión:** ¿usé la población correcta?, ¿declaré unidades y supuestos?, ¿mi evidencia permite esa conclusión?')
        respuesta.metadata['tags']=['respuesta-estudiante'];respuesta.id=hashlib.sha256(f'{codigo}-{n}-respuesta'.encode()).hexdigest()[:12]
        nb.cells.extend([practica,respuesta]);nbformat.write(nb,path)
        pauta+=f'<a id="nb{n:02}"></a>\n## {title}\n\n**Consigna:** {consigna}\n\n**Pauta razonada:** {solucion}\n\n**Error frecuente:** {error}\n\n**Discusión:** {discusion}\n\n**Criterio:** {m["logro"]}\n\n'
        manual+=f'**Transferencia NB{n:02}:** {consigna}\n\n'
    (carpeta/'material_propio/PAUTA_DOCENTE.md').write_text(pauta.rstrip()+'\n',encoding='utf-8')
    (carpeta/'RUTA_APRENDIZAJE.md').write_text(md.rstrip()+'\n',encoding='utf-8')
    path=carpeta/'material_propio'/f'{codigo}_manual_cientifico.qmd'; text=path.read_text(encoding='utf-8')
    text=re.sub(r'<!-- BA_APRENDIZAJE_INICIO -->.*?<!-- BA_APRENDIZAJE_FIN -->\s*','',text,flags=re.S)
    headings=list(re.finditer(r'^# (?!\|)',text,re.M)); assert len(headings)>1
    position=headings[1].start()
    text=text[:position]+'<!-- BA_APRENDIZAJE_INICIO -->\n'+manual+'<!-- BA_APRENDIZAJE_FIN -->\n\n'+text[position:]
    path.write_text(text,encoding='utf-8')

def construir_guia(codigo):
    curso=CURSOS[codigo];carpeta,rows=recursos(codigo);path=carpeta/curso['guia']
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser');main=soup.find('main');aside=soup.find('aside')
    # Recuperar controles originales antes de reemplazar los bloques propios de una construcción previa.
    original_mode=soup.find(id='clase-toggle'); mode_label=original_mode.find_parent('label').extract() if original_mode else None
    original_search=soup.find(id='buscar'); original_search=original_search.extract() if original_search else None
    wrapper=soup.find(id='ba-panel-indice')
    if wrapper:wrapper.unwrap()
    for node in soup.select('[data-ba-generado]'):node.decompose()
    def fragment(markup):return BeautifulSoup(markup,'html.parser')
    style=soup.new_tag('style',id='ba-estilo');style['data-ba-generado']='';style.string=(RAIZ/'_transversal/interfaz/guia.css').read_text(encoding='utf-8');soup.head.append(style)
    script=soup.new_tag('script',id='ba-interfaz');script['data-ba-generado']='';script.string=(RAIZ/'_transversal/interfaz/guia.js').read_text(encoding='utf-8');soup.body.append(script)
    main['id']=main.get('id','contenido')
    soup.body.insert(0,fragment(f'<a data-ba-generado class="ba-saltar" href="#{main["id"]}">Saltar al contenido</a>'))
    bar=fragment(f'<nav data-ba-generado class="ba-barra" aria-label="Recursos del curso"><a href="../index.html">Biblioteca</a><a href="#ruta-aprendizaje">Ruta de aprendizaje</a><a href="material_propio/{codigo}_manual_cientifico.pdf">Manual PDF</a><a href="material_propio/{codigo}_manual_cientifico.html">Manual HTML</a></nav>').nav
    if not mode_label:mode_label=fragment('<label><input type="checkbox" id="clase-toggle">Modo clase</label>').label
    bar.append(mode_label);main.insert(0,bar)
    nav=aside.find('nav'); assert nav
    panel=soup.new_tag('div',id='ba-panel-indice');nav.insert_before(panel)
    panel.append(nav.extract())
    label=fragment('<label class="ba-busqueda" data-ba-generado>Buscar en el curso</label>').label
    if original_search:
        old=aside.find('label',attrs={'for':'buscar'})
        if old:old.decompose()
        search=original_search
    else:search=soup.new_tag('input',id='ba-buscar',type='search')
    search['placeholder']='Concepto, método o actividad…';label['for']=search['id'];label.append(search);panel.insert(0,label)
    label.insert_after(fragment('<span data-ba-generado id="ba-conteo" role="status" aria-live="polite"></span><ul data-ba-generado id="ba-resultados" hidden></ul>'))
    panel.insert_before(fragment('<button data-ba-generado id="ba-menu" type="button" aria-expanded="false" aria-controls="ba-panel-indice">Mostrar índice</button>'))
    nav.insert(0,fragment('<a data-ba-generado href="#ruta-aprendizaje">Ruta de aprendizaje</a>'))
    cards=[]
    for m in rows:
        cards.append(f'''<article class="ba-modulo" id="modulo-{m['numero']:02}"><span class="ba-nivel">{E(m['nivel'])} · {E(m['duracion'])} orientativos</span>
<h3>{m['numero']:02} · {E(m['titulo'])}</h3><p><strong>Objetivo.</strong> {E(m['objetivo'])}</p>
<details><summary>Preparar, practicar y comprobar</summary><dl><dt>Preparación</dt><dd>{E(m['preparacion'])}</dd><dt>Ejemplo trabajado</dt><dd>{E(m['ejemplo'])}</dd><dt>Tu práctica</dt><dd>{E(m['actividad'])}</dd><dt>Criterio de logro</dt><dd>{E(m['logro'])}</dd></dl></details>
<div class="ba-recursos"><a href="#{m['ancla']}">Estudiar el tema</a><a href="notebooks/{m['notebook']}">Notebook {m['numero']:02}</a><a href="material_propio/{codigo}_manual_cientifico.html#{m['manual']}">Fundamento</a></div></article>''')
        chapter=soup.find(id=m['ancla']); assert chapter,m['ancla']
        heading=chapter.find(['h1','h2'])
        heading.insert_after(fragment(f'<div data-ba-generado class="ba-clase-objetivo"><strong>Al terminar:</strong> {E(m["objetivo"])} <a href="#modulo-{m["numero"]:02}">Ver práctica y criterio de logro</a></div>'))
    calendar=''
    if codigo=='MPN':
        calendar='''<div class="ba-calendario"><h3>Elige tu calendario</h3><button type="button" data-ba-ruta="5" aria-pressed="false">Intensivo · 5 semanas</button><button type="button" data-ba-ruta="12" aria-pressed="true">Extendido · 12 semanas</button><p data-ba-calendario="5" hidden>Semana 1: problema y diagnóstico; 2: técnicas; 3: preparación y clasificación; 4: validación; 5: regresión y comunicación. <a href="#ruta-intensiva">Abrir planificación de cinco semanas</a>. Los módulos 01–06 son la referencia; seleccionar las actividades indicadas en esa planificación.</p><p data-ba-calendario="12">Distribuye preparación, modelos, evaluación y comunicación durante doce semanas. <a href="#c12">Abrir planificación de doce semanas</a>. El módulo 07 es profundización.</p></div>'''
    route=fragment(f'<section data-ba-generado id="ruta-aprendizaje" class="ba-ruta"><h2>Tu recorrido de aprendizaje</h2><p><strong>Antes de empezar:</strong> {E(curso["prerrequisito"])}</p><p>Anticipa un resultado, ejecuta el ejemplo, cambia una condición y explica la decisión. Los tiempos son orientativos: ajusta la preparación y la práctica a tu diagnóstico.</p>{calendar}<div class="ba-modulos">{"".join(cards)}</div></section>')
    # La ruta permanece cerca de la portada y sus enlaces llevan al contenido existente.
    initial=main.find(['header','section'],recursive=False)
    if initial:initial.insert_after(route)
    else:bar.insert_after(route)
    orientacion = fragment('<p class="ba-laboratorios">Los notebooks necesitan Jupyter y los datos de la colección. <a href="../index.html#laboratorios">Preparar los laboratorios</a>. La guía y sus simuladores se pueden usar directamente en el navegador.</p>')
    soup.find(id='ruta-aprendizaje').find('div',class_='ba-modulos').insert_before(orientacion)
    for enlace in soup.select('a[href$=".ipynb"]'):enlace['download']=''
    chapters=main.find_all('section',recursive=False)
    for i,chapter in enumerate(chapters):
        if chapter.get('id')=='ruta-aprendizaje':continue
        links=[]
        for j,label in [(i-1,'← Anterior'),(i+1,'Siguiente →')]:
            if 0<=j<len(chapters):
                target=chapters[j];heading=target.find(['h1','h2']);title=heading.get_text(' ',strip=True) if heading else 'Inicio'
                links.append(f'<a href="#{target["id"]}">{label}: {E(title)}</a>')
        chapter.append(fragment(f'<nav data-ba-generado class="ba-pasos" aria-label="Secuencia del capítulo">{"".join(links)}</nav>'))
    # Un nombre programático no se obtiene de un texto vecino sin asociación.
    names={'mu-slider':('Media de la normal','unidades'),'sd-slider':('Desviación estándar de la normal','unidades'),
           'x-slider':('Punto de corte de la normal','unidades'),'k-slider':('Número de grupos K-means','grupos'),
           'th-slider':('Umbral de clasificación','por ciento'),'horas':('Capacidad de horas','horas'),
           'material':('Capacidad de material','unidades'),'prob':('Probabilidad del escenario alto',''),
           'peso':('Peso de rentabilidad en la decisión multicriterio',''),'tasa':('Tasa de descuento anual',''),
           'precio':('Multiplicador del precio de SolarSur',''),'rho':('Correlación entre producción y precio',''),
           'reduccion':('Reducción relativa supuesta de incidentes',''),'costo':('Costo de la intervención','UM'),
           'precio-nl':('Precio en el modelo no lineal','UM')}
    for id,(name,unit) in names.items():
        control=soup.find(id=id)
        if codigo in {'FBA','AED'} and control and control.name=='input':control['aria-label']=name;control['data-unidad']=unit
    chart_names={'ds-hist':'Histograma de los valores ingresados: frecuencia por intervalo','ds-box':'Caja de los valores ingresados: mediana, cuartiles y extremos',
                 'mini-hist':'Ejemplo de histograma para comparar frecuencias','mini-box':'Ejemplo de cajas para comparar mediana y dispersión de tres grupos',
                 'mini-scatter':'Ejemplo de dispersión que muestra asociación positiva','mini-bar':'Ejemplo de barras para comparar categorías',
                 'mini-line':'Ejemplo de línea para describir una secuencia temporal','mini-heat':'Ejemplo de mapa de calor con intensidad codificada por color',
                 'corr-canvas':'Dispersión simulada: cambia la correlación con el control y consulta el valor calculado',
                 'norm-canvas':'Densidad normal y probabilidad acumulada hasta el punto de corte',
                 'reg-canvas':'Ajuste lineal y observaciones del ejemplo interactivo','km-canvas':'Asignación simulada de puntos a grupos K-means',
                 'cm-canvas':'Matriz de confusión del umbral seleccionado; los conteos se muestran junto al gráfico'}
    for canvas in soup.find_all('canvas'):
        canvas['role']='img'
        if codigo=='FBA' and canvas.get('id') in chart_names:canvas['aria-label']=chart_names[canvas['id']]
        canvas.string=canvas.get('aria-label','Gráfico del ejemplo; consultar los resultados numéricos adyacentes.')
    for a in soup.select('aside a[href="../README.md"]'):a['href']='../index.html'
    path.write_text(str(soup),encoding='utf-8')
    print(f'{codigo}: ruta, navegación y controles accesibles construidos.')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--curso',choices=CURSOS);parser.add_argument('--fuentes',action='store_true');args=parser.parse_args()
    for code in ([args.curso] if args.curso else CURSOS):
        if args.fuentes:preparar_fuentes(code)
        else:construir_guia(code)

if __name__=='__main__':main()
