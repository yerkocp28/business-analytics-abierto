# Ruta de aprendizaje · Estadística Aplicada a Business Analytics

[Curso](README.md) · [Guía](guia_maestra_eba.html#ruta-aprendizaje)

**Preparación de entrada:** Fundamentos: variables, gráficos y porcentajes; lectura y ejecución básica de Python.

Los tiempos orientan una práctica guiada y deben ajustarse al diagnóstico del grupo. Cada módulo sigue la secuencia: anticipar → ejecutar → modificar → explicar. La profundización se consulta después del núcleo.

## 01 · Problema, descripción y muestreo

Núcleo · 180 min guiados + 45 min autónomos orientativos.

**Objetivo:** Definir población y estimando y justificar a quién representa la muestra.

**Preparación:** Tipos de variables, media, mediana y lectura de gráficos.

**Ejemplo de referencia:** ComercioSur: distinguir el marco de 5000 pedidos de la muestra de 600.

**Práctica:** Comparar precisión al aumentar n y discutir un marco que excluye un canal.

**Criterio de logro:** Entregar contrato de análisis con población, diseño, estimando y fuentes de sesgo.

**Distribución orientativa:** explicación 45 min; práctica guiada 135 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-problema) · [Manual](material_propio/EBA_manual_cientifico.html#sec-problema) · [Notebook](notebooks/EBA_01_problema_descripcion_muestreo.ipynb)

## 02 · Probabilidad, Bayes y distribuciones

Núcleo · 90 min guiados + 30 min autónomos orientativos.

**Objetivo:** Construir un modelo probabilístico cuyo soporte y supuestos sean explícitos.

**Preparación:** Módulo 01; porcentajes y tablas de frecuencias.

**Ejemplo de referencia:** En 10000 casos, prevalencia 2%, sensibilidad 90% y especificidad 95% dan 180 alertas verdaderas y 490 falsas.

**Práctica:** Modificar la prevalencia y una meta binomial; explicar independencia y tasa base.

**Criterio de logro:** Calcular e interpretar el posterior 180/670 y explicar por qué no equivale a sensibilidad.

**Distribución orientativa:** explicación 30 min; práctica guiada 60 min; trabajo autónomo 30 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-probabilidad) · [Manual](material_propio/EBA_manual_cientifico.html#sec-probabilidad) · [Notebook](notebooks/EBA_02_probabilidad_bayes_distribuciones.ipynb)

## 03 · Estimación e intervalos

Núcleo · 90 min guiados + 40 min autónomos orientativos.

**Objetivo:** Elegir un intervalo según el parámetro, la población y el diseño.

**Preparación:** Muestreo y distribuciones de los módulos 01–02.

**Ejemplo de referencia:** Contrastar un IC t para tiempo medio con Wilson para proporción de pedidos resueltos.

**Práctica:** Cambiar confianza y n; separar variabilidad de pedidos de incertidumbre sobre la media.

**Criterio de logro:** Reportar estimación, intervalo, unidad, población objetivo y condiciones de validez.

**Distribución orientativa:** explicación 30 min; práctica guiada 60 min; trabajo autónomo 40 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-intervalos) · [Manual](material_propio/EBA_manual_cientifico.html#sec-intervalos) · [Notebook](notebooks/EBA_03_estimacion_intervalos.ipynb)

## 04 · Correlación y regresión

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Interpretar coeficientes condicionados y evaluar diagnósticos del modelo.

**Preparación:** Dispersión, correlación e intervalos; unidad de cada variable.

**Ejemplo de referencia:** Modelar tiempo con ticket, canal y campaña y examinar residuos y errores HC3.

**Práctica:** Comparar ajuste simple y múltiple y explicar por qué un coeficiente cambia.

**Criterio de logro:** Justificar especificación, interpretar un coeficiente y señalar un límite causal.

**Distribución orientativa:** explicación 40 min; práctica guiada 80 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-regresion) · [Manual](material_propio/EBA_manual_cientifico.html#sec-regresion) · [Notebook](notebooks/EBA_04_correlacion_regresion.ipynb)

## 05 · Contrastes, ANOVA y decisión

Núcleo · 150 min guiados + 60 min autónomos orientativos.

**Objetivo:** Elegir un contraste y comunicar efecto, incertidumbre y relevancia práctica.

**Preparación:** Intervalos y diseño independiente o pareado.

**Ejemplo de referencia:** Comparar campañas con Welch y ANOVA; usar Holm cuando se examinan varios pares.

**Práctica:** Cambiar costo del tratamiento sin modificar p y revisar si cambia la recomendación.

**Criterio de logro:** Entregar diferencia, IC, p, ajuste por multiplicidad y una decisión condicionada.

**Distribución orientativa:** explicación 40 min; práctica guiada 110 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-contrastes) · [Manual](material_propio/EBA_manual_cientifico.html#sec-contrastes) · [Notebook](notebooks/EBA_05_hipotesis_anova.ipynb)

## 06 · Series y pronóstico

Núcleo · 150 min guiados + 60 min autónomos orientativos.

**Objetivo:** Comparar pronósticos con igual horizonte y orden temporal preservado.

**Preparación:** Módulos 01–04; tendencia, estacionalidad y error de predicción.

**Ejemplo de referencia:** ComercioSur: 36 meses iniciales, orígenes 36/42/48 y 12 meses finales reservados.

**Práctica:** Comparar una referencia estacional con SES, Holt y ARIMA sin seleccionar con prueba.

**Criterio de logro:** Dibujar las ventanas y explicar métrica, referencia y dependencia entre errores solapados.

**Distribución orientativa:** explicación 40 min; práctica guiada 110 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-series) · [Manual](material_propio/EBA_manual_cientifico.html#sec-series) · [Notebook](notebooks/EBA_06_series_tiempo.ipynb)

## 07 · Visualización y herramientas

Núcleo · 90 min guiados + 45 min autónomos orientativos.

**Objetivo:** Conciliar un indicador entre herramientas y diseñar un tablero interpretable.

**Preparación:** Agregaciones, filtros y conclusiones de los módulos anteriores.

**Ejemplo de referencia:** Comparar los agregados por canal y campaña en Python y el libro Excel.

**Práctica:** Cambiar un filtro, revisar población y denominador y explicar la misma medida en DAX.

**Criterio de logro:** Entregar un tablero con unidades, filtros y totales conciliados; identificar qué se ejecutó.

**Distribución orientativa:** explicación 30 min; práctica guiada 60 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-visualizacion) · [Manual](material_propio/EBA_manual_cientifico.html#sec-visualizacion) · [Notebook](notebooks/EBA_07_visualizacion_herramientas.ipynb)

## 08 · Integrador y comunicación

Núcleo · 120 min guiados + 60 min autónomos orientativos.

**Objetivo:** Defender una recomendación con efecto, incertidumbre y costo.

**Preparación:** Resultados reproducibles de los módulos 01–07.

**Ejemplo de referencia:** ComercioSur: unir comparación de campañas, costo por minuto y supuestos económicos.

**Práctica:** Redactar un memo y defenderlo frente a un escenario que invierte la decisión.

**Criterio de logro:** Entregar memo, cálculo, gráfico y defensa con población, sensibilidad y siguiente evidencia.

**Distribución orientativa:** explicación 20 min; práctica guiada 100 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_eba.html#sec-comunicacion) · [Manual](material_propio/EBA_manual_cientifico.html#sec-comunicacion) · [Notebook](notebooks/EBA_08_integrador_comunicacion.ipynb)
