# Business Analytics · material docente abierto

Material para enseñar y aprender **Business Analytics** en pregrado, con profundizaciones para postgrado. Cubre cuatro cursos encadenados: desde la pregunta de negocio y los datos hasta la inferencia, los modelos predictivos y las decisiones bajo restricciones.

**Sitio web:** [yerkocp28.github.io/business-analytics-abierto](https://yerkocp28.github.io/business-analytics-abierto/) — guías y manuales listos para abrir en el navegador.

Cada curso tiene el mismo formato:

- **Guía maestra interactiva** (HTML): capítulos, simuladores y autoevaluación. Funciona sin conexión a internet.
- **Manual científico** (PDF y HTML, con fuente Quarto): fundamentos, fórmulas, supuestos, ejercicios resueltos y bibliografía.
- **Notebooks de laboratorio** (Jupyter): cálculos que se pueden modificar, controles interactivos y una autoevaluación por notebook.
- **Matriz de cobertura**: vincula cada criterio de evaluación con un capítulo, una sección del manual y una actividad del notebook.
- **Reproducibilidad**: scripts que reconstruyen el material y comprueban sus resultados.

| Curso | Guía | Manual | Notebooks | Cobertura |
|---|---|---|--:|---|
| [Fundamentos de Business Analytics](01_Fundamentos_Business_Analytics/README.md) | [Abrir](01_Fundamentos_Business_Analytics/guia_maestra_ba.html) | [PDF](01_Fundamentos_Business_Analytics/material_propio/FBA_manual_cientifico.pdf) | 5 | [15 criterios](01_Fundamentos_Business_Analytics/COBERTURA.md) |
| [Estadística Aplicada a Business Analytics](02_Estadistica_Business_Analytics/README.md) | [Abrir](02_Estadistica_Business_Analytics/guia_maestra_eba.html) | [PDF](02_Estadistica_Business_Analytics/material_propio/EBA_manual_cientifico.pdf) | 8 | [12 criterios y 17 contenidos](02_Estadistica_Business_Analytics/COBERTURA.md) |
| [Modelos Predictivos para los Negocios](03_Modelos_Predictivos_Negocios/README.md) | [Abrir](03_Modelos_Predictivos_Negocios/guia_maestra_mpn.html) | [PDF](03_Modelos_Predictivos_Negocios/material_propio/MPN_manual_cientifico.pdf) | 7 | [15 criterios](03_Modelos_Predictivos_Negocios/COBERTURA.md) |
| [Analítica Estratégica de Datos](04_Analitica_Estrategica_Datos/README.md) | [Abrir](04_Analitica_Estrategica_Datos/guia_maestra_aed.html) | [PDF](04_Analitica_Estrategica_Datos/material_propio/AED_manual_cientifico.pdf) | 8 | [13 criterios](04_Analitica_Estrategica_Datos/COBERTURA.md) |

## Cómo empezar

**Estudiantes.** Abra la guía de su curso desde el [sitio web](https://yerkocp28.github.io/business-analytics-abierto/), o descargue el repositorio (botón *Code › Download ZIP*) para usarla sin conexión. Para los laboratorios, prepare el entorno de Python como se indica abajo y ejecute las celdas en orden.

**Docentes.** Cada guía trae una ruta de doce semanas con objetivos, actividades de 90 minutos, preguntas gatillantes y recursos por semana; Modelos Predictivos incluye además una [ruta intensiva de cinco semanas](03_Modelos_Predictivos_Negocios/RUTA_INTENSIVA.md). Las rúbricas son formativas: cada curso define sus ponderaciones y reglas de evaluación.

## Entorno para los notebooks

Desde la raíz del repositorio, con Python 3.12:

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows · en macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Abra Jupyter desde la raíz del repositorio o desde una subcarpeta: los notebooks ubican los datos en `_transversal/datos`. Para reconstruir manuales y guías y repetir las verificaciones, vea la carpeta `reproducibilidad/` de cada curso. Antes de publicar cambios, ejecute `python _transversal/verificar_publico.py`: comprueba enlaces, notebooks ejecutados, metadatos y que no se incluya material institucional.

## Datos

Todas las empresas son ficticias y todos los datos son simulados con un [generador documentado](_transversal/datos/generar_datos.py) de semilla fija: FinCordillera (banca), QuillayMarket (retail), PulpaLenga (celulosa), CasaPeumo (hogar), BoldoNet (servicio digital) y ComercioSur (comercio). Algunos conjuntos traen defectos de calidad deliberados para practicar limpieza. Consulte el [diccionario de datos](_transversal/datos/README.md).

## Licencia y forma de citar

- **Textos, guías, manuales, notebooks y datos:** [CC BY-NC-SA 4.0](LICENSE). Puede copiarlos y adaptarlos con fines no comerciales, citando la autoría y compartiendo sus adaptaciones con la misma licencia.
- **Código** (scripts de `reproducibilidad/`, generador de datos y funciones auxiliares): [MIT](LICENSE-CODE).

Cita sugerida: Carreño Pérez, Y. (2026). *Business Analytics: material docente abierto* [Material docente]. https://github.com/yerkocp28/business-analytics-abierto. También puede usar [CITATION.cff](CITATION.cff).

## Autoría y alcance

Elaborado por **Yerko Carreño Pérez**. Los cálculos, simuladores y enlaces se comprueban automáticamente (ver `reproducibilidad/`). La revisión académica de pares sigue en curso: si encuentra un error, abra un *issue*.

Es material independiente: no representa a ninguna institución ni reemplaza los programas oficiales de un curso.
