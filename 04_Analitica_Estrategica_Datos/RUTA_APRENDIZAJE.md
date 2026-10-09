# Ruta de aprendizaje · Analítica Estratégica de Datos

[Curso](README.md) · [Guía](guia_maestra_aed.html#ruta-aprendizaje)

**Preparación de entrada:** Descriptiva, probabilidad y lectura de modelos; programación lineal se introduce con dos variables.

Los tiempos orientan una práctica guiada y deben ajustarse al diagnóstico del grupo. Cada módulo sigue la secuencia: anticipar → ejecutar → modificar → explicar. La profundización se consulta después del núcleo.

## 01 · Proceso y calidad

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Diseñar un proceso con entregables y reglas de calidad que cambian la decisión.

**Preparación:** Claves, tipos de variable y pregunta de negocio.

**Ejemplo de referencia:** CasaPeumo: comparar original y derivado; BoldoNet: distinguir cohortes maduras de incompletas.

**Práctica:** Mover la fecha de corte y explicar por qué cambia la población elegible del KPI.

**Criterio de logro:** Entregar contrato, auditoría, denominadores y registro de exclusiones reproducible.

**Distribución orientativa:** explicación 30 min; práctica guiada 90 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#proceso) · [Manual](material_propio/AED_manual_cientifico.html#sec-proceso) · [Notebook](notebooks/AED_01_proceso_calidad.ipynb)

## 02 · Selección de técnicas

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Elegir técnica según pregunta, respuesta, estructura y decisión.

**Preparación:** Módulo 01, lectura de regresión, clasificación y segmentación.

**Ejemplo de referencia:** Distinguir describir demora, predecir incumplimiento y asignar turnos con capacidad limitada.

**Práctica:** Comparar predicción y agrupamiento sobre el mismo caso y discutir cómo se usaría cada salida.

**Criterio de logro:** Justificar técnica, referencia, validación y una implicación práctica que no confunda asociación y efecto.

**Distribución orientativa:** explicación 40 min; práctica guiada 80 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#tecnicas) · [Manual](material_propio/AED_manual_cientifico.html#sec-tecnicas) · [Notebook](notebooks/AED_02_tecnicas_analiticas.ipynb)

## 03 · KPIs y dashboard

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Definir y conciliar una medida con grano, unidad, denominador y responsable.

**Preparación:** Agregaciones, ratios y calidad del módulo 01.

**Ejemplo de referencia:** Ventas de 100 y 900 con márgenes 50 y 90: margen total 140/1000 = 14%, no 30%.

**Práctica:** Filtrar canal y región y conciliar pandas, SQL y la definición DAX.

**Criterio de logro:** Entregar ficha de KPI y tablero con fuente, población, período y acción ante desviaciones.

**Distribución orientativa:** explicación 30 min; práctica guiada 90 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#kpis) · [Manual](material_propio/AED_manual_cientifico.html#sec-kpis) · [Notebook](notebooks/AED_03_kpis_dashboard.ipynb)

## 04 · Optimización y restricciones

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Formular y resolver una decisión factible e interpretar sensibilidad local.

**Preparación:** Ecuaciones lineales, unidades y costos de oportunidad.

**Ejemplo de referencia:** Con 100 horas y 90 de material, A=110/3 y B=80/3 producen 6800/3 UM.

**Práctica:** Cambiar horas a 110 y después a 200; comprobar cuándo deja de valer el precio sombra inicial.

**Criterio de logro:** Presentar variables, objetivo, restricciones, solución, holguras y una decisión de capacidad.

**Distribución orientativa:** explicación 35 min; práctica guiada 85 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#restricciones) · [Manual](material_propio/AED_manual_cientifico.html#sec-optimizacion) · [Notebook](notebooks/AED_04_optimizacion_restricciones.ipynb)

## 05 · Alternativas e información

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Comparar acciones bajo riesgo y valorar información antes de pagar por ella.

**Preparación:** Probabilidades y valor esperado; distinguir acción de estado del mundo.

**Ejemplo de referencia:** Con p alto = 0,4: expandir vale 20 kUM y piloto 27; información perfecta vale como máximo 14.

**Práctica:** Mover p a 0,6 y contrastar valor esperado, peor caso y preferencia del decisor.

**Criterio de logro:** Entregar matriz de pagos, alternativa, sensibilidad y cota del costo de información.

**Distribución orientativa:** explicación 35 min; práctica guiada 85 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#decision) · [Manual](material_propio/AED_manual_cientifico.html#sec-decision) · [Notebook](notebooks/AED_05_alternativas_decision.ipynb)

## 06 · SolarSur y Monte Carlo

Núcleo · 120 min guiados + 60 min autónomos orientativos.

**Objetivo:** Comparar proyectos con flujos, dependencia y precisión numérica explícitos.

**Preparación:** Valor presente, media, percentiles y distribuciones lognormales.

**Ejemplo de referencia:** SolarSur: simular producción y precio dependientes y contrastar VAN medio con su esperanza analítica.

**Práctica:** Duplicar escenarios y cambiar correlación por separado; distinguir qué cambio reduce error Monte Carlo.

**Criterio de logro:** Informar VAN, pérdida, SE de la media, supuestos y sensibilidad de una recomendación.

**Distribución orientativa:** explicación 40 min; práctica guiada 80 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#simulacion) · [Manual](material_propio/AED_manual_cientifico.html#sec-simulacion) · [Notebook](notebooks/AED_06_solarsur_monte_carlo.ipynb)

## 07 · Integración e implementación

Núcleo · 120 min guiados + 60 min autónomos orientativos.

**Objetivo:** Defender una alternativa y diseñar el piloto que evaluará su efecto.

**Preparación:** KPIs, restricciones y análisis de incertidumbre de los módulos anteriores.

**Ejemplo de referencia:** Traducir una reducción supuesta de incidentes a beneficio incremental y punto de equilibrio.

**Práctica:** Cambiar costo y efecto esperado; formular una métrica primaria y una de protección.

**Criterio de logro:** Entregar memo con alternativas, factibilidad, incertidumbre, piloto, responsable y criterio de revisión.

**Distribución orientativa:** explicación 30 min; práctica guiada 90 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#comunicacion) · [Manual](material_propio/AED_manual_cientifico.html#sec-comunicacion) · [Notebook](notebooks/AED_07_comunicacion_integracion.ipynb)

## 08 · Profundización prescriptiva

Profundización · 240 min guiados + 90 min autónomos orientativos.

**Objetivo:** Analizar sensibilidad, colas y aprendizaje secuencial sin extrapolar garantías.

**Preparación:** Álgebra, probabilidad, optimización y lectura de funciones en Python.

**Ejemplo de referencia:** Comparar media-varianza, riesgo de cola y políticas UCB sobre múltiples semillas.

**Práctica:** Modificar aversión al riesgo o mecanismo de recompensa y evaluar estabilidad de la política.

**Criterio de logro:** Defender supuestos, criterio de riesgo, comparación independiente y límite de transferencia.

**Distribución orientativa:** explicación 60 min; práctica guiada 180 min; trabajo autónomo 90 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_aed.html#avanzado) · [Manual](material_propio/AED_manual_cientifico.html#sec-profundizacion) · [Notebook](notebooks/AED_08_profundizacion_prescriptiva.ipynb)
