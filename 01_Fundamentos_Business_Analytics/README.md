# Fundamentos de Business Analytics

[Volver al inicio](../README.md) · [Cobertura curricular](COBERTURA.md) · [Reproducción y pruebas](reproducibilidad/README.md)

**Edición 2026.** Tres unidades —conceptos, análisis visual y herramientas— con profundizaciones de probabilidad y modelos. Los 15 criterios de evaluación se vinculan con actividades concretas. Los casos son ficticios y sus datos, simulados.

## Material principal para clase

| Formato | Recurso | Uso |
|---|---|---|
| HTML interactivo | [Guía maestra](guia_maestra_ba.html) | Simuladores, filtros, sensibilidad y autoevaluación sin conexión |
| PDF, 19 páginas | [Manual científico](material_propio/FBA_manual_cientifico.pdf) | Fundamentos, ecuaciones, supuestos, casos y bibliografía |
| Quarto | [Fuente QMD](material_propio/FBA_manual_cientifico.qmd) | Editar y regenerar el PDF y su HTML de lectura |
| HTML de lectura | [Manual científico navegable](material_propio/FBA_manual_cientifico.html) | Buscar, consultar fórmulas y abrir referencias |

## Laboratorios interactivos completos

| Notebook | Alcance | Nivel |
|---|---|---|
| [01 · Negocio y datos](notebooks/FBA_01_negocio_datos.ipynb) | BA, BI, Big Data, decisión, calidad, CRISP-DM y ética | Núcleo U1 / RA1 |
| [02 · Exploración visual](notebooks/FBA_02_exploracion_visual.ipynb) | Descripción, gráficos, asociación, mezcla y comunicación | Núcleo U2 / RA2 |
| [03 · Herramientas y caso integrador](notebooks/FBA_03_herramientas_caso_integrador.ipynb) | Excel/pandas, filtros, tablas, búsquedas, SQL, sensibilidad e informe | Núcleo U3 / RA3 |
| [04 · Probabilidad y simulación](notebooks/FBA_04_probabilidad_simulacion.ipynb) | Bayes, distribuciones, normal y medias muestrales | Profundización |
| [05 · Modelos y evaluación](notebooks/FBA_05_modelos_evaluacion.ipynb) | Regresión, clasificación, validación, umbral, métricas y clustering | Profundización |

Descargue el repositorio completo y ejecute los notebooks con el entorno documentado. Los controles requieren kernel activo; las salidas guardadas permiten lectura previa. Los datos de QuillayMarket y FinCordillera son simulados y están en `_transversal/datos`. Los ejemplos simulados y los supuestos económicos se identifican expresamente.

## Validación

Cada notebook se ejecuta en un kernel nuevo y se prueban sus controles interactivos y su autoevaluación. La guía se verifica en Chrome sin conexión: sus cálculos se contrastan con Python, se revisan los enlaces y la vista móvil. El manual se genera desde la fuente QMD. La evidencia está en [reproducibilidad](reproducibilidad/README.md). La ejecución correcta y la cobertura documentada no sustituyen la revisión de pares.
