# Mantener y verificar la colección

[Biblioteca](README.md) · [Informe de mejoras](docs/mejoras_publico_2026-10-09_analisis_codex.md)

## Fuentes y productos

| Recurso | Fuente que se modifica | Producto que se reconstruye |
|---|---|---|
| Objetivos y prácticas de los 28 módulos | [_transversal/rutas.py](_transversal/rutas.py) | `RUTA_APRENDIZAJE.md`, introducción de cada notebook, sección del manual y tarjetas de la guía |
| Fundamentos científicos, fórmulas y bibliografía | `material_propio/*_manual_cientifico.qmd` y `referencias.bib` de cada curso | Manual HTML y PDF |
| Guías de Fundamentos y Modelos Predictivos | HTML de la guía, fuera de los bloques `data-ba-generado` | El constructor reemplaza solamente sus bloques compartidos |
| Guía de Estadística | Manual QMD y `reproducibilidad/construir_guia.py` | HTML de la guía |
| Guía de Analítica Estratégica | `material_propio/guia_maestra_aed.template.html` | HTML de la guía |
| Presentación común | [_transversal/interfaz/](_transversal/interfaz/) | CSS y JavaScript incorporados en las publicaciones |
| Laboratorios | Celdas originales de los notebooks y funciones de `reproducibilidad/` | Notebooks con salidas y evidencia de ejecución |
| Actividades de transferencia y soluciones | [_transversal/practicas.py](_transversal/practicas.py) | Problema en cada notebook, sección del QMD y `PAUTA_DOCENTE.md` por curso |
| Tiempos de trabajo | `TIEMPOS` en [_transversal/rutas.py](_transversal/rutas.py) | Explicación, práctica y autonomía coherentes en las rutas |
| Libro FBA y controles BI | [_transversal/herramientas.py](_transversal/herramientas.py) | XLSX con fórmulas y caché calculado en Python; controles CSV de medidas M/DAX |
| Contratos y perfil de datos | [_transversal/datos/CATALOGO.md](_transversal/datos/CATALOGO.md), `perfilar.py` y generadores | Perfil de las columnas de 19 tablas analíticas |

No edite las salidas generadas para corregir un problema de origen. Las rutas se generan con `python _transversal/construir_interfaz.py --fuentes`; sus bloques se reemplazan de forma idempotente. El comando completo realiza este paso automáticamente.

## Entorno y verificación completa

Entorno de referencia: Python 3.12 y Quarto 1.10.18. Desde la raíz:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m ipykernel install --sys-prefix --name python3 --display-name "Business Analytics"
python -m playwright install chromium
# PowerShell: $env:BA_BROWSER_CHANNEL='chromium'
# bash: export BA_BROWSER_CHANNEL=chromium
python _transversal/construir_todo.py
```

Sin `BA_BROWSER_CHANNEL`, las comprobaciones usan Chrome instalado en el sistema. El kernel se registra dentro del entorno, sin cambiar el kernel del usuario. Los PDF usan las fuentes predeterminadas de Typst; no requieren una fuente comercial específica.

El constructor completo ejecuta los 28 notebooks, modifica controles para comprobar los cálculos, verifica las autoevaluaciones, reconstruye los cuatro manuales en HTML/PDF, genera las guías y comprueba cobertura, navegación e interfaz. Se detiene ante el primer error y deja su registro en `.cache-fba/verificacion/`.

Incluye diez pruebas en [_transversal/verificar_metodologia.py](_transversal/verificar_metodologia.py): cambio de prevalencia y categorías en PSI; particiones disjuntas; cuantil conformal finito; ajuste efectivo del escalador en cada pliegue; disponibilidad de resultados al emitir pronósticos; incidencias de BoldoNet; todas las alternativas de los 28 quizzes; y fórmulas/caché de ambos libros. Se pueden ejecutar por separado con `python _transversal/verificar_metodologia.py`.

Las prácticas BI incluyen M, DAX y controles numéricos para importación local. La comprobación automática ejecuta Python, no los motores nativos de Excel o Power BI. El caché del libro facilita la consulta sin perder fórmulas; quien lo adapte debe recalcular y conciliar en su herramienta.

```bash
python _transversal/construir_todo.py --solo-render
python _transversal/construir_todo.py --solo-verificar
```

`--solo-render` regenera manuales y guías, ejecuta el código de los QMD y valida el resultado; reutiliza las salidas guardadas de los notebooks. `--solo-verificar` revisa las publicaciones existentes sin reconstruirlas. Ninguna opción sustituye la ejecución completa cuando cambia código de un notebook.

## Evidencia y automatización

- Cada carpeta `reproducibilidad/` conserva los resultados de su ejecución y comprobaciones de contenido.
- [verificacion/interfaz.json](verificacion/interfaz.json) registra nueve páginas en cuatro anchos: 320, 390, 768 y 1440 píxeles. Comprueba proporciones y carga de figuras, controles con nombre, búsqueda, menú, teclado, modo clase y ampliación de imágenes.
- [verificacion/ultima_ejecucion.json](verificacion/ultima_ejecucion.json) indica el modo, las versiones y los resultados de la última orden global. Si dice `solo-render`, consulte además la evidencia de ejecución de notebooks por curso.
- [entorno_windows_py312.txt](verificacion/entorno_windows_py312.txt) conserva las versiones instaladas durante la revisión local; es evidencia de ese entorno, no una lista de instalación universal para otros sistemas.
- [El flujo de GitHub Actions](.github/workflows/validar.yml) reconstruye y valida con Windows y Chromium en cada cambio a `main` y solicitud de incorporación. Los registros se adjuntan como artefactos; un fallo debe corregirse antes de considerar validada la entrega.

La revisión local usa Chrome en Windows. El flujo remoto requiere una ejecución efectiva para confirmar ese entorno; no se infiere su resultado a partir de la prueba local. macOS y Linux no están certificados por esta evidencia. Tampoco constituye una certificación integral de accesibilidad ni una revisión académica de pares.

## Actualizar y publicar

1. Corregir la fuente y explicar el caso que motiva el cambio. Si afecta el razonamiento, revisar el ejemplo, sus supuestos y su criterio de logro en los tres formatos.
2. Revisar las matrices de cobertura y conservar las distinciones entre contenido nuclear y profundización.
3. Ejecutar la construcción necesaria y comprobar las capturas, además de los resultados automáticos.
4. Ejecutar `python _transversal/verificar_publico.py`, revisar el diff y comprobar autoría, licencias, datos y ausencia de rutas personales.
5. Publicar el commit, revisar el resultado de Actions y comprobar la portada, guías y descargas en GitHub Pages. Una subida a GitHub y una publicación de Pages son comprobaciones diferentes.

## Relación con otras ediciones

Esta colección tiene casos ficticios, estructura y licencias propias. La sincronización es editorial: trasladar una mejora de método o un cálculo, adaptar nombres y recursos, conservar su procedencia y reconstruir. No reemplazar directorios completos desde otra edición. Cada cambio debe tener una fuente identificable, una comprobación y un commit; evita mantener correcciones diferentes dentro de PDF, HTML y notebook.

Los ejemplos regulatorios deben incluir jurisdicción, fuente y fecha de vigencia. La documentación pública de Estados Unidos se usa como referencia metodológica contextualizada, sin presentarla como obligación local.
