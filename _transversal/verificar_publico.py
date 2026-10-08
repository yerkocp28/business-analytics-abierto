"""Controles antes de publicar: contenido propio, metadatos neutros, enlaces y notebooks ejecutados.

Uso, desde la raíz del repositorio:  python _transversal/verificar_publico.py
Termina con código 1 si encuentra un problema.
"""
import re
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlparse

import nbformat

RAIZ = Path(__file__).resolve().parents[1]
IGNORAR = {".git", ".venv", ".cache-fba", ".quarto", "__pycache__", ".ipynb_checkpoints"}
AUTORES = {"Yerko Carreño Pérez", "Colección abierta de Business Analytics", "openpyxl", ""}
# Referencias que no corresponden a material abierto: documentos institucionales y rutas de un equipo local.
PROHIBIDO = re.compile(r"Universidad Aut[oó]noma|[Ss]yllabus|\bAPUS\d*\b|apuntes institucionales|programa recibido"
                       r"|[A-Za-z]:\\{1,2}Users\\{1,2}|/Users/[A-Za-z]+/|Vespertino TECH")
TEXTO = {".md", ".qmd", ".py", ".ipynb", ".html", ".csv", ".js", ".css", ".bib", ".cff", ".txt"}
problemas = []


def archivos():
    for p in RAIZ.rglob("*"):
        if p.is_file() and not (set(p.relative_to(RAIZ).parts) & IGNORAR):
            yield p


def texto_visible(p):
    t = p.read_text(encoding="utf-8")
    # Las imágenes incrustadas en base64 producen coincidencias espurias.
    return re.sub(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=\\n]+|\"image/png\": \"[^\"]*\"", "", t)


for p in archivos():
    rel = p.relative_to(RAIZ).as_posix()
    if p.suffix in TEXTO and p.name != "verificar_publico.py":
        for m in PROHIBIDO.finditer(texto_visible(p)):
            problemas.append(f"Referencia no abierta en {rel}: {m.group(0)!r}")
    if p.suffix in {".xlsx", ".docx", ".pptx"}:
        core = zipfile.ZipFile(p).read("docProps/core.xml").decode("utf-8", "ignore")
        for autor in re.findall(r"<(?:dc:creator|cp:lastModifiedBy)>([^<]*)<", core):
            if autor not in AUTORES:
                problemas.append(f"Autor no esperado en metadatos de {rel}: {autor!r}")
    if p.suffix == ".pdf":
        import pymupdf
        autor = (pymupdf.open(p).metadata or {}).get("author") or ""
        if autor not in AUTORES:
            problemas.append(f"Autor no esperado en metadatos de {rel}: {autor!r}")
    if p.suffix == ".md":
        for m in re.finditer(r"\]\(<?([^)>\s]+)>?\)", p.read_text(encoding="utf-8")):
            u = urlparse(m.group(1))
            if u.scheme or m.group(1).startswith(("#", "mailto")):
                continue
            if not (p.parent / unquote(u.path)).exists():
                problemas.append(f"Enlace roto en {rel}: {m.group(1)}")
    if p.suffix == ".ipynb" and "notebooks" in p.parts:
        nb = nbformat.read(p, 4)
        codigo = [c for c in nb.cells if c.cell_type == "code"]
        if any(c.execution_count is None for c in codigo):
            problemas.append(f"Notebook sin ejecutar completo: {rel}")
        if any(o.get("output_type") == "error" for c in codigo for o in c.get("outputs", [])):
            problemas.append(f"Notebook con salida de error: {rel}")

for linea in problemas:
    print("✗", linea)
print("Verificación del repositorio abierto:", "OK" if not problemas else f"{len(problemas)} problemas")
sys.exit(1 if problemas else 0)
