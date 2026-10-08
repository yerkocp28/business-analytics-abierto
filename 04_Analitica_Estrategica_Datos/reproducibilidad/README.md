# Reproducción y pruebas · Analítica Estratégica de Datos

[Volver al curso](../README.md)

## Entorno para usar los notebooks

Desde la raíz del repositorio, con Python 3.12:

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows · en macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Abra Jupyter desde la raíz del repositorio o desde una subcarpeta: los notebooks ubican los datos en `_transversal/datos`.

## Reconstruir y verificar la edición

Requiere además `pip install -r requirements-dev.txt`, `playwright install chrome` y [Quarto CLI](https://quarto.org).

```bash
python 04_Analitica_Estrategica_Datos/reproducibilidad/construir.py
```

| Script | Función |
|---|---|
| [construir.py](construir.py) | Reconstruye la edición completa; con `--solo-render` solo regenera el manual |
| [construir_guia.py](construir_guia.py) | Genera la guía HTML a partir de su plantilla o del manual |
| [ejecutar_notebooks.py](ejecutar_notebooks.py) | Ejecuta cada notebook en un kernel nuevo, prueba controles y autoevaluaciones y guarda las salidas |
| [verificar_edicion.py](verificar_edicion.py) | Verifica notebooks, guía (en Chrome, sin conexión), manual y matriz de cobertura |
| [aed_recursos.py](aed_recursos.py) | Rutas, carga y contratos de datos, utilidades compartidas por los notebooks |

## Evidencia

[ejecucion_notebooks.json](ejecucion_notebooks.json), [verificacion_edicion.json](verificacion_edicion.json) y la carpeta [capturas](capturas/) registran la última verificación. Validado en Windows con Python 3.12.13 y Quarto 1.10.18; no se ha probado en macOS ni Linux. Las pruebas técnicas no miden aprendizaje.
