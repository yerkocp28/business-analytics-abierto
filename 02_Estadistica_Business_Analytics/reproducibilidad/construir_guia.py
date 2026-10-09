"""Guía autónoma: capítulos de la fuente QMD renderizada y simuladores con datos locales."""
from pathlib import Path
import json, html, os
from urllib.parse import urlsplit, urlunsplit, unquote, quote
import numpy as np
from scipy import stats
from bs4 import BeautifulSoup
from eba_recursos import CURSO, pedidos, serie, anova, welch

def main():
    material=CURSO/'material_propio';soup=BeautifulSoup((material/'EBA_manual_cientifico.html').read_text(encoding='utf-8'),'html.parser')
    sections=soup.select('main > section.level1');assert len(sections)==16,len(sections)
    nav=[]
    for s in sections:
        heading=s.find(['h1','h2']);nav.append(f'<a href="#{s["id"]}">{html.escape(heading.get_text(" ",strip=True))}</a>')
        for x in s.select('.anchorjs-link'):x.decompose()
        # El manual vive un nivel más abajo. Reubicar cualquier recurso local,
        # incluidos directorios nuevos, conservando consultas y anclas.
        for elemento in s.select('[href], [src]'):
            for atributo in ['href', 'src']:
                if not elemento.has_attr(atributo):
                    continue
                u = urlsplit(elemento[atributo])
                if u.scheme or u.netloc or not u.path:
                    continue
                destino = (material / unquote(u.path)).resolve()
                ruta = Path(os.path.relpath(destino, CURSO)).as_posix()
                elemento[atributo] = urlunsplit(('', '', quote(ruta, safe='/'), u.query, u.fragment))
    df=pedidos();a=df.loc[df.campana.eq('A'),'tiempo_min'];b=df.loc[df.campana.eq('B'),'tiempo_min']
    payload={'pedidos':df.to_dict('records'),'serie':serie().tolist(),
             'tcrit':{str(n):{str(c):float(stats.t.ppf((1+c)/2,n-1)) for c in [.9,.95,.99]} for n in range(20,601,20)},
             'anova':{canal:anova(df if canal=='Todos' else df[df.canal.eq(canal)]) for canal in ['Todos','Web','Tienda']},
             'welch':welch(b,a)}
    def select(id,label,options):return f'<label for="{id}">{label}<select id="{id}">'+''.join(f'<option value="{v}">{t}</option>' for v,t in options)+'</select></label>'
    def slider(id,label,value,min,max,step):return f'<label for="{id}">{label} <output id="{id}-v">{value}</output><input id="{id}" type="range" value="{value}" min="{min}" max="{max}" step="{step}"></label>'
    def panel(id,title,controls,extra=''):return f'<div class="laboratorio" id="lab-{id}"><span class="etiqueta">EXPERIMENTAR · SIN CONEXIÓN</span><h3>{title}</h3><div class="controles">{controls}</div><div id="{id}-resultado" role="status" aria-live="polite"></div>{extra}</div>'
    panels={
      'sec-problema':panel('metodo','Del objetivo al método',select('objetivo','Objetivo',[('describir','Describir'),('medias','Comparar dos medias'),('proporcion','Estimar una proporción'),('relacion','Evaluar relación'),('futuro','Pronosticar')])+select('diseno','Diseño de comparación',[('independiente','Grupos independientes'),('pareado','Mismas unidades antes/después')])),
      'sec-descripcion':panel('resumen','Describir el mismo conjunto de pedidos',select('resumen-canal','Canal',[(v,v) for v in ['Todos','Web','Tienda']])) ,
      'sec-muestreo':panel('muestra','Planificar respuestas completas',slider('margen','Margen absoluto',.05,.02,.15,.01)+slider('respuesta','Respuesta esperada',.8,.4,1,.1)),
      'sec-probabilidad':panel('eventos','Comprobar una probabilidad condicionada',select('evento-campana','Campaña',[(v,v) for v in ['A','B','C']])) ,
      'sec-bayes':panel('bayes','Una alerta no es una certeza',slider('prevalencia','Prevalencia',.02,.001,.2,.001)+slider('sensibilidad','Sensibilidad',.9,.5,.99,.01)+slider('especificidad','Especificidad',.95,.8,.999,.001)),
      'sec-distribuciones':panel('binomial','Probabilidad de cumplir una meta',slider('bin-n','Ensayos independientes',20,5,50,1)+slider('bin-p','Probabilidad de éxito',.8,.05,.95,.05)+slider('bin-k','Éxitos mínimos',18,0,50,1)),
      'sec-intervalos':panel('intervalo','Cambiar n y confianza',slider('ic-n','Primeros n pedidos de la muestra',100,20,600,20)+select('ic-nivel','Confianza',[(str(v),f'{v:.0%}') for v in [.9,.95,.99]]),'<p>Muestra anidada para explorar precisión; no repetir cortes hasta obtener el resultado deseado. IC t de superpoblación.</p>'),
      'sec-regresion':panel('relacion','Pearson frente a un dibujo',select('relacion-canal','Canal',[(v,v) for v in ['Todos','Web','Tienda']]),'<canvas id="dispersion" width="700" height="280" aria-label="Dispersión de ticket en miles de UM y tiempo en minutos"></canvas><p>Asociación observacional; los puntos no prueban causalidad.</p>'),
      'sec-contrastes':panel('decision','Traducir B−A a beneficio',slider('costo','Costo adicional B (UM/pedido)',.5,0,2,.1)+slider('valor','Valor del minuto (UM)',.2,.05,.5,.05)),
      'sec-anova':panel('anova','Contraste global por población',select('anova-canal','Canal',[(v,v) for v in ['Todos','Web','Tienda']]),'<p>Exploración por segmento, sin ajuste por búsqueda de segmentos. Eta² es descriptivo; ANOVA global no identifica pares.</p>'),
      'sec-series':panel('suavizamiento','Reacción del nivel ante ruido',slider('alpha','Alfa SES',.3,.05,.95,.05),'<canvas id="serie" width="700" height="280" aria-label="Demanda y nivel suavizado en 36 meses de desarrollo"></canvas><p>SES inicializado en la primera observación; ejercicio pedagógico distinto de la inicialización estimada del notebook.</p>'),
      'sec-visualizacion':panel('dashboard','Un filtro, una población y denominadores visibles',select('dash-canal','Canal',[(v,v) for v in ['Todos','Web','Tienda']])+select('dash-campana','Campaña',[(v,v) for v in ['Todas','A','B','C']])),
    }
    quizzes=[('sec-problema','¿Qué se define primero?','El algoritmo más complejo','La decisión, población y estimando','La pregunta y el diseño determinan el método.'),
      ('sec-muestreo','¿Mayor n corrige un marco incompleto?','Siempre','No','Tamaño y representatividad son propiedades distintas.'),
      ('sec-bayes','¿P(+|riesgo) equivale a P(riesgo|+)?','Sí','No','El posterior incorpora prevalencia y falsos positivos.'),
      ('sec-intervalos','¿El IC de la media contiene 95% de pedidos?','Sí','No','Describe incertidumbre del parámetro, no dispersión individual.'),
      ('sec-regresion','¿R² prueba causalidad?','Sí','No','Causalidad requiere diseño y supuestos adicionales.'),
      ('sec-anova','¿ANOVA identifica todos los pares distintos?','Sí','No','El contraste global se complementa con contrastes y multiplicidad.'),
      ('sec-series','¿La prueba sirve para elegir el modelo?','Sí','No','Elegir con prueba elimina su independencia evaluativa.'),
      ('sec-comunicacion','¿p>.05 prueba que no hay deterioro?','Sí','No','No inferioridad requiere margen y precisión adecuados.')]
    for sid,panelhtml in panels.items():soup.find(id=sid).append(BeautifulSoup(panelhtml,'html.parser'))
    for i,(sid,q,wrong,right,why) in enumerate(quizzes,1):
        s=f'<fieldset class="quiz" id="quiz-{i}"><legend>{html.escape(q)}</legend><label><input type="radio" name="q{i}" value="0">{wrong}</label><label><input type="radio" name="q{i}" value="1">{right}</label><button type="button" data-quiz="{i}" data-explicacion="{html.escape(why,quote=True)}">Comprobar</button><p role="status" aria-live="polite"></p></fieldset>'
        soup.find(id=sid).append(BeautifulSoup(s,'html.parser'))
    notebooks=''.join(f'<a class="recurso" href="notebooks/{p.name}">{html.escape(p.stem.replace("EBA_","",1).replace("_"," "))}</a>' for p in sorted((CURSO/'notebooks').glob('*.ipynb')))
    css=(material/'guia.css').read_text(encoding='utf-8');js=(material/'guia.js').read_text(encoding='utf-8')
    result=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Estadística Aplicada · Guía maestra</title><style>{css}</style></head><body>
