# Estadística Aplicada a Business Analytics

[Inicio](../README.md) · [Ruta por módulo](RUTA_APRENDIZAJE.md) · [Cobertura](COBERTURA.md) · [Reproducibilidad](reproducibilidad/README.md) · [Datos y diccionario](datos/README.md)

**Edición 2026.** 12 criterios de evaluación y 17 contenidos mínimos. Un caso simulado común, ComercioSur, conecta métodos, incertidumbre, decisión y comunicación. La secuencia propuesta tiene doce semanas y es ajustable.

| Recurso | Uso |
|---|---|
| [Guía maestra interactiva](guia_maestra_eba.html) | 16 capítulos, 12 experimentos y 8 autoevaluaciones; funciona sin conexión |
| [Manual científico PDF](material_propio/EBA_manual_cientifico.pdf) | Fórmulas, supuestos, resultados calculados, doce ejercicios resueltos y rúbrica |
| [Manual HTML](material_propio/EBA_manual_cientifico.html) · [fuente QMD](material_propio/EBA_manual_cientifico.qmd) | Consulta y edición; fuente común de los capítulos de la guía |
| [Libro Excel](material_propio/EBA_tablero_excel.xlsx) | Datos, agregados, fórmulas y gráfico; práctica de conciliación con Python |
| [Matriz de cobertura](matriz_cobertura.csv) | Criterio, tema, capítulo, notebook y evidencia |

## Laboratorios

| Notebook | Temas | Semanas propuestas |
|---|---|---|
| [01](notebooks/EBA_01_problema_descripcion_muestreo.ipynb) | Problema, descripción, calidad, muestreo y precisión | 1–2 |
| [02](notebooks/EBA_02_probabilidad_bayes_distribuciones.ipynb) | Probabilidad, Bayes, distribuciones y simulación | 3–4 |
| [03](notebooks/EBA_03_estimacion_intervalos.ipynb) | Estimación, Wilson, bootstrap y cobertura | 5 |
| [04](notebooks/EBA_04_correlacion_regresion.ipynb) | Pearson/Spearman, regresión simple/múltiple y diagnóstico | 6 |
| [05](notebooks/EBA_05_hipotesis_anova.ipynb) | Medias/proporciones, pareado, ANOVA, Holm y decisión | 7–8 |
| [06](notebooks/EBA_06_series_tiempo.ipynb) | Referencias, SES, Holt, ARIMA y validación temporal | 9 |
| [07](notebooks/EBA_07_visualizacion_herramientas.ipynb) | Diseño, dashboard, Python/Excel y receta Power BI | 10–11 |
| [08](notebooks/EBA_08_integrador_comunicacion.ipynb) | Integrador: evidencia, costo, memo y rúbrica | 12 |

Abra el repositorio completo en Jupyter y ejecute en orden. Los controles necesitan kernel activo; las salidas están guardadas para lectura. Cada notebook incluye cálculo, interpretación, ejercicio y autoevaluación. La ruta de clase usa una pregunta, un ejemplo, una modificación y una explicación con límite; se evita repetir el mismo temario en tres formatos independientes.

## Validación

Cada notebook se ejecuta en un kernel nuevo y se prueban sus controles interactivos y su autoevaluación. La guía se verifica en Chrome sin conexión: sus cálculos se contrastan con Python, se revisan los enlaces y la vista móvil. El manual se genera desde la fuente QMD. La evidencia está en [reproducibilidad](reproducibilidad/README.md). La ejecución correcta y la cobertura documentada no sustituyen la revisión de pares.
