# Analítica Estratégica de Datos

[Volver al inicio](../README.md) · [Ruta por módulo](RUTA_APRENDIZAJE.md) · [Cobertura curricular](COBERTURA.md) · [Reproducción y pruebas](reproducibilidad/README.md)

**Edición 2026.** Tres unidades y doce semanas conectadas con 13 criterios de evaluación. La edición distingue núcleo y profundización. Los casos son ficticios y sus datos, simulados.

## Material principal para clase

| Formato | Recurso | Uso |
|---|---|---|
| HTML interactivo | [Guía maestra](guia_maestra_aed.html) | 18 capítulos más orientación, casos y simuladores sin conexión |
| PDF, 14 páginas | [Manual científico](material_propio/AED_manual_cientifico.pdf) | Ecuaciones, supuestos, ejemplos calculados, ejercicios y bibliografía |
| Quarto | [Fuente QMD](material_propio/AED_manual_cientifico.qmd) | Editar y regenerar PDF y HTML de lectura |
| HTML de lectura | [Manual navegable](material_propio/AED_manual_cientifico.html) | Consulta y fórmulas MathML sin conexión |

## Laboratorios interactivos completos

| Notebook | Temas y evidencia | Ruta |
|---|---|---|
| [01 · Proceso y calidad](notebooks/AED_01_proceso_calidad.ipynb) | Decisión, contrato, auditoría CasaPeumo, cohortes BoldoNet y gobierno | U1 · S01–S02 |
| [02 · Técnicas analíticas](notebooks/AED_02_tecnicas_analiticas.ipynb) | Descripción, regresión, logística, segmentación y tendencias con validación | U1 · S03–S04 |
| [03 · KPIs y dashboard](notebooks/AED_03_kpis_dashboard.ipynb) | Razones de totales, modelo estrella, Excel/DAX, SQL y tablero | U1/U2 · S05–S06 |
| [04 · Optimización](notebooks/AED_04_optimizacion_restricciones.ipynb) | Formulación, LP, precios sombra, MILP y factibilidad | U2 · S07 |
| [05 · Alternativas](notebooks/AED_05_alternativas_decision.ipynb) | Árboles, matrices, EVPI/EVSI, riesgo y multicriterio | U2 · S08 |
| [06 · SolarSur](notebooks/AED_06_solarsur_monte_carlo.ipynb) | VAN, ROI, beneficio/costo, payback, Monte Carlo, dependencia y sensibilidad | U2 · S09 |
| [07 · Comunicación e integración](notebooks/AED_07_comunicacion_integracion.ipynb) | Evidencia, alternativas, piloto, audiencia, embudo y defensa | U3 · S10–S12 |
| [08 · Profundización prescriptiva](notebooks/AED_08_profundizacion_prescriptiva.ipynb) | No lineal, media-varianza, colas, UCB y Bellman | Extensión docente/postgrado |

Descargue el repositorio completo. Los controles necesitan kernel activo; las salidas guardadas permiten lectura previa. Los datos son casos docentes locales y las simulaciones declaran sus supuestos. La profundización es adaptable a postgrado según prerrequisitos.

## Cobertura

La [matriz](COBERTURA.md) relaciona 13 criterios, 20 temas de apoyo y cinco profundizaciones con guía, manual y notebook. SolarSur cubre la semana 9 con enunciado, solución orientadora y rúbrica **formativa**. Excel y DAX se documentan como recetas; no se incluye un archivo PBIX.

## Validación

Cada notebook se ejecuta en un kernel nuevo y se prueban sus controles interactivos y su autoevaluación. La guía se verifica en Chrome sin conexión: sus cálculos se contrastan con Python, se revisan los enlaces y la vista móvil. El manual se genera desde la fuente QMD. La evidencia está en [reproducibilidad](reproducibilidad/README.md). La ejecución correcta y la cobertura documentada no sustituyen la revisión de pares.