<a class="saltar" href="#contenido">Saltar al contenido</a><aside><a class="marca" href="../README.md">BA / BIBLIOTECA DOCENTE</a><h2>Estadística aplicada</h2><label for="buscar">Buscar capítulos</label><input id="buscar" type="search" placeholder="Bayes, ANOVA, intervalos…"><nav aria-label="Capítulos">{''.join(nav)}</nav><a href="#laboratorios">Ocho laboratorios</a><a href="README.md">Índice del curso</a></aside>
<main id="contenido"><header><p class="etiqueta">BUSINESS ANALYTICS · GUÍA MAESTRA · EDICIÓN 2026</p><h1>De los datos a una conclusión defendible.</h1><p class="bajada">Método, incertidumbre y decisiones. Un recorrido para entender, calcular, experimentar y explicar.</p><div class="fichas"><span>3 resultados de aprendizaje</span><span>17 contenidos mínimos</span><span>12 experimentos</span><span>8 notebooks</span></div><p>ComercioSur es un caso simulado. Lectura y experimentos sin conexión; notebooks con kernel activo. La ruta de doce semanas es una propuesta docente ajustable.</p><div class="recursos"><a class="recurso" href="material_propio/EBA_manual_cientifico.pdf">Manual PDF</a><a class="recurso" href="material_propio/EBA_manual_cientifico.qmd">Fuente QMD</a><a class="recurso" href="COBERTURA.md">Cobertura verificable</a><a class="recurso" href="material_propio/EBA_tablero_excel.xlsx">Libro Excel</a></div></header>
<section id="laboratorios"><h2>Aprender haciendo</h2><p>Ejecutar → cambiar una condición → interpretar → declarar el límite. La misma pregunta conecta guía, manual y laboratorio.</p><div class="recursos">{notebooks}</div></section>
{''.join(str(s) for s in sections)}<p id="sin-resultados" hidden>No hay capítulos para esa búsqueda.</p><footer>Material propio · Yerko Carreño Pérez · CC BY-NC-SA 4.0 · Verificación técnica documentada en reproducibilidad.</footer></main>
<script id="datos-eba" type="application/json">{json.dumps(payload,ensure_ascii=False,allow_nan=False)}</script><script>{js}</script></body></html>'''
    (CURSO/'guia_maestra_eba.html').write_text(result,encoding='utf-8');print('Guía generada: 16 capítulos, 12 experimentos y 8 autoevaluaciones.')

if __name__=='__main__':main()
