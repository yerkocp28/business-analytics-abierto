"""Autoevaluaciones formativas locales, con opciones en orden reproducible y variable."""
import hashlib
import html
import random
import ipywidgets as widgets
from IPython.display import display


def pregunta(enunciado, opciones, correcta, explicacion, mostrar=True):
    """La clave identifica la respuesta original; su posición visible no es fija."""
    if len(opciones) < 2 or len(set(opciones)) != len(opciones):
        raise ValueError('Se necesitan al menos dos alternativas distintas.')
    if not 0 <= correcta < len(opciones):
        raise ValueError('La respuesta correcta debe pertenecer a las alternativas.')
    alternativas = [(texto, f'respuesta_{i}') for i, texto in enumerate(opciones)]
    semilla = int.from_bytes(hashlib.sha256(enunciado.encode('utf-8')).digest()[:8], 'big')
    random.Random(semilla).shuffle(alternativas)
    clave = f'respuesta_{correcta}'
    elegir = widgets.RadioButtons(options=alternativas, value=None, layout={'width': '95%'})
    boton = widgets.Button(description='Comprobar', button_style='info')
    salida = widgets.HTML('<p role="status">Selecciona una respuesta.</p>')

    def revisar(_):
        if elegir.value is None:
            mensaje = 'Selecciona una respuesta para recibir retroalimentación.'
        else:
            mensaje = ('Correcto. ' if elegir.value == clave else 'Revisa tu respuesta. ') + explicacion
        salida.value = '<p role="status" aria-live="polite">' + html.escape(mensaje) + '</p>'

    boton.on_click(revisar)
    caja = widgets.VBox([widgets.HTML('<b>' + html.escape(enunciado) + '</b>'), elegir, boton, salida])
    caja._ba_clave = clave  # Identificador para comprobar retroalimentación; no es una evaluación sumativa.
    if mostrar:
        display(caja)
    return caja
