"""Retira reglas de iconos que no se utilizan en un documento HTML autónomo."""
from pathlib import Path
import re

REGLA = re.compile(r'^\.bi-([a-z0-9-]+)::before[ \t]*\{[^{}\r\n]*\}[ \t]*(?:\r?\n|$)', re.MULTILINE)
ESTILO = re.compile(r'<style\b[^>]*>.*?</style>', re.DOTALL | re.IGNORECASE)


def depurar_iconos(ruta):
    ruta = Path(ruta)
    contenido = ruta.read_bytes().decode('utf-8')
    # Conservar también los nombres usados por JavaScript para estados interactivos.
    fuera_de_estilos = ESTILO.sub('', contenido)
    usados = set(re.findall(r'\bbi-([a-z0-9-]+)\b', fuera_de_estilos))

    def depurar_estilo(match):
        estilo = REGLA.sub(lambda regla: regla.group(0) if regla.group(1) in usados else '', match.group(0))
        return re.sub(r'^[ \t]*\r?\n', '', estilo, flags=re.MULTILINE)

    resultado = ESTILO.sub(depurar_estilo, contenido)
    if resultado != contenido:
        ruta.write_bytes(resultado.encode('utf-8'))


if __name__ == '__main__':
    import sys
    for argumento in sys.argv[1:]:
        depurar_iconos(argumento)
