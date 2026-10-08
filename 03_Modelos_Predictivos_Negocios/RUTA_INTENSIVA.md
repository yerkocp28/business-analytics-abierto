# Modelos Predictivos: ruta intensiva de cinco semanas

[Curso](README.md) · [Cobertura](COBERTURA.md) · [Guía maestra](guia_maestra_mpn.html#ruta-intensiva)

Esta ruta organiza RA1 en las semanas 1–2, RA2 en las 3–4 y RA3 en la 5. La guía conserva también una ruta de doce semanas: son dos calendarios para los mismos resultados, no dos temarios que deban acumularse. La ruta no presupone una cantidad fija de horas por sesión.

| Semana | Preparación y núcleo | Trabajo en clase | Evidencia |
|---|---|---|---|
| 1 | Diagnóstico de Python/sklearn; objetivo, unidad, horizonte, regresión/clasificación | [NB01 diagnóstico](notebooks/MPN_01_problema_predictivo.ipynb#diagnostico-python), [tipos](notebooks/MPN_01_problema_predictivo.ipynb#tipos), [línea base](notebooks/MPN_01_problema_predictivo.ipynb#linea-base) y [fuga](notebooks/MPN_01_problema_predictivo.ipynb#fuga) | Ficha del problema y explicación de un error de validación |
| 2 | Lineal simple/múltiple, logística, árbol y principio neuronal | [NB01 técnicas](notebooks/MPN_01_problema_predictivo.ipynb#tecnicas), [red mínima](notebooks/MPN_01_problema_predictivo.ipynb#red-neuronal); demostraciones [MCO](notebooks/MPN_03_regresion_demanda.ipynb#mco) y [logística](notebooks/MPN_04_clasificacion_abandono.ipynb#logistica) | Comparación razonada de técnicas · evaluación 1 |
| 3 | CRISP-DM, variables, limpieza, partición y entrenamiento de clasificación | [NB02 contrato](notebooks/MPN_02_crisp_preparacion.ipynb#contrato), [calidad](notebooks/MPN_02_crisp_preparacion.ipynb#calidad), [preparación sin fuga](notebooks/MPN_02_crisp_preparacion.ipynb#fuga-preparacion); NB04 clasificación | Pipeline reproducible y decisión de algoritmo frente a referencia |
| 4 | Evaluación de clasificación; matriz de confusión y métricas | [NB05 laboratorio de métricas](notebooks/MPN_05_validacion_evaluacion.ipynb#laboratorio-s8), [validación](notebooks/MPN_05_validacion_evaluacion.ipynb#cv) y [umbral](notebooks/MPN_05_validacion_evaluacion.ipynb#umbral-costo) | Informe de clasificación · evaluación 2 |
| 5 | Construcción y evaluación de regresión; límites y mejoras | [NB03 regresión](notebooks/MPN_03_regresion_demanda.ipynb#mco), métricas MAE/RMSE/R² de NB05; [NB06 comunicación](notebooks/MPN_06_limitaciones_comunicacion.ipynb#comunicacion) y [mejoras](notebooks/MPN_06_limitaciones_comunicacion.ipynb#mejoras) | Modelo de regresión, ficha y recomendación · evaluación 3 |

La regresión se presenta conceptualmente en semana 2 y se construye y evalúa en semana 5. Introducir una métrica al explicar la referencia en semana 1 evita entrenar sin saber qué se quiere mejorar; no adelanta toda la evaluación de RA3.

Para ganar claridad: usar FinCordillera para clasificación y QuillayMarket para regresión; predecir qué ocurrirá antes de ejecutar; cambiar una sola decisión por actividad; cerrar con tres frases —resultado, límite y acción—. El diagnóstico permite omitir repaso ya dominado, conservando los materiales para quien lo necesite.

Consultar después del núcleo: Ridge/Lasso, intervalos conformales, recalibración avanzada, fraude, PSI y pronóstico temporal. El fundamento y límites de redes neuronales **sí** aparecen en CE1.1; entrenar redes profundas no es una exigencia añadida. El notebook 07 amplía series: CE2.3 menciona regresión **o** series, mientras que semana 5 exige regresión.

Cada curso define las ponderaciones de sus evaluaciones. Para retroalimentación, reutilizar la rúbrica del manual y pedir un notebook ejecutable con decisión de negocio, comparación con referencia, separación de datos y límites.
