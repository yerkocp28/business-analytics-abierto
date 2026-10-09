# Modelos Predictivos para los Negocios

[Volver al inicio](../README.md) · [Ruta por módulo](RUTA_APRENDIZAJE.md) · [Cobertura curricular](COBERTURA.md) · [Reproducción y pruebas](reproducibilidad/README.md) · [Datos compartidos](../_transversal/datos/README.md)

**Edición 2026.** Tres unidades (U1 S01–S02, U2 S03–S07, U3 S08–S12) con profundización en pronóstico de series de tiempo. Los 15 criterios de evaluación se vinculan con actividades concretas. Además de la ruta de doce semanas hay una [ruta intensiva de cinco semanas](RUTA_INTENSIVA.md).

## Material principal para clase

| Formato | Recurso | Uso |
|---|---|---|
| HTML interactivo | [Guía maestra](guia_maestra_mpn.html) | 16 capítulos, 12 simuladores, ruta de doce semanas, glosario y 36 preguntas de autoevaluación, sin conexión |
| PDF actualizado | [Manual científico](material_propio/MPN_manual_cientifico.pdf) | Fundamentos, fórmulas, supuestos, casos calculados, ejercicios resueltos, rúbrica y bibliografía |
| Quarto | [Fuente QMD](material_propio/MPN_manual_cientifico.qmd) | Editar y regenerar el PDF y su HTML de lectura |
| HTML de lectura | [Manual científico navegable](material_propio/MPN_manual_cientifico.html) | Buscar, consultar fórmulas y abrir referencias |

## Laboratorios interactivos completos

| Notebook | Alcance | Nivel |
|---|---|---|
| [01 · Problema predictivo](notebooks/MPN_01_problema_predictivo.ipynb) | Y = f(X) + ε, error irreducible, tipos de problema, línea base, fuga, técnicas y comunicación | Núcleo U1 / RA1 |
| [02 · CRISP-DM y preparación](notebooks/MPN_02_crisp_preparacion.ipynb) | Contrato de datos, vacíos MCAR/MNAR, extremos, fuga en la preparación, partición y pipeline | Núcleo U2 / RA2 |
| [03 · Regresión de demanda](notebooks/MPN_03_regresion_demanda.ipynb) | MCO con errores estándar, estacionalidad, diagnóstico, Ridge/Lasso, árboles y escenarios con intervalo conformal | Núcleo U2 / RA2 |
| [04 · Clasificación de abandono](notebooks/MPN_04_clasificacion_abandono.ipynb) | Logística y razones de chances, árbol, KNN y escala, bosque, KS/Gini/AP/Brier, ganancia y campaña | Núcleo U2 / RA2 |
| [05 · Validación y evaluación](notebooks/MPN_05_validacion_evaluacion.ipynb) | Validación cruzada, hiperparámetros, umbral por costo, calibración, fraude desbalanceado y laboratorio S8 | Núcleo U3 / RA3 |
| [06 · Limitaciones y comunicación](notebooks/MPN_06_limitaciones_comunicacion.ipynb) | Segmentos, estabilidad bootstrap, deriva y PSI, sensibilidad a costos, ficha del modelo, mejoras y mensajes | Núcleo U3 / RA3 |
| [07 · Pronóstico de demanda](notebooks/MPN_07_pronostico_demanda.ipynb) | Referencias ingenuas, tendencia y estacionalidad, origen móvil, MASE e intervalos por horizonte | Profundización |

Descargue el repositorio completo y ejecute los notebooks con el entorno documentado. Los controles requieren kernel activo; las salidas guardadas permiten lectura previa. Los datos son los casos simulados de `_transversal/datos`; las simulaciones adicionales se identifican en cada notebook.

## Decisiones metodológicas de la edición

- Cada notebook separa **entrenamiento, validación y prueba**: los modelos, hiperparámetros, umbrales y costos se eligen sin la prueba, que se consulta una vez.
- Toda transformación aprendida (imputación, escalamiento, selección) vive dentro de un **pipeline**.
- El umbral de decisión y la comparación de modelos se hacen con predicciones fuera de pliegue o con validación, nunca con la prueba; KNN y logística siempre se escalan dentro del pipeline.
- La cobertura empírica de los intervalos (conformal y de pronóstico) se informa junto con su error estándar, y cada notebook discute cuándo una diferencia con el nivel nominal es relevante.

## Validación

Cada notebook se ejecuta en un kernel nuevo y se prueban sus controles interactivos y su autoevaluación. La guía se verifica en Chrome sin conexión: sus cálculos se contrastan con Python, se revisan los enlaces y la vista móvil. El manual se genera desde la fuente QMD. La evidencia está en [reproducibilidad](reproducibilidad/README.md). La ejecución correcta y la cobertura documentada no sustituyen la revisión de pares.
