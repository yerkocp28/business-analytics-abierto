"""Regresión de rutas, aprendizaje e interfaz de las publicaciones finales."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from datetime import datetime, timezone
import json
import os
import re
import nbformat
import pymupdf as fitz
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from construir_interfaz import recursos
from rutas import CURSOS

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = RAIZ / 'verificacion'
SALIDA.mkdir(exist_ok=True)
(SALIDA / 'capturas').mkdir(exist_ok=True)


def exigir(condicion, mensaje):
    if not condicion:
        raise AssertionError(mensaje)


def verificar_rutas(paginas):
    total = 0
    cache = {}
    for origen in paginas:
        soup = BeautifulSoup(origen.read_text(encoding='utf-8'), 'html.parser')
        for elemento in soup.select('[href], [src]'):
            url = elemento.get('href', elemento.get('src', ''))
            partes = urlsplit(url)
            if partes.scheme or partes.netloc or not url or url.startswith('javascript:'):
                continue
            destino = (origen.parent / unquote(partes.path)).resolve() if partes.path else origen
            exigir(destino.is_relative_to(RAIZ), f'Ruta fuera del repositorio: {origen.name}: {url}')
            exigir(destino.exists(), f'Ruta inexistente: {origen.name}: {url}')
            if partes.fragment and destino.suffix == '.html':
                if destino not in cache:
                    cache[destino] = BeautifulSoup(destino.read_text(encoding='utf-8'), 'html.parser')
                exigir(cache[destino].find(id=unquote(partes.fragment)) is not None,
                       f'Ancla inexistente: {origen.name}: {url}')
            total += 1
    return total


def verificar_aprendizaje():
    total = 0
    for codigo, curso in CURSOS.items():
        carpeta, modulos = recursos(codigo)
        guia = BeautifulSoup((carpeta / curso['guia']).read_text(encoding='utf-8'), 'html.parser')
        qmd = (carpeta / 'material_propio' / f'{codigo}_manual_cientifico.qmd').read_text(encoding='utf-8')
        ruta = (carpeta / 'RUTA_APRENDIZAJE.md').read_text(encoding='utf-8')
        for modulo in modulos:
            nb = nbformat.read(carpeta / 'notebooks' / modulo['notebook'], as_version=4)
            contratos = [c for c in nb.cells if 'ruta-aprendizaje' in c.metadata.get('tags', [])]
            exigir(len(contratos) == 1, f'{codigo}: contrato ausente o duplicado')
            tarjeta = guia.find(id=f'modulo-{modulo["numero"]:02}')
            exigir(tarjeta is not None, f'{codigo}: falta módulo en guía')
            for campo in ('objetivo', 'logro'):
                for texto in (contratos[0].source, qmd, ruta, tarjeta.get_text(' ', strip=True)):
                    exigir(modulo[campo] in texto, f'{codigo}: divergencia del {campo} en módulo {modulo["numero"]}')
            total += 1
    return total


def verificar_pdf():
    salida = []
    for codigo, curso in CURSOS.items():
        pdf = RAIZ / curso['carpeta'] / 'material_propio' / f'{codigo}_manual_cientifico.pdf'
        with fitz.open(pdf) as doc:
            exigir(len(doc) >= 10, f'{codigo}: PDF incompleto')
            fuera = []
            for numero, pagina in enumerate(doc, 1):
                for palabra in pagina.get_text('words'):
                    x0, y0, x1, y1 = palabra[:4]
                    if x0 < -1 or y0 < -1 or x1 > pagina.rect.width + 1 or y1 > pagina.rect.height + 1:
                        fuera.append((numero, palabra[4]))
            exigir(not fuera, f'{codigo}: texto fuera de página: {fuera[:5]}')
            texto = ''.join(p.get_text() for p in doc)
            exigir('Objetivos y evidencias' in texto, f'{codigo}: PDF sin la ruta actualizada')
            salida.append({'curso': codigo, 'paginas': len(doc), 'texto_fuera_pagina': len(fuera)})
    return salida


MEDICIONES = """() => {
 const visibles = el => !!(el.getClientRects().length && getComputedStyle(el).visibility !== 'hidden');
 const imagenes = [...document.querySelectorAll('main img')].filter(visibles).map(el => {
   const r=el.getBoundingClientRect();
   return {alt:el.getAttribute('alt'),carga:el.complete&&el.naturalWidth>0,
     errorRatio:Math.abs((r.width/r.height)/(el.naturalWidth/el.naturalHeight)-1),
     dentro:r.left>=-1&&r.right<=innerWidth+1};
 });
 const sinNombre=[...document.querySelectorAll('input:not([type=hidden]),select,textarea,button')]
   .filter(visibles).filter(el=>!(el.getAttribute('aria-label')||el.getAttribute('aria-labelledby')||
     el.labels?.length||el.title||el.textContent.trim()||(['submit','button'].includes(el.type)&&el.value)))
   .map(el=>el.id||el.outerHTML.slice(0,120));
 return {desborde:Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth,
         imagenes,sinNombre};
}"""


def verificar_navegador(paginas):
    resultados = []
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(channel=os.environ.get('BA_BROWSER_CHANNEL', 'chrome'), headless=True)
        contexto = navegador.new_context(viewport={'width': 1440, 'height': 950}, offline=True)
        pagina = contexto.new_page()
        errores = []
        pagina.on('pageerror', lambda error: errores.append(str(error)))
        for archivo in paginas:
            errores.clear()
            pagina.goto(archivo.as_uri(), wait_until='load')
            pagina.wait_for_timeout(150)
            es_guia = archivo.name.startswith('guia_maestra')
            es_manual = archivo.name.endswith('_manual_cientifico.html')
            for ancho in (320, 390, 768, 1440):
                pagina.set_viewport_size({'width': ancho, 'height': 950})
                pagina.wait_for_timeout(100)
                medidas = pagina.evaluate(MEDICIONES)
                exigir(medidas['desborde'] <= 1, f'{archivo.name}/{ancho}: desborde {medidas["desborde"]}')
                exigir(not medidas['sinNombre'], f'{archivo.name}: controles sin nombre: {medidas["sinNombre"]}')
                for img in medidas['imagenes']:
                    exigir(img['alt'] and img['carga'] and img['dentro'] and img['errorRatio'] < .015,
                           f'{archivo.name}/{ancho}: figura recortada, deformada o sin descripción: {img}')
                resultados.append({'pagina': archivo.relative_to(RAIZ).as_posix(), 'ancho': ancho,
                                   'desborde_px': medidas['desborde'], 'figuras': len(medidas['imagenes'])})
            if es_guia:
                pagina.set_viewport_size({'width': 390, 'height': 844})
                menu = pagina.locator('#ba-menu')
                exigir(menu.get_attribute('aria-expanded') == 'false', 'Índice móvil debe comenzar cerrado')
                menu.click()
                exigir(menu.get_attribute('aria-expanded') == 'true', 'Índice no abre')
                buscar = pagina.locator('#ba-buscar, #buscar')
                buscar.fill('decision')
                pagina.wait_for_timeout(100)
                exigir(pagina.locator('#ba-resultados a').count() > 0, 'Búsqueda sin resultados para decisión')
                pagina.locator('#ba-resultados a').first.click()
                exigir(buscar.input_value() == '', 'La navegación no restablece la búsqueda')
                exigir(menu.get_attribute('aria-expanded') == 'false', 'Navegar debe cerrar el índice móvil')
                menu.click()
                pagina.keyboard.press('Escape')
                exigir(menu.get_attribute('aria-expanded') == 'false', 'Escape no cierra índice')
                pagina.locator('#clase-toggle').check()
                exigir(pagina.locator('body').evaluate('(el)=>el.classList.contains("ba-clase")'), 'Modo clase inactivo')
                exigir(pagina.evaluate(MEDICIONES)['desborde'] <= 1, 'Desborde en modo clase')
                pagina.locator('#clase-toggle').uncheck()
                if 'mpn' in archivo.name:
                    pagina.locator('[data-ba-ruta="5"]').click()
                    exigir(pagina.locator('[data-ba-calendario="5"]').is_visible(), 'Ruta intensiva no visible')
                    exigir(not pagina.locator('[data-ba-calendario="12"]').is_visible(), 'Ruta extendida no se oculta')
                    pagina.locator('[data-ba-ruta="12"]').click()
                pagina.evaluate("scrollTo({top:0,behavior:'instant'})")
                pagina.screenshot(path=str(SALIDA / 'capturas' / f'{archivo.stem}_movil.png'))
            if es_manual:
                pagina.set_viewport_size({'width': 390, 'height': 844})
                boton = pagina.get_by_role('button', name=re.compile('Ampliar figura')).first
                exigir(boton.count() == 1, 'Falta ampliación de figuras')
                boton.click()
                exigir(pagina.locator('dialog[open]').count() == 1, 'Figura no abre')
                pagina.keyboard.press('Escape')
                exigir(pagina.locator('dialog[open]').count() == 0, 'Escape no cierra la figura')
                exigir(boton.evaluate('(el)=>el===document.activeElement'), 'No se restablece el foco')
                pagina.screenshot(path=str(SALIDA / 'capturas' / f'{archivo.stem}_movil.png'))
            exigir(not errores, f'{archivo.name}: errores JavaScript: {errores}')
        navegador.close()
    return resultados


def main():
    paginas = [RAIZ / 'index.html']
    for codigo, curso in CURSOS.items():
        carpeta = RAIZ / curso['carpeta']
        paginas.extend([carpeta / curso['guia'], carpeta / 'material_propio' / f'{codigo}_manual_cientifico.html'])
    resultado = {'fecha_utc': datetime.now(timezone.utc).isoformat(),
                 'enlaces_locales_y_anclas': verificar_rutas(paginas),
                 'modulos_coherentes': verificar_aprendizaje(),
                 'pdf': verificar_pdf(), 'pantallas': verificar_navegador(paginas),
                 'alcance': 'Comprobación funcional y accesibilidad básica; no certifica conformidad WCAG completa.'}
    (SALIDA / 'interfaz.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
