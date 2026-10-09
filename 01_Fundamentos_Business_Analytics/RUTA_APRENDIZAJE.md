# Ruta de aprendizaje · Fundamentos de Business Analytics

[Curso](README.md) · [Guía](guia_maestra_ba.html#ruta-aprendizaje)

**Preparación de entrada:** Porcentajes, lectura de tablas y operaciones básicas; Python se introduce con ejemplos.

Los tiempos orientan una práctica guiada y deben ajustarse al diagnóstico del grupo. Cada módulo sigue la secuencia: anticipar → ejecutar → modificar → explicar. La profundización se consulta después del núcleo.

## 01 · Pregunta de negocio y datos

Núcleo · 60–90 min orientativos.

**Objetivo:** Formular una decisión con unidad de análisis, variable y regla de calidad.

**Preparación:** Distinguir una fila de una variable y calcular un porcentaje.

**Ejemplo de referencia:** QuillayMarket: convertir «mejorar ventas» en una pregunta con período, responsable e indicador.

**Práctica:** Cambiar la unidad de venta a cliente y explicar qué agregado deja de ser válido.

**Criterio de logro:** Entregar una ficha con pregunta, unidad, fuente, decisión y dos límites.

[Capítulo](guia_maestra_ba.html#c1) · [Manual](material_propio/FBA_manual_cientifico.html#sec-negocio) · [Notebook](notebooks/FBA_01_negocio_datos.ipynb)

## 02 · Exploración y comunicación visual

Núcleo · 60–90 min orientativos.

**Objetivo:** Elegir un resumen y un gráfico coherentes con la pregunta y el denominador.

**Preparación:** Ficha del módulo 01; media, mediana y tipo de variable.

**Ejemplo de referencia:** Comparar ingresos por producto y evolución mensual sin atribuir causalidad a una línea.

**Práctica:** Filtrar un segmento y comprobar si cambia el mensaje al mantener el mismo denominador.

**Criterio de logro:** Presentar un gráfico con unidad, período, población y una interpretación verificable.

[Capítulo](guia_maestra_ba.html#c5) · [Manual](material_propio/FBA_manual_cientifico.html#sec-visualizacion) · [Notebook](notebooks/FBA_02_exploracion_visual.ipynb)

## 03 · Herramientas y caso integrador

Núcleo · 60–90 min orientativos.

**Objetivo:** Reproducir un indicador con filtros, agregaciones y una unión validada.

**Preparación:** Módulos 01–02; claves de una tabla y lectura de una fórmula.

**Ejemplo de referencia:** Conciliar el ingreso de QuillayMarket entre pandas y SQL sobre las mismas filas.

**Práctica:** Introducir una clave repetida en una copia y detectar por qué se inflan los totales.

**Criterio de logro:** Entregar cálculo conciliado, control de cardinalidad y recomendación con sensibilidad.

[Capítulo](guia_maestra_ba.html#c14) · [Manual](material_propio/FBA_manual_cientifico.html#sec-herramientas) · [Notebook](notebooks/FBA_03_herramientas_caso_integrador.ipynb)

## 04 · Probabilidad y simulación

Profundización · 90–120 min orientativos.

**Objetivo:** Explicar una probabilidad condicionada y la variación de una estimación.

**Preparación:** Fracciones, porcentajes y distribuciones descritas en el módulo 02.

**Ejemplo de referencia:** Comparar probabilidad de alerta dada una condición y condición dada una alerta.

**Práctica:** Cambiar la tasa base conservando sensibilidad y especificidad; anticipar el posterior.

**Criterio de logro:** Dibujar una tabla de frecuencias y explicar el efecto de n sin confundir sesgo con precisión.

[Capítulo](guia_maestra_ba.html#c8) · [Manual](material_propio/FBA_manual_cientifico.html#sec-probabilidad) · [Notebook](notebooks/FBA_04_probabilidad_simulacion.ipynb)

## 05 · Puente hacia modelos predictivos

Profundización · 90–120 min orientativos.

**Objetivo:** Comparar un modelo con una referencia usando datos reservados.

**Preparación:** Módulos 01–02 y noción de probabilidad; ejecutar celdas en orden.

**Ejemplo de referencia:** Separar ajuste y evaluación y observar cómo cambia una decisión al mover el umbral.

**Práctica:** Justificar un costo distinto de falso negativo y comprobar su efecto en la recomendación.

**Criterio de logro:** Informar partición, referencia, métrica, costo y un límite de generalización.

[Capítulo](guia_maestra_ba.html#c9) · [Manual](material_propio/FBA_manual_cientifico.html#sec-modelos) · [Notebook](notebooks/FBA_05_modelos_evaluacion.ipynb)
