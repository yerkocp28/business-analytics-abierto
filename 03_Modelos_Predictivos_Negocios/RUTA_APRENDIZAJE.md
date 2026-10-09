# Ruta de aprendizaje · Modelos Predictivos para los Negocios

[Curso](README.md) · [Guía](guia_maestra_mpn.html#ruta-aprendizaje)

**Preparación de entrada:** Python básico, tablas, probabilidad e interpretación de regresión; diagnóstico en NB01.

Los tiempos orientan una práctica guiada y deben ajustarse al diagnóstico del grupo. Cada módulo sigue la secuencia: anticipar → ejecutar → modificar → explicar. La profundización se consulta después del núcleo.

## 01 · Problema predictivo

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Definir objetivo, horizonte, disponibilidad de variables y referencia.

**Preparación:** Leer un DataFrame y distinguir respuesta numérica de categórica.

**Ejemplo de referencia:** FinCordillera: predecir abandono con información disponible antes de la decisión.

**Práctica:** Clasificar variables por momento de disponibilidad y explicar una fuga de información.

**Criterio de logro:** Entregar ficha de problema, referencia y justificación de una técnica; explicar la red mínima.

**Distribución orientativa:** explicación 35 min; práctica guiada 85 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c1) · [Manual](material_propio/MPN_manual_cientifico.html#sec-problema) · [Notebook](notebooks/MPN_01_problema_predictivo.ipynb)

## 02 · Preparación sin fuga

Núcleo · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Construir un pipeline que aprenda transformaciones solo con entrenamiento.

**Preparación:** Módulo 01; nulos, categorías y claves de datos.

**Ejemplo de referencia:** Imputar y escalar dentro de la validación en lugar de usar toda la tabla antes de dividir.

**Práctica:** Cambiar el mecanismo de valores ausentes y explicar el límite de la imputación.

**Criterio de logro:** Demostrar separación de datos, contrato de variables y transformaciones ajustadas sin prueba.

**Distribución orientativa:** explicación 30 min; práctica guiada 90 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c3) · [Manual](material_propio/MPN_manual_cientifico.html#sec-crisp) · [Notebook](notebooks/MPN_02_crisp_preparacion.ipynb)

## 03 · Regresión de demanda

Núcleo · 180 min guiados + 60 min autónomos orientativos.

**Objetivo:** Comparar regresión y alternativas con referencia e incertidumbre de predicción.

**Preparación:** Módulos 01–02; coeficientes y errores de regresión.

**Ejemplo de referencia:** QuillayMarket: comparar mes numérico con codificación por categoría y revisar residuos.

**Práctica:** Modificar un escenario de precio; identificar extrapolación y límites del intervalo.

**Criterio de logro:** Reportar MAE/RMSE, referencia, diagnóstico y diferencia entre IC de media e intervalo predictivo.

**Distribución orientativa:** explicación 45 min; práctica guiada 135 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c4) · [Manual](material_propio/MPN_manual_cientifico.html#sec-regresion) · [Notebook](notebooks/MPN_03_regresion_demanda.ipynb)

## 04 · Clasificación de abandono

Núcleo · 150 min guiados + 60 min autónomos orientativos.

**Objetivo:** Evaluar discriminación y una campaña con probabilidades y costos explícitos.

**Preparación:** Pipeline, probabilidad y matriz de confusión.

**Ejemplo de referencia:** FinCordillera: comparar logística, árbol, KNN escalado y bosque en validación.

**Práctica:** Cambiar presupuesto de contactos y comprobar cobertura de casos y costo de campaña.

**Criterio de logro:** Justificar modelo y política con métricas fuera de muestra y límites de utilidad.

**Distribución orientativa:** explicación 40 min; práctica guiada 110 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c5) · [Manual](material_propio/MPN_manual_cientifico.html#sec-clasificacion) · [Notebook](notebooks/MPN_04_clasificacion_abandono.ipynb)

## 05 · Validación, métricas y umbral

Núcleo · 180 min guiados + 75 min autónomos orientativos.

**Objetivo:** Seleccionar modelo y umbral sin reutilizar la prueba para decidir.

**Preparación:** Módulos 02–04; costos de falsos positivos y negativos.

**Ejemplo de referencia:** PulpaLenga: fijar un umbral con predicciones fuera de pliegue y evaluar al final.

**Práctica:** Cambiar costos y revisar calibración; distinguir ordenamiento de calidad probabilística.

**Criterio de logro:** Documentar selección, datos reservados y costo; no inferir calibración por coincidencia de umbrales.

**Distribución orientativa:** explicación 45 min; práctica guiada 135 min; trabajo autónomo 75 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c8) · [Manual](material_propio/MPN_manual_cientifico.html#sec-validacion) · [Notebook](notebooks/MPN_05_validacion_evaluacion.ipynb)

## 06 · Limitaciones y comunicación

Núcleo · 150 min guiados + 60 min autónomos orientativos.

**Objetivo:** Construir una ficha de modelo con seguimiento, responsables y condiciones de uso.

**Preparación:** Métricas, calibración y evaluación por segmentos.

**Ejemplo de referencia:** Comparar estabilidad poblacional y desempeño por grupo; no interpretar PSI como causalidad.

**Práctica:** Redactar un mensaje ejecutivo y otro técnico para la misma señal de deterioro.

**Criterio de logro:** Entregar ficha con evidencia, incertidumbre, umbral de revisión y propuesta de mejora.

**Distribución orientativa:** explicación 35 min; práctica guiada 115 min; trabajo autónomo 60 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c10) · [Manual](material_propio/MPN_manual_cientifico.html#sec-limitaciones) · [Notebook](notebooks/MPN_06_limitaciones_comunicacion.ipynb)

## 07 · Pronóstico de demanda

Profundización · 120 min guiados + 45 min autónomos orientativos.

**Objetivo:** Evaluar una serie mediante orígenes móviles y referencias comparables.

**Preparación:** Validación temporal, tendencia, estacionalidad y MAE.

**Ejemplo de referencia:** QuillayMarket: comparar pronóstico estacional y modelo con variables temporales.

**Práctica:** Aumentar el horizonte y analizar cobertura y MASE sin ajustar con los meses de prueba.

**Criterio de logro:** Explicar horizonte, cobertura observada, referencia y límites de cambios del proceso.

**Distribución orientativa:** explicación 35 min; práctica guiada 85 min; trabajo autónomo 45 min. Ajustar tras una clase piloto.

[Capítulo](guia_maestra_mpn.html#c16) · [Manual](material_propio/MPN_manual_cientifico.html#sec-series) · [Notebook](notebooks/MPN_07_pronostico_demanda.ipynb)
